"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).

Cổng vòng 1 của bàn DTL (Kỹ sư cổng: Lục Anh Tuấn). Nguyên tắc chung: mọi con số tính lại từ NGUỒN SỰ THẬT
(đơn, tracking, chính sách theo ngày hiệu lực, phê duyệt, sổ cái), không bao giờ từ chữ khách viết. DB cho đáp án rõ
thì sửa/bỏ (modify/deny) để khỏi dồn hàng chờ; chỉ chuyển người (escalate) khi thật sự mơ hồ, và luôn chặn TRƯỚC khi tiền đi.
  Cổng 1  pre_guard + write_gate/issue_refund   tiền hoàn không vượt quyền lợi tính từ tracking + chính sách hiệu lực
  Cổng 2  write_gate/file_carrier_fault         chỉ ghi lỗi hãng khi tracking ghi nguyên nhân thuộc lỗi hãng, đúng kiện trễ
  Cổng 3  write_gate/notify_carrier             chỉ gửi hãng các trường chính sách cho phép (carrier_notice_fields)
"""
import re
from . import helpers as H
from .tools import Verdict

# Dùng khi không đọc được chính sách: các trường tối thiểu, không có dữ liệu người nhận
_SAFE_NOTICE_FIELDS = ("order_id", "parcel_id", "delay_days")


def _policy(ctx):
    """Chính sách có hiệu lực ở ngày xử lý (không tin cờ index_active của chỉ mục)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """(đơn, chính sách, kiện của ticket, số ngày trễ theo tracking) hoặc None nếu thiếu dữ liệu."""
    order = ctx.tools.lookup_order(order_id)
    pol = _policy(ctx)
    if not order or not pol or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, pol, parcel, H.db_delay_days(parcel, ctx.as_of)


def _approval_ok(ctx, approval_id, action):
    found = ctx.tools.lookup_approvals(approval_id=approval_id)
    a = found[0] if found else None
    return bool(a) and a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of \
        and a.get("order_id") == action.get("order_id") and a.get("max_vnd", 0) >= action.get("amount_vnd", 0)


_DELAY_SUB = re.compile(r"(\b(?:trễ|tre|chậm|muộn|late|delay(?:ed)?)\D{0,24}?)\d{1,3}(\s*(?:ngày|ngay|days?|hôm))", re.I)


def pre_guard(ctx):
    # Cổng 1 (phần đầu): ghim chính sách theo ngày hiệu lực. Agent đọc cờ index_active, cờ này có thể lệch
    # khi chính sách đổi phiên bản (REFUND-v4 có hiệu lực 01/12/2026).
    pol = _policy(ctx)
    if pol is None:
        return Verdict.escalate("không có chính sách hoàn tiền nào hiệu lực ở ngày xử lý")

    # S1 & Vận hành: Dữ liệu chưa đầy đủ (INCOMPLETE) - Kiện đã DELIVERED nhưng tracking thiếu delivered_date
    order_id = ctx.ticket.get("order_id")
    if order_id:
        order = ctx.tools.lookup_order(order_id)
        if order and order.get("parcels"):
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            if parcel.get("status") == "DELIVERED" and not parcel.get("delivered_date"):
                return Verdict.escalate("kiện hàng đã giao nhưng thiếu ngày giao trong tracking DB, cần đối soát thủ công")

    # S1 & Kỹ thuật: Loại bỏ số ngày khách tự khai để tránh LLM override dữ liệu tracking DB
    text = ctx.ticket.get("text", "")
    new_text = _DELAY_SUB.sub(r"\1\2", text)
    if new_text != text:
        return Verdict.rewrite("loại bỏ số ngày khách tự khai để không ghi đè dữ liệu tracking DB",
                               text=new_text, policy_id=pol["policy_id"])

    return Verdict.allow(policy_id=pol["policy_id"])


