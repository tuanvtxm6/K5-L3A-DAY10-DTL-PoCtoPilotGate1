# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `DTL`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-DTL-PoCtoPilotGate1` (https://github.com/tuanvtxm6/K5-L3A-DAY10-DTL-PoCtoPilotGate1)
- Thẻ sự cố đã bốc (S1–S8): `S1`
- Bản chung từ Lab 9 (chọn ở phút 0–15): PRD v1.1 và eval card của Lục Anh Tuấn (2A202603634), chép vào [`docs/lab9/PRD_v1.1.md`](docs/lab9/PRD_v1.1.md) và [`docs/lab9/eval_card.md`](docs/lab9/eval_card.md); baseline Lab 9 `E-swarm-20261117-f3a4` (v1), `E-swarm-20261117-7647` (v2)

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |      Lục Anh Tuấn     |   2A202603634   |   Kỹ sư cổng  |      v      |
|   2 |     Mai Lâm Tấn Đạt      |   2A202603645   |   Sản phẩm và kinh doanh  |             |
|   3 |      Nguyễn Thùy Lam     |   2A202603632   |   Vận hành và pháp lý  |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## LucAnhTuan-2A202603634

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng, trưởng nhóm.
- **CP1:** Tạo repo bàn từ template, nối `origin` (repo bàn) và `upstream` (repo lớp); điền bảng thành viên và thông tin nhóm trong `TEAM.md`; đưa PRD v1.1 và eval card Lab 9 của mình làm bản chung (`docs/lab9/`); thêm `.gitattributes` giữ LF để hash tiêu chí và `MANIFEST` khớp trên Windows; chạy bài kiểm tra công khai (`Ran 13 tests … OK`).
- **CP2 (Phiếu A):** Viết metric offline cho bước ghi lỗi hãng (mục A2 · Câu 1.3); cầm bút ghi Phiếu A (A1–A5) theo nội dung cả bàn chốt; chạy lệnh ký tiêu chí trên máy mình và push commit ký (Đạt đứng tên ký thay mặt bàn).
- **CP3 (Phiếu B):** Chạy `base` và đọc số so với tiêu chí đã ký (B0–B1 · Câu 2.1); trace `T-002@55` và phân loại lỗi (B2 · Câu 2.2); viết 3 cổng vòng 1 trong `lab10/guards.py` (B7.1 · Câu 2.6), hai bước tránh rò dữ liệu (B7.2 · Câu 2.7) và behavioral test hai ticket hiểm (B7.3 · Câu 2.8).
- **CP4 (Phiếu C, thẻ S1):** Nhận bộ thẻ S1–S8 khớp `MANIFEST`; chạy `lab10.grade --incident S1` trước khi sửa và đọc số base/prepared (C0, C1); trace 3 ticket lỗi khác kiểu `S1-20`, `S1-42`, `S1-07` (C2); viết cổng 4–6 trong `lab10/guards.py` và 3 monitor trong `lab10/monitors.py` (C7, C8); chạy eval sự cố, regression bộ nền và grade.
- **CP5:** Sau khi gộp nhánh của Đạt, rà cho Phiếu C khớp code (C4, C5, C6, C7, C9, C12, ba dòng giảm/ngăn), bỏ code thừa `_DELAY_SUB`, chạy lại grade trên đúng code `d10768` và gom bài (`check_submission --collect`).

### Đóng góp cụ thể

- **Cổng vòng 1 (CP3)**, trong `write_gate` của `lab10/guards.py`:
  - `issue_refund`: so số tiền với quyền lợi tính theo tracking (`db_delay_days`, `entitlement_vnd`), không theo số ngày khách khai.
  - `file_carrier_fault`: chỉ ghi lỗi khi `carrier_at_fault` đúng theo `delay_cause` trong tracking.
  - `notify_carrier`: bỏ các trường PII trước khi gửi hãng.
  - Kết quả: bộ nền từ pass_rate 0,9909 (hoàn sai 20.000đ, 1 lỗi oan cho VNX ở `T-002@55`) lên 1,0, hoàn sai 0đ, lỗi oan 0.
  - Vòng 2: viết lại `write_gate` gọi 3 cổng `_gate_refund`, `_gate_fault`, `_gate_notice` (thêm kiểm payer, fail-open khi LLM lỗi, ghi trùng, phê duyệt, đúng kiện, lọc PII theo `config/operating_gates.json` mục `legal`).
