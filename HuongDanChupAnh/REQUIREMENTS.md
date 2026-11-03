# Photo Coach Camera, Yêu cầu dự án (Requirements)

> Tài liệu này dành cho Claude Code. Hãy đọc toàn bộ, đề xuất kế hoạch ngắn, rồi làm theo từng Milestone. Sau mỗi milestone phải build được và chạy được trên máy thật trước khi sang bước tiếp.

## 1. Tổng quan

- **Tên tạm:** Photo Coach Camera
- **Mục tiêu:** App camera riêng cho Android, hướng dẫn người dùng chụp ảnh người đẹp hơn như một nhiếp ảnh gia: đứng gần/xa, máy cao/thấp, zoom, ánh sáng, bố cục.
- **Người dùng:** người không chuyên, thường chụp ảnh người thân/bạn bè bằng điện thoại.
- **Nguyên tắc cốt lõi:**
  - Thông số máy (zoom, EV, focus) thì **app tự chỉnh bằng 1 nút "Áp dụng"**.
  - Việc phải di chuyển (lùi/tiến, hạ máy, xoay người mẫu) thì **app hướng dẫn trực quan bằng overlay + giọng nói**.
  - Mỗi lúc chỉ hiện **1 gợi ý ưu tiên nhất** để không rối.
- **Ngôn ngữ giao diện & lời khuyên:** tiếng Việt (chuẩn bị sẵn i18n để thêm tiếng Anh sau).

## 2. Phạm vi

### Trong phạm vi (MVP)
- App camera riêng, chỉ Android.
- Phân tích real-time trên máy (on-device) + gợi ý bằng overlay.
- Nút "Áp dụng" tự chỉnh zoom / EV / focus.
- Nút "Chuyên gia nhận xét" gửi ảnh nhỏ lên server để AI vision phân tích.
- **Giai đoạn test:** app gọi thẳng vision API bằng API key đặt trong app (chỉ dùng cá nhân, KHÔNG phát hành).
- **Trước khi phát hành:** chuyển sang server trung gian (Cloudflare Worker), nằm ngoài MVP nhưng kiến trúc phải sẵn sàng (xem F7.7).

### Ngoài phạm vi (làm sau)
- iOS / đa nền tảng.
- Layer đè lên app camera có sẵn (đã loại: không đọc được khung hình, không điều khiển được, rủi ro chính sách Google Play).
- Huấn luyện model riêng chấm "ảnh đẹp".
- Chỉnh sửa/hậu kỳ ảnh, tài khoản người dùng, thanh toán.

## 3. Công nghệ

- **Ngôn ngữ/UI:** Kotlin, Jetpack Compose (overlay vẽ bằng Compose Canvas hoặc custom View đặt trên `PreviewView`).
- **Camera:** CameraX (`Preview`, `ImageAnalysis`, `ImageCapture`). Dùng `Camera2Interop` chỉ khi cần ISO/shutter/WB.
- **Đồ chuẩn hoá toạ độ:** `ImageAnalysis.COORDINATE_SYSTEM_VIEW_REFERENCED` và `CoordinateTransform` (không tự tính tay).
- **Hiệu ứng hãng:** CameraX Extensions (HDR, Night, Bokeh, Face Retouch) kiểm tra bằng `ExtensionsManager`, có fallback.
- **AI on-device:** ML Kit hoặc MediaPipe (face detection, pose landmarks, selfie segmentation nếu cần).
- **Cảm biến:** accelerometer / gyroscope / rotation vector.
- **Mạng:** Retrofit hoặc Ktor client, HTTPS.
- **Kiến trúc:** MVVM, Hilt, Coroutines/Flow, module hoá rõ ràng.
- **AI đám mây (giai đoạn test):** gọi trực tiếp từ app tới vision API (Claude hoặc Gemini) bằng HTTPS. Key đọc từ `local.properties` qua `BuildConfig`.
- **Backend (giai đoạn sau):** Cloudflare Worker (TypeScript) làm proxy, thay thế việc gọi trực tiếp trước khi phát hành.
- **minSdk:** 26 trở lên (đề xuất), targetSdk mới nhất.

## 4. Yêu cầu chức năng

