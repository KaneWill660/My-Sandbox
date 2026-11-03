# Photo Coach Camera

App camera Android hướng dẫn chụp ảnh người. Yêu cầu đầy đủ: [REQUIREMENTS.md](REQUIREMENTS.md).

> **Bản test chỉ dùng cá nhân.** Không gửi APK cho người khác, không đưa lên Google Play.
> Từ M5 app chứa API key trong `local.properties` (đã nằm trong `.gitignore`, không bao giờ commit).

## Trạng thái

| Milestone | Nội dung | Trạng thái |
|---|---|---|
| M1 | Preview, chụp & lưu, quyền, lưới 1/3, thước cân bằng | ✅ Đã merge |
| M2 | Histogram, face detection, quy đổi toạ độ | ✅ Code xong, chờ thử máy thật |
| M3 | Rule engine, overlay gợi ý, nút Áp dụng / Hoàn tác | ⏳ |
| M4 | Giọng nói tiếng Việt, màn Cài đặt | ⏳ |
| M5 | Chuyên gia nhận xét (Claude + Gemini), cấu hình prompt F9 | ⏳ |

## Build

Cần JDK 17 và Android SDK 35.

```bash
# Android Studio: mở thư mục này, Run 'app'.
# Dòng lệnh (Windows, JDK 17 portable):
JAVA_HOME="$USERPROFILE/.jdks/temurin-17" ./gradlew assembleDebug testDebugUnitTest
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

`local.properties` (không commit) chứa `sdk.dir`; xem mẫu ở `local.properties.example`.

## Cấu trúc

```
app/src/main/java/com/photocoach/camera/
├── camera/      CameraX (Preview + ImageCapture), màn camera, ViewModel
├── analysis/    Cảm biến trọng lực, FrameAnalyzer (ML Kit + histogram), phần tính toán
│                thuần Kotlin có unit test: TiltMath, ImageGeometry, LumaStats, ExposureClassifier
├── config/      CoachThresholds — mọi ngưỡng ở một chỗ (M5 sẽ nạp từ JSON)
├── overlay/     Lưới 1/3, thước cân bằng, vòng lấy nét
├── permission/  Xin quyền có giải thích, xử lý từ chối vĩnh viễn
└── ui/theme/
```

Đến M3 rule engine sẽ được tách thành module Kotlin thuần riêng (`:rules`) để unit test không cần Android.

## Tự kiểm tra M1 trên máy thật

1. **Quyền:** cài mới → app giải thích rồi xin quyền Camera. Từ chối 2 lần → hiện nút "Mở Cài đặt"; bật quyền trong Cài đặt rồi quay lại → camera mở ngay.
2. **Preview:** khung 3:4 ở giữa màn hình, mượt, không méo.
3. **Chụp:** bấm nút tròn → màn hình nháy trắng, hiện "Đã lưu ảnh…", ảnh thu nhỏ xuất hiện ở góc. Bấm ảnh thu nhỏ → mở trình xem ảnh. Kiểm tra trong Thư viện, album **PhotoCoach** (Android 10+), ảnh đúng chiều, đúng khung như preview.
4. **Đổi camera:** bấm nút đổi → chuyển camera trước (preview lật gương), chụp được.
5. **Flash:** bấm xoay vòng Tắt → Tự động → Bật; chụp trong tối với "Bật" → đèn nháy. Camera trước không có flash → nút ẩn.
6. **Chạm lấy nét:** chạm vào vật gần/xa → vòng vàng hiện tại điểm chạm, nét và độ sáng đổi theo.
7. **Lưới 1/3:** nút lưới bật/tắt.
8. **Thước cân bằng:** nghiêng máy trái/phải → đường giữa xoay, giữ song song với mặt đất, chữ "Nghiêng N°"; khi gần 0° chuyển xanh "Đã cân bằng". Chúc/ngửa máy → "Máy chúc xuống / ngửa lên N°". Đặt máy nằm ngang trên bàn → thước ẩn.
9. **Xoay màn hình:** xoay ngang hai chiều và dọc ngược → nút chuyển sang hai bên, thước vẫn đúng, ảnh chụp đúng chiều.
10. **Nền:** về màn hình chính rồi quay lại → camera mở lại bình thường.

## Tự kiểm tra M2 trên máy thật

Bật nút **số đo** (biểu tượng biểu đồ, hàng trên) để thấy dòng số đo thô ở góc dưới preview.

1. **Khung mặt bám đúng:** hướng camera sau vào một người → khung góc trắng ôm sát mặt, di chuyển theo mặt. Nhiều người → mặt lớn nhất khung đậm, mặt khác khung mờ.
2. **Camera trước:** đổi sang camera trước, nghiêng đầu sang trái/phải → khung đi cùng chiều với hình trên màn hình (đã tính lật gương).
3. **Mọi hướng xoay:** xoay máy dọc, ngang trái, ngang phải, dọc ngược → sau khi preview ổn định (~0.5 giây), khung vẫn ôm đúng mặt.
4. **Tỷ lệ mặt:** tiến lại gần → "cao N%" tăng; lùi xa → giảm.
5. **Thiếu sáng:** che bớt ống kính/vào phòng tối → chip vàng "Thiếu sáng".
6. **Cháy sáng:** chĩa vào bóng đèn/bầu trời nắng → "Cháy sáng".
7. **Ngược sáng:** cho người đứng quay lưng ra cửa sổ sáng → "Ngược sáng, mặt bị tối", số "mặt/nền" khoảng dưới 0.6.
8. **Mượt:** preview không giật khi bật phân tích; về nền rồi quay lại vẫn chạy.

Ngưỡng đo sáng nằm trong `config/CoachThresholds.kt` (`ExposureThresholds`). Nếu báo sai trên máy của bạn, chụp màn hình kèm dòng số đo gửi tôi để chỉnh ngưỡng.

## Giới hạn & phương án dự phòng

- Android 8–9: ảnh lưu vào thư mục Pictures gốc (không có `RELATIVE_PATH`), cần thêm quyền lưu trữ.
- Máy không có cảm biến trọng lực → dùng gia tốc kế + lọc thông thấp; không có cả hai → ẩn thước.
- Máy chỉ có một camera → ẩn nút đổi camera.
- Khi xoay màn hình camera được ràng buộc lại (ViewPort đổi theo hướng), preview chớp nhẹ một lần — đổi lại toạ độ overlay luôn đúng.
- ML Kit dùng model đóng gói sẵn (không cần Google Play Services, chạy offline) nên APK debug khoảng 57MB vì chứa thư viện cho mọi kiến trúc CPU. Có thể giới hạn `abiFilters` khi cần.
