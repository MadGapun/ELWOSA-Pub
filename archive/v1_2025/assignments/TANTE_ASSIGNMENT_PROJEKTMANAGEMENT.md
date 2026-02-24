# 🚀 TANTE CODEX ASSIGNMENT - ELWOSA PROJEKTMANAGEMENT + API-INTEGRATION
**Datum:** 04. Juli 2025  
**Priorität:** HOCH  
**Status:** READY TO START  

---

## 🎯 MISSION OVERVIEW

**Hauptziel:** Entwickle ein vollständiges Projektmanagement-System für ELWOSA mit GANTT-Charts, Milestones und optimierter API-Integration.

**Warum wichtig:** ELWOSA wird dadurch von einem einfachen Task-Manager zu einem Enterprise-Level Projektmanagement-Tool!

---

## 📊 AKTUELLE SITUATION

### ✅ WAS BEREITS FUNKTIONIERT
- Task-API V6 läuft stabil auf Port 8001 (Remote: 192.168.178.200:8001)
- PostgreSQL Datenbank mit 900+ Tasks
- PHP-Interface Grundstruktur vorhanden
- Moderne Task-Management UI bereits implementiert

### ❌ WAS FEHLT
1. **Projektmanagement-Features** (komplett)
2. **GANTT-Charts & Timeline-Views**
3. **Projekt-Hierarchie & Milestones**  
4. **API-Integration PHP ↔ Task-API V6**
5. **Dashboard für Projekt-KPIs**

---

## 🔧 TECHNISCHE AUFGABEN

### **1. API-INTEGRATION REPARIEREN**
**Problem:** PHP-Interface hat keine Verbindung zur Task-API V6
**Files:** `src/frontend/php/tasks_api.php`, `src/frontend/php/config.php`

**Lösung:**
```php
// Bereits vorbereitet: Proxy-Funktion zu Task-API V6
function get_tasks_from_api() {
    $api_url = "http://192.168.178.200:8001/tasks";
    // Implementierung mit Fallback zur direkten DB-Verbindung
}
```

### **2. DATENBANK-SCHEMA ERWEITERN**
**Neue Tabellen erstellen:**
```sql
-- Projekte mit Hierarchie
CREATE TABLE projects (
    project_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_project_id VARCHAR(50),
    status VARCHAR(50) DEFAULT 'PLANNING',
    start_date DATE,
    end_date DATE,
    -- ... siehe Vollspezifikation
);

-- Milestones
CREATE TABLE milestones (
    milestone_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING'
    -- ...
);

-- Task-Dependencies
CREATE TABLE dependencies (
    dependency_id SERIAL PRIMARY KEY,
    task_id VARCHAR(50) NOT NULL,
    depends_on_task_id VARCHAR(50) NOT NULL,
    dependency_type VARCHAR(50) DEFAULT 'finish_to_start'
);
```

### **3. GANTT-CHART IMPLEMENTIERUNG**
**Frontend-Technology:** 
- JavaScript Library: **dhtmlx-gantt** (Community Edition) ODER
- React Component: **@nivo/gantt**

**Core Features:**
- Drag & Drop Task-Scheduling
- Dependencies mit Pfeilen
- Kritischer Pfad (rot)
- Milestone-Diamonds
- Zoom: Tag/Woche/Monat/Quartal

### **4. PROJEKT-HIERARCHIE UI**
```
├─ 🏢 ELWOSA Master
│  ├─ 🔧 Foundation Phase (38 Tasks)
│  ├─ 🏠 Smart Home Integration (PLANNING)  
│  └─ 🤖 AI Workflow (PLANNING)
└─ 🐱 MIAUMIAU Robotics (ON HOLD)

Orphan Tasks: 127 (Tasks ohne Projekt)
```

---

## 📋 DEVELOPMENT ROADMAP

### **Phase 1: API Integration (Woche 1)**
1. ✅ API-Proxy reparieren (`tasks_api.php`)
2. ✅ Database-Config mit korrektem Passwort
3. ✅ CRUD-Operations für Tasks über API
4. ✅ Error-Handling & Fallback zur direkten DB

### **Phase 2: Database Schema (Woche 1-2)**
1. ✅ Projektmanagement-Tabellen erstellen
2. ✅ Foreign Keys zu bestehender Task-Tabelle
3. ✅ Beispiel-Daten für ELWOSA-Projekte
4. ✅ Migration-Script

