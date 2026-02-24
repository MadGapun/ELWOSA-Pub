# ELWOSA Coding Standards

## Überblick

Diese Dokumentation definiert die Coding Standards und Best Practices für die ELWOSA-Entwicklung, um Code-Konsistenz, Wartbarkeit und Qualität sicherzustellen.

## 🐍 **Python Standards (Backend)**

### **PEP 8 Konformität**
```python
# ✅ Gut: Aussagekräftige Namen
def calculate_task_priority(urgency_score: int, business_value: float) -> int:
    """Berechnet Priorität basierend auf Dringlichkeit und Geschäftswert."""
    return int(urgency_score * business_value * 0.7)

# ❌ Schlecht: Unklare Namen
def calc_prio(u: int, bv: float) -> int:
    return int(u * bv * 0.7)
```

### **Type Hints (mandatory)**
```python
from typing import List, Dict, Optional, Union
from datetime import datetime

class TaskService:
    def __init__(self, db_connection: DatabaseConnection) -> None:
        self.db = db_connection
    
    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        assignee_id: Optional[int] = None,
        due_date: Optional[datetime] = None
    ) -> Task:
        """Erstellt eine neue Task mit optionalen Parametern."""
        # Implementation...
```

### **Docstring Standards (Google Style)**
```python
def process_ai_response(
    prompt: str,
    model: str = "gpt-4",
    temperature: float = 0.7
) -> Dict[str, Union[str, float]]:
    """Verarbeitet KI-Antwort und extrahiert Metadaten.
    
    Args:
        prompt: Der Input-Prompt für das KI-Model
        model: Name des zu verwendenden KI-Models
        temperature: Kreativitäts-Parameter (0.0-1.0)
    
    Returns:
        Dictionary mit response, confidence, und processing_time
    
    Raises:
        AIServiceError: Wenn KI-Service nicht verfügbar
        ValidationError: Wenn Prompt ungültig
    
    Example:
        >>> result = process_ai_response("Erstelle Task für Bug-Fix")
        >>> print(result['response'])
        "Bug-Fix Task erstellt: Kritischer Frontend-Fehler beheben"
    """
```

### **Error Handling**
```python
# ✅ Spezifische Exceptions
class TaskNotFoundError(Exception):
    """Wird ausgelöst wenn Task mit gegebener ID nicht existiert."""
    pass

class InsufficientPermissionsError(Exception):
    """Wird ausgelöst bei unzureichenden Benutzerberechtigungen."""
    pass

# ✅ Proper Exception Handling
def get_task_by_id(task_id: int) -> Task:
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundError(f"Task mit ID {task_id} nicht gefunden")
        return task
    except DatabaseError as e:
        logger.error(f"Datenbankfehler beim Laden von Task {task_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}")
        raise InternalServerError("Task konnte nicht geladen werden")
```

## ⚛️ **TypeScript/React Standards (Frontend)**

### **Component Structure**
```typescript
// ✅ Functional Components mit TypeScript
import React, { useState, useEffect } from 'react';
import { Task, TaskStatus } from '../types/Task';
import { useTaskStore } from '../stores/taskStore';

interface TaskCardProps {
  task: Task;
  onStatusChange: (taskId: string, status: TaskStatus) => void;
  className?: string;
}

export const TaskCard: React.FC<TaskCardProps> = ({ 
  task, 
  onStatusChange, 
  className = '' 
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const { updateTask } = useTaskStore();

  const handleStatusToggle = () => {
    const newStatus = task.status === 'completed' ? 'open' : 'completed';
    onStatusChange(task.id, newStatus);
  };

  return (
    <div className={`task-card ${className}`}>
      {/* Component content */}
    </div>
  );
};
```

### **Naming Conventions**
```typescript
// ✅ Interfaces/Types
interface UserProfile {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
}

type TaskPriority = 'low' | 'medium' | 'high' | 'critical';

// ✅ Components
const TaskManagementDashboard: React.FC = () => {};
const UserProfileModal: React.FC<UserProfileModalProps> = () => {};

// ✅ Hooks
const useTaskFiltering = () => {};
const useAuthenticationState = () => {};

// ✅ Constants
export const API_ENDPOINTS = {
  TASKS: '/api/v1/tasks',
  USERS: '/api/v1/users',
  AUTH: '/api/v1/auth'
} as const;
```

