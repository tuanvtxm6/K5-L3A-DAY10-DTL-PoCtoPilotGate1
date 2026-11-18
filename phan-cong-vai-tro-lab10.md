# Phân công công việc theo checkpoint · LAB 10

> Bản theo dõi này chia công việc theo đúng checkpoint. **✅ Hoàn tất** dựa trên file/commit hiện có; **⬜ Chưa làm hoặc chưa xác nhận**. Các vai là người cầm bút chính, còn quyết định quan trọng do cả bàn cùng chốt.

## Ba vai

- **Kỹ sư cổng:** chạy eval/trace, phân tích bằng chứng kỹ thuật, viết cổng trong code và monitor.
- **Sản phẩm và kinh doanh:** mục tiêu, tiêu chí, chi phí, ROI, phạm vi pilot và quyết định.
- **Vận hành và pháp lý:** người trực, năng lực, quy trình/runbook, điều kiện dừng, dữ liệu cá nhân và gom bài.

## CP1 · Cài đặt và chia vai (phút 0–15)

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ✅ | Trưởng nhóm/cả bàn | Repo nhóm đã có các commit trên `main`; bảng thành viên và vai đã được điền. | Repo GitHub; `TEAM.md`, bảng thành viên |
| ✅ | Cả bàn | Đã chọn PRD v1.1 và eval card Lab 9 làm nguồn chung; đã ghi tên người chọn và baseline. | `TEAM.md`; tài liệu nguồn ở `docs/lab9/` được Phiếu A dẫn chiếu |
| ⬜ | Trưởng nhóm | Xác nhận repo đúng tên, có `origin` và `upstream`, và đã mời team chấm quyền Read trở lên. | Git remotes; GitHub Collaborators |
| ⬜ | Kỹ sư cổng | Chạy bài kiểm tra công khai và xác nhận `Ran 13 tests … OK`. | `python3 -m unittest discover -s tests` |
| ⬜ | Mỗi thành viên | Viết mục đóng góp cá nhân trước khi nộp. | `TEAM.md`, mục `## HoVaTen-MSSV` (hoàn tất ở CP5) |

## CP2 · Viết và ký tiêu chí (phút 15–65) · Phiếu A

**CP2 đã hoàn tất theo Phiếu A, tiêu chí và lock hiện có.** Không chạy eval trước khi ký; sau khi ký không sửa tiêu chí.

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ✅ | Sản phẩm và kinh doanh | Nêu mục tiêu cấp hệ thống và tiêu chí thành công. | `templates/form-a-criteria.md`, A1 câu 1.1 và A4 câu 1.6 |
| ✅ | Vận hành và pháp lý | Viết mục tiêu theo góc nhìn chị Oanh/chị Hạnh và telemetry production. | Phiếu A, A1 câu 1.2 và A2 câu 1.4 |
| ✅ | Kỹ sư cổng | Thiết kế metric offline cho một bước trợ lý. | Phiếu A, A2 câu 1.3 |
| ✅ | Cả bàn | Trả lời ví dụ khoảng tin cậy; rà tiêu chí và ghi hai ranh giới đầu ra. | Phiếu A, A3 câu 1.5 và A4 câu 1.6 |
| ✅ | Sản phẩm và kinh doanh, cả bàn duyệt | Điền team, người ký, ngưỡng, `business_ops`, `stop_condition` và bốn `decision_rule`. | `config/acceptance_criteria.json` |
| ✅ | Người ký được nhóm giao; cả bàn đồng thuận | Ký, tạo lock, ghi thời gian/mã commit và push. | `config/acceptance_criteria.lock`; Phiếu A, A5; commit `dc9855b` |

**Lưu ý:** tiêu chí được ký lúc `2026-11-18T15:12:32`, SHA-256 bắt đầu `f8456224`. Từ đây không sửa `config/acceptance_criteria.json`.

## CP3 · Đo, tìm rủi ro, dựng cổng vòng 1 và quyết định v1 (phút 65–115) · Phiếu B

**Chưa có thẻ sự cố ở CP3.** Tình trạng các mục CP3 chưa được xác nhận từ những file đã xem, nên để ⬜.

### CP3A · Đo và tìm rủi ro (phút 65–85)

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ⬜ | Kỹ sư cổng | Chạy `base`, so với tiêu chí ký; ghi mã run và đọc số kinh doanh/vận hành, kho/hãng. | Phiếu B, B0–B1; lệnh `eval`, `gate` |
| ⬜ | Kỹ sư cổng | Trace `T-002@55`, ghi bằng chứng và phân loại lỗi. | Phiếu B, B2; lệnh `trace` |
| ⬜ | Sản phẩm và kinh doanh | Lập bản đồ dữ liệu, nêu ví dụ drift và metric phát hiện. | Phiếu B, B3 |
| ⬜ | Vận hành và pháp lý | Làm HAZOP vòng 1 và checklist 9 nhóm có PIC nêu tên. | Phiếu B, B4–B5 |
| ⬜ | Cả bàn | Làm pre-mortem bốn lăng kính, chọn 2–3 lý do thành cổng. | Phiếu B, B6 |

