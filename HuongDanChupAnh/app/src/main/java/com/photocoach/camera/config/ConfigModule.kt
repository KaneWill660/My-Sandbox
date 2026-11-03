package com.photocoach.camera.config

import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object ConfigModule {
    // M5 (F9): thay bằng ngưỡng đọc từ cấu hình JSON (override > URL đã cache > assets).
    @Provides
    @Singleton
    fun provideThresholds(): CoachThresholds = CoachThresholds()
}