### **State Management (Zustand)**
```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface TaskStore {
  tasks: Task[];
  filter: TaskFilter;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchTasks: () => Promise<void>;
  addTask: (task: Omit<Task, 'id'>) => Promise<void>;
  updateTask: (id: string, updates: Partial<Task>) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  setFilter: (filter: TaskFilter) => void;
}

export const useTaskStore = create<TaskStore>()(devtools((set, get) => ({
  tasks: [],
  filter: { status: 'all', priority: 'all' },
  isLoading: false,
  error: null,
  
  fetchTasks: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/tasks');
      set({ tasks: response.data, isLoading: false });
    } catch (error) {
      set({ error: 'Fehler beim Laden der Tasks', isLoading: false });
    }
  },
  
  // Weitere Actions...
})));
```

## 🎨 **CSS/Styling Standards**

### **Tailwind CSS Conventions**
```tsx
// ✅ Responsive Design mit Tailwind
const TaskCard = ({ task, priority }) => (
  <div className={
    cn(
      // Base styles
      "rounded-lg border bg-white p-4 shadow-sm transition-all duration-200",
      // Hover states
      "hover:shadow-md hover:scale-[1.02]",
      // Responsive
      "w-full md:w-1/2 lg:w-1/3",
      // Priority-based styling
      priority === 'high' && "border-red-500 bg-red-50",
      priority === 'medium' && "border-yellow-500 bg-yellow-50",
      priority === 'low' && "border-green-500 bg-green-50"
    )
  }>
    {/* Content */}
  </div>
);
```

### **CSS Custom Properties**
```css
/* ✅ Design System Variablen */
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-secondary: #64748b;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Typography */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
}
```

## 🗄️ **Database Standards**

### **SQLAlchemy Models**
```python
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Task(Base):
    """Task Model für Projektaufgaben."""
    __tablename__ = "tasks"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core fields
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="open", index=True)
    priority = Column(Integer, nullable=False, default=3, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign Keys
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # Relationships
    assignee = relationship("User", back_populates="assigned_tasks")
    project = relationship("Project", back_populates="tasks")
    steps = relationship("TaskStep", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
```

### **Migration Standards**
```python
"""Add task priority index

Revision ID: abc123def456
Revises: def456ghi789
Create Date: 2025-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    """Upgrade database schema."""
    # Add index for better query performance
    op.create_index(
        'idx_tasks_priority_status', 
        'tasks', 
        ['priority', 'status'],
        postgresql_using='btree'
    )
    
    # Add new column with default value
    op.add_column('tasks', sa.Column('estimated_hours', sa.Float, nullable=True))

def downgrade() -> None:
    """Downgrade database schema."""
    op.drop_column('tasks', 'estimated_hours')
    op.drop_index('idx_tasks_priority_status', table_name='tasks')
```

## 🧪 **Testing Standards**

### **Unit Tests (pytest)**
```python
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from services.task_service import TaskService
from models.task import Task
from exceptions import TaskNotFoundError

class TestTaskService:
    """Test Suite für TaskService."""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database connection."""
        return Mock()
    
    @pytest.fixture
    def task_service(self, mock_db):
        """TaskService instance mit mocked database."""
        return TaskService(mock_db)
    
    def test_create_task_success(self, task_service, mock_db):
        """Test erfolgreiche Task-Erstellung."""
        # Arrange
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "assignee_id": 1
        }
        expected_task = Task(id=1, **task_data)
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = expected_task
        
        # Act
        result = task_service.create_task(**task_data)
        
        # Assert
        assert result.title == task_data["title"]
        assert result.assignee_id == task_data["assignee_id"]
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_get_task_not_found(self, task_service, mock_db):
        """Test TaskNotFoundError bei nicht existierender Task."""
        # Arrange
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act & Assert
        with pytest.raises(TaskNotFoundError, match="Task mit ID 999 nicht gefunden"):
            task_service.get_task_by_id(999)
```

### **Integration Tests**
```python
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_test_db

client = TestClient(app)

class TestTaskAPI:
    """Integration Tests für Task API."""
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, test_db):
        """Setup test data für jeden Test."""
        # Create test user
        self.test_user = create_test_user(test_db)
        self.auth_headers = get_auth_headers(self.test_user)
        
    def test_create_task_endpoint(self):
        """Test Task-Erstellung über API."""
        task_data = {
            "title": "API Test Task",
            "description": "Created via API",
            "priority": 1
        }
        
        response = client.post(
            "/api/v1/tasks",
            json=task_data,
            headers=self.auth_headers
        )
        
        assert response.status_code == 201
        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        assert created_task["id"] is not None
```

