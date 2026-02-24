# 🏗️ ELWOSA Architektur

## Systemübersicht

ELWOSA besteht aus zwei Hauptkomponenten: dem **Server** (Debian Linux) und einem oder mehreren **Pi-Clients** (Raspberry Pi).

## Server ([SERVER-IP])

### Hardware
- **OS:** Debian Linux
- **RAM:** 16 GB
- **Speicher:** 500 GB SSD + 4 TB HDD (Backup)
- **Netzwerk:** LAN (WLAN-Chip hat PCIe-Bugs → Ethernet bevorzugt)

### Aktive Services

| Service | Port | Funktion |
|---------|------|----------|
| `voice_backend.service` | 8100 (HTTPS) | FastAPI v0.10.0 — STT, Chat, TTS, Pipeline, Translate |
| `elwosa-mcp.service` | 8000 (HTTP) | MCP Gateway v2.0 mit 3 SSH Targets |
| `cloudflare-tunnel.service` | — | Externer HTTPS-Zugang über elwosa-mcp.elwosa.de |
| `elwosa-queue-worker.service` | — | PostgreSQL Queue, LLM-Tasks via OpenAI |
| `ollama.service` | 11434 | Lokales LLM (aya-expanse:8b) |
| `elwosa-state-update.timer` | — | Automatische State-Regenerierung |
| `elwosa-backup-hourly.timer` | — | Stündliche Backups (:05) |
| `elwosa-backup-daily.timer` | — | Tägliche Full Backups (03:00) |
| `elwosa-pi-backup.timer` | — | Pi-Backup via SSH (04:00) |
| `elwosa-file-watcher.service` | — | inotifywait auf /home/chatgpt + /home/claude |

### Voice Backend (app.py)

FastAPI-Anwendung mit folgenden Endpoints:

| Endpoint | Methode | Funktion |
|----------|---------|----------|
| `/api/voice/stt` | POST | Speech-to-Text (OpenAI Whisper) |
| `/api/voice/chat` | POST | Chat (GPT-4o-mini) |
| `/api/voice/tts` | POST | Text-to-Speech (OpenAI TTS) |
| `/api/voice/pipeline` | POST | Komplett-Pipeline (STT→Chat→TTS) |
| `/api/voice/stream-pipeline` | POST | **Streaming-Pipeline** (Satz-für-Satz) |
| `/api/voice/translate` | POST | Echtzeit-Übersetzer (DE↔LV) |
| `/api/keyword-detect` | POST | Wake-Word-Verifizierung (lokaler Whisper) |

### Admin Hub (admin_router.py + index.html)

~3500 Zeilen Single-Page Application mit 10 Tabs und 45+ API-Endpoints:

- **Dashboard:** Server-Monitoring, Token-Stats, Backup-Status, Client-Übersicht, Notizen
- **Clients:** Registry, SSH-Healthcheck, TTS-Konfiguration
- **Wake Words:** ONNX-Upload, Training (Fast/Normal/Full), Deploy
- **Projektmanagement:** 4-Ebenen-Hierarchie (Programm → Projekt → Task → Subtask), 4 Ansichten
- **Einstellungen:** Nachtmodus, Cost Limits (EUR), Auth-System (vorbereitet)
- **Übersetzer:** Browser-Aufnahme, Auto/DE→LV/LV→DE
- **Stimm-Training:** Multi-User Samples, Training + Deploy
- **Backup:** Status, HDD-Info, Retention, manueller Trigger
- **Wecker:** Recurrence (weekly/custom/once), Per-Client, Schlummern
- **Kalender:** 4 Ansichten (Monat/Woche/Tag/Agenda), 9+Custom Kategorien

### Datenbank (PostgreSQL)

Datenbank `elwosa_main` mit 15 Tabellen:
- Projektmanagement (programs, projects, tasks, task_steps)
- Queue-System (llm_queue)
- Weitere Service-Tabellen

Zusätzliche JSON-basierte Datenbanken:
- `data/settings.json` — Nachtmodus, Limits, Backup, Auth
- `data/clients.json` — Client-Registry
- `data/usage_stats.json` — Token-Tracking
- `data/alarms.json` — Wecker/Timer
- `data/calendar.json` — Kalender-Events + Kategorien
- `data/notes.json` — Notizen

---

## Pi Client-01 ([PI-IP])

### Hardware
- **Model:** Raspberry Pi 3B (1 GB RAM, 32 GB SD)
- **OS:** Debian 12 bookworm (aarch64)
- **Display:** LAFVIN 10.1" IPS Touch (1024×600) via HDMI
- **Mikrofon:** USB (Trust GXT 210)
- **Audio Out:** HDMI (Card 0)
- **Kühlung:** GPIO-Fan (Pin 14, ab 55°C)

