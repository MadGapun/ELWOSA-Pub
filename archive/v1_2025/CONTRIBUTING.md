# Zu ELWOSA beitragen

Wir freuen uns, dass Sie Interesse daran haben, zu ELWOSA beizutragen! Dieses Dokument enthält Richtlinien für die Mitarbeit am Projekt.

## 🤝 Verhaltenskodex

Durch die Teilnahme an diesem Projekt verpflichten Sie sich, eine respektvolle und inklusive Umgebung für alle Mitwirkenden zu schaffen.

## 🚀 Erste Schritte

1. **Repository forken** auf GitHub
2. **Fork lokal klonen**:
   ```bash
   git clone https://github.com/IHR-BENUTZERNAME/ELWOSA-Pub.git
   cd ELWOSA-Pub
   ```
3. **Upstream Remote hinzufügen**:
   ```bash
   git remote add upstream https://github.com/MadGapun/ELWOSA-Pub.git
   ```

## 🌳 Branching-Strategie

Wir verwenden folgende Branch-Struktur:
- `main` - Produktionsbereiter Code
- `develop` - Integrations-Branch für Features
- `feature/*` - Neue Features
- `bugfix/*` - Fehlerbehebungen
- `hotfix/*` - Kritische Fixes für Produktion

## 📝 Änderungen vornehmen

1. **Feature-Branch erstellen**:
   ```bash
   git checkout -b feature/ihr-feature-name
   ```

2. **Änderungen vornehmen**:
   - Sauberen, lesbaren Code schreiben
   - Bestehenden Code-Stil befolgen
   - Tests für neue Funktionen hinzufügen
   - Dokumentation bei Bedarf aktualisieren

3. **Änderungen committen**:
   ```bash
   git commit -m "feat: neues Feature hinzugefügt"
   ```
   
   Wir befolgen [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` Neues Feature
   - `fix:` Fehlerbehebung
   - `docs:` Dokumentationsänderungen
   - `style:` Code-Stil Änderungen
   - `refactor:` Code-Refactoring
   - `test:` Test-Ergänzungen oder -Änderungen
   - `chore:` Build-Prozess oder Hilfswerkzeug-Änderungen

## 🧪 Testing

Vor dem Einreichen einer PR stellen Sie sicher:
- Alle Tests bestehen: `npm test` und `pytest`
- Keine Linting-Fehler: `npm run lint`
- Code-Coverage wird beibehalten oder verbessert

## 📤 Pull Request einreichen

1. **Zu Ihrem Fork pushen**:
   ```bash
   git push origin feature/ihr-feature-name
   ```

2. **Pull Request erstellen** auf GitHub

3. **PR-Beschreibung** sollte enthalten:
   - Welche Änderungen vorgenommen wurden
   - Warum diese Änderungen notwendig waren
   - Eventuelle Breaking Changes
   - Zugehörige Issue-Nummern

## 👀 Code-Review-Prozess

- PRs benötigen mindestens eine Freigabe
- Alle Feedback-Kommentare bearbeiten
- PRs fokussiert und angemessen groß halten
- PR basierend auf Feedback aktualisieren

## 📋 Entwicklungsumgebung einrichten

### Backend Setup
```bash
cd src/backend
python -m venv venv
source venv/bin/activate  # oder `venv\Scripts\activate` unter Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Frontend Setup
```bash
cd src/frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up -d
```

## 🐛 Issues melden

- GitHub Issues für Bug-Reports und Feature-Requests verwenden
- Bestehende Issues prüfen bevor Sie ein neues erstellen
- Klare Reproduktionsschritte für Bugs angeben
- Relevante Systeminformationen einschließen

## 📚 Dokumentation

- README.md für benutzerseitige Änderungen aktualisieren
- Code-Kommentare für komplexe Logik hinzufügen
- API-Dokumentation für Endpoint-Änderungen aktualisieren
- Beispiele für neue Features einschließen

## ❓ Fragen?

Zögern Sie nicht, ein Issue für Fragen zur Mitwirkung zu öffnen!

---
Vielen Dank für Ihren Beitrag zu ELWOSA! 🎉