#!/usr/bin/env python3
"""
OBD2 Car Dashboard - Main Application Entry Point
Multiplatform OBD2 diagnostic tool with car-friendly UI
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from kivy.app import App
from kivy.config import Config
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

from ui.dashboard import DashboardScreen
from obd2.connector import OBD2Manager
from obd2.emulator import OBD2Emulator
from utils.config import AppConfig

# Configure Kivy for multiplatform
if platform == 'android':
    Config.set('graphics', 'width', '0')  # Use full screen on Android
    Config.set('graphics', 'height', '0')
else:
    Config.set('graphics', 'width', '1024')
    Config.set('graphics', 'height', '768')
    Config.set('graphics', 'minimum_width', '800')
    Config.set('graphics', 'minimum_height', '600')

Config.set('graphics', 'resizable', '1')

class OBD2DashboardApp(MDApp):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "OBD2 Car Dashboard"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Orange"
        
        # Initialize components
        self.config = AppConfig()
        self.obd2_manager = OBD2Manager()
        self.emulator = OBD2Emulator()
        self.dashboard = None
        
    def build(self):
        """Build the application UI"""
        self.dashboard = DashboardScreen(
            obd2_manager=self.obd2_manager,
            emulator=self.emulator,
            config=self.config
        )
        
        # Schedule periodic updates
        Clock.schedule_interval(self.update_dashboard, 1/10)  # 10 FPS for data updates
        
        return self.dashboard
    
    def update_dashboard(self, dt):
        """Update dashboard data"""
        if self.dashboard:
            self.dashboard.update_data()
    
    def on_start(self):
        """Called when app starts"""
        Logger.info("OBD2Dashboard: Application started")
        
        # Start emulator if no real device connected
        if not self.obd2_manager.is_connected():
            self.emulator.start()
            Logger.info("OBD2Dashboard: Started emulator mode")
    
    def on_stop(self):
        """Called when app stops"""
        Logger.info("OBD2Dashboard: Application stopping")
        self.obd2_manager.disconnect()
        self.emulator.stop()

def main():
    """Main entry point"""
    OBD2DashboardApp().run()

if __name__ == '__main__':
    main()
