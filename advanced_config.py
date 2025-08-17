#!/usr/bin/env python3
"""
Advanced Controller Configuration
Configurazione centralizzata per il sistema Advanced Controller
"""

# Configurazione Sensori Ultrasonici
ULTRASONIC_CONFIG = {
    'default_update_rate': 0.2,        # Letture al secondo (5 Hz)
    'fast_update_rate': 0.1,           # Modalità veloce (10 Hz)
    'slow_update_rate': 0.5,           # Modalità lenta (2 Hz)
    'max_distance': 200,               # Distanza massima in cm
    'min_distance': 2,                 # Distanza minima in cm
    'warning_distance': 30,            # Soglia di avvertimento in cm
    'critical_distance': 15,           # Soglia critica in cm
}

# Configurazione Video
VIDEO_CONFIG = {
    'default_resolution': {
        'width': 640,
        'height': 480
    },
    'high_resolution': {
        'width': 1024,
        'height': 768
    },
    'optimized_resolution': {
        'width': 320,
        'height': 240
    },
    'default_fps': 20,
    'high_fps': 30,
    'optimized_fps': 15,
    'default_quality': 80,
    'high_quality': 95,
    'optimized_quality': 60,
}

# Configurazione Movimento
MOVEMENT_CONFIG = {
    'default_speed': 50,               # Velocità predefinita (0-100)
    'max_speed': 100,                  # Velocità massima
    'min_speed': 10,                   # Velocità minima
    'servo_step': 5,                   # Step per movimento servo
    'servo_min': 0,                    # Posizione minima servo
    'servo_max': 180,                  # Posizione massima servo
}

# Configurazione WebSocket
WEBSOCKET_CONFIG = {
    'port': 8888,                      # Porta WebSocket
    'host': '0.0.0.0',                 # Host WebSocket
    'max_clients': 10,                 # Max client connessi
    'heartbeat_interval': 30,          # Intervallo heartbeat
}

# Configurazione Flask
FLASK_CONFIG = {
    'port': 5000,                      # Porta Flask
    'host': '0.0.0.0',                 # Host Flask
    'debug': False,                    # Modalità debug
}

# Configurazione GPIO
GPIO_CONFIG = {
    'ultrasonic_trigger': 23,          # Pin trigger sensore
    'ultrasonic_echo': 24,             # Pin echo sensore
    'motor_pins': {
        'left_forward': 12,
        'left_backward': 13,
        'right_forward': 20,
        'right_backward': 21,
    }
}

# Configurazione Interfaccia
UI_CONFIG = {
    'chart_max_points': 50,            # Max punti nel grafico
    'chart_update_interval': 200,      # Intervallo update chart (ms)
    'sensor_display_precision': 2,     # Decimali per distanza
    'auto_reconnect': True,            # Riconnessione automatica WebSocket
    'reconnect_interval': 3000,        # Intervallo riconnessione (ms)
}

# Messaggi di sistema
SYSTEM_MESSAGES = {
    'sensor_error': 'Errore lettura sensore ultrasonico',
    'websocket_connected': 'WebSocket connesso',
    'websocket_disconnected': 'WebSocket disconnesso',
    'monitoring_started': 'Monitoraggio continuo avviato',
    'monitoring_stopped': 'Monitoraggio continuo fermato',
    'video_optimized': 'Video ottimizzato per rete lenta',
    'video_high_quality': 'Video impostato su alta qualità',
}

def get_preset_config(preset_name):
    """
    Ottiene configurazione preset per diversi scenari d'uso
    
    Args:
        preset_name (str): Nome del preset ('indoor', 'outdoor', 'demo', 'performance')
    
    Returns:
        dict: Configurazione ottimizzata per il preset
    """
    
    presets = {
        'indoor': {
            'sensor_rate': ULTRASONIC_CONFIG['default_update_rate'],
            'video_resolution': VIDEO_CONFIG['default_resolution'],
            'video_fps': VIDEO_CONFIG['default_fps'],
            'video_quality': VIDEO_CONFIG['default_quality'],
            'movement_speed': 40,
        },
        'outdoor': {
            'sensor_rate': ULTRASONIC_CONFIG['fast_update_rate'],
            'video_resolution': VIDEO_CONFIG['high_resolution'],
            'video_fps': VIDEO_CONFIG['high_fps'],
            'video_quality': VIDEO_CONFIG['high_quality'],
            'movement_speed': 70,
        },
        'demo': {
            'sensor_rate': ULTRASONIC_CONFIG['slow_update_rate'],
            'video_resolution': VIDEO_CONFIG['optimized_resolution'],
            'video_fps': VIDEO_CONFIG['optimized_fps'],
            'video_quality': VIDEO_CONFIG['optimized_quality'],
            'movement_speed': 30,
        },
        'performance': {
            'sensor_rate': ULTRASONIC_CONFIG['fast_update_rate'],
            'video_resolution': VIDEO_CONFIG['optimized_resolution'],
            'video_fps': VIDEO_CONFIG['optimized_fps'],
            'video_quality': VIDEO_CONFIG['optimized_quality'],
            'movement_speed': 80,
        }
    }
    
    return presets.get(preset_name, presets['indoor'])

def validate_config():
    """
    Valida la configurazione del sistema
    
    Returns:
        tuple: (is_valid, errors_list)
    """
    errors = []
    
    # Valida configurazione sensori
    if ULTRASONIC_CONFIG['max_distance'] <= ULTRASONIC_CONFIG['min_distance']:
        errors.append("Max distance deve essere maggiore di min distance")
    
    if ULTRASONIC_CONFIG['warning_distance'] <= ULTRASONIC_CONFIG['critical_distance']:
        errors.append("Warning distance deve essere maggiore di critical distance")
    
    # Valida configurazione video
    if VIDEO_CONFIG['default_fps'] <= 0:
        errors.append("FPS deve essere maggiore di 0")
    
    if not (0 <= VIDEO_CONFIG['default_quality'] <= 100):
        errors.append("Qualità video deve essere tra 0 e 100")
    
    # Valida configurazione movimento
    if not (0 <= MOVEMENT_CONFIG['default_speed'] <= 100):
        errors.append("Velocità deve essere tra 0 e 100")
    
    return len(errors) == 0, errors

def print_current_config():
    """Stampa la configurazione corrente del sistema"""
    print("🔧 Advanced Controller Configuration")
    print("=" * 50)
    
    print("\n📡 Sensori Ultrasonici:")
    for key, value in ULTRASONIC_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n📹 Video:")
    for key, value in VIDEO_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n🎮 Movimento:")
    for key, value in MOVEMENT_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n🌐 WebSocket:")
    for key, value in WEBSOCKET_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\n🔗 Flask:")
    for key, value in FLASK_CONFIG.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    # Test configurazione
    print_current_config()
    
    is_valid, errors = validate_config()
    if is_valid:
        print("\n✅ Configurazione valida")
    else:
        print("\n❌ Errori di configurazione:")
        for error in errors:
            print(f"  - {error}")
    
    print("\n📋 Preset disponibili:")
    for preset in ['indoor', 'outdoor', 'demo', 'performance']:
        config = get_preset_config(preset)
        print(f"  {preset}: speed={config['movement_speed']}, "
              f"sensor_rate={config['sensor_rate']}, "
              f"video_fps={config['video_fps']}")