### F1. Camera & Preview
- F1.1 Hiển thị preview toàn màn hình, nút chụp, nút đổi camera trước/sau, nút flash.
- F1.2 Chụp ảnh chất lượng đầy đủ, lưu vào bộ sưu tập (MediaStore, thư mục riêng của app).
- F1.3 Xin quyền CAMERA (và quyền lưu ảnh nếu cần) với giải thích rõ ràng, xử lý từ chối quyền.
- F1.4 Chạm vào preview để lấy nét + đo sáng thủ công.
- F1.5 Bật CameraX Extensions khi máy hỗ trợ; ẩn tuỳ chọn khi không hỗ trợ.

### F2. Phân tích real-time (on-device)
- F2.1 Luồng `ImageAnalysis` độ phân giải khoảng 480p, 10 đến 15 khung hình/giây, bỏ khung khi xử lý chưa xong (`STRATEGY_KEEP_ONLY_LATEST`).
- F2.2 Nhận diện khuôn mặt: vị trí, kích thước tương đối so với khung hình.
- F2.3 (Milestone sau) Nhận diện tư thế: phát hiện cắt ở khớp tay/chân, người mẫu bị cắt khỏi khung.
- F2.4 Đo sáng bằng histogram: thiếu sáng, cháy sáng, ngược sáng (mặt tối hơn nền đáng kể).
- F2.5 Đọc gyro: góc nghiêng (pitch) và độ lệch ngang (roll) của máy.
- F2.6 Chỉ đưa ra gợi ý khi cảnh **ổn định vài giây** (tránh nhấp nháy).

### F3. Rule engine (gợi ý)
Mỗi luật nhận số đo, trả về: `id`, `độ ưu tiên`, `loại` (chỉnh máy / di chuyển), `nội dung tiếng Việt`, `hành động áp dụng` (nếu có).

Các luật tối thiểu cho MVP:
- **Khoảng cách:** tỷ lệ mặt/thân so với khung hình quá nhỏ hoặc quá lớn thì gợi ý "tiến/lùi N bước" hoặc "zoom Nx". Chân dung ưu tiên tiêu cự tương đương 50 đến 85mm, tránh góc rộng gây méo mặt.
- **Độ cao máy:** chân dung ngang tầm mắt; dáng người cao thì hạ máy thấp hơn một chút. Dựa vào pitch gyro.
- **Đường chân trời/độ nghiêng:** cảnh báo khi máy nghiêng ngang quá ngưỡng.
- **Bố cục:** lưới 1/3, khoảng trống phía trên đầu hợp lý, không cắt ở khớp.
- **Ánh sáng:** thiếu sáng thì tăng EV hoặc bật đèn; ngược sáng thì giảm EV/đổi hướng "xoay người mẫu về phía nguồn sáng".
- Chỉ hiển thị **1 gợi ý có độ ưu tiên cao nhất** tại một thời điểm.
- Ngưỡng của các luật phải cấu hình được (file config/hằng số), không hard-code rải rác.

### F4. Overlay trên camera
- F4.1 Lớp overlay cùng kích thước `PreviewView`, nằm chồng phía trên.
- F4.2 Vẽ: khung quanh mặt, lưới 1/3 (bật/tắt được), thanh cân bằng gyro, mũi tên di chuyển ("lùi 1 bước", "hạ máy xuống"), chữ gợi ý.
- F4.3 Khi mọi điều kiện đạt: khung chuyển xanh, hiện "Hoàn hảo, chụp đi!".
- F4.4 Toạ độ phải khớp preview ở mọi hướng xoay màn hình và với camera trước (lật gương).

### F5. Nút "Áp dụng" (điều khiển thông số)
- F5.1 Với gợi ý loại chỉnh máy, hiện nút **"Áp dụng"**: bấm 1 lần là app chỉnh:
  - Zoom: `CameraControl.setZoomRatio()`
  - EV: `setExposureCompensationIndex()` (kẹp trong khoảng máy hỗ trợ)
  - Focus + đo sáng: `FocusMeteringAction` đặt vào khuôn mặt
  - Torch/flash
  - ISO, shutter, white balance: qua `Camera2Interop`, chỉ khi máy hỗ trợ
- F5.2 Chế độ **"Tự động"** (tuỳ chọn, mặc định tắt): app tự áp dụng khi cảnh ổn định.
- F5.3 Nút **"Hoàn tác / Về mặc định"** luôn có sẵn.
- F5.4 Không đổi thông số liên tục; có thời gian chờ tối thiểu giữa 2 lần tự chỉnh.
- F5.5 Zoom số quá cao làm vỡ ảnh: ưu tiên ống kính tele nếu có (chọn camera phù hợp), nếu không thì gợi ý "đứng xa hơn" thay vì zoom thêm.

