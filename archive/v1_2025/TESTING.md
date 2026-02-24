# ELWOSA Testing Strategy

## Überblick

ELWOSA implementiert eine umfassende Testing-Strategie mit automatisierten Tests auf allen Ebenen, um Code-Qualität, Stabilität und Zuverlässigkeit sicherzustellen.

## 🏗️ **Test-Pyramide**

```
                    🔺
                   /   \
               E2E /     \ E2E
                  /       \
              📱 /         \ 🌐
                /_____Tests_____\
               /                 \
              /   Integration     \
             /       Tests        \
            /_____________________\
           /                       \
          /       Unit Tests        \
         /_________________________\
```

### **Test-Verteilung:**
- **70% Unit Tests**: Schnell, isoliert, hohe Abdeckung
- **20% Integration Tests**: API-Endpoints, Service-Integration
- **10% E2E Tests**: Kritische User-Journeys

## 🧪 **Unit Testing**

### **Backend Testing (pytest)**

#### **Test-Setup**
```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test Database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    """Erstellt Test-Datenbank für Session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    """Erstellt isolierte DB-Session für jeden Test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Test-Client mit mocked Database."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

#### **Service Layer Tests**
```python
# test_task_service.py
import pytest
from datetime import datetime
from services.task_service import TaskService
from models.task import Task
from models.user import User
from exceptions import TaskNotFoundError, InsufficientPermissionsError

class TestTaskService:
    """Umfassende Tests für TaskService."""
    
    @pytest.fixture
    def sample_user(self, db_session):
        user = User(id=1, email="test@example.com", name="Test User")
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def sample_task(self, db_session, sample_user):
        task = Task(
            title="Test Task",
            description="Test Description",
            assigned_to=sample_user.id,
            priority=1,
            status="open"
        )
        db_session.add(task)
        db_session.commit()
        return task
    
    def test_create_task_success(self, db_session, sample_user):
        """Test erfolgreiche Task-Erstellung."""
        # Arrange
        service = TaskService(db_session)
        task_data = {
            "title": "New Task",
            "description": "Task Description",
            "assigned_to": sample_user.id,
            "priority": 2
        }
        
        # Act
        result = service.create_task(**task_data)
        
        # Assert
        assert result.id is not None
        assert result.title == task_data["title"]
        assert result.assigned_to == sample_user.id
        assert result.status == "open"  # Default value
        
        # Verify in database
        db_task = db_session.query(Task).filter(Task.id == result.id).first()
        assert db_task is not None
        assert db_task.title == task_data["title"]
    
    def test_create_task_invalid_data(self, db_session):
        """Test Task-Erstellung mit ungültigen Daten."""
        service = TaskService(db_session)
        
        with pytest.raises(ValueError, match="Titel darf nicht leer sein"):
            service.create_task(title="", priority=1)
    
    def test_get_task_by_id_success(self, db_session, sample_task):
        """Test erfolgreiche Task-Abfrage."""
        service = TaskService(db_session)
        
        result = service.get_task_by_id(sample_task.id)
        
        assert result.id == sample_task.id
        assert result.title == sample_task.title
    
    def test_get_task_by_id_not_found(self, db_session):
        """Test TaskNotFoundError bei nicht existierender Task."""
        service = TaskService(db_session)
        
        with pytest.raises(TaskNotFoundError, match="Task mit ID 999 nicht gefunden"):
            service.get_task_by_id(999)
    
    @pytest.mark.asyncio
    async def test_ai_task_creation(self, db_session, sample_user):
        """Test KI-gestützte Task-Erstellung."""
        service = TaskService(db_session)
        
        with patch('services.ai_service.generate_task_details') as mock_ai:
            mock_ai.return_value = {
                "title": "KI-generierte Task",
                "description": "Detaillierte Beschreibung",
                "estimated_hours": 4.5
            }
            
            result = await service.create_task_from_prompt(
                prompt="Erstelle Task für Bug-Fix",
                user_id=sample_user.id
            )
            
            assert "KI-generierte" in result.title
            assert result.estimated_hours == 4.5
            mock_ai.assert_called_once()
```

### **Frontend Testing (Jest + React Testing Library)**

#### **Component Tests**
```typescript
// TaskCard.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskCard } from './TaskCard';
import { Task } from '../types/Task';

const mockTask: Task = {
  id: '1',
  title: 'Test Task',
  description: 'Test Description',
  status: 'open',
  priority: 'high',
  assigneeId: 'user-1',
  createdAt: new Date('2025-01-01')
};

const mockProps = {
  task: mockTask,
  onStatusChange: jest.fn(),
  onEdit: jest.fn(),
  onDelete: jest.fn()
};

