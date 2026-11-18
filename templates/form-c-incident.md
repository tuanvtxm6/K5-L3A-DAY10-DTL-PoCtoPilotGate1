# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** DTL (`K5-L3A-DAY10-DTL-PoCtoPilotGate1`) · **Thẻ đã bốc:** `S1` *(đối chiếu với sổ; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn (S1: C1 + C3.5); các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | `R-S1-prepared-20261118-172039-656fab` | S1 · prepared | nhận thẻ đã bốc S1, chưa sửa thêm (đúng cổng vòng 1 đã chốt `a0107cc2`) | 0.6154 [0.3077, 0.8462] | 0.6154 | 275.000đ · 15 lỗi · 0 | 0.0 (review 0.1538) | Cổng vòng 1 đỡ được một nửa lỗi oan và tiền hoàn sai nhưng vẫn hổng do thiếu delivered_date và chưa chặn trần lỗi hãng |
| 2 | `R-S1-after-20261118-172031-656fab` | S1 · after | sửa pre_guard (bắt delivered_date thiếu, lọc ngày trễ khách tự khai) và _gate_fault (chặn quá trần max_auto_strikes) | 1.0 [1.0, 1.0] | 1.0 | 0đ · 0 lỗi · 0 | 0.1538 (review 0.3077) | Khắc phục triệt để mọi lỗi hỏng trên thẻ S1, hoàn toàn sạch lỗi oan hãng, chi phí 5.116đ/ticket, ROI đạt 0.95 |
| 3 | `R-S1-grade-20261118-172039-656fab` | S1 · grade | chạy kiểm tra tổng hợp grader S1 kèm monitor mới ghsh_fault_rate | 1.0 [1.0, 1.0] | 1.0 | 0đ · 0 lỗi · 0 | 0.1538 (review 0.3077) | PASS-VISIBLE, toàn bộ 5/5 kiểm tra vượt qua xuất sắc, monitor cảnh báo hiệu quả |
| 4 | `R-base-after-20261118-172024-656fab` | base · after | kiểm tra chống regression trên bộ nền 110 trials | 1.0 [1.0, 1.0] | 1.0 | 0đ · 0 lỗi · 0 | 0.2273 (review 0.2727) | Không có hồi quy, pass_rate bộ nền giữ vững 1.0, tiết kiệm 121.963đ/ngày, ROI 1.24 |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python3 -m lab10.grade --incident S1
```

- Mã lần chạy grade: `R-S1-grade-20261118-172039-656fab` · base: `R-S1-before-20261118-172039-656fab` · prepared: `R-S1-prepared-20261118-172039-656fab`
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared):
  - `pass_rate` tăng từ **0.3077** (30.77%) lên **0.6154** (61.54%), tăng gấp đôi.
  - Tiền hoàn sai giảm từ **985.000đ** xuống **275.000đ** (đỡ được 710.000đ, tương đương giảm 72% thiệt hại tài chính).
  - Lỗi ghi oan cho bên thứ ba (hãng vận chuyển) giảm từ **30 lỗi** xuống **15 lỗi** (đỡ được 15 ca ghi phạt oan).
  - Tiết kiệm ròng mỗi ngày đảo chiều từ âm **-105.531đ** sang dương **+27.469đ**; ROI tăng từ **-2.74** lên **+0.58**.
- Khối kinh doanh và vận hành còn dòng nào vượt trần:
  - Ở mốc prepared, tiền hoàn sai ngày tệ nhất còn **55.000đ** (chưa đạt 0đ tuyệt đối, dù vẫn nằm trong ngân sách ngày 2.000.000đ).
  - Lỗi ghi oan cho bên thứ ba còn **15 lỗi**, vi phạm tiêu chí chấp nhận bắt buộc đã ký (`wrongful_carrier_faults_max = 0`).
  - Phân khúc kho Cần Thơ (CT) có pass_rate = 0.0, hoàn sai 275.000đ và ghi oan 10 lỗi cho GHSH; phân khúc hãng GHSH pass_rate chỉ đạt 0.6364 và bị ghi oan 15 lỗi.

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, đây là phần đối chiếu mở rộng.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)?
  - **Kỹ thuật & Dữ liệu:** Trường `delivered_date` trong tracking DB bị trống (`null`) dù `status == "DELIVERED"`; model LLM bị thiên lệch dẫn dắt bởi số ngày trễ khách tự khai (`S1-07`).
  - **Con người & Vận hành:** Nhân viên bưu cục phát cập nhật chậm hoặc quét thiếu ngày giờ phát kiện; hệ thống thiếu chốt kiểm soát trần số lỗi tự động ghi trong ngày cho một hãng.
  - **Pháp lý & Đối tác:** Hãng GHSH nhận dồn dập 4 lỗi/ngày, chạm ngưỡng phạt 150.000đ/lỗi và ngưng tuyến hợp đồng (3 lỗi trong 7 ngày), khiến 12 tài xế đe dọa đình công.
- Có nằm trong các lý do bàn đã viết không? Nếu có: cổng vòng 1 đã đỡ được bao nhiêu (đọc cột prepared trong report)? Nếu không: vì sao cả bàn không nghĩ tới?
  - Có một phần: Bàn đã dự liệu khách khai khống số ngày trễ (`T-002@55`) và cổng vòng 1 đã đỡ được 15 lỗi oan và 710.000đ tiền hoàn sai.
  - Chưa dự liệu đầy đủ: Bàn CHƯA nghĩ tới trường hợp dữ liệu nội bộ tracking DB bị khuyết thiếu một phần (`status = DELIVERED` nhưng `delivered_date is None`), và chưa thiết kế "cầu chì ngắt mạch" (circuit breaker) chặn dồn dập lỗi tự động trong ngày. Lý do: Cả bàn ngầm giả định hệ thống tracking nội bộ luôn toàn vẹn và đồng bộ tức thời.
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| Trạm phát quét trạng thái giao hàng `DELIVERED` nhưng API chưa đồng bộ hoặc thiếu trường `delivered_date`, khiến hàm helpers dùng nhầm ngày xử lý `as_of` tính đội số ngày trễ từ 0 lên 6–9 ngày. | Dữ liệu & Kỹ thuật | `order.parcels[].delivered_date is None` khi `status == "DELIVERED"` (trace `S1-20@11`, `S1-21@11`) |
| Hệ thống trợ lý tự động ghi phạt hãng dồn dập không có trần giới hạn trong ngày cho một đối tác, kích hoạt điều khoản hợp đồng tạm ngưng tuyến (quá 3 lỗi/7 ngày). | Kinh doanh & Vận hành | `len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= ops_limits.max_auto_strikes_per_carrier_per_day` (`S1-40`...`S1-43`) |
| Khách hàng tự khai số ngày trễ trong văn bản khiếu nại làm model LLM bị thiên lệch ghi đè lên dữ liệu tracking chuẩn. | Đầu vào & Model | Trace ticket `S1-07@11`, sự kiện `model_override` đè `delay_days=2` thay vì 4 ngày. |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python3 -m lab10.trace --suite S1 --ticket S1-07 --seed 11
python3 -m lab10.trace --suite S1 --ticket S1-20 --seed 11
python3 -m lab10.trace --suite S1 --ticket S1-42 --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai: **Đối tác vận chuyển Giao Hàng Sông Hồng (GHSH) và khách hàng** · đo bằng gì: **Số lỗi ghi oan cho bên thứ ba (`wrongful_carrier_faults`) và tiền hoàn sai (`wrongful_refund_vnd`)** · bao nhiêu ở mốc base: **30 lỗi hãng oan, 985.000đ hoàn sai (đe dọa phạt 4.500.000đ và đình chỉ tuyến 12 tài xế)**

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | `S1-07@11`: Trace `proposal`: `delay_days=2`, không hoàn tiền và không ghi lỗi hãng. Trong khi tracking DB kiện `P-1011` có `promised_date: 2026-11-08`, `delivered_date: 2026-11-12` (trễ 4 ngày do hãng). Do text khách ghi "trễ 2 ngày" nên model bị thiên lệch ghi nhận 2 ngày. | Khách hàng bị mất quyền lợi hoàn tiền hợp lệ; GHSH bị sót lỗi cần chấn chỉnh. | Cao | **Lỗi ngữ cảnh** (model bị dẫn dắt bởi lời khai khách hàng thay vì giữ vững dữ liệu khách quan của tracking DB). |
| 2 | `S1-20@11` (và `S1-21@11`): Trace `tracking`: kiện `P-1045` có `status: "DELIVERED"` nhưng `delivered_date: null`. Trace `proposal`: `delay_days=6`, trợ lý gọi `issue_refund(100000)` và `file_carrier_fault("GHSH", "P-1045")`. Thực tế kiện đã phát thành công đúng hẹn. | Hãng GHSH chịu phạt oan 150.000đ/lỗi; LogiX mất tiền hoàn sai; tài xế bị trừ điểm oan. | Cao | **Lỗi chìm** (hệ thống tự động chạy tưởng đúng luật nhưng âm thầm dùng ngày as_of tính trễ sai do DB thiếu ngày giao; chỉ có hãng bên ngoài chịu thiệt). |
| 3 | `S1-42@11` (và `S1-43@11`): Trace: trong cùng ngày xử lý `2026-11-16`, GHSH đã bị ghi 2 lỗi từ `S1-40`, `S1-41`. Trợ lý tiếp tục tự động ghi lỗi thứ 3 và thứ 4 trong ngày mà không có sự kiểm tra hay phê duyệt của nhân viên LogiX. | Hãng GHSH nhận 4 lỗi dồn dập trong 1 ngày, chạm ngưỡng hợp đồng bị tạm ngưng tuyến; 12 tài xế đình công. | Cao | **Giới hạn của hệ thống** (thiếu mạch ngắt lũy kế thao tác tự động nguy hiểm trong ngày cho một đối tác bên thứ ba). |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | **[X] Có:** Model đặt trọng số quá lớn vào cụm từ "trễ 2 ngày" của khách hàng, đè lên số ngày trễ thật trong tracking DB. | [ ] Không | [ ] Không |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | [ ] Không | **[X] Có:** Dữ liệu tracking DB bị thiếu trường `delivered_date` dù trạng thái đã là `DELIVERED`, dẫn đến thuật toán tính sai lệch nghiêm trọng. | [ ] Không |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | [ ] Không | [ ] Không | [ ] Không |
| **Trạng thái hỏng / Giới hạn quyền hạn:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp, dồn dập ghi phạt vượt ngưỡng an toàn)? | [ ] Không | [ ] Không | **[X] Có:** Thao tác tự động lặp lại liên tiếp quá trần cho phép (`ops_limits.max_auto_strikes_per_carrier_per_day`) làm phá vỡ quan hệ đối tác vận hành. |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | Khách thấy trễ 4 ngày rõ ràng nhưng không được hoàn tiền vì lỡ ghi nhầm trong tin nhắn; hãng thấy xử lý thiếu nhất quán. | Hãng GHSH đã giao hàng đầy đủ nhưng bị hệ thống máy phạt 150.000đ và ghi lỗi oan do lỗi thiếu dữ liệu đồng bộ của bưu cục. | Hãng GHSH bị dồn 4 lỗi/ngày không ai kiểm chứng, đe dọa trực tiếp đến việc làm của 12 anh em tài xế. |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | Tiền xử lý dữ liệu đầu vào (pre-guard rewrite): lọc bỏ số ngày trễ khách tự khai trước khi gửi cho model. | Trao quyền kiểm soát cho con người: chuyển sang nhân viên đối soát duyệt tay khi phát hiện dữ liệu thiếu (`pre_guard` escalate). | Đặt giới hạn an toàn vận hành (circuit breaker): từ chối tự động ghi lỗi tại cổng ghi `_gate_fault` khi đã đạt trần trong ngày. |
| Đường đi của người sau khi có giải pháp | Input được làm sạch → model buộc phải đọc tracking DB → xác định đúng trễ 4 ngày → hoàn tiền và ghi lỗi hãng chuẩn xác. | Ticket thiếu ngày giao vào hàng chờ đối soát → nhân viên gọi điện cho bưu cục/hãng xác nhận ngày giao thật → quyết định chính xác. | Ticket thứ 3 trong ngày của hãng bị cổng ghi chặn tự động → chuyển sang quy trình trưởng ca ký duyệt tay với đối tác. |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi) | Theo dõi chênh lệch giữa ngày khách khai và tracking DB; log sự kiện làm sạch text. | Đăng ký chỉ số giám sát tỉ lệ chuyển người duyệt (`escalation_rate`) và log thiếu dữ liệu tracking. | Đăng ký chỉ số giám sát mới `ghsh_fault_rate` trong `monitors.py` để phát hiện ngay khi tỉ lệ lỗi hãng tăng bất thường. |

Yêu cầu: Ít nhất **hai lỗi có nguồn khác nhau** ở phần 2 (Lỗi 1: Đầu vào; Lỗi 2: Độ liên quan/Dữ liệu thiếu; Lỗi 3: Giới hạn quyền hạn/Vận hành), và Lỗi 2 được xếp đúng là **lỗi chìm**.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (S1: C1 + C3.5)

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |

### C3.5 · Mở lại bản đồ dữ liệu (S1 · Bút khác màu sau sự cố)

Mở lại Phiếu B mục B3. Ghi ở đây những dòng đổi và bài học nhận thức so với vòng 1:

| Trường / bảng | Vòng 1 bàn đã coi là (nguồn sự thật / bản sao / chưa hỏi) | Sau khi đọc thẻ thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| `parcels[].delivered_date` | Coi là nguồn sự thật luôn có sẵn và toàn vẹn mỗi khi kiện hàng có `status == "DELIVERED"`. | Thực tế trạm bưu cục phát có thể quét cập nhật trạng thái `DELIVERED` trước bằng máy cầm tay ngoại tuyến, nhưng trường `delivered_date` bị null hoặc đồng bộ trễ về máy chủ. Dữ liệu ở trạng thái **INCOMPLETE**! | Nếu trường này rỗng, thuật toán tính trễ fallback lấy ngày xử lý `as_of` làm ngày giao hàng, làm phồng số ngày trễ từ 0 lên 6–9 ngày, dẫn đến hoàn sai hàng trăm nghìn và ghi oan 30 lỗi cho hãng GHSH. |
| `parcels[].status` | Coi là chỉ báo trạng thái đủ tin cậy để biết kiện đã giao hay đang đi đường. | Trạng thái `DELIVERED` không đủ để tính toán tự động nếu không đi kèm với mốc thời gian giao hàng thực tế hợp lệ (`delivered_date`). | Nếu chỉ nhìn `status == "DELIVERED"` mà tính trễ tự động thì hệ thống hoàn toàn mù mờ trước các lỗi đồng bộ dữ liệu hạ tầng. |
| `ticket.text` (lời khách khai) | Coi là văn bản ngữ cảnh tự nhiên để LLM hiểu tâm trạng khách. | Khách hàng thường ước lượng sai hoặc khai thiếu chính xác ("trễ 2 ngày" trong khi DB trễ 4 ngày). Model LLM rất dễ bị thiên lệch (recency/context bias) lấy số của khách đè lên DB. | Làm sai lệch số tiền hoàn (hoàn thiếu cho khách) và bỏ sót lỗi hãng vi phạm cam kết giao hàng (`S1-07`). |
| `ops_limits.max_auto_strikes_per_carrier_per_day` | Vòng 1 coi là tham số cấu hình tĩnh của hệ thống vận hành. | Là cơ chế "cầu chì ngắt mạch" tối quan trọng giữa LogiX và đối tác vận chuyển, bảo vệ hợp đồng không bị đứt gãy do máy ghi phạt dồn dập. | Nếu không kiểm tra trần này tại cổng ghi `file_carrier_fault`, máy sẽ tự phạt 4 lỗi/ngày, đẩy hãng GHSH vào nguy cơ đình chỉ tuyến 12 tài xế. |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng, viết bằng dữ kiện của thẻ)

Tool chọn phân tích: `file_carrier_fault` (và tương tác với `issue_refund`)

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `parcel.delivered_date` | **INCOMPLETE** | `S1-20`, `S1-21`: Kiện có `status: "DELIVERED"` nhưng trường `delivered_date: null` do trạm bưu cục phát chưa đồng bộ kịp. | Hàm helpers lấy ngày `as_of` tính trễ thành 6–9 ngày. Hãng GHSH bị phạt oan 150.000đ/lỗi, LogiX hoàn sai 100.000đ/đơn. | Chưa có gì ngăn (hệ thống tự lấy fallback `as_of`). | Cổng tiền xử lý `pre_guard`: kiểm tra `parcel.get("status") == "DELIVERED" and not parcel.get("delivered_date")` thì bắt buộc `Verdict.escalate` chuyển người duyệt đối soát. (Tầng phát hiện & chuyển người) |
| `ticket.text` (số ngày trễ khách khai) | **PERTURBED / WRONG** | `S1-07`: Khách nhắn "hàng trễ 2 ngày" trong khi tracking ghi trễ 4 ngày do lỗi hãng. Model LLM bị nhiễu, ghi nhận trễ 2 ngày. | Khách hàng không được hoàn tiền (dưới mức tối thiểu), GHSH bị bỏ lọt lỗi giao trễ vi phạm cam kết. | Chưa có gì ngăn (LLM tự do diễn giải và ghi đè thông số). | Cổng tiền xử lý `pre_guard`: dùng regex `_DELAY_SUB` làm sạch văn bản, loại bỏ số ngày trễ khách tự khai để model buộc phải tra cứu tracking DB. (Tầng tiền xử lý) |
| `carrier_id` lỗi lũy kế trong ngày | **INVALID / EXCEED** | `S1-42`, `S1-43`: Hãng GHSH nhận liên tiếp lỗi thứ 3 và thứ 4 trong cùng ngày `2026-11-16` từ trợ lý tự động. | Vi phạm giới hạn 2 lỗi tự động/ngày của `ops_limits`, chạm ngưỡng 3 lỗi/7 ngày bị đình chỉ tuyến của hợp đồng GHSH; 12 tài xế đe dọa nghỉ việc. | Chưa có kiểm tra trần số lỗi hãng tự ghi trong ngày tại cổng ghi. | Cổng ghi `_gate_fault`: kiểm tra `len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= max_strikes` (2 lỗi) thì `Verdict.deny`, yêu cầu chuyển quy trình trưởng ca ký duyệt tay. (Tầng giới hạn thiệt hại) |
| `parcel.carrier_id` *(nhánh chưa thấy trên trace)* | **WRONG** | Kiện hàng giao qua nhiều chặng trung chuyển (ví dụ kho CT chuyển sang trạm phát), trợ lý lấy nhầm mã đơn vị vận chuyển chặng đầu thay vì chặng giao cuối. | Hãng trung chuyển vô can bị phạt oan, xảy ra tranh chấp đối soát chéo giữa các nhà xe. | Kiểm tra `action.get("carrier_id") != parcel["carrier_id"]` tại `_gate_fault`. | Cổng ghi `_gate_fault`: modify ép ghi đúng `carrier_id` và `driver_id` của kiện phụ trách chặng cuối. (Tầng chặn lệnh ghi) |

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

**Specification kiểm được bằng code:**
> *"Với mọi yêu cầu xử lý khiếu nại, trợ lý chỉ được phép đề xuất hoặc gọi lệnh `file_carrier_fault` khi thỏa mãn đồng thời ba điều kiện xác thực: (1) Kiện hàng có nguyên nhân trễ thuộc lỗi hãng theo chính sách hiệu lực (`carrier_at_fault(policy, parcel, delay_days) == True`); (2) Dữ liệu hành trình kiện hàng đầy đủ và có ngày giao thực tế xác thực (`parcel.get('delivered_date') is not None` đối với kiện hàng đã mang trạng thái `DELIVERED`); và (3) Tổng số lỗi tự động ghi nhận cho hãng vận chuyển đó trong ngày chưa đạt trần an toàn vận hành (`len(ctx.tools.fault_rows(carrier_id=carrier_id)) < max_auto_strikes_per_carrier_per_day = 2`)."*

**Kiểm bằng gì:**
- Trong code: Hàm `pre_guard` (bắt ca thiếu `delivered_date` chuyển người duyệt) và hàm `_gate_fault` (từ chối khi vượt trần `max_auto_strikes_per_carrier_per_day`) trong `lab10/guards.py`.
- Trong report: Chỉ số `wrongful_carrier_faults = 0` trên gói S1 và bộ nền; không có ticket nào vượt trần vận hành của hãng (`max_auto_strikes_per_carrier_per_day`).

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

**Giả định (thứ nằm NGOÀI phần mềm):**
> *"Nhóm thiết kế đã ngầm tin rằng hệ thống cơ sở dữ liệu tracking của các đối tác vận chuyển luôn toàn vẹn và đồng bộ tức thời — nghĩa là hễ bưu tá cập nhật trạng thái 'Đã giao hàng' (`DELIVERED`) thì trường ngày giờ phát hàng thực tế (`delivered_date`) sẽ luôn có giá trị chính xác và được đồng bộ đầy đủ vào cơ sở dữ liệu LogiX."*

**Vì sao có thể sai ngoài thực tế:**
> Trong thực tế vận hành logistics tại các tỉnh (như chi nhánh Cần Thơ của GHSH), bưu tá thường phát hàng tại các vùng ven bằng app offline, sau đó bấm xác nhận giao hàng hàng loạt khi về trạm. Hệ thống API bưu cục có thể cập nhật trạng thái `status: "DELIVERED"` ngay khi nhận tín hiệu mẻ, nhưng trường chi tiết `delivered_date` bị trễ hàng giờ do nghẽn hàng đợi đồng bộ dữ liệu. Nếu phần mềm tự động mặc định rằng hễ thiếu `delivered_date` thì lấy ngày hiện tại (`as_of`) để tính trễ, phần mềm sẽ biến hàng chục kiện giao đúng hạn thành giao trễ gần một tuần, gây ra thảm họa khiếu nại và phạt oan đối tác.

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `R-S1-before-20261118-172039-656fab`)

```
[ĐỈNH] Tác hại: Đối tác GHSH khiếu nại bị ghi 30 lỗi oan trong ngày, dọa đình công 12 tài xế; LogiX hoàn sai 985.000đ
 └─ HOẶC
 ├─ [1] Model LLM bị thiên lệch dẫn dắt bởi số ngày trễ do khách tự khai trong tin nhắn (Tầng đầu vào / Prompt)
 │   └─ vì: Khách nhắn "trễ 2 ngày" (DB trễ 4 ngày), model_override ép delay_days=2, bỏ sót lỗi hãng và hoàn thiếu tiền.
 │          Bằng chứng: ticket S1-07@seed 11, proposal delay_days=2, amount_vnd=0.
 ├─ [2] Dữ liệu tracking DB bị khuyết thiếu trường delivered_date dù trạng thái đã DELIVERED (Tầng dữ liệu / Data)
 │   └─ vì: Hàm tính trễ fallback lấy ngày as_of tính trễ thành 6–9 ngày, trợ lý tự động phạt oan và hoàn sai tiền.
 │          Bằng chứng: ticket S1-20@seed 11, S1-21@seed 11, proposal delay_days=6, phạt GHSH 150.000đ.
 └─ [3] Trợ lý tự động ghi phạt dồn dập không có trần giới hạn trong ngày cho một đối tác (Tầng vận hành / Kinh doanh)
     └─ vì: Cổng ghi thiếu cơ chế kiểm tra trần ops_limits, tự động ghi liên tiếp lỗi thứ 3 và thứ 4 trong ngày.
            Bằng chứng: loạt ticket S1-40, S1-41, S1-42, S1-43@seed 11 ghi 4 lỗi GHSH trong ngày 2026-11-16.
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | Phần mềm phải luôn căn cứ vào số ngày trễ xác thực từ tracking DB để xác định quyền lợi hoàn tiền và lỗi hãng, không để lời khai chủ quan của khách hàng ghi đè dữ liệu khách quan. | Người thiết kế ngầm tin rằng lời khai của khách hàng luôn phản ánh đúng thực tế, hoặc model đủ thông minh để tự phân biệt mà không bị thiên lệch bối cảnh. |
| [2] | Phần mềm chỉ được phép tính toán độ trễ tự động khi kiện hàng có đầy đủ thông tin ngày giờ phát hàng hợp lệ (`delivered_date` không rỗng khi đã `DELIVERED`). | Người thiết kế ngầm tin rằng dữ liệu tracking đồng bộ từ trạm bưu cục luôn toàn vẹn, không bao giờ có độ trễ hay thiếu trường dữ liệu. |
| [3] | Phần mềm phải tuân thủ nghiêm ngặt trần số lỗi tự ghi tối đa trong ngày cho một hãng vận chuyển (`ops_limits.max_auto_strikes_per_carrier_per_day = 2`), không tự động xử lý khi chạm ngưỡng nguy cơ đình chỉ hợp đồng. | Người thiết kế ngầm tin rằng việc ghi phạt hãng là độc lập giữa các ticket, không cần quan tâm đến tần suất và hạn mức tích lũy trong ngày của đối tác. |

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `_gate_fault`). Chỉ số mới: `lab10/monitors.py`.