### F6. Hướng dẫn bằng giọng nói
- F6.1 Đọc gợi ý bằng Android TextToSpeech tiếng Việt, bật/tắt được.
- F6.2 Không đọc lặp lại cùng một gợi ý liên tục (cooldown).

### F7. "Chuyên gia nhận xét" (AI đám mây)
- F7.1 Nút trên màn hình camera, chỉ gửi khi người dùng bấm (không gửi tự động liên tục).
- F7.2 Tạo ảnh nhỏ: lấy 1 khung hình, xoay đúng chiều theo `rotationDegrees`, cạnh dài khoảng 1024px, JPEG chất lượng 80 (khoảng 100 đến 200KB), xử lý trên luồng nền.
- F7.3 Gọi **trực tiếp** vision API từ app (HTTPS POST, ảnh base64 theo định dạng của nhà cung cấp), kèm prompt hệ thống yêu cầu chỉ trả JSON đúng schema ở mục 6.
- F7.7 Đặt việc gọi AI sau interface `VisionAnalyzer` với 2 implementation: `DirectApiAnalyzer` (gọi thẳng, dùng bây giờ) và `ProxyAnalyzer` (gọi Worker, làm sau). Chọn bằng một cờ cấu hình, không để logic UI phụ thuộc cách gọi.
- F7.4 Nhận JSON phản hồi theo schema ở mục 6, hiển thị dạng thẻ nổi trên preview (lời khuyên + nút "Áp dụng" cho thông số đề xuất). Preview tiếp tục chạy trong lúc chờ.
- F7.5 Xử lý lỗi: mất mạng, timeout, JSON sai định dạng, hết hạn mức. Hiện thông báo thân thiện, không làm app crash.
- F7.6 Hiển thị loading rõ ràng và cho huỷ.

### F8. Cài đặt
- Bật/tắt: lưới, giọng nói, chế độ Tự động, tính năng AI đám mây.
- Màn hình/hộp thoại giải thích quyền riêng tư (xem mục 5).

### F9. Prompt & cấu hình cập nhật không cần build lại APK
- F9.1 **Không hard-code prompt trong code.** Prompt và cấu hình AI nằm trong một file JSON, có trường `version`. Nội dung gồm: `systemPrompt`, `fewShotExamples`, `rules` (danh sách quy tắc nhiếp ảnh), `model`, `temperature`, `maxTokens`, và ngưỡng của rule engine.
- F9.2 **Thứ tự ưu tiên nguồn cấu hình** (cao đến thấp):
  1. Bản **chỉnh tay trong app** (override cục bộ, F9.5)
  2. Bản **tải từ URL** đã cache
  3. Bản **mặc định** đóng gói trong `assets/` (luôn có, dùng khi mất mạng)
- F9.3 Tải bản mới từ URL (mặc định là một file JSON công khai, cấu hình được; thiết kế sẵn để đổi sang Firebase Remote Config hoặc Worker sau này) khi mở app, tối đa 1 lần/ngày, có nút "Tải lại ngay" trong màn Cài đặt.
- F9.4 **Validate** trước khi dùng: JSON hợp lệ, đủ trường bắt buộc, không rỗng, không quá dài, giá trị trong khoảng cho phép. Nếu sai thì giữ bản đang dùng và báo lỗi nhẹ, không crash.
- F9.5 **Màn hình "Chỉnh prompt" (chế độ nhà phát triển):**
  - Cách vào: một nút **"Chỉnh prompt"** hiển thị rõ ràng trong màn Cài đặt (giai đoạn test chưa cần ẩn). Khi chuẩn bị phát hành thì ẩn hoặc gỡ.
  - Sửa được: `systemPrompt`, các ví dụ mẫu, quy tắc, model, temperature, maxTokens, ngưỡng rule engine.
  - Nút **"Lưu"**: lưu thành override cục bộ (DataStore hoặc Room), có hiệu lực ngay ở lần gọi AI kế tiếp.
  - Nút **"Chạy thử"**: gửi ảnh vừa chụp gần nhất với prompt đang sửa, hiển thị JSON thô và kết quả đã phân tích ngay trên màn hình, **chưa lưu** nếu chưa bấm Lưu.
  - Nút **"Khôi phục"**: quay về bản tải từ URL hoặc bản mặc định.
  - **Lịch sử** vài bản gần nhất (thời gian, version) để quay lại bản cũ.
  - Nút **"Xuất / Nhập JSON"**: sao chép hoặc chia sẻ toàn bộ cấu hình ra ngoài để tôi đưa lên URL chung, và dán lại khi cần.