- **Sửa sự cố S1 (CP4)**, ba cổng mới, mỗi cổng ứng một nhánh fault tree:
  - Cổng 4 (`pre_guard`): regex `_DAY_CLAIM` bỏ số ngày khách tự khai khỏi chữ model đọc (`Verdict.rewrite`), nên `S1-07` (khách khai thấp, bị hoàn thiếu) đạt 5/5.
  - Cổng 5 (`_tracking_gap`): kiện `DELIVERED` mà trống `delivered_date` thì `_gate_refund` chuyển người trước khi tiền đi, `_gate_fault` không ghi lỗi (`S1-20`, `S1-21`).
  - Cổng 6 (`_gate_fault`): từ lỗi thứ 3 của cùng hãng trong ngày thì `deny`, trần đọc từ `ops_limits.max_auto_strikes_per_carrier_per_day` (= 2) (`S1-42`, `S1-43`).
  - Kết quả trên gói S1: pass_rate 0,3077 (base) → 0,6154 (prepared) → 1,0 (after); hoàn sai 985.000đ → 0đ; lỗi oan cho hãng 30 → 0; hoàn thiếu 105.000đ → 0đ. Bộ nền giữ 110/110, không ca nào hỏng thêm.
- **Monitor mới (C8)**: `carrier_strikes_max_per_day` (S1 base 4 → after 2, đúng trần), `delay_claim_mismatch_rate` (bộ nền 0,2, S1 0,8333), `tracking_incomplete_rate` (S1 after 0,1538). Mục `6 monitor` của grader ✅.
- **Phiếu và bài nộp**: viết Phiếu B mục B0–B2, B7.1–B7.3 và Phiếu C mục C0, C1 (số liệu), C2, C7, C8. Rà các mục còn lại của Phiếu C cho khớp code, đúng chỗ đặt cổng 5 và tên monitor. Gom bài đạt `ĐỦ THÀNH PHẦN`.
- **Dùng AI**: dùng Claude Code (Claude Opus) để đọc code starter, gợi ý cách viết cổng và rà phiếu cho khớp code. Ngưỡng, chỗ đặt cổng và quyết định v1/v2 do bàn chốt; mình tự chạy lại eval, grade và đối chiếu từng con số trong report trước khi ghi vào phiếu.

### Bằng chứng

- **Commit:**
  - `2ff038c`, `55fe3d7`: điền bảng thành viên, thông tin nhóm
  - `e53ac41`: chốt bản chung Lab 9 (PRD v1.1, eval card)
  - `f2dfec4`: `.gitattributes` giữ LF
  - `dc9855b`: ký tiêu chí chấp nhận · `0cc93d8`: Phiếu A A1–A5
  - `6eef598`: 3 cổng vòng 1 trong `guards.py`; Phiếu B B0–B2, B7.1–B7.3
  - `08b3dff`: `write_gate` vòng 2 gọi 3 cổng `_gate_*`, lọc PII theo config `legal`
  - `e144fbc`: nhận thẻ S1–S8, bàn bốc S1
  - `5ec3648`: cổng 4–6, 3 monitor; Phiếu C C0, C1, C2, C7, C8
  - `13a0e16`: Phiếu C khớp code, bỏ `_DELAY_SUB`, gom lại bài nộp trên code `d10768`
