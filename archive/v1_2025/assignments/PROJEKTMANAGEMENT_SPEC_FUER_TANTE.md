# 📊 ELWOSA PROJEKTMANAGEMENT SYSTEM - VOLLSPEZIFIKATION FÜR TANTE CODEX

## 🎯 ÜBERSICHT

Liebe Tante Codex, hier kommt deine **MEGA-AUFGABE**: Ein vollständiges Projektmanagement-System für ELWOSA!

**Kernaussage:** "Menschen verstehen GANTT und Waterfall, nur Entwickler verstehen SCRUM" - Wir wollen das Beste aus allen Welten!

---

## 📋 ANFORDERUNGEN

### 1. DATENMODELL-ERWEITERUNG

#### Neue Tabelle: `projects`
```sql
CREATE TABLE projects (
    project_id VARCHAR(50) PRIMARY KEY,  -- Format: PROJ-XXXX
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_project_id VARCHAR(50),       -- Für Sub-Projekte
    status VARCHAR(50) DEFAULT 'PLANNING',
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10,2),
    owner VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    project_type VARCHAR(50), -- 'waterfall', 'agile', 'hybrid'
    stage VARCHAR(50),        -- Für Stage-Gate
    FOREIGN KEY (parent_project_id) REFERENCES projects(project_id)
);
```

#### Neue Tabelle: `milestones`
```sql
CREATE TABLE milestones (
    milestone_id VARCHAR(50) PRIMARY KEY,  -- Format: MS-XXXX
    project_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    completion_percentage INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
```

#### Neue Tabelle: `dependencies`
```sql
CREATE TABLE dependencies (
    dependency_id SERIAL PRIMARY KEY,
    task_id VARCHAR(50) NOT NULL,
    depends_on_task_id VARCHAR(50) NOT NULL,
    dependency_type VARCHAR(50) DEFAULT 'finish_to_start',
    lag_days INT DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(task_id)
);
```

#### Neue Tabelle: `sprints` (für SCRUM-Elemente)
```sql
CREATE TABLE sprints (
    sprint_id VARCHAR(50) PRIMARY KEY,  -- Format: SPRINT-XXXX
    project_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    goal TEXT,
    status VARCHAR(50) DEFAULT 'PLANNED',
    velocity INT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
```

#### Task-Tabelle erweitern:
```sql
ALTER TABLE tasks 
ADD COLUMN milestone_id VARCHAR(50),
ADD COLUMN sprint_id VARCHAR(50),
ADD COLUMN estimated_hours DECIMAL(5,2),
ADD COLUMN actual_hours DECIMAL(5,2),
ADD COLUMN completion_percentage INT DEFAULT 0,
ADD COLUMN start_date DATE,
ADD COLUMN due_date DATE,
ADD COLUMN task_type VARCHAR(50), -- 'feature', 'bug', 'epic', 'story'
ADD FOREIGN KEY (milestone_id) REFERENCES milestones(milestone_id),
ADD FOREIGN KEY (sprint_id) REFERENCES sprints(sprint_id);
```

---

## 🎨 UI/UX ANFORDERUNGEN

### A. HAUPT-DASHBOARD ERWEITERUNG

```
┌─────────────────────────────────────────────────────────────────┐
│  ELWOSA Control Center - Projektmanagement                      │
├─────────────────────────────────────────────────────────────────┤
│  [📊 GANTT] [📋 KANBAN] [🎯 SPRINTS] [📈 REPORTS] [⚙️ SETTINGS] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PROJEKT-HIERARCHIE           │  GANTT-DIAGRAMM                 │
│  ├─ 🏢 ELWOSA Master         │  ━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  │  ├─ 🔧 Foundation Phase   │  ████████░░░░░░░░ TASK-101      │
│  │  ├─ 🏠 Smart Home         │  ░░░████████░░░░░ TASK-102      │
│  │  └─ 🤖 AI Integration     │  ░░░░░░████████░░ TASK-103      │
│  └─ 🐱 MIAUMIAU (ON HOLD)    │                                  │
│                               │  [Zoom: Day|Week|Month|Quarter] │
└─────────────────────────────────────────────────────────────────┘
```

### B. GANTT-CHART KOMPONENTE

**Technologie:** Verwende **@nivo/gantt** oder **dhtmlx-gantt** (Community Edition)

**Features:**
- Drag & Drop für Task-Verschiebung
- Abhängigkeiten als Pfeile zwischen Tasks
- Kritischer Pfad (rot hervorgehoben)
- Ressourcen-Auslastung unten
- Milestone-Diamonds
- Wochenenden/Feiertage grau

### C. PROJEKT-MANAGER VIEW

```typescript
interface ProjectManagerView {
  // Linke Sidebar
  projectTree: {
    masterProjects: Project[];
    orphanTasks: Task[]; // Tasks ohne Projekt
  };
  
  // Hauptbereich
  activeView: 'gantt' | 'kanban' | 'sprint' | 'waterfall';
  
  // Rechte Sidebar
  projectDetails: {
    info: ProjectInfo;
    team: TeamMember[];
    budget: BudgetTracking;
    risks: Risk[];
  };
}
```