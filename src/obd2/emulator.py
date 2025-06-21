"""
OBD2 Emulator - Simulates OBD2 data for testing
"""

import random
import time
import threading
from typing import Dict, Any
from kivy.logger import Logger
from kivy.clock import Clock

class OBD2Emulator:
    """Emulates OBD2 device data for testing purposes"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.data = {
            'speed': 0,
            'rpm': 800,
            'coolant_temp': 85,
            'engine_load': 15,
            'fuel_level': 75,
            'connected': True
        }
        
        # Simulation parameters
        self.speed_target = 0
        self.rpm_target = 800
        self.driving_mode = 'idle'  # idle, city, highway
        
    def start(self):
        """Start the emulator"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._simulation_loop)
            self.thread.daemon = True
            self.thread.start()
            Logger.info("OBD2Emulator: Started")
    
    def stop(self):
        """Stop the emulator"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        Logger.info("OBD2Emulator: Stopped")
    
    def _simulation_loop(self):
        """Main simulation loop"""
        while self.is_running:
            self._update_driving_scenario()
            self._simulate_realistic_data()
            time.sleep(0.1)  # 10Hz update rate
    
    def _update_driving_scenario(self):
        """Update driving scenario randomly"""
        if random.random() < 0.01:  # 1% chance per update
            scenarios = ['idle', 'city', 'highway', 'acceleration', 'deceleration']
            self.driving_mode = random.choice(scenarios)
            
            if self.driving_mode == 'idle':
                self.speed_target = 0
                self.rpm_target = 800
            elif self.driving_mode == 'city':
                self.speed_target = random.randint(20, 50)
                self.rpm_target = random.randint(1500, 2500)
            elif self.driving_mode == 'highway':
                self.speed_target = random.randint(60, 120)
                self.rpm_target = random.randint(2000, 3000)
            elif self.driving_mode == 'acceleration':
                self.speed_target = min(self.data['speed'] + 20, 140)
                self.rpm_target = random.randint(3000, 5000)
            elif self.driving_mode == 'deceleration':
                self.speed_target = max(self.data['speed'] - 15, 0)
                self.rpm_target = random.randint(1000, 2000)
    
    def _simulate_realistic_data(self):
        """Simulate realistic OBD2 data"""
        # Smooth transitions for speed and RPM
        speed_diff = self.speed_target - self.data['speed']
        self.data['speed'] += speed_diff * 0.05  # Gradual change
        
        rpm_diff = self.rpm_target - self.data['rpm']
        self.data['rpm'] += rpm_diff * 0.1
        
        # Add some noise
        self.data['speed'] += random.uniform(-1, 1)
        self.data['rpm'] += random.uniform(-50, 50)
        
        # Ensure realistic bounds
        self.data['speed'] = max(0, min(200, self.data['speed']))
        self.data['rpm'] = max(600, min(6000, self.data['rpm']))
        
        # Engine load based on speed and RPM
        base_load = (self.data['speed'] / 100) * 50
        rpm_load = max(0, (self.data['rpm'] - 800) / 4000) * 30
        self.data['engine_load'] = min(100, base_load + rpm_load + random.uniform(-5, 5))
        
        # Coolant temperature (slowly increases with load)
        target_temp = 85 + (self.data['engine_load'] / 100) * 15
        temp_diff = target_temp - self.data['coolant_temp']
        self.data['coolant_temp'] += temp_diff * 0.01
        
        # Fuel level (slowly decreases)
        if random.random() < 0.001:  # Very slow fuel consumption
            self.data['fuel_level'] = max(0, self.data['fuel_level'] - 0.1)
    
    def get_data(self) -> Dict[str, Any]:
        """Get current emulated data"""
        return self.data.copy()
    
    def set_scenario(self, scenario: str):
        """Manually set driving scenario"""
        self.driving_mode = scenario
        self._update_driving_scenario()