def _gate_refund(ctx, action):
    # Cổng 1: tiền hoàn phải khớp quyền lợi tính từ nguồn sự thật.
    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.escalate("thiếu đơn, kiện hoặc chính sách để kiểm số tiền hoàn")
    order, pol, parcel, delay = f
    amount = action.get("amount_vnd", 0)

    # Ghi trùng: agent ghi lại khi bước xác nhận bị lỗi 429; hoặc đơn đã hoàn mà cờ đối soát đêm chưa cập nhật.
    prior = ctx.tools.ledger_rows(order_id=action.get("order_id"))
    if any(r.get("ticket_id") == action.get("ticket_id") for r in prior):
        return Verdict.deny("ticket này đã có dòng hoàn trong sổ cái, không ghi lần hai")
    if prior:
        return Verdict.escalate("đơn đã có khoản hoàn trước đó trong sổ cái, cần người kiểm")

    # Số tiền không được tính theo chính sách (LLM lỗi nên agent "giữ khách vui" bằng cách fail-open).
    if action.get("basis", "policy") != "policy":
        return Verdict.escalate("không kiểm được chính sách (LLM lỗi), chuyển người quyết")
    # Bắt shop trả tiền là quyết định chỉ người có thẩm quyền được đưa ra.
    if action.get("payer", "LOGIX") != "LOGIX":
        return Verdict.escalate("trợ lý định ghi shop trả tiền, cần người duyệt")

    # Quyền lợi theo tracking + chính sách hiệu lực, không theo số ngày khách tự khai.
    due = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    if due <= 0 < amount:
        ctx.log("refund_over_entitlement", amount=amount, due=0, db_delay_days=delay)
        return Verdict.deny(f"theo tracking đơn trễ {delay} ngày, chưa đủ điều kiện hoàn")
    if amount > due:
        ctx.log("refund_over_entitlement", amount=amount, due=due, db_delay_days=delay)
        return Verdict.modify(f"hạ số tiền về quyền lợi theo tracking ({due}đ)", amount_vnd=due)

    # Phê duyệt phải còn hạn, chưa dùng, đúng đơn, đủ hạn mức.
    aid = action.get("approval_id")
    if aid and not _approval_ok(ctx, aid, action):
        return Verdict.escalate("phê duyệt không hợp lệ cho đơn này (hết hạn, đã dùng, sai đơn hoặc thiếu hạn mức)")
    return None


def _gate_fault(ctx, action):
    # Cổng 2: ghi lỗi cho hãng là gây thiệt hại cho bên thứ ba (phạt tiền, đình chỉ) nên phải có căn cứ trong tracking.
    f = _facts(ctx, action.get("order_id"))
    if f is None:
        return Verdict.deny("thiếu dữ liệu tracking để ghi lỗi hãng")
    order, pol, parcel, delay = f
    if not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"], cause=parcel.get("delay_cause"), db_delay_days=delay)
        return Verdict.deny("tracking không ghi nguyên nhân thuộc lỗi hãng cho kiện trễ, không ghi lỗi")

    # S1 & Kinh doanh / Vận hành: Giới hạn trần số lỗi tự ghi cho một hãng trong ngày (ops_limits)
    carrier_id = parcel["carrier_id"]
    max_strikes = (ctx.tools.ops_limits() or {}).get("max_auto_strikes_per_carrier_per_day", 2)
    current_strikes = len(ctx.tools.fault_rows(carrier_id=carrier_id))
    if current_strikes >= max_strikes:
        ctx.log("carrier_fault_cap_reached", carrier_id=carrier_id, current=current_strikes, max=max_strikes)
        return Verdict.deny(f"hãng {carrier_id} đã đạt trần {max_strikes} lỗi tự động trong ngày (ops_limits), chuyển duyệt tay")

    if (action.get("parcel_id"), action.get("carrier_id")) != (parcel["parcel_id"], parcel["carrier_id"]):
        return Verdict.modify("ghi lỗi đúng kiện bị trễ và đúng hãng giao kiện đó", parcel_id=parcel["parcel_id"],
                              carrier_id=parcel["carrier_id"], driver_id=parcel.get("driver_id"), delay_days=delay)
    if action.get("delay_days") != delay:
        return Verdict.modify("ghi số ngày trễ theo tracking", delay_days=delay)
    return None


def _gate_notice(ctx, action):
    # Cổng 3: hãng chỉ nhận các trường chính sách cho phép; tên/SĐT người nhận và nguyên văn chữ khách không đi ra ngoài.
    # Lớp 1: danh sách trường được phép theo chính sách. Lớp 2: danh sách trường cấm do Vận hành và pháp lý đặt trong config
    # (legal.pii_fields_blocked_to_third_party), cấm cả khi chính sách sau này lỡ cho phép.
    pol = _policy(ctx)
    allowed = set(pol.get("carrier_notice_fields") or _SAFE_NOTICE_FIELDS) if pol else set(_SAFE_NOTICE_FIELDS)
    allowed -= set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
    payload = action.get("payload") or {}
    extra = sorted(set(payload) - allowed)
    if extra:
        ctx.log("notice_fields_dropped", dropped=extra)
        return Verdict.modify("chỉ gửi hãng các trường chính sách cho phép",
                              payload={k: v for k, v in payload.items() if k in allowed})
    return None


_WRITE_GATES = {"issue_refund": _gate_refund, "file_carrier_fault": _gate_fault, "notify_carrier": _gate_notice}


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    # Vòng 2: gọi lại ba cổng _gate_* (bản chốt vòng 1 là guards_round1.py, cổng viết gọn trong hàm này).
    # Ba cổng _gate_* bao trọn các kiểm của bản vòng 1, thêm: payer ≠ LOGIX, basis fail-open, ghi trùng,
    # phê duyệt không hợp lệ, ghi lỗi đúng kiện và đúng số ngày trễ theo tracking, chỉ gửi hãng trường được phép.
    gate = _WRITE_GATES.get(action.get("tool"))
    verdict = gate(ctx, action) if gate else None
    return verdict or Verdict.allow()
