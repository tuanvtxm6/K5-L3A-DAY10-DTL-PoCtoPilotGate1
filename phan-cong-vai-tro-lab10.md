# Phân công công việc theo checkpoint · LAB 10

> Tài liệu này phân công **toàn bộ bài lab theo đúng thời điểm thực hiện**. Mỗi mục nêu checkpoint, người phụ trách chính, file và vị trí cần điền. Các vai là người cầm bút chính; cả bàn vẫn cùng thảo luận và chịu trách nhiệm với quyết định chung.

## Ba vai trong nhóm

- **Kỹ sư cổng:** chạy lệnh đánh giá/trace, đọc bằng chứng kỹ thuật, viết và sửa cổng trong code, thêm monitor.
- **Sản phẩm và kinh doanh:** mục tiêu sản phẩm, tiêu chí, chi phí, ROI, phạm vi pilot, quyết định kinh doanh.
- **Vận hành và pháp lý:** nhân sự trực, năng lực xử lý, quy trình/runbook, trách nhiệm, điều kiện dừng, dữ liệu cá nhân và bài nộp.

---

## CP1 · Cài đặt và chia vai (phút 0–15)

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Trưởng nhóm | Tạo repo của bàn, clone về máy, gắn `upstream`, cấu hình danh tính Git; mời team chấm theo hướng dẫn. | Repo GitHub; cấu hình Git trong repo |
| Cả bàn | Chọn eval card và PRD v1.1 từ Lab 9 làm bản chung; thống nhất ba vai. | Chưa điền phiếu |
| Trưởng nhóm | Ghi họ tên, MSSV và vai của mọi người. | `TEAM.md`, bảng thành viên |
| Mỗi thành viên | Viết mục đóng góp cá nhân của mình trước khi nộp. | `TEAM.md`, mục `## HoVaTen-MSSV` (hoàn tất trước khi nộp ở CP5) |
| Kỹ sư cổng | Chạy bài kiểm tra công khai. | Lệnh `python3 -m unittest discover -s tests` (kỳ vọng `Ran 13 tests … OK`) |

## CP2 · Viết và ký tiêu chí (phút 15–65) · Phiếu A

**Chưa chạy trợ lý hoặc `eval` trong CP2.** Tiêu chí phải được thống nhất, ký, commit và push trước lần đánh giá đầu tiên.

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Sản phẩm và kinh doanh | Nêu mục tiêu cấp hệ thống (1.1); cùng nhóm soạn tiêu chí thành công, ngưỡng và hành động tương ứng (1.6). | `templates/form-a-criteria.md`, A1 câu 1.1 và A4 câu 1.6 |
| Vận hành và pháp lý | Viết mục tiêu theo góc nhìn chị Oanh và chị Hạnh (1.2); thiết kế telemetry production (1.4). | `templates/form-a-criteria.md`, A1 câu 1.2 và A2 câu 1.4 |
| Kỹ sư cổng | Thiết kế metric offline cho một bước của trợ lý (1.3). | `templates/form-a-criteria.md`, A2 câu 1.3 |
| Cả bàn | Chọn kết luận cho ví dụ khoảng tin cậy (1.5); rà tiêu chí theo bốn câu hỏi; thống nhất hai ranh giới đầu ra. | `templates/form-a-criteria.md`, A3 câu 1.5 và A4 câu 1.6 |
| Sản phẩm và kinh doanh (cả bàn duyệt) | Điền tên repo, người ký, ngưỡng bắt buộc/nên có, `business_ops`, `stop_condition` và bốn `decision_rule`. | `config/acceptance_criteria.json` |
| Người được nhóm giao ký; sản phẩm/kinh doanh chuẩn bị | Ký đúng một lần, rồi commit và push tiêu chí cùng lock. Ghi giờ ký và mã commit vào phiếu. | Lệnh `python3 -m lab10.criteria sign`; `templates/form-a-criteria.md`, A5; Git commit/push |

