#!/usr/bin/env python3
# File name   : ultrasonic_monitor.py
# Description : Continuous ultrasonic sensor monitoring
# Website     : www.adeept.com
# Author      : Advanced Controller
# Date        : 2025/08/17

import threading
import time
import ultra
import json

class UltrasonicMonitor(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = False
        self.continuous = False
        self.update_rate = 10  # Hz
        self.last_distance = 0
        self.callback = None
        self._stop_event = threading.Event()

    def set_callback(self, callback):
        """Set callback function to receive sensor data"""
        self.callback = callback

    def start_continuous(self, rate=10):
        """Start continuous sensor reading"""
        self.update_rate = rate
        self.continuous = True
        if not self.running:
            self.running = True
            self.start()

    def stop_continuous(self):
        """Stop continuous sensor reading"""
        self.continuous = False

    def get_single_reading(self):
        """Get single sensor reading"""
        try:
            distance = ultra.checkdist()
            self.last_distance = distance
            return distance
        except Exception as e:
            print(f"Sensor reading error: {e}")
            return -1

    def run(self):
        """Main thread loop"""
        while self.running and not self._stop_event.is_set():
            if self.continuous:
                try:
                    distance = self.get_single_reading()
                    
                    if self.callback and distance >= 0:
                        # Send sensor data to callback
                        sensor_data = {
                            'type': 'ultrasonic',
                            'distance': round(distance, 2),
                            'timestamp': time.time()
                        }
                        self.callback(sensor_data)
                    
                    # Sleep based on update rate
                    sleep_time = 1.0 / self.update_rate
                    time.sleep(sleep_time)
                    
                except Exception as e:
                    print(f"Ultrasonic monitor error: {e}")
                    time.sleep(1)
            else:
                # Wait for continuous mode to be enabled
                time.sleep(0.1)

    def stop(self):
        """Stop the monitor thread"""
        self.running = False
        self.continuous = False
        self._stop_event.set()

# Global instance
ultrasonic_monitor = UltrasonicMonitor()

def start_ultrasonic_monitor(callback=None):
    """Start the ultrasonic monitor with callback"""
    if callback:
        ultrasonic_monitor.set_callback(callback)
    
    if not ultrasonic_monitor.running:
        ultrasonic_monitor.start()

def get_ultrasonic_monitor():
    """Get the global ultrasonic monitor instance"""
    return ultrasonic_monitor

if __name__ == '__main__':
    def test_callback(data):
        print(f"Distance: {data['distance']} cm")
    
    # Test the monitor
    monitor = UltrasonicMonitor()
    monitor.set_callback(test_callback)
    monitor.start_continuous(rate=5)
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()
