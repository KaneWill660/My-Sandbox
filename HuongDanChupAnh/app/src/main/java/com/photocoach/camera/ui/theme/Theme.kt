package com.photocoach.camera.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val CoachGreen = Color(0xFF4CD964)
val CoachAmber = Color(0xFFFFC94D)

private val DarkColors = darkColorScheme(
    primary = CoachAmber,
    onPrimary = Color.Black,
    secondary = CoachGreen,
    background = Color.Black,
    surface = Color(0xFF121212),
)

@Composable
fun PhotoCoachTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = DarkColors, content = content)
}