### **Phase 3: Projekt-Management UI (Woche 2-3)**
1. ✅ Projekt-Hierarchie Sidebar
2. ✅ Task-zu-Projekt Zuordnung (Drag & Drop)
3. ✅ Projekt-Dashboard mit KPIs
4. ✅ Milestone-Tracking

### **Phase 4: GANTT-Chart (Woche 3-4)**
1. ✅ GANTT-Library Integration
2. ✅ Task-Scheduling mit Drag & Drop
3. ✅ Dependencies & Critical Path
4. ✅ Resource-Planning

### **Phase 5: Advanced Features (Woche 4-5)**
1. ✅ Stage-Gate Process (Waterfall)
2. ✅ Sprint-Planning (Agile)  
3. ✅ Reports & Analytics
4. ✅ Export (PDF, Excel)

---

## 🎨 UI/UX REQUIREMENTS

### **Hauptnavigation erweitern:**
```
[📊 GANTT] [📋 KANBAN] [🎯 SPRINTS] [📈 REPORTS] [⚙️ PROJECTS]
```

### **GANTT-View Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ PROJEKT-TREE          │ GANTT-DIAGRAMM                      │
│ ├─ ELWOSA Master      │ ████████░░░░░░░░ TASK-101          │  
│ │  ├─ Foundation      │ ░░░████████░░░░░ TASK-102          │
│ │  └─ Smart Home      │ ░░░░░░████████░░ TASK-103          │
│ └─ MIAUMIAU (HOLD)    │ Timeline: [D|W|M|Q]                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 FILE STRUCTURE

```
src/frontend/php/
├── config.php                 ✅ (DB-Config mit Passwort)
├── tasks_api.php             ✅ (API-Proxy implementiert)  
├── projects_api.php          🆕 (Projekt-CRUD)
├── gantt_api.php            🆕 (GANTT-Daten)
├── project_manager.php      🆕 (Hauptansicht)
└── components/
    ├── gantt_chart.js       🆕 (GANTT-Component)
    ├── project_tree.js      🆕 (Hierarchie-Tree)
    └── milestone_tracker.js 🆕 (Milestone-UI)
```

---

## 🔥 SPECIAL REQUIREMENTS

### **1. ELWOSA-Spezifische Features**
- **Goldene Regeln Integration:** Prio-0 Tasks prominent anzeigen
- **Papa Claude Tasks:** Spezielle Kennzeichnung für AI-Tasks  
- **Multi-User Support:** Papa Claude, Tante Codex, Opa Markus

### **2. Enterprise Features**
- **Stage-Gate Process:** Waterfall mit Review-Gates
- **Resource Management:** Wer arbeitet an was?
- **Budget-Tracking:** Geschätzte vs. tatsächliche Stunden
- **Risk Management:** Kritische Pfade und Bottlenecks

### **3. Developer Experience**
- **GitHub Integration:** Issues ↔ Tasks synchronisieren
- **API-First:** Alles über REST-APIs
- **Real-time Updates:** WebSocket für Live-Collaboration
- **Mobile Responsive:** Auch auf Tablets nutzbar

---

## 🎯 SUCCESS CRITERIA

### **Minimum Viable Product (MVP):**
✅ **Projekt-Hierarchie:** Tasks können Projekten zugeordnet werden  
✅ **GANTT-Basic:** Timeline-View mit Drag & Drop  
✅ **API-Integration:** PHP ↔ Task-API V6 funktioniert  
✅ **Milestone-Tracking:** Wichtige Deadlines sichtbar  

### **Full Feature Set:**
✅ **Dependencies:** Task-Abhängigkeiten mit Critical Path  
✅ **Resource Planning:** Team-Auslastung visualisieren  
✅ **Reports:** Burn-Down, Velocity, Budget-Tracking  
✅ **Export:** PDF-Reports für Stakeholder  

---

## 💻 DEVELOPMENT SETUP

### **Lokale Entwicklung:**
```bash
# Existierender Stack nutzen:
# - PostgreSQL: 192.168.178.200:5432
# - Task-API V6: 192.168.178.200:8001  
# - PHP-Development-Server: localhost:8080

cd src/frontend/php
php -S localhost:8080
```

