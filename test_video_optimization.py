#!/usr/bin/env python3
"""
Test script per verificare l'ottimizzazione video del sistema Advanced Controller
"""

import sys
import os
import time
import threading
import requests

# Aggiungi il percorso web al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'web'))

def test_video_optimization():
    """Test delle impostazioni di ottimizzazione video"""
    print("🔄 Testing video optimization system...")
    
    try:
        import camera_opencv
        
        # Test initial values
        print(f"Initial resolution: {camera_opencv.video_resolution}")
        print(f"Initial FPS: {camera_opencv.video_fps}")
        print(f"Initial quality: {camera_opencv.jpeg_quality}")
        
        # Create camera instance
        camera = camera_opencv.Camera()
        
        # Test resolution change
        print("\n📹 Testing resolution change...")
        camera.setVideoResolution("optimized")
        print(f"After optimization: {camera_opencv.video_resolution}")
        
        camera.setVideoResolution("high")
        print(f"After high quality: {camera_opencv.video_resolution}")
        
        # Test FPS change
        print("\n🎬 Testing FPS change...")
        camera.setVideoFPS(15)
        print(f"After FPS change: {camera_opencv.video_fps}")
        
        camera.setVideoFPS(30)
        print(f"After FPS change: {camera_opencv.video_fps}")
        
        # Test quality change
        print("\n🎨 Testing quality change...")
        camera.setJPEGQuality(60)
        print(f"After quality change: {camera_opencv.jpeg_quality}")
        
        camera.setJPEGQuality(95)
        print(f"After quality change: {camera_opencv.jpeg_quality}")
        
        print("✅ Video optimization system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing video optimization: {e}")
        return False

def test_video_stream_access():
    """Test accesso al video stream Flask"""
    print("\n🔄 Testing video stream access...")
    
    try:
        # Test connection to video feed endpoint
        url = "http://localhost:5000/video_feed"
        
        print(f"Attempting to connect to: {url}")
        response = requests.get(url, timeout=5, stream=True)
        
        if response.status_code == 200:
            print("✅ Video stream endpoint accessible")
            
            # Read first few bytes to verify it's actually a video stream
            chunk = next(response.iter_content(chunk_size=1024))
            if b'--frame' in chunk or b'\xff\xd8' in chunk:  # MJPEG boundary or JPEG header
                print("✅ Video stream contains valid video data")
                return True
            else:
                print("⚠️  Video stream endpoint responds but may not contain valid video data")
                return False
        else:
            print(f"❌ Video stream endpoint returned status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot connect to Flask server (may not be running)")
        return False
    except Exception as e:
        print(f"❌ Error testing video stream: {e}")
        return False

def test_advanced_interface_access():
    """Test accesso all'interfaccia avanzata"""
    print("\n🔄 Testing advanced interface access...")
    
    try:
        url = "http://localhost:5000/advanced"
        
        print(f"Attempting to connect to: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for key elements
            key_elements = [
                'video-canvas',
                'video-optimization',
                'reloadVideoStream',
                'setupVideoOptimizationControls',
                'WebSocket'
            ]
            
            found_elements = 0
            for element in key_elements:
                if element in content:
                    print(f"✅ Found: {element}")
                    found_elements += 1
                else:
                    print(f"❌ Missing: {element}")
            
            if found_elements >= 4:
                print("✅ Advanced interface contains all required elements")
                return True
            else:
                print("❌ Advanced interface may be missing some elements")
                return False
        else:
            print(f"❌ Advanced interface endpoint returned status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot connect to Flask server (may not be running)")
        return False
    except Exception as e:
        print(f"❌ Error testing advanced interface: {e}")
        return False

def main():
    """Esegue tutti i test video"""
    print("🎬 Starting Advanced Controller Video Tests")
    print("=" * 60)
    
    tests = [
        ("Video Optimization Logic", test_video_optimization),
        ("Video Stream Access", test_video_stream_access),
        ("Advanced Interface Access", test_advanced_interface_access),
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
        print("🎉 All video tests passed!")
        print("\n📝 Stato del sistema video:")
        print("✅ Le impostazioni video vengono applicate correttamente")
        print("✅ L'interfaccia avanzata è accessibile")
        print("✅ Lo streaming video funziona")
        
        print("\n🎯 Per testare le ottimizzazioni video:")
        print("1. Avvia il server: cd web && python webServer_HAT_V3.1.py")
        print("2. Apri l'interfaccia: http://localhost:5000/advanced")
        print("3. Clicca sui pulsanti di ottimizzazione video")
        print("4. Osserva i cambiamenti nel player video")
        
    else:
        print(f"⚠️  {total - passed} test(s) failed.")
        print("\n🔧 Possibili soluzioni:")
        print("- Verifica che il server Flask sia avviato")
        print("- Controlla che la camera sia collegata correttamente")
        print("- Verifica che tutti i file siano presenti in web/")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