- F9.6 Ghi `version` của cấu hình đang dùng vào log mỗi lần gọi AI, để so sánh chất lượng giữa các bản.
- F9.7 Chỉ tải **nội dung cấu hình**, tuyệt đối không tải hay chạy code thực thi.
- F9.8 Màn hình này **không** tự đẩy prompt lên server chung. Việc đưa lên URL chung do tôi làm thủ công qua Xuất JSON, tránh phải xây hệ thống đăng nhập/phân quyền ở giai đoạn này.

## 5. Yêu cầu phi chức năng

- **Hiệu năng:** preview mượt (không giật), phân tích không chặn luồng chính; độ trễ gợi ý dưới khoảng 300ms sau khi cảnh ổn định.
- **Pin/nhiệt:** giảm tần suất phân tích khi cảnh ổn định; dừng phân tích khi app ở nền.
- **Tương thích:** kiểm tra nhiều dòng máy; mọi tính năng phụ thuộc phần cứng (Extensions, ISO/shutter, tele) phải có kiểm tra khả năng và phương án dự phòng.
- **Bảo mật (giai đoạn test):** key nằm trong app nên có thể bị trích ra khỏi APK. Chấp nhận được chỉ khi app dùng cá nhân. Bắt buộc:
  - Key để trong `local.properties`, đã nằm trong `.gitignore`, tuyệt đối không commit lên git.
  - Dùng key riêng cho dự án này, đặt **giới hạn chi tiêu hàng tháng thấp** ở trang quản lý của nhà cung cấp, và đổi key ngay nếu nghi bị lộ.
  - Không gửi APK này cho người khác, không đưa lên Google Play.
  - Giới hạn lượt gọi ở phía app (cooldown giữa 2 lần bấm, trần số lượt/ngày) để tránh tốn tiền do bấm nhầm.
  - Thêm ghi chú `TODO: chuyển sang ProxyAnalyzer trước khi phát hành` ở chỗ đọc key.
- **Bảo mật (trước khi phát hành):** không nhúng key trong app. App chỉ gọi Worker; Worker giữ key, giới hạn số lượt dùng theo thiết bị/ngày, giới hạn kích thước ảnh.
- **Riêng tư:** phân tích real-time chạy hoàn toàn trên máy. Ảnh chỉ rời máy khi người dùng bấm "Chuyên gia nhận xét", có thông báo rõ ràng trước lần đầu và cho tắt tính năng. Không lưu ảnh trên server; không ghi log nội dung ảnh.
- **Chất lượng mã:** có unit test cho rule engine (đầu vào số đo, đầu ra gợi ý), kiểm tra quy đổi toạ độ, và xử lý lỗi mạng.
- **Khả năng mở rộng:** rule engine dạng plugin/strategy để thêm luật mới dễ dàng; các chuỗi hiển thị nằm trong `strings.xml`.

## 6. Hợp đồng dữ liệu AI

Giai đoạn test: app gọi thẳng API của nhà cung cấp, nhưng **kết quả mà `VisionAnalyzer` trả về cho phần còn lại của app luôn theo schema dưới đây**, để sau này đổi sang Worker không phải sửa UI.

**Đầu vào của `VisionAnalyzer.analyze(...)`:** ảnh JPEG đã thu nhỏ, `mode` (`portrait` / `group` / `food` / `landscape`), `locale` (`vi`).

**Kết quả (JSON, app phải tự validate vì model có thể trả sai định dạng):**
```json
{
  "summary": "Ánh sáng ngược, mặt hơi tối.",
  "issues": [
    { "id": "backlight", "severity": "high", "advice": "Xoay người mẫu về phía cửa sổ." }
  ],
  "suggested": { "zoom": 2.0, "ev": 1, "moveHint": "lùi 1 bước" },
  "score": 6
}
```
- Mọi trường tuỳ chọn trừ `summary`; app phải chịu được trường thiếu hoặc giá trị ngoài khoảng (ví dụ zoom/EV phải kẹp vào khoảng máy hỗ trợ).
- Prompt hệ thống: vai nhiếp ảnh gia chân dung, **chỉ trả JSON đúng schema**, lời khuyên ngắn tiếng Việt.
- Xử lý lỗi từ API: `401` (sai key), `429` (hết hạn mức), timeout, JSON sai định dạng. Hiện thông báo thân thiện.
- Khi chuyển sang Worker (giai đoạn sau): `POST /analyze` nhận ảnh và trả đúng schema trên, thêm giới hạn lượt theo thiết bị và lỗi `413` (ảnh quá lớn).

