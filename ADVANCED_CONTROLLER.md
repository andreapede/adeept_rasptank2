# Advanced Controller Interface

## Panoramica
L'interfaccia **Advanced Controller** è una sostituzione completa dell'interfaccia originale del RaspTank che fornisce controllo completo del robot con monitoraggio continuo dei sensori ultrasonici.

## Caratteristiche Principali

### 🎮 Controllo Robot
- **Controllo Movimento**: Controlli direzionali completi (avanti, indietro, sinistra, destra, rotazioni)
- **Controllo Velocità**: Slider per impostare la velocità del movimento
- **Controllo Servo**: Controllo della camera con servo motori (su/giù, sinistra/destra)

### 📡 Monitoraggio Sensori
- **Lettura Continua**: Monitoraggio in tempo reale della distanza dagli ostacoli
- **Grafici Storici**: Visualizzazione grafica delle letture dei sensori nel tempo
- **Allarmi Visivi**: Indicatori colorati per distanze critiche
- **Configurazione Rate**: Possibilità di modificare la frequenza di aggiornamento

### 📹 Streaming Video
- **Video in Tempo Reale**: Stream video dalla camera del robot
- **Controlli Qualità**: Regolazione qualità, risoluzione e FPS con applicazione immediata
- **Modalità Ottimizzata**: Presets per diverse condizioni di rete
- **Aggiornamento Automatico**: Il video stream si aggiorna automaticamente quando cambiano le impostazioni
- **Feedback Visivo**: Indicatori di caricamento durante le modifiche alle impostazioni

### 🔧 Automazioni
- **Modalità Automatica**: Navigazione autonoma con evitamento ostacoli
- **Tracking Linea**: Seguimento automatico di linee colorate
- **Find Color**: Rilevamento e inseguimento di oggetti colorati

## Come Accedere

### 1. Via Browser
```
http://[IP_RASPBERRY]:5000/advanced
```

### 2. Via Rete Locale
Se il RaspTank è connesso alla rete WiFi, accedi tramite l'IP assegnato:
```
http://192.168.1.XXX:5000/advanced
```

### Controllo Video
```javascript
// Cambia risoluzione (High: 640x480, Optimized: 480x360)
ws.send('videoResolution high');     // o 'optimized'
ws.send('videoFPS 30');             // FPS: 30 o 15
ws.send('jpegQuality 95');          // Qualità: 95 o 60
```

## Ottimizzazioni Video Applicate

### 🎯 Cambiamenti Immediati
- **Qualità JPEG**: Applicata istantaneamente al prossimo frame
- **FPS**: Modificato dinamicamente nel loop di acquisizione
- **Feedback Visivo**: I pulsanti mostrano stato di caricamento

### 🔄 Cambiamenti con Riavvio
- **Risoluzione**: Richiede riconfigurazione della camera
- **Dimensioni Canvas**: Aggiornate automaticamente nell'interfaccia
- **Cache Busting**: URL con timestamp per forzare il refresh

### ⚡ Performance
- **High Quality**: 640x480, 30 FPS, Qualità 95 (per reti veloci)
- **Optimized**: 480x360, 15 FPS, Qualità 60 (per reti lente/WiFi debole)

## Comandi WebSocket

### Controllo Sensori
```javascript
// Lettura singola del sensore
ws.send('sensorRead');

// Avvia monitoraggio continuo
ws.send('sensorStart');

// Ferma monitoraggio continuo
ws.send('sensorStop');

// Cambia frequenza di aggiornamento (es: 0.1 = 10 volte al secondo)
ws.send('sensorRate 0.1');
```

### Controllo Movimento
```javascript
// Movimento direzionale
ws.send('forward');
ws.send('backward');
ws.send('left');
ws.send('right');

// Stop movimento
ws.send('stop');

// Controllo velocità
ws.send('wsB 50');  // Velocità da 0 a 100
```

### Controllo Video
```javascript
// Cambia risoluzione
ws.send('videoResolution high');     // o 'optimized'
ws.send('videoFPS 30');             // FPS: 30 o 15
ws.send('jpegQuality 95');          // Qualità: 95 o 60
```

## Struttura File

```
web/
├── advanced_controller.html      # Interfaccia completa (2000+ righe)
├── ultrasonic_monitor.py         # Sistema monitoraggio continuo sensori
├── webServer_HAT_V3.1.py        # Server WebSocket con supporto sensori
└── app.py                       # Flask app con rotta /advanced
```

## Tecnologie Utilizzate
- **Frontend**: HTML5, CSS3, JavaScript nativo
- **Backend**: Python Flask + WebSocket
- **Grafica**: Chart.js per grafici tempo reale
- **Comunicazione**: WebSocket per comunicazione bidirezionale
- **Sensori**: GPIO con gpiozero per letture precise

## Vantaggi Rispetto all'Originale

### ✅ Monitoraggio Continuo
- L'interfaccia originale legge i sensori solo in modalità automatica
- La nuova interfaccia permette monitoraggio continuo anche in controllo manuale

### ✅ Grafici Tempo Reale
- Visualizzazione storica delle letture sensori
- Identificazione trend e pattern negli ostacoli

### ✅ Controlli Avanzati
- Controllo granulare di video e movimento
- Presets ottimizzati per diverse situazioni

### ✅ Design Moderno
- Interfaccia responsive e intuitiva
- Indicatori visivi chiari per stato sistema

### ✅ Estensibilità
- Codice sorgente completo e modificabile
- Facile aggiunta di nuove funzionalità

## Risoluzione Problemi

### Video Non Si Aggiorna Dopo Modifica Impostazioni
1. **Controlla la Connessione WebSocket**: Verifica che l'indicatore di connessione sia verde
2. **Attendi il Caricamento**: I pulsanti mostrano "Loading..." durante l'applicazione delle modifiche
3. **Aggiornamento Automatico**: Il video si dovrebbe aggiornare automaticamente dopo 1-2 secondi
4. **Ricarica Manuale**: Se necessario, ricarica la pagina per resettare il video stream

### Sensori Non Rispondono
1. Verificare connessioni GPIO (pin 23 e 24)
2. Controllare che ultra.py sia accessibile
3. Verificare permessi GPIO per l'utente

### Video Non Carica
1. Verificare che la camera sia attiva
2. Controllare la rotta `/video_feed` in Flask
3. Verificare risoluzione e qualità video

### WebSocket Disconnesso
1. Controllare che il server WebSocket sia in ascolto sulla porta 8888
2. Verificare firewall e rete
3. Controllare log del server per errori

## Sviluppi Futuri
- Integrazione sensori aggiuntivi (temperatura, giroscopio)
- Controllo luci RGB avanzato
- Registrazione percorsi e replay automatico
- API REST per controllo remoto
