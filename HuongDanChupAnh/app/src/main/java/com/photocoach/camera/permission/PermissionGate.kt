package com.photocoach.camera.permission

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.PhotoCamera
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import com.photocoach.camera.R

/** Camera luôn cần; Android 8–9 cần thêm quyền ghi bộ nhớ để lưu ảnh vào MediaStore. */
private val requiredPermissions: Array<String> =
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
        arrayOf(Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE)
    } else {
        arrayOf(Manifest.permission.CAMERA)
    }

private fun Context.allGranted() = requiredPermissions.all {
    ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
}

/**
 * F1.3: chỉ hiện [content] khi đã có đủ quyền. Giải thích lý do trước khi xin,
 * và hướng người dùng sang Cài đặt khi quyền bị từ chối vĩnh viễn.
 */
@Composable
fun PermissionGate(content: @Composable () -> Unit) {
    val context = LocalContext.current
    var granted by rememberSaveable { mutableStateOf(context.allGranted()) }
    var askedOnce by rememberSaveable { mutableStateOf(false) }
    var deniedForever by rememberSaveable { mutableStateOf(false) }

    val launcher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions(),
    ) { _ ->
        granted = context.allGranted()
        askedOnce = true
        // Sau khi đã xin mà hệ thống không còn cho hiện lời giải thích => đã chọn "Không hỏi lại".
        val activity = context.findActivity()
        deniedForever = !granted && activity != null && requiredPermissions.none {
            ContextCompat.checkSelfPermission(context, it) != PackageManager.PERMISSION_GRANTED &&
                activity.shouldShowRequestPermissionRationale(it)
        }
    }

    // Người dùng có thể bật quyền trong Cài đặt rồi quay lại app.
    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) {
        granted = context.allGranted()
        if (granted) deniedForever = false
    }

    if (granted) {
        content()
        return
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .safeDrawingPadding()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Icon(Icons.Outlined.PhotoCamera, contentDescription = null, tint = Color.White)
        Spacer(Modifier.height(16.dp))
        Text(
            stringResource(R.string.perm_title),
            style = MaterialTheme.typography.titleLarge,
            color = Color.White,
        )
        Spacer(Modifier.height(12.dp))
        Text(
            stringResource(if (deniedForever) R.string.perm_denied_forever else R.string.perm_body),
            color = Color.White.copy(alpha = 0.85f),
            textAlign = TextAlign.Center,
        )
        if (!deniedForever && requiredPermissions.size > 1) {
            Spacer(Modifier.height(8.dp))
            Text(
                stringResource(R.string.perm_body_storage),
                color = Color.White.copy(alpha = 0.7f),
                textAlign = TextAlign.Center,
                style = MaterialTheme.typography.bodySmall,
            )
        }
        Spacer(Modifier.height(24.dp))
        if (deniedForever) {
            Button(onClick = { context.openAppSettings() }) {
                Text(stringResource(R.string.perm_open_settings))
            }
        } else {
            Button(onClick = { launcher.launch(requiredPermissions) }) {
                Text(stringResource(R.string.perm_grant))
            }
        }
    }

    // Lần đầu mở app: xin quyền ngay sau khi hiện lời giải thích.
    if (!askedOnce && !deniedForever) {
        LaunchedEffect(Unit) { launcher.launch(requiredPermissions) }
    }
}

fun Context.findActivity(): Activity? {
    var c = this
    while (c is ContextWrapper) {
        if (c is Activity) return c
        c = c.baseContext
    }
    return null
}

private fun Context.openAppSettings() {
    val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.fromParts("package", packageName, null))
        .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    startActivity(intent)
}
