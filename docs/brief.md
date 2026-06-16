# AI Fashion Editor - Brief

> *"Ai nói 2GB VRAM không làm được AI? Chúng ta sẽ chứng minh điều ngược lại."*

---

## 1. Bối cảnh (Context)

Bạn có một tấm ảnh. Bạn muốn thử xem mình mặc áo dài trắng trông sẽ như thế nào — nhưng không có chiếc áo dài nào trong tủ. Hoặc đơn giản hơn, bạn muốn nghiên cứu cách AI hiểu và tái tạo cơ thể người khi lớp vải bị loại bỏ.

Các công cụ online thì đắt, chậm, và quan trọng nhất — **ảnh của bạn sẽ đi qua server của người khác**. Đó là điều không thể chấp nhận khi nội dung có tính nhạy cảm.

**AI Fashion Editor** sinh ra để giải bài toán đó: một công cụ chỉnh sửa trang phục chạy **hoàn toàn trên máy của bạn**, không cần internet, không gửi dữ liệu đi đâu cả.

## 2. Thách thức (Challenge)

Đây không phải dự án chạy trên RTX 4090 với 24GB VRAM.

Phần cứng thực tế là một chiếc **Acer Aspire 3** — laptop phổ thông — với card đồ họa **NVIDIA MX250 chỉ có 2GB VRAM**. Con số này nhỏ đến mức hầu hết các mô hình AI sinh ảnh hiện đại (SDXL, Flux, DALL-E) đều từ chối khởi động.

Vậy câu hỏi không phải là *"dùng model nào cho tốt nhất?"* mà là *"làm sao để ép mọi thứ chạy vừa trong 2GB mà vẫn ra kết quả chấp nhận được?"*. Đó chính là thách thức cốt lõi và cũng là điều thú vị nhất của dự án này.

## 3. Giải pháp trực quan (Visionary Solution)

Hình dung quy trình sử dụng như sau:

1. **Tải ảnh lên** → Bạn chọn một bức ảnh chụp người thật (ưu tiên phụ nữ Việt Nam, mở rộng sang Nhật, Hàn, Trung trong tương lai).
2. **AI phân tích** → Hệ thống tự động nhận diện dáng người — tách biệt tóc, khuôn mặt, tay, chân, thân trên, thân dưới — và khoanh vùng chính xác phần trang phục.
3. **Bạn ra lệnh** → Gõ prompt mô tả trang phục mong muốn: *"Áo dài trắng"*, *"Váy đen công sở"*, *"Bikini đỏ"* — hoặc chọn xóa trang phục để nghiên cứu.
4. **AI vẽ lại** → Vùng trang phục được thay thế hoặc xóa bỏ, phần còn lại giữ nguyên tự nhiên.

Tất cả diễn ra ngay trên máy bạn. Không cloud. Không chờ đợi API. Không ai nhìn thấy ảnh của bạn ngoài bạn.

## 4. Định hướng kỹ thuật (Technical Direction)

Chiến lược kỹ thuật xoay quanh một lựa chọn duy nhất nhưng cực kỳ quan trọng: **Stable Diffusion 1.5 + LoRA (Low-Rank Adaptation)**.

- **Tại sao SD 1.5?** — Đủ nhẹ để chạy trên 2GB VRAM khi kết hợp với các kỹ thuật tối ưu bộ nhớ. Các phiên bản mới hơn (SDXL, SD3) quá nặng cho phần cứng này.
- **Tại sao LoRA?** — Thay vì huấn luyện lại toàn bộ mô hình (tốn hàng chục GB VRAM), LoRA chỉ tinh chỉnh một phần rất nhỏ trọng số, tạo ra file bổ sung chỉ vài chục MB mà vẫn đạt hiệu quả cao.

Nói đơn giản: LoRA giống như việc dạy thêm cho AI một *kỹ năng chuyên biệt* (nhận diện dáng người Việt, vẽ áo dài, ...) mà không cần xây lại AI từ đầu.

## 5. Phạm vi (Scope)

### ✅ Cam kết sẽ làm
- Thu thập dữ liệu hình ảnh thời trang và dáng người Việt Nam / Đông Á.
- Huấn luyện LoRA chuyên biệt cho việc nhận diện trang phục và cấu trúc cơ thể.
- Xây dựng pipeline hoàn chỉnh: Segmentation → Inpainting → Kết quả.
- Tạo giao diện web cục bộ (Gradio) đơn giản, dễ dùng.

### ❌ Cam kết KHÔNG làm
- **Không tạo người giả từ văn bản** (Text-to-Image). Dự án chỉ chỉnh sửa trên ảnh người có sẵn.
- **Không triển khai lên cloud** hay biến thành dịch vụ công cộng.
- **Không chia sẻ, phân phối** nội dung NSFW được tạo ra.

## 6. Giá trị cốt lõi (Core Values)

| Giá trị | Cam kết |
|---|---|
| **Bảo mật tuyệt đối** | 100% offline, local. Không một byte dữ liệu nào rời khỏi máy tính của bạn. |
| **Tôn trọng sự riêng tư** | Nội dung NSFW chỉ phục vụ nghiên cứu cá nhân, khép kín hoàn toàn. |
| **Tinh thần DIY** | Chứng minh rằng phần cứng bình dân vẫn chạm tới AI tiên tiến — nếu biết tối ưu đúng cách. |