describe('TaskCard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('renders task information correctly', () => {
    render(<TaskCard {...mockProps} />);
    
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('Hoch')).toBeInTheDocument(); // Priority in German
  });
  
  it('calls onStatusChange when status button is clicked', async () => {
    const user = userEvent.setup();
    render(<TaskCard {...mockProps} />);
    
    const statusButton = screen.getByRole('button', { name: /status ändern/i });
    await user.click(statusButton);
    
    expect(mockProps.onStatusChange).toHaveBeenCalledWith('1', 'completed');
  });
  
  it('shows edit form when edit button is clicked', async () => {
    const user = userEvent.setup();
    render(<TaskCard {...mockProps} />);
    
    const editButton = screen.getByRole('button', { name: /bearbeiten/i });
    await user.click(editButton);
    
    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /speichern/i })).toBeInTheDocument();
  });
  
  it('applies correct CSS classes for high priority', () => {
    const { container } = render(<TaskCard {...mockProps} />);
    
    const taskCard = container.querySelector('.task-card');
    expect(taskCard).toHaveClass('priority-high');
  });
});
```

#### **Hook Tests**
```typescript
// useTaskStore.test.ts
import { renderHook, act } from '@testing-library/react';
import { useTaskStore } from '../stores/taskStore';
import { api } from '../services/api';

jest.mock('../services/api');
const mockedApi = api as jest.Mocked<typeof api>;

describe('useTaskStore', () => {
  beforeEach(() => {
    // Reset store state
    useTaskStore.setState({
      tasks: [],
      isLoading: false,
      error: null
    });
    jest.clearAllMocks();
  });
  
  it('fetches tasks successfully', async () => {
    const mockTasks = [
      { id: '1', title: 'Task 1', status: 'open' },
      { id: '2', title: 'Task 2', status: 'completed' }
    ];
    
    mockedApi.get.mockResolvedValueOnce({ data: mockTasks });
    
    const { result } = renderHook(() => useTaskStore());
    
    await act(async () => {
      await result.current.fetchTasks();
    });
    
    expect(result.current.tasks).toEqual(mockTasks);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });
  
  it('handles fetch error correctly', async () => {
    mockedApi.get.mockRejectedValueOnce(new Error('Network error'));
    
    const { result } = renderHook(() => useTaskStore());
    
    await act(async () => {
      await result.current.fetchTasks();
    });
    
    expect(result.current.tasks).toEqual([]);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe('Fehler beim Laden der Tasks');
  });
});
```

## 🔗 **Integration Testing**

### **API Integration Tests**
```python
# test_task_api.py
import pytest
from fastapi import status
from httpx import AsyncClient

