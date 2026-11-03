package com.photocoach.camera.config

/**
 * Mọi ngưỡng của phần hướng dẫn nằm ở đây, không rải rác trong code.
 * Từ M5 (F9) các giá trị này sẽ được nạp từ file cấu hình JSON; đây là bản mặc định.
 */
data class CoachThresholds(
    val level: LevelThresholds = LevelThresholds(),
)

data class LevelThresholds(
    /** Lệch ngang dưới ngưỡng này (độ) coi là đã cân bằng. */
    val levelToleranceDeg: Float = 1.5f,
    /** Máy chúc/ngửa dưới ngưỡng này (độ) coi là thẳng đứng. */
    val pitchToleranceDeg: Float = 5f,
    /**
     * Thành phần trọng lực trong mặt phẳng màn hình (m/s²) tối thiểu để góc nghiêng
     * có nghĩa. Khi máy gần nằm ngang (đặt trên bàn) thì ẩn thước.
     */
    val minInPlaneGravity: Float = 3f,
    /** Hệ số lọc thông thấp cho cảm biến (0..1, nhỏ = mượt hơn nhưng chậm hơn). */
    val smoothingAlpha: Float = 0.15f,
)
