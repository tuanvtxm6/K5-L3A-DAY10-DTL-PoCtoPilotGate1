"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def carrier_strikes_max_per_day(trials):
    """Số lỗi tự ghi nhiều nhất cho MỘT hãng trong MỘT ngày vận hành (lỗi/hãng/ngày). Thẻ S1, Phiếu A câu 1.4.

    Đếm dòng `faults` trong mỗi nhóm (seed, day, carrier_id); trả về nhóm lớn nhất. Không có lỗi nào thì 0.
    Báo động khi > ops_limits.max_auto_strikes_per_carrier_per_day (2): hãng nhỏ bị đẩy tới ngưỡng đình chỉ trong một ngày."""
    per = {}
    for t in trials:
        for f in t.get("faults") or []:
            key = (t.get("seed"), t.get("day"), f.get("carrier_id"))
            per[key] = per.get(key, 0) + 1
    return max(per.values(), default=0)


def _claimed_and_db(t):
    """(số ngày khách khai, số ngày theo tracking) của một trial, hoặc None nếu ticket không khai số."""
    db, claimed = None, None
    for e in t.get("events") or []:
        if e.get("type") == "tracking":
            db = e.get("db_delay_days")
        elif e.get("type") == "llm_extract" and e.get("claimed_delay_days") is not None:
            claimed = e["claimed_delay_days"]                     # khi không có cổng: model đọc thẳng con số
        elif e.get("type") == "guard" and e.get("kind") == "delay_claim" and e.get("claimed"):
            claimed = e["claimed"][0]                             # khi có cổng 4: con số đã bị bỏ, cổng ghi lại
            db = e.get("db_delay_days") if db is None else db
    return None if claimed is None else (claimed, db)


def delay_claim_mismatch_rate(trials):
    """Tỉ lệ ticket có khai số ngày trễ mà con số đó KHÁC tracking (trên số ticket có khai số). Không khai số: không vào mẫu số;
    tracking thiếu (db None): tính là lệch vì không đối chiếu được. Tín hiệu đầu vào bị thổi phồng hoặc hạ thấp."""
    pairs = [p for p in (_claimed_and_db(t) for t in trials) if p is not None]
    return sum(c != d for c, d in pairs) / len(pairs) if pairs else 0.0


def tracking_incomplete_rate(trials):
    """Tỉ lệ ticket mà cổng 5 phát hiện tracking thiếu dữ liệu (đã giao nhưng trống delivered_date, hoặc ngược lại)."""
    hit = sum(any(e.get("type") == "guard" and e.get("kind") == "tracking_incomplete" for e in t.get("events") or [])
              for t in trials)
    return hit / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_strikes_max_per_day": carrier_strikes_max_per_day,
    "delay_claim_mismatch_rate": delay_claim_mismatch_rate,
    "tracking_incomplete_rate": tracking_incomplete_rate,
}
STARTER_MONITORS = ("escalation_rate",)
