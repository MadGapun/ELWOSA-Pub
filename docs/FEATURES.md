# ✨ ELWOSA Features

## 🎙️ Sprachsteuerung

### Wake Word "Elwosa"
- Lokale Erkennung via openWakeWord (ONNX-Modell)
- Server-seitige Verifizierung via faster-whisper (kostenlos)
- Anti-Self-Trigger: 2.5s Cooldown nach eigener Sprachausgabe
- Anti-Halluzination: Erkennung von Whisper-Fehlinterpretationen
- Akzeptierte Varianten: "Elwosa", "El Wosa", "Alwosa", "Elwossa"

### Streaming-Pipeline
- Satz-für-Satz TTS in Echtzeit (~2-3s bis erste Antwort)
- Binary Framing Protocol (META/AUDIO/END Frames)
- Automatischer Fallback auf Standard-Pipeline bei Fehlern
- GPT-4o-mini für natürliche, deutschsprachige Antworten

### Direktbefehle (ohne LLM-Kosten)
Regex-basierte Erkennung VOR dem LLM-Call:

| Kategorie | Beispiel-Befehle |
|-----------|-----------------|
| **Timer** | "Timer 5 Minuten", "Stoppuhr starten" |
| **Lautstärke** | "Lauter", "Leiser", "Lautstärke 50" |
| **Wecker** | "Wecker 7 Uhr", "Wecker aus" |
| **Uhrzeit/Datum** | "Wie spät ist es?", "Welcher Tag ist heute?" |
| **System** | "Stopp", "Guten Morgen", "Gute Nacht" |
| **Benachrichtigungen** | "Gelesen", "Verstanden" (Dismiss) |
| **Übersetzer** | "Übersetze: Guten Tag" |

### Echtzeit-Übersetzer
- Sprachen: Deutsch ↔ Lettisch
- Modi: Automatisch, DE→LV, LV→DE
- Stimmen: nova (Lettisch), onyx (Deutsch)
- Verfügbar als Sprachbefehl und im Admin Hub

---

## 📊 Admin Hub

### 1. Dashboard
- **Server-Status:** CPU, RAM, Disk-Auslastung
- **10 Dienste:** Live-Status aller systemd Services
- **Token-Verbrauch:** Kosten-Tracking (EUR) für OpenAI
- **Backup-Status:** Letzte Backups, HDD-Belegung
- **Client-Übersicht:** Verbundene Pi-Clients mit Wallpaper
- **Notizen-Widget:** Quick-Add, Pin, Dashboard-Integration

### 2. Clients
- Client-Registry mit Hostname, IP, Status
- SSH-basierter Verbindungstest
- TTS-Stimme pro Client konfigurierbar
- Client-spezifische Wecker/Kalender-Zuordnung

### 3. Wake Words
- ONNX-Modell-Upload
- Training Wizard (Fast/Normal/Full)
- Automatisches Deploy auf verbundene Clients

### 4. Projektmanagement
- **4-Ebenen-Hierarchie:** Programm → Projekt → Task → Subtask
- **4 Ansichten:**
  - Tabelle (MS Project-Stil, aufklappbar)
  - Gantt-Chart (KW-basiert, CSS-Grid)
  - Kanban-Board (Drag & Drop)
  - Ablauf (Timeline)
- Projekt-Filter, Status-Tracking, Prioritäten

### 5. Einstellungen
- **Nachtmodus:** Auto 22:00-06:00, manuell per Stimme
- **Cost Limits:** Monatliche EUR-Grenze für API-Kosten
- **Zugriffskontrolle:** Auth-System vorbereitet (SHA-256+Salt)
  - Passwort setzen/ändern/zurücksetzen
  - Session-Timeout konfigurierbar
  - Aktuell: DEAKTIVIERT

### 6. Übersetzer
- Browser-Aufnahme (WebAudio API)
- Sprachwahl: Auto, DE→LV, LV→DE
- Ergebnis mit Audio-Playback
- Übersetzungshistorie

### 7. Stimm-Training
- Multi-User Aufnahme-System
- Samples-Verwaltung pro Benutzer
- Training-Konfiguration + Deploy

### 8. Backup
- **Status-Karte:** Letzte hourly/daily/Pi Backups
- **HDD-Info:** Kapazität, Belegung, Bad Sectors
- **Timer-Zeiten:** Konfigurierbare Zeitpunkte
- **Snapshots:** Stündliche Verzeichnisübersicht
- **Manueller Trigger:** Backup on Demand
- **Retention:** 7 Tage hourly, 30 Tage daily

### 9. Wecker
- **Recurrence-System:**
  - Wöchentlich (Mo-So)
  - Benutzerdefiniert (alle X Stunden/Tage)
  - Einmalig
- Per-Client Zuordnung
- Schlummer-Funktion
- Countdown-Timer
- TTS-Ansage
- Historie

### 10. Kalender
- **4 Ansichten:** Monat, Woche, Tag, Agenda
- **9 System-Kategorien:** Termin, Aufgabe, Erinnerung, Geburtstag, Feiertag, Projekt, Gesundheit, Reise, Persönlich
- **Custom-Kategorien:** Erstellen, Farbe, Icon
- **Per-Client-Sichtbarkeit:** Events nur auf bestimmten Clients
- **"Alle ein/ausblenden":** Schnelles Kategorien-Toggle
- **Projekt-Integration:** Tasks aus Projektmanagement im Kalender
- **CalDAV-Vorbereitung:** Sync-Konfiguration vorbereitet

---

## 🖥️ Pi-Client Features

### Display
- 10.1" IPS Touch (1024×600)
- Uhrzeit + Datum (große Anzeige)
- Wetter-Widget (wttr.in, 3 Retry-Logik)
- Wallpaper (vom Server verwaltbar)
- Nachtmodus (schwarzer Hintergrund, gedimmte Farben)
- Status-Anzeigen: Idle, Listening, Processing, Speaking

### Audio
- ALSA-basiert mit Recovery
- Pre-Roll Buffer (3 Sekunden vor Wake Word)
- WebRTC VAD (Aggressiveness 2)
- Silence Detection (1.2s Timeout)
- Min Speech (0.8s)
- Audio-Debug: WAV-Files in /tmp/elwosa_audio/

### Benachrichtigungen
- Push vom Server (SSH + UDP)
- TTS-Ansage
- Display-Notification
- Voice Dismiss ("Gelesen", "Verstanden")
- Klick-Dismiss (Touch)

---

## 🔄 Backup-System

- **Stündlich** (xx:05): rsync + Hardlinks, 7 Tage Retention
- **Täglich** (03:00): Full Backup, 30 Tage Retention
- **Pi-Backup** (04:00): rsync via SSH
- **PostgreSQL:** pg_dump bei jedem Backup
- **Change Log:** max 10.000 Einträge
- **4TB HDD:** Seagate USB, ext4, 2TB Soft-Limit
- **Admin-Trigger:** Manuelles Backup on Demand

---

## 🌙 Nachtmodus

- **Automatisch:** 22:00–06:00 (konfigurierbar)
- **Manuell:** "Nachtmodus" / "Tagmodus" per Stimme
- **Display:** Schwarzer Hintergrund, gedimmte Farben
- **Audio:** 60% Lautstärke (statt 100%)
- **Konfiguration:** Admin Hub → Einstellungen

---

*Letzte Aktualisierung: 24.02.2026*