## 📝 **Code Review Guidelines**

### **Review Checklist**

**Funktionalität:**
- [ ] Code erfüllt die Anforderungen
- [ ] Edge Cases sind behandelt
- [ ] Error Handling ist implementiert
- [ ] Performance ist akzeptabel

**Code Qualität:**
- [ ] Code ist selbsterklärend
- [ ] Naming Conventions befolgt
- [ ] Keine Code Duplication
- [ ] SOLID Prinzipien befolgt

**Tests:**
- [ ] Unit Tests vorhanden
- [ ] Test Coverage > 80%
- [ ] Integration Tests bei API Changes
- [ ] Tests sind aussagekräftig

**Sicherheit:**
- [ ] Input Validation implementiert
- [ ] SQL Injection verhindert
- [ ] XSS Schutz vorhanden
- [ ] Sensitive Daten nicht geloggt

### **Review Template**
```markdown
## Code Review: [Feature/Bug Fix Name]

### ✅ Positives
- Saubere Implementierung
- Gute Test-Abdeckung
- Performance-optimiert

### 🔧 Verbesserungsvorschläge
- [ ] Längere Methode in kleinere aufteilen (Zeile 45-80)
- [ ] Type Hints für return value hinzufügen
- [ ] Error Message benutzerfreundlicher gestalten

### ❓ Fragen
- Warum wurde Algorithmus X statt Y gewählt?
- Ist die neue Dependency wirklich notwendig?

### 🚨 Kritische Punkte
- SQL Query auf Zeile 23 anfällig für Injection
- Passwort wird im Log ausgegeben (Zeile 67)

**Gesamtbewertung:** Approve nach Behebung der kritischen Punkte
```

## 🚀 **Performance Guidelines**

### **Database Optimierung**
```python
# ✅ Effiziente Queries
def get_user_tasks_optimized(user_id: int) -> List[Task]:
    """Optimierte Abfrage mit Eager Loading."""
    return db.query(Task)\
        .options(joinedload(Task.assignee))\
        .options(joinedload(Task.project))\
        .filter(Task.assigned_to == user_id)\
        .order_by(Task.priority.desc(), Task.created_at.desc())\
        .all()

# ❌ N+1 Query Problem
def get_user_tasks_inefficient(user_id: int) -> List[Task]:
    tasks = db.query(Task).filter(Task.assigned_to == user_id).all()
    for task in tasks:
        # Triggers additional query for each task
        print(f"Assignee: {task.assignee.name}")
    return tasks
```

### **Frontend Performance**
```typescript
// ✅ Memoization für teure Berechnungen
const TaskList: React.FC<TaskListProps> = ({ tasks, filters }) => {
  const filteredTasks = useMemo(() => {
    return tasks.filter(task => {
      return filters.status === 'all' || task.status === filters.status;
    });
  }, [tasks, filters.status]);
  
  return (
    <div>
      {filteredTasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
};

// ✅ Lazy Loading für große Listen
const TaskCard = lazy(() => import('./TaskCard'));
```

## 📊 **Monitoring & Logging**

### **Structured Logging**
```python
import structlog
from typing import Dict, Any

logger = structlog.get_logger()

class TaskService:
    def create_task(self, task_data: Dict[str, Any]) -> Task:
        logger.info(
            "Task creation started",
            user_id=task_data.get('assigned_to'),
            title=task_data.get('title'),
            priority=task_data.get('priority')
        )
        
        try:
            task = Task(**task_data)
            db.add(task)
            db.commit()
            
            logger.info(
                "Task created successfully",
                task_id=task.id,
                duration_ms=timer.elapsed
            )
            return task
            
        except Exception as e:
            logger.error(
                "Task creation failed",
                error=str(e),
                task_data=task_data,
                exc_info=True
            )
            raise
```

## 🔒 **Security Guidelines**

### **Input Validation**
```python
from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_email: Optional[EmailStr] = None
    priority: int
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Titel darf nicht leer sein')
        if len(v) > 255:
            raise ValueError('Titel zu lang (max. 255 Zeichen)')
        return v.strip()
    
    @validator('priority')
    def priority_must_be_valid(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError('Priorität muss zwischen 1 und 5 liegen')
        return v
```

---

**Diese Standards werden regelmäßig überprüft und aktualisiert.**

*Letzte Aktualisierung: Januar 2025*