**Kết thúc CP2 khi:** máy báo `ĐÃ KÝ.` và commit ký đã được push. Từ đây không sửa `config/acceptance_criteria.json`.

## CP3 · Đo, phân tích rủi ro, dựng cổng vòng 1 và quyết định v1 (phút 65–115) · Phiếu B

**CP3 chưa có thẻ sự cố.** Nhóm làm trên bộ nền và các rủi ro đã biết; chỉ chỉnh code/config ở phần cổng vòng 1 theo đề.

### CP3A · Đo và tìm rủi ro (phút 65–85)

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Kỹ sư cổng | Chạy mốc `base`, đối chiếu với tiêu chí đã ký, ghi mã lần chạy và đọc các bảng kết quả; trace `T-002@55` rồi phân loại lỗi. | `templates/form-b-evaluation-gates.md`, B0–B2; lệnh `eval`, `gate`, `trace` |
| Sản phẩm và kinh doanh | Lập bản đồ dữ liệu và nêu một ví dụ drift có trường dữ liệu, thời điểm, metric bị ảnh hưởng. | Phiếu B, B3 |
| Vận hành và pháp lý | Làm HAZOP vòng 1, thêm ít nhất hai nhánh ngoài kỹ thuật; điền checklist 9 nhóm, mỗi dòng có PIC được nêu tên. | Phiếu B, B4–B5 |
| Cả bàn | Làm pre-mortem qua bốn lăng kính và chọn 2–3 nguyên nhân để xử lý bằng cổng. | Phiếu B, B6 |

### CP3B · Dựng cổng vòng 1 (phút 85–105)

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Kỹ sư cổng | Viết 2–3 cổng phòng ngừa gắn với pre-mortem/HAZOP; thử trên bộ nền và behavioral test với hai ticket tự tạo; ghi cách giảm rò rỉ dữ liệu. | `lab10/guards.py`; Phiếu B, B7.1–B7.3 |
| Sản phẩm và kinh doanh | Chọn trần hoàn tự động, ngân sách mỗi ticket, phạm vi pilot và ngưỡng ROI; ghi lý do theo dữ liệu lab. | `config/operating_gates.json`, mục `business`; Phiếu B, B7.4 |
| Vận hành và pháp lý | Chọn PIC, người duyệt, số người trực, công suất, SLA, điều kiện dừng/kênh cảnh báo và quy tắc dữ liệu/ghi lỗi hãng; viết runbook 1–3 và mục giờ cao điểm. | `config/operating_gates.json`, mục `operations` và `legal`; Phiếu B, B7.5–B7.6 |
| Cả bàn | Chạy lại đánh giá/test, đảm bảo cổng không làm hỏng ca đúng. | Lệnh `eval --stage after`; `python3 -m unittest discover -s tests` |

### CP3C · Chốt cổng và quyết định v1 (phút 105–115)

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Kỹ sư cổng | Tạo snapshot cổng vòng 1; chạy `prepared` và `gate`; lưu mã lần chạy/bằng chứng. | Lệnh `python3 -m lab10.checkpoint`, `eval --stage prepared`, `gate`; snapshot do lệnh tạo |
| Cả bàn | Chọn v1 theo tiêu chí đã ký và số liệu; ghi ba bằng chứng, `decision_rule` phù hợp và ngày quyết định lại; commit/push. | Phiếu B, B8; Git |

**Kết thúc CP3 khi:** cổng vòng 1 đã được chốt và quyết định v1 đã commit/push. Không sửa các snapshot vòng 1.

## CP4 · Nhận thẻ, phân tích và xử lý sự cố (bắt đầu phút 125; khối chính đến phút 185) · Phiếu C

