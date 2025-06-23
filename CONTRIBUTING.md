# Contributing to ELWOSA

We're excited that you're interested in contributing to ELWOSA! This document provides guidelines for contributing to the project.

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ELWOSA-Pub.git
   cd ELWOSA-Pub
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/MadGapun/ELWOSA-Pub.git
   ```

## 🌳 Branching Strategy

We use the following branch structure:
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical fixes for production

## 📝 Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, readable code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit your changes**:
   ```bash
   git commit -m "feat: add new feature"
   ```
   
   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions or changes
   - `chore:` Build process or auxiliary tool changes

## 🧪 Testing

Before submitting a PR, ensure:
- All tests pass: `npm test` and `pytest`
- No linting errors: `npm run lint`
- Code coverage is maintained or improved

## 📤 Submitting a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub

3. **PR Description** should include:
   - What changes were made
   - Why these changes were necessary
   - Any breaking changes
   - Related issue numbers

## 👀 Code Review Process

- PRs require at least one approval
- Address all feedback comments
- Keep PRs focused and reasonably sized
- Update PR based on feedback

## 📋 Development Setup

### Backend Setup
```bash
cd src/backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
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

## 🐛 Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Check existing issues before creating a new one
- Provide clear reproduction steps for bugs
- Include relevant system information

## 📚 Documentation

- Update README.md for user-facing changes
- Add code comments for complex logic
- Update API documentation for endpoint changes
- Include examples for new features

## ❓ Questions?

Feel free to open an issue for any questions about contributing!

---
Thank you for contributing to ELWOSA! 🎉