## 7. Cấu trúc dự án đề xuất

```
photo-coach/
├── app/                    # Android app (Kotlin, Compose)
│   ├── camera/             # CameraX setup, controls, extensions
│   ├── analysis/           # ML Kit/MediaPipe, histogram, gyro
│   ├── rules/              # Rule engine + các luật + config ngưỡng
│   ├── overlay/            # Overlay view/Compose, hướng dẫn, mũi tên
│   ├── ai/                 # Client gọi Worker, model dữ liệu JSON
│   ├── tts/                # Giọng nói
│   └── settings/
└── worker/                 # (GIAI ĐOẠN SAU) Cloudflare Worker, chưa làm trong MVP
    ├── src/index.ts
    └── wrangler.toml
```

## 8. Lộ trình (Milestones)

1. **M1: Camera nền tảng.** Preview, chụp ảnh, lưu ảnh, quyền, lưới 1/3, thước cân bằng gyro. *Done khi:* chụp và lưu ảnh được trên máy thật.
2. **M2: Phân tích on-device.** Histogram (thiếu/cháy/ngược sáng), face detection, quy đổi toạ độ đúng cho overlay. *Done khi:* khung mặt bám đúng ở mọi hướng và camera trước/sau.
3. **M3: Rule engine + overlay + "Áp dụng".** Luật khoảng cách, độ cao, ánh sáng, bố cục; 1 gợi ý ưu tiên; nút Áp dụng zoom/EV/focus; Hoàn tác. *Done khi:* gợi ý ổn định, không nhấp nháy.
4. **M4: Giọng nói tiếng Việt + Cài đặt.** TTS với cooldown, màn Cài đặt.
5. **M5: AI đám mây (gọi trực tiếp), gồm cả F9 (cấu hình/prompt cập nhật được và màn Chỉnh prompt).** `VisionAnalyzer` + `DirectApiAnalyzer`, hàm tạo ảnh nhỏ, thẻ nhận xét, xử lý lỗi, cooldown/trần lượt phía app, thông báo riêng tư. Key đọc từ `local.properties`.
5b. **M5b (trước khi phát hành, không thuộc MVP):** dựng Cloudflare Worker, viết `ProxyAnalyzer`, gỡ key khỏi app.
6. **M6: Nâng cao.** Pose (cắt khớp tay/chân), CameraX Extensions, chế độ cảnh (nhóm, đồ ăn, phong cảnh), ISO/shutter/WB qua Camera2Interop.

## 9. Tiêu chí nghiệm thu MVP (M1 đến M5)

- Chạy ổn định trên ít nhất 2 dòng máy Android khác nhau.
- Preview không giật khi bật phân tích real-time.
- Gợi ý hiển thị đúng, đúng thứ tự ưu tiên, không nhấp nháy.
- "Áp dụng" chỉnh được zoom/EV/focus và "Hoàn tác" hoạt động.
- Nút "Chuyên gia nhận xét" trả về nhận xét và hiển thị thẻ trong vòng vài giây trên mạng bình thường; lỗi mạng được xử lý êm.
- Key không bị commit lên git (kiểm tra `.gitignore`); ghi chú rõ APK bản test này chỉ dùng cá nhân.

## 10. Hướng dẫn làm việc cho Claude Code

- Trước khi code: đọc tài liệu, nêu kế hoạch ngắn cho M1 và các giả định.
- Làm từng milestone; sau mỗi milestone phải build thành công và liệt kê cách tự kiểm tra thủ công.
- Giữ rule engine thuần Kotlin (không phụ thuộc Android) để dễ unit test.
- Khi gặp giới hạn phần cứng/OS, ghi lại lựa chọn dự phòng thay vì bỏ tính năng im lặng.
- Hỏi lại tôi khi cần quyết định về: nhà cung cấp vision API (Claude hay Gemini), danh sách máy thử, trần số lượt gọi AI mỗi ngày.
- Không bao giờ in key ra log, không đưa key vào file được commit. Nếu thấy key sắp bị commit, dừng lại và báo tôi.