### **API-Endpoints (verfügbar):**
```
GET  /tasks                    # Alle Tasks
POST /tasks                    # Neue Task erstellen  
PUT  /tasks/{id}              # Task updaten
GET  /tasks/{id}/steps        # Task-Steps

# Neu zu entwickeln:
GET  /projects                # Projekt-Hierarchie
POST /projects                # Neues Projekt
GET  /projects/{id}/gantt     # GANTT-Daten
```

---

## 📚 RESOURCES & LINKS

### **API-Dokumentation:**
- Task-API V6: Live auf `http://192.168.178.200:8001/tasks`
- Database: PostgreSQL mit 27 Tabellen, 900+ Tasks

### **Libraries & Tools:**
- **GANTT:** dhtmlx-gantt (Community) oder @nivo/gantt
- **UI Framework:** Bootstrap 5 oder Tailwind CSS
- **Icons:** FontAwesome oder Lucide
- **Charts:** Chart.js für Reports

### **Beispiel-Projekte:**
```sql
-- Bereits in DB vorhanden:
ELWOSA-0200: "Phase 1: Foundation - Basis-System aufsetzen"
ELWOSA-0201: "Phase 2: Smart Home Integration" 
ELWOSA-0202: "Phase 3: KI-Integration"
ELWOSA-0203: "Phase 4: ESP32-Netzwerk & Robotik"
```

---

## 🚀 GETTING STARTED

### **Step 1: Repository Setup**
Alle Files sind bereits im GitHub Repository vorbereitet:
- `src/frontend/php/` - PHP-Interface mit API-Proxy
- `docs/assignments/` - Diese Spezifikation
- Database-Schema in `docs/database/`

### **Step 2: API-Test**  
```bash
# Teste Task-API V6:
curl http://192.168.178.200:8001/tasks

# Teste lokales PHP-Interface:
curl http://localhost:8080/tasks_api.php
```

### **Step 3: Database-Schema**
```sql
-- Erstelle Projektmanagement-Tabellen:
-- (SQL-Scripts sind im Repository)
```

### **Step 4: Entwicklung starten**
1. GANTT-Library integrieren
2. Projekt-Tree Component
3. API-Integration vervollständigen
4. UI/UX polieren

---

## 🎉 MOTIVATION

Tante Codex, du baust hier **das Herzstück von ELWOSA**! 

Wenn das fertig ist, haben wir:
- ✅ **Enterprise-Level Projektmanagement**
- ✅ **GANTT-Charts wie Microsoft Project**  
- ✅ **Agile + Waterfall in einem Tool**
- ✅ **KI-Integration für automatische Planung**

**Das wird ELWOSA zum konkurrenzfähigen PM-Tool machen!** 🚀

---

**Ready to code?** Let's build something amazing! 💪

_Papa Claude & Opa Markus_  
_Juli 2025_## 🔗 **GITHUB LINKS FÜR DICH**

**Hauptauftrag:**
https://github.com/MadGapun/ELWOSA-Pub/blob/main/docs/assignments/TANTE_ASSIGNMENT_PROJEKTMANAGEMENT.md

**Technische Spezifikation:**
https://github.com/MadGapun/ELWOSA-Pub/blob/main/docs/assignments/PROJEKTMANAGEMENT_SPEC_FUER_TANTE.md

**PHP-Interface (vorbereitet):**
https://github.com/MadGapun/ELWOSA-Pub/tree/main/src/frontend/php

**Strategic Roadmap:**
https://github.com/MadGapun/ELWOSA-Pub/blob/main/docs/ELWOSA_STRATEGIC_ROADMAP.md

---

## ⚡ **QUICK START GUIDE**

### **1. Repository clonen:**
```bash
git clone https://github.com/MadGapun/ELWOSA-Pub.git
cd ELWOSA-Pub
```

### **2. API-Status prüfen:**
```bash
# Task-API V6 testen:
curl http://192.168.178.200:8001/tasks

# Sollte 900+ Tasks zurückgeben!
```

### **3. PHP-Interface starten:**
```bash
cd src/frontend/php
php -S localhost:8080

# Teste: http://localhost:8080/tasks_api.php
```

### **4. Database-Config:**
```php
// Bereits vorbereitet in config.php:
$DB_PASS = 'claude';  // ✅ Passwort ist gesetzt!
```

---

## 🎯 **DEINE MISSION**

**Ziel:** Verwandle ELWOSA in ein **Enterprise-Level Projektmanagement-Tool** mit:

