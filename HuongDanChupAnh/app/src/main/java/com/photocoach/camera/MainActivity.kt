package com.photocoach.camera

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.photocoach.camera.camera.CameraScreen
import com.photocoach.camera.permission.PermissionGate
import com.photocoach.camera.ui.theme.PhotoCoachTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PhotoCoachTheme {
                PermissionGate {
                    CameraScreen()
                }
            }
        }
    }
}