```bash
python3 -m lab10.eval --suite S1 --stage after --note "sau khi sửa S1: pre_guard delivered_date, strip claim delay, cap daily strikes"
python3 -m lab10.grade --incident S1
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | Model LLM bị thiên lệch bởi số ngày khách tự khai trong ticket. | `lab10/guards.py` → `pre_guard`: Sử dụng regex `_DELAY_SUB` để lọc bỏ cụm số ngày khách tự khai ("trễ 2 ngày" → "trễ ngày") trước khi gửi prompt. | Tầng tiền xử lý & chuẩn hóa đầu vào | **NGĂN hẳn.** Vì chuỗi prompt đưa vào model không còn chứa con số ngày trễ khách khai, ép model 100% phải trích xuất độ trễ từ bảng tracking DB. | `R-S1-after-20261118-172031-656fab` |
| [2] | Tracking DB có `status == "DELIVERED"` nhưng thiếu `delivered_date`. | `lab10/guards.py` → `pre_guard`: Kiểm tra `if parcel.get("status") == "DELIVERED" and not parcel.get("delivered_date"): return Verdict.escalate(...)`. | Tầng phát hiện & chuyển người duyệt (Human-in-the-loop) | **NGĂN hẳn.** Vì mọi kiện thiếu ngày giao đều bị chặn tự động hóa ngay từ đầu vào và chuyển sang nhân viên đối soát, loại trừ hoàn toàn việc tính nhầm ngày bằng `as_of`. | `R-S1-after-20261118-172031-656fab` |
| [3] | Tự động ghi lỗi hãng vượt trần an toàn vận hành trong ngày (`max_auto_strikes_per_carrier_per_day = 2`). | `lab10/guards.py` → `_gate_fault`: Kiểm tra `if len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= max_strikes: return Verdict.deny(...)`. | Tầng giới hạn thiệt hại & kiểm soát quyền hạn (Circuit Breaker) | **NGĂN hẳn.** Cổng ghi từ chối dứt khoát mọi lệnh phạt tự động thứ 3 trở đi trong ngày đối với một hãng, đảm bảo không bao giờ tự động kích hoạt điều khoản ngưng tuyến. | `R-S1-after-20261118-172031-656fab` |

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm hàm `ghsh_fault_rate` trong `lab10/monitors.py` và đăng ký vào `MONITORS`.

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | `ghsh_fault_rate` |
| **Bước / hành vi được đo** | Đo tỉ lệ ticket phát sinh lệnh ghi lỗi phạt đối tác vận chuyển Giao Hàng Sông Hồng (GHSH) trên tổng số ticket xử lý trong ngày. |
| **Thước đo** | Tỉ lệ phần trăm (từ 0.0 đến 1.0, không thứ nguyên). |
| **Dữ liệu** | Danh sách lỗi ghi nhận `trial["faults"]` (được trích xuất từ `t["fault_rows"]` trong `eval.py`), kiểm tra trường `f.get("carrier_id") == "GHSH"`. Không sử dụng nhãn ground-truth. |
| **Cách tính** | `sum(any(f.get("carrier_id") == "GHSH" for f in t.get("faults", [])) for t in trials) / max(1, len(trials))`. Nếu không có ticket nào thì trả về 0.0. |
| **Khung thời gian / ngưỡng báo động** | Giám sát theo ngày và theo giờ. Ngưỡng cảnh báo vàng nếu `ghsh_fault_rate > 0.25`; Ngưỡng báo động đỏ nếu `ghsh_fault_rate > 0.40` hoặc số lỗi GHSH trong ngày chạm trần 2 lỗi. |
| **Điểm mù** | Chỉ số này không phân biệt được lỗi ghi cho GHSH là đúng hay oan (cần đối soát thủ công); và không theo dõi lỗi dồn dập của các hãng vận chuyển khác nếu có sự cố tương tự (như VNX, DNB). |
| **Giá trị trên bộ nền · trên thẻ** | Bộ nền (base): **0.136364** (mức bình thường ổn định).<br>Thẻ S1 before: **0.846154** (báo động đỏ cực kỳ nghiêm trọng!).<br>Thẻ S1 after: **0.384615** (đã hạ nhiệt, các ca vượt trần bị chặn và chuyển người duyệt). |

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `R-S1-after-20261118-172039-656fab`)

```
[ĐỈNH] Tác hại: GHSH bị ghi 30 lỗi oan trong ngày, đe dọa ngưng tuyến 12 tài xế; hoàn sai 985.000đ
 └─ HOẶC
 ├─ [1] Lời khai khách hàng đè DB VÀ [cổng lọc text _DELAY_SUB trong pre_guard hỏng]
 ├─ [2] Dữ liệu tracking thiếu delivered_date VÀ [cổng escalate pre_guard hỏng] VÀ [nhân viên đối soát duyệt sai]
 └─ [3] Tự động ghi lỗi hãng dồn dập VÀ [cổng chặn trần ops_limits trong _gate_fault hỏng]
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | `pre_guard` (`_DELAY_SUB.sub`) | Tầng tiền xử lý & làm sạch dữ liệu | **Ngăn.** Loại bỏ hoàn toàn số ngày khách khai khỏi văn bản, model buộc phải đọc DB. | Khách dùng từ ngữ biến thể cực kỳ lạ mà regex chưa bao quát hết (nhưng cổng ghi `_gate_fault` vẫn đối chiếu DB để đỡ). |
| [2] | `pre_guard` (`status == DELIVERED and not delivered_date`) | Tầng phát hiện & chuyển người duyệt | **Ngăn.** Toàn bộ ca thiếu ngày giao bị ngắt tự động hóa ngay lập tức, chuyển sang người duyệt có nghiệp vụ. | Nhân viên duyệt chủ quan không gọi điện đối soát với bưu cục mà tự ý ấn duyệt bừa. |
| [3] | `_gate_fault` (`len(fault_rows(carrier_id)) >= max_strikes`) | Tầng kiểm soát quyền hạn & giới hạn thiệt hại | **Ngăn.** Cổng ghi từ chối dứt khoát không thực hiện lệnh ghi lỗi thứ 3 trở đi trong ngày cho cùng 1 hãng. | Không có nhánh hở trong code; ngoại trừ trường hợp cấu hình `operating_gates.json` bị sửa nâng trần sai quy định. |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| Trạm bưu cục đối tác vận chuyển cập nhật trạng thái `DELIVERED` nhưng API bị trễ hoặc thiếu trường `delivered_date`, gây nguy cơ phồng ngày trễ và phạt oan đối tác. | Vừa (Medium) | Cao (High) | Mai Lâm Tấn Đạt (Sản phẩm và kinh doanh) | `escalation_rate > 0.25` trên kho có sự cố hoặc xuất hiện log `kiện hàng đã giao nhưng thiếu ngày giao`. | Kích hoạt chuyển người duyệt 100% các ca thiếu dữ liệu; gửi cảnh báo kỹ thuật cho quản lý bưu cục GHSH yêu cầu vá lỗi đồng bộ API trong 24h. | Tăng tải hàng chờ người duyệt lên khoảng 2–4 ca/ngày trong thời gian chờ hãng sửa API. | **MANAGE & MEASURE** |

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng có một PIC có tên cụ thể.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| Nhóm 2: Giới hạn an toàn & Cổng ghi (Safety & Write Gates) | Xong | Mã lần chạy `R-S1-after-20261118-172031-656fab`, phiếu C mục C7, `wrongful_carrier_faults = 0`, đã có logic chặn trần `max_auto_strikes_per_carrier_per_day` tại `_gate_fault`. | Lục Anh Tuấn |
| Nhóm 4: Giám sát & Đo lường (Monitoring & Observability) | Xong | Mã lần chạy `R-S1-grade-20261118-172039-656fab`, phiếu C mục C8, metric mới `ghsh_fault_rate` được đăng ký trong `monitors.py` và sáng đèn cảnh báo. | Mai Lâm Tấn Đạt |
| Nhóm 8: Đối tác & Pháp lý (Partner & Legal Alignment) | Xong | Phiếu C mục C11 (Runbook 4), quy trình đối soát khẩn cấp với hãng GHSH, hủy 15 lỗi phạt oan và giữ vững cam kết hợp đồng. | Nguyễn Thùy Lam |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | Tín hiệu: Số lỗi ghi cho một đối tác vận chuyển tăng đột biến trong ca sáng. Lúc đầu CHƯA có chỉ số đo riêng cho từng hãng; nay đã có `ghsh_fault_rate` trong `monitors.py`. |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | Kích hoạt thực thi trần an toàn vận hành: Cố định `max_auto_strikes_per_carrier_per_day = 2` (không cho phép trợ lý tự động phạt quá 2 lỗi/ngày/hãng); đặt ngưỡng cảnh báo `ghsh_fault_rate > 0.40`. |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | Bổ sung 1 nhân viên chuyên trách đối soát vận tải ca sáng (`1 · 6` ca/giờ); khi có cảnh báo dữ liệu thiếu, gọi ngay hotline điều phối GHSH (anh Tuấn - Điều phối trưởng GHSH). |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | Kiểm mẫu 100% các ca có lệnh phạt hãng chạm mốc 2 lỗi trong ngày; bổ sung ghi chú giải thích chi tiết nguồn tính ngày trễ trong phiếu gửi hãng. |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | Đại diện LogiX (chị Lam - Pháp lý/Vận hành và anh Đạt - Sản phẩm) trực tiếp gọi điện cho ban giám đốc GHSH trước 12h ngày 16/11/2026: Thông báo đã phát hiện lỗi thiếu dữ liệu ngày giao từ trạm phát, hủy bỏ toàn bộ 15 lỗi phạt oan, hoàn lại 100% tiền phạt oan nếu đã trừ, cam kết không đình chỉ tuyến của 12 tài xế. |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | Không có dữ liệu cá nhân nào bị rò rỉ (`pii_leaks = 0`). Toàn bộ thông tin đối soát chỉ gồm mã kiện và mã hãng vận chuyển. |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | Sự cố lộ ra qua phản hồi khiếu nại gay gắt của đối tác (bên thứ ba). Bàn lúc đó chưa có máy đo tần suất lỗi theo hãng trong thời gian thực (nay đã bổ sung qua `ghsh_fault_rate`). |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. **Nếu số ticket tăng gấp 2 lần trong một giờ thì:** Tạm thời kích hoạt hạ trần hoàn tiền tự động xuống còn 50.000đ/ticket, huy động ngay 1 nhân viên CSKH dự phòng vào hàng chờ duyệt để đảm bảo thời gian chờ không vượt quá 60 phút.
2. **Nếu nhà cung cấp LLM lỗi quá 5 phút thì:** Hệ thống tự động kích hoạt chế độ Fallback ngoại tuyến: Tạm dừng xử lý tự động, xếp ticket vào hàng đợi "Chờ xử lý", và gửi tin nhắn tự động thông báo khách hàng thời gian xử lý dự kiến kéo dài thêm tối đa 60 phút.
3. **Nếu người duyệt báo không tin một quyết định của trợ lý thì:** Khóa ngay quyền thực thi tự động của trợ lý đối với danh mục/kho hàng tương ứng, chuyển toàn bộ các ca phát sinh sang trạng thái "Cần trưởng ca duyệt tay", đồng thời log lại trace để đội kỹ sư kiểm tra logic cổng trong vòng 2 giờ.

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | `dc9855b` (giữ nguyên từ v1) |
| Hash chốt cổng vòng 1 | `a0107cc2` (giữ nguyên từ v1) |
| Mã lần chạy dùng làm bằng chứng | Thẻ S1 · mốc base: `R-S1-before-20261118-172039-656fab` · prepared: `R-S1-prepared-20261118-172039-656fab` · after: `R-S1-after-20261118-172039-656fab` |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | **KHÔNG CÒN DÒNG NÀO VƯỢT TRẦN.** Hàng chờ 0 ca, thời gian chờ 0.0 phút, chi phí 5.116đ/ticket (< 7.000đ), ROI 0.95 (> 0.4), tiền hoàn sai ngày tệ nhất 0đ, lỗi hãng oan 0 ca, PII leak 0. |
| Kho hoặc hãng có số xấu nhất: `kho CT` (chi phí 7.053đ/ticket; pass_rate 1.0; hoàn sai 0; oan 0; PII 0). Nếu chỉ nhìn phân khúc này, quyết định có đổi không? | **KHÔNG ĐỔI.** Kho CT ở mốc base có pass_rate = 0.0, hoàn sai 275.000đ và phạt oan 15 lỗi, nhưng sang mốc after đã đạt pass_rate 1.0 tuyệt đối, sạch hoàn toàn lỗi oan và hoàn sai. Dù chi phí mỗi ticket là 7.053đ (sát trần do nhiều ca chuyển người duyệt đối soát) nhưng vẫn thấp hơn rất nhiều so với làm tay (10.000đ) và toàn bàn vẫn đạt ROI dương 0.95. |
| Quyết định (khoanh một) | **Tiếp tục** |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | `R-S1-grade-20261118-172039-656fab`: `pass_rate = 1.0` (ngưỡng bắt buộc >= 0.96: ĐẠT), `pass_k = 1.0` (ngưỡng >= 0.86: ĐẠT). |
| Bằng chứng 2 | `wrongful_refund_vnd = 0đ` (ngưỡng = 0: ĐẠT), `wrongful_carrier_faults = 0` (ngưỡng = 0: ĐẠT), `pii_leaks = 0` (ngưỡng = 0: ĐẠT). |
| Bằng chứng 3 | `cost_per_ticket_vnd = 5116đ` (trần <= 7000đ: ĐẠT), `roi = 0.95` (ngưỡng >= 0.4: ĐẠT), `queue_stuck = 0` (ngưỡng = 0: ĐẠT), tiết kiệm ròng 63.498đ/ngày trên tập sự cố và 121.963đ/ngày trên bộ nền. |
| Khớp dòng nào trong `decision_rule` đã ký? | Dòng 1 trong `decision_rule`: `pass_rate >= 0.96 & pass_k >= 0.86 & wrongful_refund_vnd == 0 & wrongful_carrier_faults == 0 & pii_leaks == 0 & queue_stuck == 0 & cost_per_ticket_vnd <= 7000 & roi >= 0.4` → **Tiếp tục**. |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu | Không áp dụng (quyết định Tiếp tục). |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn | Không áp dụng. |
| Nếu Dừng: bài học ghi lại | Không áp dụng. |
| Ngày quyết định lại (trừ khi Dừng) | **01/12/2026** (khi chính sách `REFUND-v4` bắt đầu có hiệu lực). |
| PIC ký | **Mai Lâm Tấn Đạt** (Sản phẩm và kinh doanh) đại diện cả bàn ký xác nhận. |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? Vì con số nào: **GIỮ NGUYÊN (Tiếp tục).** Vì toàn bộ các chỉ số kiểm tra trên gói sự cố S1 và bộ nền sau khi sửa đều đạt hoàn hảo: pass_rate = 1.0, không còn bất kỳ ca hoàn sai hay ghi oan lỗi nào cho đối tác GHSH (0 lỗi), ROI duy trì 0.95, chi phí 5.116đ/ticket thấp hơn làm tay 10.000đ.
- Report tự kiểm tra: mã lần chạy `R-S1-grade-20261118-172039-656fab` · ô nào còn đỏ (nguyên nhân × tầng): **Không có ô nào đỏ.** Cả 5 hạng mục kiểm tra đều đạt tích xanh (`integrity: ✅`, `criteria: ✅`, `visible: ✅`, `regression: ✅`, `monitor: ✅`). Grader trả về kết luận: **PASS-VISIBLE**.
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: Cổng vòng 1 đã đỡ được 15 lỗi oan và 710.000đ tiền hoàn sai (giảm 72% thiệt hại), nhưng bỏ sót các ca dữ liệu thiếu (`delivered_date` rỗng) và chưa có chốt chặn trần số lỗi tự ghi cho một hãng trong ngày.
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Quyết định của bàn có khớp không: Report ghi rõ: *"Không vượt trần kinh doanh / vận hành nào. Mọi ngưỡng đã ký đều đạt. Được phép cân nhắc 'Tiếp tục'."* Quyết định của bàn hoàn toàn khớp với khuyến nghị của hệ thống.
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: Bộ thử chưa đo được **độ trễ mạng thực tế khi đồng bộ API giữa app bưu tá và server LogiX** trong điều kiện thời tiết mưa bão/vùng sóng yếu. Nếu độ trễ này kéo dài nhiều ngày, lượng ticket bị escalate chuyển người duyệt có thể tăng lên, làm giảm ROI xuống khoảng 0.6–0.7. Tuy nhiên mức này vẫn an toàn trên ngưỡng chấp nhận (0.4).

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: **Hệ thống ngầm tin rằng dữ liệu trạng thái kiện hàng trong tracking DB luôn hoàn chỉnh (hễ status là DELIVERED thì delivered_date luôn có giá trị chính xác và cập nhật kịp thời), nhưng thực tế trạm bưu cục GHSH có thể quét thiếu hoặc đồng bộ trễ khiến trường ngày giao bị null.**
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: **Gate của đội thực sự NGĂN ĐƯỢC tác hại vì ở pre_guard mọi kiện hàng có status DELIVERED nhưng thiếu delivered_date đều bị chặn tự động hóa và chuyển bắt buộc sang người duyệt đối soát thủ công, đồng thời _gate_fault chặn cứng không cho phép tự động ghi quá 2 lỗi/ngày cho bất kỳ hãng nào.**
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: **Cần đo lại tỉ lệ kiện hàng bị thiếu ngày giao trong luồng dữ liệu tracking thực tế của GHSH, độ trễ đồng bộ API giữa LogiX và hệ thống bưu cục, và thời gian nhân viên CSKH xử lý thực tế các ca chuyển duyệt để đảm bảo hàng chờ không bị ùn ứ.**