**Chỉ bắt đầu phần thẻ sau khi Lab Coach phát thẻ và nhóm bốc số.** Chỉ làm đúng thẻ nhóm đã bốc. Việc đầu tiên là chạy `grade` trước khi sửa bất kỳ code/config nào.

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Cả bàn | Ghi số thẻ; chạy `grade` trước sửa; so sánh `base` với `prepared`, đối chiếu pre-mortem. | `templates/form-c-incident.md`, dòng thẻ và C0–C1; lệnh `python3 -m lab10.grade --incident Sx` |
| Kỹ sư cổng | Trace ít nhất hai ticket lỗi khác kiểu; ghi bằng chứng và phân loại; đề xuất/sửa cổng kỹ thuật nếu đúng nguyên nhân. | Phiếu C, C2; `lab10/guards.py` |
| Vận hành và pháp lý | Làm HAZOP riêng của thẻ và phần phân tích riêng theo đúng số thẻ; cùng nhóm lập fault tree trước sửa. | Phiếu C, C3 (chỉ phần của thẻ đã bốc), C4, C6 |
| Sản phẩm và kinh doanh | Viết specification kiểm được và giả định môi trường; điều chỉnh con số/phạm vi kinh doanh nếu nguyên nhân nằm ở đó. | Phiếu C, C5; `config/operating_gates.json`, mục `business` |
| Kỹ sư cổng | Thêm ít nhất một metric mới, không tính `escalation_rate` có sẵn; chạy đánh giá sau sửa, regression bộ nền và grade. | `lab10/monitors.py`, dict `MONITORS`; Phiếu C, C8; lệnh `eval` và `grade` |
| Cả bàn, vận hành/pháp lý ghi chính | Ghi sửa theo từng nguyên nhân; cập nhật fault tree sau sửa, risk register, checklist và runbook phần 4–5. | Phiếu C, C7, C9–C11 |

**CP4 chỉ làm được sau khi có thẻ:** các mục C0–C11, trace `Sx`, HAZOP của thẻ, fault tree và sửa theo sự cố. Không làm các mục này ở CP2 hay CP3.

## CP5 · Quyết định v2, demo và nộp bài (phút 185–240)

| Người phụ trách | Công việc | File/vị trí |
|---|---|---|
| Cả bàn | Chốt quyết định v2 theo tiêu chí và bằng chứng ba mốc; điền ba câu bắt buộc về giả định môi trường, hiệu lực cổng, và điều cần đo lại trong pilot thật. | `templates/form-c-incident.md`, C12 |
| Vận hành và pháp lý (cả bàn kiểm tra) | Điền thông tin nhóm/thẻ, quyết định v1/v2 và chép nguyên ba câu từ C12. | `submission/submission.json` |
| Cả bàn | Gom bài, xử lý mọi dòng `[THIẾU]` đến khi báo `ĐỦ THÀNH PHẦN`. | Lệnh `python3 -m lab10.check_submission --collect` |
| Cả bàn | Demo ba mốc `base · prepared · after`; nếu có thay thử config, trả lại cấu hình v2 và chạy lại `grade` cùng lệnh gom bài. | Report trong `runs/`; lệnh `grade` và `check_submission --collect` |
| Trưởng nhóm | Commit/push bài cuối và gửi link repo cho team chấm theo hướng dẫn. | Git; repo của bàn |
| Mỗi thành viên | Viết mục đóng góp cá nhân và tự nộp link repo trên LMS trước hạn. | `TEAM.md`, mục cá nhân; LMS |

## Các việc cả bàn luôn cùng chịu trách nhiệm

- Thống nhất ngưỡng CP2; không giao một người tự quyết tiêu chí thay cả bàn.
- Cùng đọc bằng chứng và chốt quyết định v1 ở CP3, v2 ở CP5.
- Đảm bảo quyết định khớp tiêu chí đã ký và kết quả đo. Nếu còn vượt trần hoặc ngưỡng bắt buộc chưa đạt, không chọn “Tiếp tục”.
- Không làm hỏng các ca bộ nền vốn đang đúng; không xử lý riêng theo mã ticket/câu chữ; không mở thẻ của bàn khác.
- AI được phép hỗ trợ, nhưng ngưỡng, con số và quyết định là của bàn; mỗi thành viên ghi việc dùng AI trong mục cá nhân `TEAM.md`.
