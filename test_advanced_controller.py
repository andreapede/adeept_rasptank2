#!/usr/bin/env python3
"""
Test script per verificare l'integrazione completa del sistema Advanced Controller
"""

import sys
import os
import time
import json

# Aggiungi il percorso web al PYTHONPATH per importare i moduli
sys.path.append(os.path.join(os.path.dirname(__file__), 'web'))

def test_imports():
    """Test che tutti i moduli necessari siano importabili"""
    print("🔄 Testing imports...")
    
    try:
        import ultra
        print("✅ ultra.py imported successfully")
    except ImportError as e:
        print(f"❌ Error importing ultra: {e}")
        return False
    
    try:
        import ultrasonic_monitor
        print("✅ ultrasonic_monitor.py imported successfully")
    except ImportError as e:
        print(f"❌ Error importing ultrasonic_monitor: {e}")
        return False
    
    try:
        import functions
        print("✅ functions.py imported successfully")
    except ImportError as e:
        print(f"❌ Error importing functions: {e}")
        return False
    
    return True

def test_ultrasonic_sensor():
    """Test lettura del sensore ultrasonico"""
    print("\n🔄 Testing ultrasonic sensor...")
    
    try:
        import ultra
        
        # Test singola lettura
        distance = ultra.checkdist()
        print(f"✅ Sensor reading: {distance:.2f} cm")
        
        if distance < 0:
            print("⚠️  Warning: Negative distance reading")
        elif distance > 200:
            print("⚠️  Warning: Distance reading seems too high")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing sensor: {e}")
        return False

def test_continuous_monitoring():
    """Test sistema di monitoraggio continuo"""
    print("\n🔄 Testing continuous monitoring...")
    
    try:
        import ultrasonic_monitor
        
        # Crea monitor
        monitor = ultrasonic_monitor.UltrasonicMonitor(update_rate=2.0)
        
        # Test callback
        readings = []
        def test_callback(data):
            readings.append(data)
            print(f"📊 Sensor data: {data}")
        
        # Avvia monitoraggio per 5 secondi
        monitor.start_monitoring(callback=test_callback)
        print("✅ Monitoring started...")
        
        time.sleep(5)
        
        monitor.stop_monitoring()
        print("✅ Monitoring stopped")
        
        if len(readings) > 0:
            print(f"✅ Received {len(readings)} readings")
            return True
        else:
            print("❌ No readings received")
            return False
            
    except Exception as e:
        print(f"❌ Error testing continuous monitoring: {e}")
        return False

def test_webserver_integration():
    """Test integrazione con webServer"""
    print("\n🔄 Testing webServer integration...")
    
    # Verifica che il file webServer sia modificato correttamente
    web_server_path = os.path.join(os.path.dirname(__file__), 'web', 'webServer_HAT_V3.1.py')
    
    if not os.path.exists(web_server_path):
        print(f"❌ webServer file not found: {web_server_path}")
        return False
    
    with open(web_server_path, 'r') as f:
        content = f.read()
    
    # Verifica che gli import siano presenti
    if 'import ultrasonic_monitor' in content:
        print("✅ ultrasonic_monitor import found")
    else:
        print("❌ ultrasonic_monitor import missing")
        return False
    
    if 'import ultra' in content:
        print("✅ ultra import found")
    else:
        print("❌ ultra import missing")
        return False
    
    # Verifica che i comandi sensori siano presenti
    sensor_commands = ['sensorRead', 'sensorStart', 'sensorStop', 'sensorRate']
    for cmd in sensor_commands:
        if cmd in content:
            print(f"✅ {cmd} command found")
        else:
            print(f"❌ {cmd} command missing")
            return False
    
    return True

def test_flask_integration():
    """Test integrazione con Flask app"""
    print("\n🔄 Testing Flask integration...")
    
    app_path = os.path.join(os.path.dirname(__file__), 'web', 'app.py')
    
    if not os.path.exists(app_path):
        print(f"❌ app.py file not found: {app_path}")
        return False
    
    with open(app_path, 'r') as f:
        content = f.read()
    
    # Verifica rotta per advanced controller
    if '/advanced' in content and 'advanced_controller.html' in content:
        print("✅ Advanced controller route found")
        return True
    else:
        print("❌ Advanced controller route missing")
        return False

def test_advanced_interface():
    """Test presenza interfaccia avanzata"""
    print("\n🔄 Testing advanced interface...")
    
    interface_path = os.path.join(os.path.dirname(__file__), 'web', 'advanced_controller.html')
    
    if not os.path.exists(interface_path):
        print(f"❌ advanced_controller.html not found: {interface_path}")
        return False
    
    with open(interface_path, 'r') as f:
        content = f.read()
    
    # Verifica elementi chiave dell'interfaccia
    key_elements = [
        'WebSocket',
        'sensorRead',
        'chart',
        'video_feed',
        'movement controls'
    ]
    
    found_elements = 0
    for element in key_elements:
        if element.lower() in content.lower():
            print(f"✅ {element} found in interface")
            found_elements += 1
        else:
            print(f"⚠️  {element} not found in interface")
    
    if found_elements >= 3:
        print("✅ Advanced interface appears complete")
        return True
    else:
        print("❌ Advanced interface may be incomplete")
        return False

def main():
    """Esegue tutti i test"""
    print("🚀 Starting Advanced Controller Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Ultrasonic Sensor Test", test_ultrasonic_sensor),
        ("Continuous Monitoring Test", test_continuous_monitoring),
        ("WebServer Integration Test", test_webserver_integration),
        ("Flask Integration Test", test_flask_integration),
        ("Advanced Interface Test", test_advanced_interface),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} CRASHED: {e}")
    
    print("\n" + "="*60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Sistema pronto per l'uso.")
        print("\n📝 Prossimi passi:")
        print("1. Avvia il server: cd web && python webServer_HAT_V3.1.py")
        print("2. Accedi all'interfaccia: http://[IP_RASPBERRY]:5000/advanced")
        print("3. Testa il monitoraggio continuo dei sensori")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Controllare i messaggi di errore.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