✅ **GANTT-Charts** (wie Microsoft Project)
✅ **Projekt-Hierarchie** (Master → Sub-Projekte)  
✅ **Milestone-Tracking** (wichtige Deadlines)
✅ **Task-Dependencies** (kritischer Pfad)
✅ **Resource Planning** (wer arbeitet an was?)

### **Development Roadmap:**
- **Woche 1:** API-Integration + Database-Schema
- **Woche 2-3:** GANTT-Chart + Projekt-Tree UI  
- **Woche 3-4:** Dependencies + Critical Path
- **Woche 4-5:** Reports + Export Features

---

## 🔧 **TECHNOLOGIE-STACK**

- **Backend:** PHP + PostgreSQL (bereits läuft)
- **Frontend:** HTML/CSS/JavaScript  
- **GANTT-Library:** dhtmlx-gantt (Community) oder @nivo/gantt
- **API:** Task-API V6 auf Port 8001 (funktional)

---

## 🎨 **UI MOCKUP**

```
┌─────────────────────────────────────────────────────────────┐
│ [📊 GANTT] [📋 KANBAN] [🎯 SPRINTS] [📈 REPORTS]           │
├─────────────────────────────────────────────────────────────┤
│ PROJEKT-TREE          │ GANTT-DIAGRAMM                      │
│ ├─ 🏢 ELWOSA Master   │ ████████░░░░░░░░ TASK-101          │
│ │  ├─ Foundation      │ ░░░████████░░░░░ TASK-102          │
│ │  ├─ Smart Home      │ ░░░░░░████████░░ TASK-103          │
│ │  └─ AI Integration  │ Timeline: [Day|Week|Month|Quarter] │
│ └─ 🐱 MIAUMIAU (HOLD) │                                     │
│                       │ Orphan Tasks: 127 (ohne Projekt)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏆 **SUCCESS CRITERIA**

### **MVP (Minimum Viable Product):**
- ✅ Projekt-Hierarchie mit Task-Zuordnung
- ✅ Basic GANTT-Chart mit Timeline-View
- ✅ API-Integration zur Task-API V6
- ✅ Milestone-Tracking

### **Full Feature Release:**
- ✅ Task-Dependencies mit Critical Path
- ✅ Resource Management & Team-Auslastung
- ✅ Burn-Down Charts & Velocity-Reports
- ✅ PDF-Export für Stakeholder

---

## 💡 **ELWOSA-SPEZIFISCHE FEATURES**

### **Goldene Regeln Integration:**
- Prio-0 Tasks (goldene Regeln) prominent anzeigen
- Warnung wenn goldene Regeln verletzt werden

### **Multi-User Support:**
- **Papa Claude:** AI-Tasks speziell kennzeichnen
- **Tante Codex:** Frontend-Tasks zuweisen  
- **Opa Markus:** Executive Dashboard mit KPIs

### **GitHub Integration:**
- Issues ↔ Tasks synchronisieren
- Pull Requests automatisch zu Tasks zuordnen

---

## 🔥 **WARUM DAS WICHTIG IST**

Tante, du baust hier **das Herzstück von ELWOSA**!

Nach Abschluss haben wir:
- 🏆 **Enterprise-Level PM-Tool** (konkurriert mit Jira/Asana)
- 📊 **GANTT-Charts** besser als GitHub Projects
- 🤖 **AI-Integration** für automatische Planung
- 💼 **Hybrid-Ansatz** (Agile + Waterfall + Stage-Gate)

**Das macht ELWOSA zu einem marktfähigen Produkt!** 🚀

---

## 🎯 **DEIN NÄCHSTER SCHRITT**

1. **Repository clonen** und durchschauen
2. **API-Integration testen** (tasks_api.php)
3. **Database-Schema planen** (projects, milestones, dependencies)
4. **GANTT-Library evaluieren** (dhtmlx vs. @nivo)
5. **Mit Papa Claude koordinieren** bei Fragen

---

## 💪 **MOTIVATION**

**Tante Codex, das wird dein MEISTERWERK!**

Du entwickelst nicht nur Features - du baust die Zukunft von ELWOSA! Ein Tool, das sowohl Entwickler als auch Manager lieben werden.

**Ready to change the game?** 🎮

---

**Mit viel Vertrauen und Vorfreude,**

_Papa Claude & Opa Markus_  
_4. Juli 2025_

**P.S.:** Bei Fragen oder Problemen - einfach Papa Claude über GitHub Issues kontaktieren! 💬