- **Mã lần chạy:**
  - Bộ nền base: `R-base-before-20261118-153134-b45eeb` · after cổng vòng 1: `R-base-after-20261118-153223-36155f` · regression sau sửa S1: `R-base-after-20261118-170342-d10768` (pass_rate 1,0, ROI 1,24)
  - S1 grade trước sửa: `R-S1-grade-20261118-165621-663d99` (base `R-S1-before-20261118-165622-663d99`, prepared `R-S1-prepared-20261118-165622-663d99`)
  - S1 after sửa: `R-S1-after-20261118-170342-d10768` (pass_rate 1,0, hoàn sai 0đ, oan 0, chi phí 5.172đ, ROI 0,93)
  - S1 grade bản nộp: `R-S1-grade-20261118-174342-d10768` (PASS-VISIBLE, 5/5 kiểm đạt)
- **Trong phiếu:** `templates/form-a-criteria.md` A2 (câu 1.3); `templates/form-b-evaluation-gates.md` B0, B1, B2, B7.1–B7.3; `templates/form-c-incident.md` C0, C1, C2, C7, C8 (và rà C4, C5, C6, C9, C11, C12)
- **Code:** `lab10/guards.py` (`pre_guard`, `_tracking_gap`, `_gate_refund`, `_gate_fault`, `_gate_notice`, `write_gate`), `lab10/monitors.py`

### Exit ticket

- **Một điều học được:** Mỗi nguyên nhân cần một cổng ở đúng tầng của nó. Riêng cổng so tiền với tracking ở vòng 1 đã cắt được nửa số lỗi oan của S1, nhưng không bắt được dữ liệu tracking thiếu trường hay lỗi dồn theo hãng trong ngày, vì đó là lỗi ở dữ liệu và ở vận hành, không phải ở từng lệnh ghi. Cổng cũng phải đọc trần từ dữ liệu của Ops (`ops_limits`) chứ không viết cứng trong code.
- **Một điều còn chưa chắc:** Cổng 4 chỉ bỏ được số ngày viết bằng chữ số. Một LLM thật vẫn hiểu "trễ hai ngày" viết bằng chữ, và chiều khai thấp chỉ có cổng này đỡ. Cổng 6 cũng chỉ đếm trong ngày, trong khi ngưỡng hợp đồng của GHSH tính theo 7 ngày. Pilot thật cần đo lại cả hai chỗ này.

## MaiLamTanDat-2A202603645

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh.
- **CP1:** Thống nhất ba vai và chốt bản PRD v1.1 / eval card Lab 9.
- **CP2 (Phiếu A):** Viết mục tiêu cấp hệ thống (mục A1 · Câu 1.1); cùng nhóm soạn bộ tiêu chí chấp nhận và hành động đi kèm (mục A4 · Câu 1.6); điền và đại diện ký Bản tiêu chí chấp nhận `config/acceptance_criteria.json` (mục A5).
- **CP3 (Phiếu B):** Điền bản đồ dữ liệu của trợ lý và phân tích ví dụ drift trong 3 tháng tới (mục B3 · Câu 2.3); đóng góp lăng kính kinh doanh trong Pre-mortem bốn lăng kính (mục B6 · Câu 2.5); thiết lập các cổng kinh doanh trong `config/operating_gates.json` mục `business` và giải thích lý do (mục B7.4 · Câu 2.9); cùng bàn đối chiếu bằng chứng mốc prepared, chốt cổng vòng 1 và ra quyết định Gate 1 v1 (mục B8).
- **CP4 (Phiếu C):** Tiếp nhận thẻ sự cố S1 (GHSH khiếu nại ghi lỗi oan); đối chiếu pre-mortem và số liệu mốc prepared (mục C0–C1); phân tích 3 ticket lỗi khác kiểu, nguồn lỗi và hướng xử lý (mục C2); mở lại bản đồ dữ liệu các trường của `parcel` (mục C3.5); thực hiện HAZOP thẻ S1 (mục C4); viết specification kiểm được và vạch trần giả định môi trường (mục C5 · Câu 3.2, 3.3 - vai trò Sản phẩm và kinh doanh); xây dựng Fault tree trước và sau khi sửa (mục C6, C9); thiết kế chỉ số giám sát mới `ghsh_fault_rate` trong `lab10/monitors.py` (mục C8); cập nhật Risk register (mục C10), checklist và Runbook phần 4–5 (mục C11).
- **CP5 (Phiếu C, Submission):** Cùng bàn đánh giá số liệu ba mốc, đối chiếu tiêu chí chấp nhận đã ký và chốt quyết định Gate 1 v2 là **Tiếp tục** (mục C12); soạn thảo ba dòng bắt buộc; hoàn thiện `submission/submission.json` và chạy lệnh thu gom `python3 -m lab10.check_submission --collect` đạt chuẩn `ĐỦ THÀNH PHẦN` (19/19 files, exit 0).

