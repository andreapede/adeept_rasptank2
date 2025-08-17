#!/usr/bin/env python
# File name   : battery_monitor.py
# Description : Battery level monitoring for RaspTank
# Author      : Based on 08_Battrey_level.py example

import time
import board
import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn

class BatteryMonitor:
    def __init__(self):
        self.i2c = None
        self.adc = None
        self.chan0 = None
        self.initialized = False
        self.last_voltage = 0.0
        self.init_adc()
    
    def init_adc(self):
        """Initialize the ADC for battery monitoring"""
        try:
            self.i2c = board.I2C()
            self.adc = ADC.ADS7830(self.i2c, 0x48)  # default is 0x48
            self.chan0 = AnalogIn(self.adc, 0)  # Battery voltage on channel 0
            self.initialized = True
            print("Battery monitor initialized successfully")
        except Exception as e:
            print(f"Failed to initialize battery monitor: {e}")
            self.initialized = False
    
    def read_voltage(self):
        """Read battery voltage from ADC"""
        if not self.initialized:
            return self.last_voltage
        
        try:
            # Convert ADC reading to voltage (2x 18650 batteries = max 8.4V)
            voltage = self.chan0.value / 65535 * 8.4
            self.last_voltage = voltage
            return voltage
        except Exception as e:
            print(f"Error reading battery voltage: {e}")
            return self.last_voltage
    
    def get_battery_percentage(self, voltage):
        """Convert voltage to percentage for Li-ion batteries"""
        # Voltage curve for 2x 18650 Li-ion batteries in series (7.4V nominal)
        # Full: 8.4V (4.2V per cell)
        # Empty: 6.0V (3.0V per cell - safe minimum)
        if voltage >= 8.4:
            return 100
        elif voltage <= 6.0:
            return 0
        else:
            # Simple linear interpolation
            # Could be improved with actual Li-ion discharge curve
            return round(((voltage - 6.0) / (8.4 - 6.0)) * 100)
    
    def get_battery_status(self):
        """Get complete battery status"""
        voltage = self.read_voltage()
        percentage = self.get_battery_percentage(voltage)
        
        return {
            'voltage': round(voltage, 2),
            'percentage': percentage,
            'status': self.get_status_text(percentage),
            'initialized': self.initialized
        }
    
    def get_status_text(self, percentage):
        """Get battery status text based on percentage"""
        if percentage > 75:
            return 'Good'
        elif percentage > 50:
            return 'Fair'
        elif percentage > 25:
            return 'Low'
        elif percentage > 10:
            return 'Very Low'
        else:
            return 'Critical'

# Global battery monitor instance
battery_monitor = None

def get_battery_monitor():
    """Get or create battery monitor instance"""
    global battery_monitor
    if battery_monitor is None:
        battery_monitor = BatteryMonitor()
    return battery_monitor

if __name__ == "__main__":
    # Test the battery monitor
    monitor = BatteryMonitor()
    
    while True:
        status = monitor.get_battery_status()
        print(f"Battery: {status['voltage']}V ({status['percentage']}%) - {status['status']}")
        time.sleep(2)
