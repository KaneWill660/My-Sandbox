package com.photocoach.camera.analysis

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import com.photocoach.camera.config.CoachThresholds
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.conflate
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Phát vector trọng lực đã lọc. Ưu tiên TYPE_GRAVITY (đã hợp nhất gyro + gia tốc kế),
 * nếu máy không có thì dùng gia tốc kế (dự phòng, rung hơn nên vẫn lọc thông thấp).
 * Chỉ đăng ký cảm biến khi có người thu thập Flow, nên tự dừng khi app vào nền.
 */
@Singleton
class GravitySensor @Inject constructor(
    @ApplicationContext context: Context,
    private val thresholds: CoachThresholds,
) {
    private val sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    private val sensor: Sensor? =
        sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY)
            ?: sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

    val isAvailable: Boolean get() = sensor != null

    fun gravity(): Flow<Gravity> = callbackFlow {
        val s = sensor
        if (s == null) {
            close()
            return@callbackFlow
        }
        var filtered: Gravity? = null
        val listener = object : SensorEventListener {
            override fun onSensorChanged(event: SensorEvent) {
                val raw = Gravity(event.values[0], event.values[1], event.values[2])
                filtered = TiltMath.lowPass(filtered, raw, thresholds.level.smoothingAlpha)
                trySend(filtered!!)
            }

            override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) = Unit
        }
        sensorManager.registerListener(listener, s, SensorManager.SENSOR_DELAY_UI)
        awaitClose { sensorManager.unregisterListener(listener) }
    }.conflate()
}