### Client-Module

| Modul | Version | Funktion |
|-------|---------|----------|
| `elwosa_client.py` | v1.5.0 | Haupt-Client (Streaming + Fallback Pipeline) |
| `server_api.py` | v4.0 | Server-API Client (Streaming + keyword_detect) |
| `audio_manager.py` | v2 | ALSA Audio (Pre-Roll Buffer 3s, VAD=2, ALSA Recovery) |
| `wake_word.py` | v6 | Wake Word (openWakeWord ONNX, PATIENCE=1, Threshold=0.5) |
| `display_manager.py` | v5.0 | Display (1024×600, Nachtmodus, Wetter, Wallpaper) |
| `command_handler.py` | v1.0 | Direktbefehle (7 Kategorien, Regex vor LLM) |
| `notification_handler.py` | — | Push-Benachrichtigungen (SSH+UDP, TTS, Voice Dismiss) |
| `youtube_controller.py` | — | YouTube-Steuerung (Chromium + xdotool) |
| `config.py` | — | Config Loader (.env) |

### Konfiguration (.env)
```
SERVER_URL=https://your-server:8100
CLIENT_ID=elwosa-client-01
SILENCE_TIMEOUT=1.2
MIN_SPEECH_SECONDS=0.8
FRAME_SIZE=480
SAMPLE_RATE=16000
PRE_BUFFER_SECONDS=3
```

---

## Streaming-Pipeline (Protokoll)

Binary Framing Protocol über HTTP POST:

| Frame-Typ | Byte | Inhalt |
|-----------|------|--------|
| META | `0x01` | JSON mit STT-Text, Modell-Info |
| AUDIO | `0x02` | MP3-Chunks (16384 Bytes) |
| END | `0x03` | JSON mit Gesamtstatistiken |

**Format:** `[1 Byte Typ][4 Bytes Länge (Big Endian)][Daten]`

```
Client sendet WAV ──▶ Server
                      │
                      ├─ STT (Whisper) ──▶ META Frame (Text)
                      │
                      ├─ GPT-4o-mini (streaming)
                      │   │
                      │   ├─ Satz 1 ──▶ TTS ──▶ AUDIO Frames
                      │   ├─ Satz 2 ──▶ TTS ──▶ AUDIO Frames
                      │   └─ Satz N ──▶ TTS ──▶ AUDIO Frames
                      │
                      └─ END Frame (Statistiken)
```

---

## Wake Word Detection (Hybrid)

```
Mikrofon (16kHz, 16bit)
        │
        ▼
┌─────────────────────┐
│ openWakeWord (lokal) │
│ elwosa_oww_v1.onnx   │
│ Threshold: 0.5       │
│ PATIENCE: 1          │
└─────────┬───────────┘
          │ Score > 0.5
          ▼
┌─────────────────────┐
│ Server Verifizierung │
│ POST /keyword-detect │
│ faster-whisper base  │
│ initial_prompt:      │
│   "Elwosa"           │
│ beam_size: 5         │
└─────────┬───────────┘
          │ "elwosa" gefunden
          ▼
      ✅ Aktiviert!
```

**Anti-Self-Trigger:** 2.5s Cooldown nach TTS-Playback + Preprocessor-Reset
**Anti-Halluzination:** "elwosa" 3+ mal im Whisper-Text → False (Halluzination)

---

## Backup-System v3

```
┌──────────────────────────────────────────┐
│        4TB HDD (/mnt/elwosa-backup)      │
│                                           │
│  backups/                                 │
│  ├── hourly/     (alle 1h, 7 Tage)       │
│  ├── daily/      (täglich 03:00, 30 Tage)│
│  └── pg_dumps/   (PostgreSQL Dumps)       │
│                                           │
│  pi-client-01/   (rsync via SSH, 04:00)   │
│  media/          (Bilder, Emojis)         │
│  logs/           (Status-JSONs)           │
│  change_log.json (max 10.000 Einträge)   │
└──────────────────────────────────────────┘
```

- **Engine:** rsync + Hardlinks (platzsparend)
- **Timer:** systemd (NICHT crontab)
- **Soft-Limit:** 2 TB
- **⚠️ HDD hat 3272 bad sectors — keine alleinige Backup-Kopie!**

---

## Nachtmodus

| Eigenschaft | Tag (06:00–22:00) | Nacht (22:00–06:00) |
|------------|-------------------|---------------------|
| Display BG | Wallpaper | Schwarz |
| Uhr-Farbe | Hell | #666666 |
| Audio | 100% | 60% |
| Aktivierung | Automatisch oder "Tagmodus" | Automatisch oder "Nachtmodus" |

---

*Letzte Aktualisierung: 24.02.2026*
