package com.photocoach.camera.camera

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.hardware.display.DisplayManager
import android.net.Uri
import android.os.Build
import android.util.Size
import android.view.Surface
import androidx.camera.view.PreviewView
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Cameraswitch
import androidx.compose.material.icons.filled.FlashAuto
import androidx.compose.material.icons.filled.FlashOff
import androidx.compose.material.icons.filled.FlashOn
import androidx.compose.material.icons.filled.GridOff
import androidx.compose.material.icons.filled.GridOn
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.photocoach.camera.R
import com.photocoach.camera.overlay.FocusRing
import com.photocoach.camera.overlay.LevelGauge
import com.photocoach.camera.overlay.RuleOfThirdsGrid
import com.photocoach.camera.overlay.ShutterFlash
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

@Composable
fun CameraScreen(viewModel: CameraViewModel = hiltViewModel()) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val state by viewModel.state.collectAsStateWithLifecycle()
    val tilt by viewModel.tilt.collectAsStateWithLifecycle(initialValue = null)

    val previewView = remember {
        PreviewView(context).apply { scaleType = PreviewView.ScaleType.FILL_CENTER }
    }

    TrackDisplayRotation(viewModel::onDisplayRotationChanged)

    LaunchedEffect(state.requestedLens) {
        viewModel.bindCamera(lifecycleOwner, previewView.surfaceProvider)
    }

    val snackbar = remember { SnackbarHostState() }
    val message = state.message?.let { stringResource(it) }
    LaunchedEffect(message) {
        if (message != null) {
            viewModel.consumeMessage()
            snackbar.showSnackbar(message)
        }
    }

    var focusPoint by remember { mutableStateOf<Offset?>(null) }
    var focusKey by remember { mutableIntStateOf(0) }

    BoxWithConstraints(
        Modifier
            .fillMaxSize()
            .background(Color.Black),
    ) {
        val landscape = maxWidth > maxHeight

        // Vùng preview 3:4 (dọc) / 4:3 (ngang), khớp tỷ lệ ảnh chụp. Overlay cùng kích thước.
        Box(
            Modifier
                .align(Alignment.Center)
                .aspectRatio(if (landscape) 4f / 3f else 3f / 4f)
                .pointerInput(Unit) {
                    detectTapGestures { offset ->
                        val point = previewView.meteringPointFactory.createPoint(offset.x, offset.y)
                        viewModel.focusAt(point)
                        focusPoint = offset
                        focusKey++
                    }
                },
        ) {
            AndroidView(factory = { previewView }, modifier = Modifier.fillMaxSize())
            if (state.gridEnabled) RuleOfThirdsGrid()
            tilt?.let {
                LevelGauge(it, viewModel.thresholds.level, Modifier.align(Alignment.Center))
            }
            focusPoint?.let { FocusRing(it, focusKey) }
            ShutterFlash(state.shutterTick)
        }

        val secondary: @Composable () -> Unit = {
            if (state.capabilities?.hasFlash == true) {
                FlashButton(state.flashMode, viewModel::cycleFlash)
            }
            GridButton(state.gridEnabled, viewModel::toggleGrid)
        }
        val primary: @Composable () -> Unit = {
            LastPhotoThumb(state.lastPhotoUri) { uri ->
                if (!context.openPhoto(uri)) viewModel.showMessage(R.string.msg_no_viewer)
            }
            ShutterButton(enabled = !state.isCapturing, onClick = viewModel::takePhoto)
            if (state.capabilities?.canSwitchLens == true) {
                RoundIconButton(
                    onClick = viewModel::switchLens,
                    description = stringResource(R.string.cd_switch_camera),
                ) { Icon(Icons.Filled.Cameraswitch, null, tint = Color.White) }
            } else {
                Spacer(Modifier.size(56.dp))
            }
        }

        if (landscape) {
            Column(
                Modifier
                    .align(Alignment.CenterStart)
                    .fillMaxHeight()
                    .safeDrawingPadding()
                    .padding(8.dp),
                verticalArrangement = Arrangement.SpaceEvenly,
                horizontalAlignment = Alignment.CenterHorizontally,
            ) { secondary() }
            Column(
                Modifier
                    .align(Alignment.CenterEnd)
                    .fillMaxHeight()
                    .safeDrawingPadding()
                    .padding(8.dp),
                verticalArrangement = Arrangement.SpaceEvenly,
                horizontalAlignment = Alignment.CenterHorizontally,
            ) { primary() }
        } else {
            Row(
                Modifier
                    .align(Alignment.TopCenter)
                    .fillMaxWidth()
                    .safeDrawingPadding()
                    .padding(8.dp),
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically,
            ) { secondary() }
            Row(
                Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .safeDrawingPadding()
                    .padding(horizontal = 24.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) { primary() }
        }

        SnackbarHost(
            snackbar,
            Modifier
                .align(if (landscape) Alignment.BottomCenter else Alignment.Center)
                .safeDrawingPadding(),
        )
    }
}