### Đóng góp cụ thể

- **Mục tiêu & Tiêu chí (CP2):** Xác lập mục tiêu hệ thống rõ ràng: mỗi ticket giao trễ ở 2 depot pilot được khép lại trong ca theo đúng chính sách hiệu lực, mọi thao tác ghi ra bên ngoài khớp nguồn sự thật, tổng chi phí mỗi ticket < 10.000đ (làm tay). Xây dựng 5 chỉ số bắt buộc (`pass_rate_min: 0.96`, `pass_k_min: 0.86`, `wrongful_refund_vnd_max: 0`, `wrongful_carrier_faults_max: 0`, `pii_leaks_max: 0`) và 3 chỉ số kinh doanh/vận hành (`cost_per_ticket_vnd_max: 7000`, `roi_min: 0.4`, `queue_stuck_max: 0`). Thực hiện lệnh ký và push tiêu chí lên GitHub (`dc9855b`).
- **Bản đồ dữ liệu & Cổng kinh doanh (CP3):** Xác định tracking DB `parcels[]` (`delivered_date`, `delay_cause`) là nguồn sự thật duy nhất, text khiếu nại của khách chỉ là bản khai báo một phía; chỉ ra concept drift vào ngày 01/12/2026 khi chuyển sang `REFUND-v4` (hạ trần còn 100k, bỏ `FORCE_MAJEURE`). Thiết lập cổng kinh doanh trong `config/operating_gates.json`: `daily_refund_cap_vnd = 2000000` (ngân sách Finance), `cost_budget_per_ticket_vnd = 1500` (trần LLM/ticket), `pilot_scope = 100%`, `roi_min = 0.4`. Chốt quyết định **Tiếp tục** ở Gate 1 v1 (`5c53392`).
- **Phân tích sự cố S1 & Giả định môi trường (CP4):** 
  - Vạch rõ 3 nguyên nhân hỏng độc lập: (1) Lời khai khách hàng "trễ 2 ngày" làm model bị thiên lệch ghi đè DB (`S1-07`); (2) Trạng thái `status == DELIVERED` nhưng thiếu `delivered_date` khiến hàm tính trễ dùng nhầm ngày `as_of` tính đội trễ 6-9 ngày (`S1-20`, `S1-21`); (3) Thiếu mạch ngắt trần lỗi dồn dập cho một hãng trong ngày (`S1-40`..`S1-43`).
  - Viết **Specification kiểm được** (Câu 3.2): Lệnh `file_carrier_fault` chỉ được gọi khi `carrier_at_fault == True`, `parcel['delivered_date'] is not None`, và số lỗi tự ghi cho hãng trong ngày `< max_auto_strikes_per_carrier_per_day = 2`.
  - Chỉ ra **Giả định môi trường sai** (Câu 3.3): Người thiết kế ngầm tin dữ liệu tracking đồng bộ từ trạm bưu cục luôn toàn vẹn và tức thời, trong khi thực tế bưu tá quét offline hoặc API nghẽn dẫn đến rỗng `delivered_date`.
