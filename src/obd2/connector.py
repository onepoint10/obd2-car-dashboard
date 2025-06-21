"""
OBD2 Connector - Handles real OBD2 device communication
"""

import asyncio
import threading
from typing import Optional, Dict, Any
import bluetooth
import obd
from bleak import BleakScanner, BleakClient
from kivy.logger import Logger

class OBD2Manager:
    """Manages OBD2 device connections and data retrieval"""
    
    def __init__(self):
        self.connection: Optional[obd.OBD] = None
        self.is_scanning = False
        self.available_devices = []
        self.current_data = {
            'speed': 0,
            'rpm': 0,
            'coolant_temp': 0,
            'engine_load': 0,
            'fuel_level': 0,
            'connected': False
        }
        
    def scan_bluetooth_devices(self) -> list:
        """Scan for available Bluetooth OBD2 devices"""
        devices = []
        try:
            self.is_scanning = True
            Logger.info("OBD2Manager: Scanning for Bluetooth devices...")
            
            # Classic Bluetooth scan
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in nearby_devices:
                if any(keyword in name.lower() for keyword in ['obd', 'elm', 'obdii']):
                    devices.append({
                        'name': name,
                        'address': addr,
                        'type': 'classic'
                    })
            
            # BLE scan (async)
            asyncio.run(self._scan_ble_devices(devices))
            
        except Exception as e:
            Logger.error(f"OBD2Manager: Bluetooth scan error: {e}")
        finally:
            self.is_scanning = False
            
        self.available_devices = devices
        return devices
    
    async def _scan_ble_devices(self, devices: list):
        """Scan for BLE OBD2 devices"""
        try:
            ble_devices = await BleakScanner.discover()
            for device in ble_devices:
                if device.name and any(keyword in device.name.lower() 
                                     for keyword in ['obd', 'elm', 'obdii']):
                    devices.append({
                        'name': device.name,
                        'address': device.address,
                        'type': 'ble'
                    })
        except Exception as e:
            Logger.error(f"OBD2Manager: BLE scan error: {e}")
    
    def connect_device(self, device_info: Dict[str, str]) -> bool:
        """Connect to an OBD2 device"""
        try:
            Logger.info(f"OBD2Manager: Connecting to {device_info['name']}")
            
            if device_info['type'] == 'classic':
                # Connect via classic Bluetooth
                connection_string = f"rfcomm://{device_info['address']}"
            else:
                # Connect via BLE
                connection_string = f"ble://{device_info['address']}"
            
            self.connection = obd.OBD(connection_string)
            
            if self.connection.is_connected():
                self.current_data['connected'] = True
                Logger.info("OBD2Manager: Successfully connected")
                return True
            else:
                Logger.error("OBD2Manager: Failed to establish connection")
                return False
                
        except Exception as e:
            Logger.error(f"OBD2Manager: Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from OBD2 device"""
        if self.connection:
            try:
                self.connection.close()
                self.current_data['connected'] = False
                Logger.info("OBD2Manager: Disconnected")
            except Exception as e:
                Logger.error(f"OBD2Manager: Disconnect error: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to OBD2 device"""
        return self.connection and self.connection.is_connected()
    
    def read_data(self) -> Dict[str, Any]:
        """Read current data from OBD2 device"""
        if not self.is_connected():
            return self.current_data
        
        try:
            # Read various OBD2 parameters
            commands = {
                'speed': obd.commands.SPEED,
                'rpm': obd.commands.RPM,
                'coolant_temp': obd.commands.COOLANT_TEMP,
                'engine_load': obd.commands.ENGINE_LOAD,
                'fuel_level': obd.commands.FUEL_LEVEL
            }
            
            for key, command in commands.items():
                response = self.connection.query(command)
                if response.value is not None:
                    if hasattr(response.value, 'magnitude'):
                        self.current_data[key] = response.value.magnitude
                    else:
                        self.current_data[key] = float(response.value)
                        
        except Exception as e:
            Logger.error(f"OBD2Manager: Data read error: {e}")
        
        return self.current_data
