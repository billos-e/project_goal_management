# Focus & Flow 🎯

Telegram-based productivity bot with AI coaching using NLU and a TARS persona.

## 📋 Overview

Focus & Flow is a personal productivity assistant that helps you build habits, track goals, and maintain momentum through positive reinforcement (Micro-Wins) and accountability (Success Days). The bot features a humorous/analytical TARS persona and smart "Cooling Algorithm" to respect your mental well-being.

## 🚀 Project Status

**Current Epic:** Epic 1 - Fondations & Cerveau TARS  
**Current Story:** Story 1.1 - Initialisation de l'infrastructure & Cœur FastAPI  
**Status:** ready-for-dev

## 🏗️ Tech Stack

- **Backend:** Python 3.11+ with FastAPI
- **Database:** Supabase (PostgreSQL)
- **AI/NLU:** Google Gemini-1.5-Flash
- **Deployment:** Render (Free Tier)
- **Automation:** GitHub Actions for CRON jobs
- **Interface:** Telegram Bot API

## 🎯 Key Features

- ✅ Habit tracking with custom frequencies
- ✅ Goal management with deadlines
- ✅ NLU intent detection via Gemini
- ✅ Adaptive reminder system
- ✅ "Cooling Algorithm" for mental well-being
- ✅ Success Days & Micro-Wins analytics
- ✅ TARS personality (humorous/analytical)
- ✅ Data export (full sovereignty)

## 📦 Project Structure

```
project_goal_management/
├── app/                    # Application code (Story 1.1+)
├── tests/                  # Test suite
├── docs/                   # Documentation
├── _bmad-output/           # BMAD artifacts (local only)
│   ├── planning-artifacts/     # PRD, Architecture, Epics
│   └── implementation-artifacts/  # Stories, Sprint tracking
├── .github/workflows/      # CI/CD automation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Git
- Supabase account (free tier)
- Render account (free tier)
- Telegram Bot Token

### Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/billos-e/project_goal_management.git
   cd project_goal_management
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run tests:**
   ```bash
   pytest
   ```

## 🔀 Git Workflow

We use **Git Flow** branching strategy:

- `main` - Production-ready releases
- `develop` - Integration branch
- `feature/story-X-Y-description` - Feature development
- `bugfix/issue-ID` - Bug fixes
- `hotfix/issue-ID` - Urgent production fixes

### Working on a Story

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/story-1-1-infrastructure

# Make changes and commit (Conventional Commits)
git add .
git commit -m "feat(infrastructure): initialize FastAPI app"

# Push and create PR
git push -u origin feature/story-1-1-infrastructure
```

See [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md) for detailed workflow.

## 📝 Code Standards

- **Formatting:** Black (line length: 88)
- **Linting:** Pylint (score >8.0)
- **Type Hints:** Required on all functions
- **Docstrings:** Google style with examples
- **Commits:** Conventional Commits format

See [CODE_STYLE.md](./CODE_STYLE.md) for complete guidelines.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_health.py

# Format and lint
black app/
pylint app/
```

## 📚 Documentation

- [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute
- [CODE_STYLE.md](./CODE_STYLE.md) - Code standards
- [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md) - Git workflow
- [GITHUB_SETUP.md](./GITHUB_SETUP.md) - Repository setup guide

### Planning Artifacts

- **PRD:** `_bmad-output/planning-artifacts/prd.md`
- **Architecture:** `_bmad-output/planning-artifacts/architecture.md`
- **Epics:** `_bmad-output/planning-artifacts/epics.md`

### Implementation Tracking

- **Sprint Status:** `_bmad-output/implementation-artifacts/sprint-status.yaml`
- **Current Story:** `_bmad-output/implementation-artifacts/1-1-infrastructure-fastapi.md`

## 🚢 Deployment

Deployment is automated via GitHub Actions and Render:

1. Push to `main` branch triggers production deploy
2. Render reads `Procfile` and `requirements.txt`
3. Environment variables configured in Render dashboard

See Story 1.1 documentation for deployment details.

## 🔒 Environment Variables

Required variables (see `.env.example`):

- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `TELEGRAM_BOT_TOKEN` - Telegram bot token (Story 1.2+)
- `TELEGRAM_WEBHOOK_SECRET` - Webhook validation secret
- `TIMEZONE` - User timezone (default: Europe/Paris)

## 📊 Project Roadmap

### MVP (Phase 1)
- [x] Epic 1: Fondations & Cerveau TARS
  - [ ] Story 1.1: Infrastructure setup
  - [ ] Story 1.2: Telegram webhook
  - [ ] Story 1.3: NLU pipeline
  - [ ] Story 1.4: Self-test diagnostic
- [ ] Epic 2: Gestion des Engagements
- [ ] Epic 3: Cycle de Suivi & Micro-Wins
- [ ] Epic 4: Discipline Adaptive & Cooling
- [ ] Epic 5: Bilan, Analytics & Souveraineté

### Growth (Phase 2)
- Multi-AI routing (Groq, HuggingFace)
- Complete 4-state Cooling system
- Web admin interface

### Vision (Phase 3)
- Voice interaction (Audio I/O)
- Local AI models (Ollama)

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

1. Fork the repository
2. Create feature branch: `feature/story-X-Y-description`
3. Follow code standards (Black, Pylint, type hints)
4. Write tests and ensure they pass
5. Use Conventional Commits format
6. Create Pull Request to `develop`

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **BMAD Method** - Project management framework
- **TARS** - Personality inspiration (Interstellar)
- **Telegram Bot API** - Communication interface
- **Google Gemini** - NLU capabilities
- **Supabase** - Database and backend services

## 📞 Contact

Project maintained by **Billux**

- GitHub: [@billos-e](https://github.com/billos-e)
- Repository: [project_goal_management](https://github.com/billos-e/project_goal_management)

---

**Built with ❤️ using the BMAD Method and Python**
