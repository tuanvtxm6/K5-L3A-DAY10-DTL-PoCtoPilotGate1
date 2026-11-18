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

## MaiLamTanDat-2A202603645

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh.
- **CP1:** Thống nhất ba vai và chốt bản PRD v1.1 / eval card Lab 9.
- **CP2 (Phiếu A):** Viết mục tiêu cấp hệ thống (mục A1 · Câu 1.1); cùng nhóm soạn bộ tiêu chí chấp nhận và hành động đi kèm (mục A4 · Câu 1.6); điền và đại diện ký Bản tiêu chí chấp nhận `config/acceptance_criteria.json` (mục A5).
- **CP3 (Phiếu B):** Điền bản đồ dữ liệu của trợ lý và phân tích ví dụ drift trong 3 tháng tới (mục B3 · Câu 2.3); đóng góp lăng kính kinh doanh trong Pre-mortem bốn lăng kính (mục B6 · Câu 2.5); thiết lập các cổng kinh doanh trong `config/operating_gates.json` mục `business` và giải thích lý do (mục B7.4 · Câu 2.9); cùng bàn đối chiếu bằng chứng mốc prepared, chốt cổng vòng 1 và ra quyết định Gate 1 v1 (mục B8).

### Đóng góp cụ thể

- Xác lập mục tiêu hệ thống rõ ràng: mỗi ticket giao trễ ở 2 depot pilot được khép lại trong ca theo đúng chính sách hiệu lực, mọi thao tác ghi ra bên ngoài khớp nguồn sự thật, tổng chi phí mỗi ticket < 10.000đ (làm tay).
- Xây dựng 5 chỉ số bắt buộc (`pass_rate_min: 0.96`, `pass_k_min: 0.86`, `wrongful_refund_vnd_max: 0`, `wrongful_carrier_faults_max: 0`, `pii_leaks_max: 0`) và 3 chỉ số kinh doanh/vận hành (`cost_per_ticket_vnd_max: 7000`, `roi_min: 0.4`, `queue_stuck_max: 0`). Thực hiện lệnh ký và push tiêu chí lên GitHub.
- Phân tích bản đồ dữ liệu: xác định tracking DB `parcels[]` (`delivered_date`, `delay_cause`) là nguồn sự thật duy nhất, text khiếu nại của khách chỉ là bản khai báo một phía; chỉ ra concept drift vào ngày 01/12/2026 khi chuyển sang `REFUND-v4` (hạ trần còn 100k, bỏ `FORCE_MAJEURE`).
- Thiết lập cổng kinh doanh trong `config/operating_gates.json`: `daily_refund_cap_vnd = 2000000` (ngân sách Finance), `cost_budget_per_ticket_vnd = 1500` (trần LLM/ticket), `pilot_scope = 100%`, `roi_min = 0.4`.
- Phân tích số liệu mốc prepared, đối chiếu `decision_rule` và cùng nhóm ra quyết định **Tiếp tục** ở Gate 1 v1.

### Bằng chứng

- **Mã commit:**
  - `dc9855b`: `Sign acceptance criteria` (ký tiêu chí chấp nhận)
  - `0cc93d8`: `Phiếu A: điền A1–A5 (CP2)`
  - `5c53392`: `LAB 10: chốt cổng vòng 1, quyết định v1`
- **Hash chốt cổng vòng 1:** `a0107cc2`
- **Mã lần chạy:**
  - Base: `R-base-before-20261118-160806-b45eeb` (pass_rate 0.9909, hoàn sai 20k, lỗi hãng oan 1)
  - After: `R-base-after-20261118-161320-2292d9` (pass_rate 1.0, hoàn sai 0đ, lỗi hãng oan 0)
  - Prepared: `R-base-prepared-20261118-161522-2292d9` (pass_rate 1.0, pass_k 1.0, wrongful_refund 0đ, wrongful_faults 0, chi phí 4.456đ, ROI 1.24, queue_stuck 0 ca)
- **Vị trí tài liệu:**
  - `templates/form-a-criteria.md`: A1, A4, A5
  - `templates/form-b-evaluation-gates.md`: B0, B3, B6, B7.4, B8
  - `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`)

### Exit ticket

- **Một điều học được:** Phải phân định rạch ròi giữa nguồn sự thật (tracking DB) và lời khai của khách hàng; cổng kiểm soát cấp hệ thống (guards & operating config gates) hiệu quả và đáng tin cậy hơn nhiều so với việc chỉ trông chờ vào prompt hay model.
- **Một điều còn chưa chắc:** Khi số lượng ticket thực tế tăng đột biến vượt xa dự tính trong mùa mega sale, liệu trần ngân sách hoàn tự động trong ngày (2.000.000đ) có làm quá tải hàng chờ người duyệt của chị Hạnh hay không.

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