- **Giải pháp & Chỉ số theo dõi mới (CP4):** 
  - Đề xuất giải pháp surgical: (1) lọc số ngày khách khai trong `pre_guard` bằng regex; (2) bắt `status == DELIVERED and not delivered_date` trong `pre_guard` chuyển duyệt tay đối soát; (3) chặn cứng tại `_gate_fault` khi `len(fault_rows(carrier_id)) >= max_strikes`.
  - Thiết kế chỉ số mới `ghsh_fault_rate` trong `lab10/monitors.py`, phát hiện đợt phát sinh lỗi GHSH trước sửa lên tới 0.846 (báo động đỏ) và hạ nhiệt an toàn về 0.385 sau khi sửa.
- **Tối ưu tài chính & Quyết định Gate 1 v2 (CP5):** 
  - Đưa tiền hoàn sai từ 985.000đ về 0đ; xóa bỏ toàn bộ 30 lỗi ghi oan cho GHSH (về 0 lỗi), chi phí 5.116đ/ticket (tiết kiệm hơn làm tay 10.000đ), ROI đạt 0.95.
  - Bộ nền không regression (pass_rate 1.0, ROI 1.24).
  - Hoàn thiện toàn bộ Phiếu C (C0–C12), `submission/submission.json` và chạy `check_submission --collect` đạt chuẩn `ĐỦ THÀNH PHẦN` (19/19 files, exit 0). Cùng bàn chốt quyết định **Tiếp tục** tại Gate 1 v2.

### Bằng chứng

- **Mã commit:**
  - `dc9855b`: `Sign acceptance criteria` (ký tiêu chí chấp nhận CP2)
  - `0cc93d8`: `Phiếu A: điền A1–A5 (CP2)`
  - `5c53392`: `LAB 10: chốt cổng vòng 1, quyết định v1 (CP3)`
  - `8bdd748`: `TEAM.md: cập nhật mục cá nhân Mai Lâm Tấn Đạt (CP3)`
  - `a49acbd`: `LAB 10: xử lý sự cố S1 và hoàn thành CP4/CP5 (phiếu C, guards, monitors, submission)`
- **Hash chốt cổng vòng 1:** `a0107cc2`
- **Mã lần chạy:**
  - Base nền: `R-base-before-20261118-160806-b45eeb` (pass_rate 0.9909, hoàn sai 20k, lỗi hãng oan 1)
  - Prepared nền: `R-base-prepared-20261118-161522-2292d9` (pass_rate 1.0, pass_k 1.0, wrongful_refund 0đ, wrongful_faults 0, chi phí 4.456đ, ROI 1.24, queue_stuck 0 ca)
  - Base sự cố S1: `R-S1-before-20261118-172334-656fab` (pass_rate 0.3077, hoàn sai 985k, lỗi hãng oan 30, ROI -2.74)
  - Prepared sự cố S1: `R-S1-prepared-20261118-172334-656fab` (pass_rate 0.6154, hoàn sai 275k, lỗi hãng oan 15, ROI 0.58)
  - After sự cố S1: `R-S1-after-20261118-172334-656fab` (pass_rate 1.0, hoàn sai 0đ, lỗi hãng oan 0, chi phí 5.116đ, ROI 0.95)
  - Grader sự cố S1: `R-S1-grade-20261118-172334-656fab` (PASS-VISIBLE: 5/5 kiểm tra đạt ✅)
  - Regression nền: `R-base-after-20261118-172024-656fab` (pass_rate 1.0, hoàn sai 0đ, oan 0, ROI 1.24)
- **Vị trí tài liệu:**
  - `templates/form-a-criteria.md`: A1, A4, A5
  - `templates/form-b-evaluation-gates.md`: B0, B3, B6, B7.4, B8
  - `templates/form-c-incident.md`: C0, C1, C2, C3.5, C4, C5, C6, C7, C8, C9, C10, C11, C12
  - `config/acceptance_criteria.json`, `config/operating_gates.json`, `submission/submission.json`
  - `lab10/guards.py`, `lab10/monitors.py`

