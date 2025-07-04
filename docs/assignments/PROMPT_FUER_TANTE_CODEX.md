# 💌 COPY-PASTE PROMPT FÜR TANTE CODEX

---

**Liebe Tante Codex,**

deine **MEGA-MISSION ist ready!** 🚀

**GitHub Repository:** https://github.com/MadGapun/ELWOSA-Pub  
**Hauptauftrag:** https://github.com/MadGapun/ELWOSA-Pub/blob/main/docs/assignments/TANTE_ASSIGNMENT_PROJEKTMANAGEMENT.md

## 🎯 **MISSION OVERVIEW**

Du entwickelst ein **vollständiges Projektmanagement-System** für ELWOSA mit:
- ✅ **GANTT-Charts** (wie Microsoft Project)
- ✅ **Projekt-Hierarchie** (Master → Sub-Projekte)
- ✅ **Milestone-Tracking & Dependencies**
- ✅ **Resource Planning & Critical Path**

## 🔧 **TECHNICAL SETUP**

**API-Status:**
- ✅ **Task-API V6:** `http://192.168.178.200:8001/tasks` (900+ Tasks verfügbar)
- ✅ **Database:** PostgreSQL mit allen ELWOSA-Daten
- ✅ **PHP-Interface:** Vorbereitet in `src/frontend/php/`

**Dein Tech-Stack:**
- **Backend:** PHP + PostgreSQL (läuft bereits)
- **Frontend:** HTML/CSS/JavaScript
- **GANTT-Library:** dhtmlx-gantt (Community) oder @nivo/gantt
- **Development:** 4-5 Wochen, phasenweise

## 📋 **ROADMAP**

### **Phase 1 (Woche 1): API Integration**
- ✅ PHP-Interface zur Task-API V6 reparieren
- ✅ Database-Schema für Projekte, Milestones, Dependencies

### **Phase 2-3 (Woche 2-3): Core Features**
- ✅ Projekt-Hierarchie UI (Tree-View)
- ✅ GANTT-Chart mit Drag & Drop
- ✅ Task-zu-Projekt Zuordnung

### **Phase 4-5 (Woche 3-5): Advanced Features**
- ✅ Dependencies mit Critical Path
- ✅ Resource Planning & Reports
- ✅ PDF-Export für Stakeholder

## 🎨 **UI VISION**

```
[📊 GANTT] [📋 KANBAN] [🎯 SPRINTS] [📈 REPORTS]

┌─────────────────────────────────────────────────────────┐
│ PROJEKT-TREE          │ GANTT-DIAGRAMM                  │
│ ├─ 🏢 ELWOSA Master   │ ████████░░░░░░░░ TASK-101      │
│ │  ├─ Foundation      │ ░░░████████░░░░░ TASK-102      │
│ │  └─ Smart Home      │ ░░░░░░████████░░ TASK-103      │
│ └─ 🐱 MIAUMIAU (HOLD) │ [Day|Week|Month|Quarter]       │
└─────────────────────────────────────────────────────────┘
```

## 🏆 **SUCCESS CRITERIA**

**MVP:** Projekt-Hierarchie + Basic GANTT + API-Integration  
**Full:** Dependencies + Critical Path + Reports + Export

## 💡 **SPECIAL REQUIREMENTS**

- **Goldene Regeln:** Prio-0 Tasks prominent hervorheben
- **Multi-User:** Papa Claude, Tante Codex, Opa Markus
- **ELWOSA-Integration:** GitHub Issues ↔ Tasks sync

## 🚀 **QUICK START**

```bash
# 1. Repository clonen
git clone https://github.com/MadGapun/ELWOSA-Pub.git

# 2. API testen  
curl http://192.168.178.200:8001/tasks

# 3. PHP-Interface starten
cd src/frontend/php
php -S localhost:8080
```

## 💪 **WHY THIS MATTERS**

**Tante, du baust das Herzstück von ELWOSA!**

Nach Abschluss haben wir ein **Enterprise-Level PM-Tool** das mit Jira/Asana konkurriert - aber besser für Entwickler-Teams optimiert ist!

**Ready to build something amazing?** 🎮

---

**Alle Details im GitHub Repository!**  
**Bei Fragen: Papa Claude über GitHub Issues kontaktieren.**

_Papa Claude & Opa Markus_  
_4. Juli 2025_