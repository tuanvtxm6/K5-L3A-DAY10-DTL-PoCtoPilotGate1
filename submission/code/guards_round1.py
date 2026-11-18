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
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")

    # Cổng 1 (Pre-mortem Kỹ thuật / HAZOP WRONG amount):
    # Đối chiếu quyền lợi hoàn tiền với tracking DB và chính sách hiệu lực,
    # không cho hoàn sai nếu tracking DB ghi không đủ ngày trễ hoặc tính sai tiền.
    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order:
            return Verdict.escalate("không tìm thấy đơn hàng trong hệ thống")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        policies = ctx.tools.lookup_policies()
        pol = H.effective_policy(policies, ctx.as_of)
        if not pol:
            return Verdict.escalate("không tìm thấy chính sách hoàn tiền hiệu lực")
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        ent = H.entitlement_vnd(pol, order, db_delay, parcel.get("delay_cause"))

        # Nếu tracking DB cho thấy đơn không đủ điều kiện hoàn (ent == 0) mà agent định hoàn tiền
        if ent == 0 and action.get("amount_vnd", 0) > 0:
            return Verdict.deny("đơn hàng chưa đủ ngày trễ để hoàn tiền theo dữ liệu tracking DB")

        # Nếu số tiền định hoàn vượt quá quyền lợi tính từ DB
        if action.get("amount_vnd", 0) > ent:
            return Verdict.modify("điều chỉnh số tiền hoàn về đúng quyền lợi theo tracking DB", amount_vnd=ent)

    # Cổng 2 (Pre-mortem Vận hành - Pháp lý / HAZOP WRONG fault):
    # Chặn ghi lỗi oan cho hãng nếu tracking DB chưa đủ ngày trễ hoặc nguyên nhân không thuộc lỗi hãng
    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order:
            return Verdict.deny("không tìm thấy đơn hàng để ghi lỗi hãng")
        parcel = next((p for p in order.get("parcels", []) if p["parcel_id"] == action.get("parcel_id")), None)
        policies = ctx.tools.lookup_policies()
        pol = H.effective_policy(policies, ctx.as_of)
        if not parcel or not pol:
            return Verdict.deny("không xác định được kiện hàng hoặc chính sách")
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(pol, parcel, db_delay):
            return Verdict.deny("kiện hàng chưa đủ điều kiện ghi lỗi hãng theo dữ liệu tracking DB")

    # Cổng 3 (Pre-mortem Pháp lý / HAZOP PERTURBED PII):
    # Bảo vệ dữ liệu cá nhân (PII), loại bỏ các trường thông tin nhạy cảm của người nhận trước khi gửi hãng
    if tool == "notify_carrier":
        payload = action.get("payload", {})
        blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or ["recipient_contact", "name", "phone", "street"])
        new_payload = {k: v for k, v in payload.items() if k not in blocked}
        if new_payload != payload:
            return Verdict.modify("loại bỏ trường thông tin cá nhân người nhận trước khi gửi bên thứ ba", payload=new_payload)

    return Verdict.allow()