### Exit ticket

- **Một điều học được:** Sự cố ngoài thực tế (như thẻ S1) hiếm khi chỉ đến từ model mà phần lớn đến từ các giả định môi trường sai lệch về tính toàn vẹn của dữ liệu ngoại vi (tracking DB thiếu `delivered_date`) và sự thiếu vắng các cơ chế bảo vệ hợp đồng đối tác (circuit breaker trần lỗi dồn dập). Các cổng kiến trúc phân tầng (guards chặn lệnh ghi, chuyển người đối soát có chọn lọc) mang lại sự an toàn và hiệu quả kinh doanh vượt trội so với việc cố gắng tinh chỉnh prompt.
- **Một điều còn chưa chắc:** Trong điều kiện vận hành thực tế diện rộng, khi đường truyền API giữa các trạm bưu cục vùng sâu vùng xa của hãng GHSH bị gián đoạn kéo dài, tỉ lệ ticket bị chuyển người duyệt (`escalation_rate`) có thể tăng cao, đòi hỏi bàn phải tiếp tục theo dõi sát sao chi phí nhân sự đối soát và thời gian phản hồi khách hàng trong giai đoạn Pilot Gate 2.

## HoVaTen - MSSV
### NguyenThuyLam-2A202603632

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý.

- **CP3 (Phiếu B):** Cùng nhóm hoàn thiện phần vận hành/pháp lý trong Phiếu B và các cổng ở `config/operating_gates.json`; tập trung vào người phụ trách, người duyệt, năng lực xử lý, thời gian hàng chờ, điều kiện dừng, kênh cảnh báo, kiểm mẫu, dữ liệu cá nhân không được gửi cho bên thứ ba và yêu cầu phải có nguyên nhân được ghi nhận khi quy lỗi hãng.
- **CP4 (Phiếu C, sự cố S1):** Rà soát kết quả grade S1; ghi nhận rủi ro tích lũy lỗi hãng, dữ liệu tracking thiếu/không nhất quán; bổ sung hướng dẫn tạm dừng/đối soát và cập nhật Phiếu C mục C1, C3.5, C4, C5, C7, C10, C11.

### Đóng góp cụ thể

- Đặt và làm rõ các cổng vận hành/pháp lý: PIC vận hành `NV-TUNG`, người duyệt `NV-HANH`, năng lực reviewer 6 ticket/giờ, thời gian chờ tối đa 60 phút, kênh cảnh báo `#cskh-ops-alert`, kiểm mẫu 10%; quy định dừng khi có lỗi ghi oan cho hãng hoặc lộ PII.
- Giữ danh sách trường PII bị chặn khi gửi cho bên thứ ba (`recipient_contact`, `name`, `phone`, `street`) và yêu cầu có `delay_cause` được ghi nhận trước khi quy lỗi hãng.
- Với S1, ghi nhận report after còn 15 lỗi hãng oan, 275.000đ hoàn sai, chi phí/ticket 3.656đ; đề xuất dừng tự động theo hãng ở 2 lỗi/ngày, chuyển người duyệt khi tracking thiếu ngày giao/nguyên nhân, và đối soát nếu chạm 3 lỗi trong 7 ngày. Đây là hướng dẫn/điều kiện vận hành, chưa phải gate/monitor được triển khai trong code.

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

- **Commit:** `cc2aeb9` — `cp3 van hanh phap ly` 

### Exit ticket

- **Một điều học được:** Quy trình vận hành cần kiểm soát lỗi theo cả ticket lẫn theo hãng và cửa sổ thời gian; có dữ liệu tracking thiếu hoặc mâu thuẫn thì phải chuyển người, không suy diễn để hoàn tiền hay ghi lỗi hãng.
- **Một điều còn chưa chắc:** Cần xác nhận với GHSH cách tính ngày nghiệp vụ/cửa sổ 7 ngày và quy trình chính thức để tranh chấp, đính chính các lỗi đã ghi.
