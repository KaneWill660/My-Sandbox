package com.photocoach.camera.camera

import android.net.Uri
import android.util.Log
import android.view.Surface
import androidx.annotation.StringRes
import androidx.camera.core.MeteringPoint
import androidx.camera.core.Preview
import androidx.lifecycle.LifecycleOwner
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.photocoach.camera.R
import com.photocoach.camera.analysis.DeviceTilt
import com.photocoach.camera.analysis.GravitySensor
import com.photocoach.camera.analysis.TiltMath
import com.photocoach.camera.config.CoachThresholds
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CameraUiState(
    val requestedLens: LensFacing = LensFacing.BACK,
    val capabilities: CameraCapabilities? = null,
    val flashMode: FlashMode = FlashMode.OFF,
    val gridEnabled: Boolean = true,
    val isCapturing: Boolean = false,
    val lastPhotoUri: Uri? = null,
    /** Tăng mỗi lần chụp thành công, để UI chạy hiệu ứng nháy màn hình. */
    val shutterTick: Int = 0,
    @StringRes val message: Int? = null,
)

@HiltViewModel
class CameraViewModel @Inject constructor(
    private val camera: CameraController,
    gravitySensor: GravitySensor,
    val thresholds: CoachThresholds,
) : ViewModel() {

    private val _state = MutableStateFlow(CameraUiState())
    val state: StateFlow<CameraUiState> = _state.asStateFlow()

    private val displayRotation = MutableStateFlow(Surface.ROTATION_0)

    /** Góc nghiêng đã quy về hướng màn hình hiện tại; cảm biến chỉ chạy khi UI đang thu thập. */
    val tilt: Flow<DeviceTilt> = combine(gravitySensor.gravity(), displayRotation) { g, rotation ->
        TiltMath.tilt(g, rotation.toDegrees(), thresholds.level.minInPlaneGravity)
    }

    suspend fun bindCamera(owner: LifecycleOwner, surfaceProvider: Preview.SurfaceProvider) {
        try {
            val caps = camera.bind(owner, surfaceProvider, _state.value.requestedLens, displayRotation.value)
            camera.setFlashMode(_state.value.flashMode)
            _state.update { it.copy(capabilities = caps) }
        } catch (e: Exception) {
            Log.e(TAG, "Bind camera failed", e)
            _state.update { it.copy(message = R.string.msg_camera_failed) }
        }
    }

    fun onDisplayRotationChanged(rotation: Int) {
        displayRotation.value = rotation
        camera.setTargetRotation(rotation)
    }

    fun switchLens() {
        _state.update {
            val current = it.capabilities?.lens ?: it.requestedLens
            it.copy(requestedLens = if (current == LensFacing.BACK) LensFacing.FRONT else LensFacing.BACK)
        }
    }

    fun cycleFlash() {
        val next = _state.value.flashMode.next()
        camera.setFlashMode(next)
        _state.update { it.copy(flashMode = next) }
    }

    fun toggleGrid() = _state.update { it.copy(gridEnabled = !it.gridEnabled) }

    fun focusAt(point: MeteringPoint) = camera.focusAt(point)

    fun takePhoto() {
        if (_state.value.isCapturing) return
        _state.update { it.copy(isCapturing = true) }
        viewModelScope.launch {
            try {
                val uri = camera.takePhoto()
                _state.update {
                    it.copy(lastPhotoUri = uri, shutterTick = it.shutterTick + 1, message = R.string.msg_saved)
                }
            } catch (e: Exception) {
                Log.e(TAG, "Capture failed", e)
                _state.update { it.copy(message = R.string.msg_capture_failed) }
            } finally {
                _state.update { it.copy(isCapturing = false) }
            }
        }
    }

    fun showMessage(@StringRes message: Int) = _state.update { it.copy(message = message) }

    fun consumeMessage() = _state.update { it.copy(message = null) }

    override fun onCleared() {
        camera.unbind()
    }

    private companion object {
        const val TAG = "CameraViewModel"
    }
}

private fun Int.toDegrees(): Int = when (this) {
    Surface.ROTATION_90 -> 90
    Surface.ROTATION_180 -> 180
    Surface.ROTATION_270 -> 270
    else -> 0
}