### CP3B · Dựng cổng vòng 1 (phút 85–105)

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ⬜ | Kỹ sư cổng | Viết 2–3 cổng; nêu biện pháp tránh rò dữ liệu; viết behavioral test và chạy hai ticket hiểm. | `lab10/guards.py`; Phiếu B, B7.1–B7.3 |
| ⬜ | Sản phẩm và kinh doanh | Chọn trần hoàn, ngân sách/ticket, phạm vi pilot và ROI; ghi căn cứ. | `config/operating_gates.json`, `business`; Phiếu B, B7.4 |
| ⬜ | Vận hành và pháp lý | Điền PIC, người duyệt, nhân lực, công suất, SLA, điều kiện dừng, kênh cảnh báo và quy tắc pháp lý; viết runbook 1–3 và giờ cao điểm. | `config/operating_gates.json`, `operations`/`legal`; Phiếu B, B7.5–B7.6 |
| ⬜ | Cả bàn | Chạy lại eval và test; xác nhận không làm hỏng ticket đang đúng. | Eval `after`; `python3 -m unittest discover -s tests` |

### CP3C · Chốt cổng và quyết định v1 (phút 105–115)

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ⬜ | Kỹ sư cổng | Chạy checkpoint để chụp snapshot vòng 1; đo `prepared` và đối chiếu tiêu chí. | Lệnh `lab10.checkpoint`, `eval --stage prepared`, `gate` |
| ⬜ | Cả bàn | Chốt v1 theo bằng chứng; ghi ba bằng chứng, quy tắc đã ký và ngày xem lại; commit/push. | Phiếu B, B8; Git |

## CP4 · Nhận thẻ, phân tích và xử lý sự cố (phút 125–185) · Phiếu C

**Chỉ làm các mục này sau khi Coach phát thẻ và nhóm bốc số. Chỉ làm đúng thẻ của nhóm. Chạy `grade` trước khi sửa.**

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ⬜ | Cả bàn | Ghi thẻ, chạy grade trước sửa, so sánh base/prepared và đối chiếu pre-mortem. | Phiếu C, C0–C1; `python3 -m lab10.grade --incident Sx` |
| ⬜ | Kỹ sư cổng | Trace ít nhất hai ticket lỗi khác kiểu; ghi bằng chứng, phân loại và nguồn lỗi. | Phiếu C, C2; lệnh `trace` |
| ⬜ | Vận hành và pháp lý | Điền phần riêng đúng thẻ; làm HAZOP sự cố và cùng nhóm vẽ fault tree trước sửa. | Phiếu C, C3 (phần của thẻ đã bốc), C4, C6 |
| ⬜ | Sản phẩm và kinh doanh | Nêu specification kiểm được và giả định môi trường; điều chỉnh cổng kinh doanh nếu nguyên nhân thuộc phạm vi/chi phí. | Phiếu C, C5; `config/operating_gates.json`, `business` |
| ⬜ | Kỹ sư cổng | Sửa cổng kỹ thuật nếu phù hợp; thêm monitor mới; chạy eval sự cố, regression nền và grade. | `lab10/guards.py`, `lab10/monitors.py`; Phiếu C, C7–C8 |
| ⬜ | Cả bàn; vận hành/pháp lý ghi chính | Cập nhật fault tree sau sửa, risk register, checklist và runbook phần 4–5. | Phiếu C, C9–C11 |

## CP5 · Quyết định v2, demo và nộp bài (phút 185–240)

| Trạng thái | Người phụ trách | Công việc | File/vị trí |
|---|---|---|---|
| ⬜ | Cả bàn | Chốt v2 theo tiêu chí/bằng chứng ba mốc; viết ba câu bắt buộc. | Phiếu C, C12 |
| ⬜ | Vận hành và pháp lý; cả bàn rà soát | Điền team, thành viên, thẻ, quyết định v1/v2 và chép ba câu C12. | `submission/submission.json` |
| ⬜ | Cả bàn | Gom bài và sửa các mục thiếu đến khi báo `ĐỦ THÀNH PHẦN`. | `python3 -m lab10.check_submission --collect` |
| ⬜ | Cả bàn | Demo ba mốc; nếu đổi thử config thì khôi phục bản v2 và chạy lại grade/gom bài. | Report `base · prepared · after`; lệnh `grade`, `check_submission` |
| ⬜ | Trưởng nhóm | Commit/push bài cuối và gửi link repo cho team chấm. | Git, repo nhóm |
| ⬜ | Mỗi thành viên | Hoàn tất mục cá nhân và tự nộp link repo lên LMS đúng hạn. | `TEAM.md`; LMS |

## Trách nhiệm chung

- Cả bàn thống nhất ngưỡng ở CP2 và quyết định v1/v2; không để một người tự quyết thay nhóm.
- Quyết định phải khớp bằng chứng và tiêu chí đã ký. Nếu còn vượt trần hoặc ngưỡng bắt buộc chưa đạt thì không chọn “Tiếp tục”.
- Không làm hỏng ca vốn đúng, không xử lý riêng theo mã ticket/câu chữ, không mở thẻ của bàn khác.
- Được dùng AI hỗ trợ, nhưng bàn phải giải thích được ngưỡng và quyết định; mỗi thành viên ghi việc dùng AI trong mục cá nhân `TEAM.md`.