class TestTaskAPI:
    """Integration Tests für Task API."""
    
    @pytest.fixture
    async def authenticated_client(self, client, test_user):
        """Client mit Authentifizierung."""
        # Login and get token
        login_response = await client.post("/auth/login", json={
            "email": test_user.email,
            "password": "testpassword"
        })
        token = login_response.json()["access_token"]
        
        client.headers.update({"Authorization": f"Bearer {token}"})
        return client
    
    async def test_create_task_endpoint(self, authenticated_client):
        """Test Task-Erstellung über API."""
        task_data = {
            "title": "API Test Task",
            "description": "Created via API",
            "priority": 1
        }
        
        response = await authenticated_client.post("/api/v1/tasks", json=task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        assert created_task["id"] is not None
        assert created_task["status"] == "open"
    
    async def test_get_tasks_with_filter(self, authenticated_client, sample_tasks):
        """Test Task-Abfrage mit Filtern."""
        response = await authenticated_client.get(
            "/api/v1/tasks?status=completed&priority=1"
        )
        
        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        
        # Verify all returned tasks match filter
        for task in tasks:
            assert task["status"] == "completed"
            assert task["priority"] == 1
    
    async def test_unauthorized_access(self, client):
        """Test Zugriff ohne Authentifizierung."""
        response = await client.get("/api/v1/tasks")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

### **Database Integration**
```python
# test_database_integration.py
import pytest
from sqlalchemy import text
from models.task import Task
from models.user import User

class TestDatabaseIntegration:
    """Tests für Datenbank-Integration."""
    
    def test_task_user_relationship(self, db_session):
        """Test Beziehung zwischen Task und User."""
        # Create user
        user = User(email="test@example.com", name="Test User")
        db_session.add(user)
        db_session.commit()
        
        # Create task assigned to user
        task = Task(
            title="Test Task",
            assigned_to=user.id,
            priority=1
        )
        db_session.add(task)
        db_session.commit()
        
        # Test relationship loading
        loaded_task = db_session.query(Task).filter(Task.id == task.id).first()
        assert loaded_task.assignee.email == "test@example.com"
        
        loaded_user = db_session.query(User).filter(User.id == user.id).first()
        assert len(loaded_user.assigned_tasks) == 1
        assert loaded_user.assigned_tasks[0].title == "Test Task"
    
    def test_database_constraints(self, db_session):
        """Test Datenbank-Constraints."""
        # Test NOT NULL constraint
        with pytest.raises(Exception):  # IntegrityError
            task = Task(title=None)  # Title is required
            db_session.add(task)
            db_session.commit()
    
    def test_database_performance(self, db_session):
        """Test Query-Performance."""
        # Create test data
        users = [User(email=f"user{i}@example.com") for i in range(100)]
        db_session.add_all(users)
        db_session.commit()
        
        tasks = [
            Task(title=f"Task {i}", assigned_to=users[i % 10].id)
            for i in range(1000)
        ]
        db_session.add_all(tasks)
        db_session.commit()
        
        # Test efficient query with join
        import time
        start_time = time.time()
        
        result = db_session.execute(text("""
            SELECT t.title, u.email 
            FROM tasks t 
            JOIN users u ON t.assigned_to = u.id 
            WHERE t.priority = 1
        """)).fetchall()
        
        query_time = time.time() - start_time
        
        # Query should complete within reasonable time
        assert query_time < 0.1  # 100ms
        assert len(result) >= 0
```

## 🌐 **End-to-End Testing**

### **Playwright E2E Tests**
```typescript
// e2e/task-management.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'testpassword');
    await page.click('[data-testid="login-button"]');
    
    // Wait for dashboard to load
    await expect(page.locator('[data-testid="dashboard"]')).toBeVisible();
  });
  
  test('should create new task successfully', async ({ page }) => {
    // Navigate to task creation
    await page.click('[data-testid="create-task-button"]');
    
    // Fill task form
    await page.fill('[data-testid="task-title"]', 'E2E Test Task');
    await page.fill('[data-testid="task-description"]', 'Created via E2E test');
    await page.selectOption('[data-testid="task-priority"]', '1');
    
    // Submit form
    await page.click('[data-testid="submit-task"]');
    
    // Verify task appears in task list
    await expect(page.locator('text=E2E Test Task')).toBeVisible();
    
    // Verify success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });
  
  test('should filter tasks by status', async ({ page }) => {
    // Go to task list
    await page.goto('/tasks');
    
    // Apply status filter
    await page.selectOption('[data-testid="status-filter"]', 'completed');
    
    // Wait for filter to apply
    await page.waitForLoadState('networkidle');
    
    // Verify only completed tasks are shown
    const taskCards = page.locator('[data-testid="task-card"]');
    const count = await taskCards.count();
    
    for (let i = 0; i < count; i++) {
      const statusBadge = taskCards.nth(i).locator('[data-testid="task-status"]');
      await expect(statusBadge).toHaveText('Abgeschlossen');
    }
  });
  
  test('should handle task deletion with confirmation', async ({ page }) => {
    await page.goto('/tasks');
    
    // Find first task and click delete
    const firstTask = page.locator('[data-testid="task-card"]').first();
    const taskTitle = await firstTask.locator('[data-testid="task-title"]').textContent();
    
    await firstTask.locator('[data-testid="delete-button"]').click();
    
    // Confirm deletion in dialog
    await expect(page.locator('[data-testid="confirm-dialog"]')).toBeVisible();
    await page.click('[data-testid="confirm-delete"]');
    
    // Verify task is removed
    await expect(page.locator(`text=${taskTitle}`)).not.toBeVisible();
  });
});
```

### **Mobile E2E Tests**
```typescript
// e2e/mobile.spec.ts
import { test, expect, devices } from '@playwright/test';

test.use({ ...devices['iPhone 12'] });

test.describe('Mobile UI Tests', () => {
  test('should have responsive design on mobile', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Check mobile navigation
    await expect(page.locator('[data-testid="mobile-menu-button"]')).toBeVisible();
    
    // Check task cards stack vertically
    const taskCards = page.locator('[data-testid="task-card"]');
    const firstCard = taskCards.first();
    const secondCard = taskCards.nth(1);
    
    const firstBox = await firstCard.boundingBox();
    const secondBox = await secondCard.boundingBox();
    
    // Second card should be below first card (not side by side)
    expect(secondBox?.y).toBeGreaterThan(firstBox?.y + firstBox?.height);
  });
  
  test('should support touch gestures', async ({ page }) => {
    await page.goto('/tasks');
    
    // Test swipe to delete
    const taskCard = page.locator('[data-testid="task-card"]').first();
    
    // Swipe left on task card
    await taskCard.hover();
    await page.mouse.down();
    await page.mouse.move(-100, 0);
    await page.mouse.up();
    
    // Delete button should appear
    await expect(taskCard.locator('[data-testid="swipe-delete"]')).toBeVisible();
  });
});
```

## 🔧 **Test Configuration**

### **pytest.ini**
```ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --durations=10
testpaths = tests
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
    unit: marks tests as unit tests
filterwarnings =
    ignore::UserWarning
    ignore::DeprecationWarning
```

### **Jest Configuration**
```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/test/**/*',
    '!src/**/*.stories.{ts,tsx}'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{ts,tsx}',
    '<rootDir>/src/**/*.{test,spec}.{ts,tsx}'
  ]
};
```

### **Playwright Configuration**
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] }
    }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
});
```

## 📊 **Test Metrics & Reporting**

### **Coverage Reports**
```bash
# Backend Coverage
pytest --cov=src --cov-report=html --cov-report=term

# Frontend Coverage
npm run test:coverage

# E2E Test Reports
npx playwright show-report
```

### **CI/CD Integration**
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
  
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npx playwright test
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

**Diese Testing-Strategie gewährleistet hohe Code-Qualität und Zuverlässigkeit.**

*Letzte Aktualisierung: Januar 2025*