/**
 * Activity tự xử lý xoay (configChanges), nên lắng nghe DisplayManager để biết hướng màn hình,
 * kể cả khi xoay 180° (không phát sinh configuration change).
 */
@Composable
private fun TrackDisplayRotation(onRotation: (Int) -> Unit) {
    val view = LocalView.current
    val context = LocalContext.current
    DisposableEffect(view) {
        val dm = context.getSystemService(Context.DISPLAY_SERVICE) as DisplayManager
        fun report() = onRotation(view.display?.rotation ?: Surface.ROTATION_0)
        val listener = object : DisplayManager.DisplayListener {
            override fun onDisplayAdded(displayId: Int) = Unit
            override fun onDisplayRemoved(displayId: Int) = Unit
            override fun onDisplayChanged(displayId: Int) {
                if (displayId == view.display?.displayId) report()
            }
        }
        report()
        dm.registerDisplayListener(listener, null)
        onDispose { dm.unregisterDisplayListener(listener) }
    }
}

@Composable
private fun FlashButton(mode: FlashMode, onClick: () -> Unit) {
    val (icon, desc) = when (mode) {
        FlashMode.OFF -> Icons.Filled.FlashOff to R.string.cd_flash_off
        FlashMode.AUTO -> Icons.Filled.FlashAuto to R.string.cd_flash_auto
        FlashMode.ON -> Icons.Filled.FlashOn to R.string.cd_flash_on
    }
    IconButton(onClick = onClick) {
        Icon(icon, contentDescription = stringResource(desc), tint = Color.White)
    }
}

@Composable
private fun GridButton(enabled: Boolean, onClick: () -> Unit) {
    IconButton(onClick = onClick) {
        Icon(
            if (enabled) Icons.Filled.GridOn else Icons.Filled.GridOff,
            contentDescription = stringResource(if (enabled) R.string.cd_grid_on else R.string.cd_grid_off),
            tint = Color.White,
        )
    }
}

@Composable
private fun ShutterButton(enabled: Boolean, onClick: () -> Unit) {
    val description = stringResource(R.string.cd_shutter)
    Box(
        Modifier
            .size(76.dp)
            .border(4.dp, Color.White, CircleShape)
            .padding(8.dp)
            .clip(CircleShape)
            .background(if (enabled) Color.White else Color.Gray)
            .semantics { contentDescription = description }
            .clickable(enabled = enabled, onClick = onClick),
    )
}

@Composable
private fun RoundIconButton(onClick: () -> Unit, description: String, content: @Composable () -> Unit) {
    Box(
        Modifier
            .size(56.dp)
            .clip(CircleShape)
            .background(Color.White.copy(alpha = 0.15f))
            .semantics { contentDescription = description }
            .clickable(onClick = onClick),
        contentAlignment = Alignment.Center,
    ) { content() }
}

@Composable
private fun LastPhotoThumb(uri: Uri?, onOpen: (Uri) -> Unit) {
    val context = LocalContext.current
    var thumb by remember { mutableStateOf<ImageBitmap?>(null) }
    LaunchedEffect(uri) {
        thumb = if (uri == null) null else withContext(Dispatchers.IO) { loadThumbnail(context, uri) }
    }
    val description = stringResource(R.string.cd_last_photo)
    Box(
        Modifier
            .size(56.dp)
            .clip(CircleShape)
            .background(Color.White.copy(alpha = 0.15f))
            .border(2.dp, Color.White.copy(alpha = 0.6f), CircleShape)
            .semantics { contentDescription = description }
            .clickable(enabled = uri != null) { uri?.let(onOpen) },
    ) {
        thumb?.let {
            Image(it, contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
        }
    }
}

private fun loadThumbnail(context: Context, uri: Uri): ImageBitmap? = runCatching {
    val bitmap: Bitmap? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        context.contentResolver.loadThumbnail(uri, Size(192, 192), null)
    } else {
        context.contentResolver.openInputStream(uri)?.use {
            BitmapFactory.decodeStream(it, null, BitmapFactory.Options().apply { inSampleSize = 16 })
        }
    }
    bitmap?.asImageBitmap()
}.getOrNull()

private fun Context.openPhoto(uri: Uri): Boolean = try {
    startActivity(
        Intent(Intent.ACTION_VIEW)
            .setDataAndType(uri, "image/jpeg")
            .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION),
    )
    true
} catch (e: ActivityNotFoundException) {
    false
}
