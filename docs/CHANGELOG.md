# 📋 ELWOSA Changelog

## Februar 2026

### Prompt 040+ (24.02.2026)
- **FIX: Streaming Pipeline** — `import json as _json` fehlte in app.py seit Erstellung → Pipeline hat NIE funktioniert, immer Fallback
- **FIX: Kalender Monatsansicht** — Zeigt jetzt alle 7 Tage (Mo–So) statt nur Mo/Di/Mi
- **FIX: Kalender Wochenansicht** — Events werden jetzt korrekt angezeigt, Ganztags-Events in eigener Reihe
- **NEU: "Alle ein/ausblenden"** — Kategorien-Toggle im Kalender
- **NEU: Direktbefehle (TASK-054)** — 7 Kategorien (Timer, Lautstärke, Wecker, Uhrzeit, System, Benachrichtigungen, Übersetzer)
- **NEU: Fallback-Pipeline Command Interception** — Direktbefehle funktionieren auch bei Streaming-Fehler
- **NEU: Audio-Debug** — WAV-Files in /tmp/elwosa_audio/ (letzte 5)
- **NEU: Whisper initial_prompt** — Befehlsvokabular für bessere STT-Erkennung
- **VERBESSERUNG: Wetter-Retry** — 3 Versuche mit Backoff (Server + Pi)
- **VERBESSERUNG: Reaktionszeit** — Silence 2.0→1.2s, MinSpeech 2.5→0.8s, VAD 1→2
- **VERBESSERUNG: Streaming** — Sentence Buffer 15→8 Zeichen, TTS Chunks 4096→16384
- **VERBESSERUNG: Context Cache** — 60s DB-Query-Cache für context_builder.py
- **VERBESSERUNG: Pre-Buffer Trimming** — Stille Frames vor erster Sprache entfernt

### Prompt 038-039 (22-23.02.2026)
- **NEU: Kalender-System (TASK-049/051)** — 4 Ansichten, 9 System-Kategorien + Custom
- **NEU: Wecker-Recurrence (TASK-048/052)** — Wöchentlich/Benutzerdefiniert/Einmalig
- **NEU: Notizen-Widget (TASK-050)** — Dashboard-Integration, Pin, Quick-Add
- **NEU: Benachrichtigungen** — Push via SSH+UDP, TTS, Voice/Touch Dismiss
- **NEU: Auto-Recovery** — Timeout für stuck Processing-State

### Prompt 035-037 (früher 02.2026)
- **NEU: Wake Word Integration (TASK-035)** — openWakeWord + Whisper Hybrid
- **NEU: Voice Training Hub (TASK-036)** — Browser-Aufnahme + Training
- **NEU: Wetter-Anzeige (TASK-037)** — wttr.in auf Pi-Display

### Prompt 032-034 (02.2026)
- **NEU: Display v5.0 (TASK-032)** — 1024×600, GPIO-Fan
- **NEU: Token-Statistiken (TASK-033)** — usage_tracker.py
- **NEU: Admin Hub (TASK-034)** — 10 Tabs, komplett deutsch

### Prompt 027-028 (01-02.2026)
- **NEU: Projektmanagement (TASK-027)** — 4-Ebenen-Hierarchie, REST-API
- **NEU: Dashboard & Reporting (TASK-028)** — Gantt, Tabelle, Kanban, Ablauf

### Prompt 020-025 (01.2026)
- **NEU: Streaming Pipeline (TASK-040)** — Satz-für-Satz TTS, mpg123 Real-Time
- **NEU: Voice Backend v0.10.0 (TASK-010)** — STT/Chat/TTS/Pipeline
- **NEU: Pi Smart Client v1.5.0 (TASK-012)** — Streaming + Wake Word
- **NEU: Übersetzer DE↔LV (TASK-011)** — Echtzeit-Sprachübersetzung
- **NEU: Selbstwahrnehmung (TASK-014)** — context_builder.py
- **NEU: Sofort-Bestätigung (TASK-017)** — processing.wav + Display States

### Dezember 2025
- **NEU: Backup-System v3 (TASK-003/045)** — rsync + Hardlinks, HDD, Timer
- **NEU: STT Sprache Fix (TASK-038)** — language=de für Whisper
- **NEU: Recording-Optimierung (TASK-039)** — Pre-Roll, VAD, Silence Detection

---

## Juni 2025 (Legacy)
- Dashboard v4 (Priority-based Task Management)
- Memory API (150+ Einträge)
- Task API v5 (125+ Tasks)
- MCP Integration für Claude Desktop
- AI Bridge (OpenAI + Ollama)
- AI-Familie Konzept (Opa, Mama, Papa, Tante, Baby)
- 16 Goldene Regeln

> Hinweis: Das Projekt wurde ab Ende 2025 komplett neu ausgerichtet — vom Projektmanagement-Tool zum vollwertigen Sprachassistenten.

---

*Letzte Aktualisierung: 24.02.2026*
