# Project Structure

## AI Mindful Eating Agent - Complete Directory Layout

**Last Updated**: November 25, 2025

---

## 📁 Root Directory

```
ai-mindful-eating-agent/
│
├── 📄 README.md                    # Main project documentation
├── 📄 PROJECT_STRUCTURE.md         # This file - directory layout
├── 📄 SUBMISSION_CHECKLIST.md      # Final submission checklist
├── 📄 .gitignore                   # Git ignore rules
├── 📄 start-fullstack.cmd          # Windows startup script
│
├── 📂 backend/                     # Backend application
│   ├── 📄 app.py                   # Flask application entry point
│   ├── 📄 agent.py                 # LangGraph agent logic
│   ├── 📄 agent_chat.py            # Conversational agent
│   ├── 📄 agent_gemini.py          # Gemini AI integration
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 .env                     # Environment variables (not in git)
│   ├── 📄 start.cmd                # Backend-only startup script
│   ├── 📄 setup.cmd                # Setup script
│   ├── 📄 run.cmd                  # Run script
│   │
│   ├── 📂 api/                     # External API endpoints
│   │   ├── 📄 __init__.py
│   │   └── 📄 external.py          # Supervisor integration API
│   │
│   ├── 📂 config/                  # Configuration files
│   │   └── 📄 settings.py
│   │
│   ├── 📂 data/                    # Static data files
│   │   └── 📄 food_database.json   # Static food nutrition data
│   │
│   ├── 📂 utils/                   # Utility modules
│   │   ├── 📄 __init__.py
│   │   ├── 📄 chromadb_client.py   # ChromaDB operations
│   │   ├── 📄 gemini_nutrition.py  # Gemini AI nutrition lookup
│   │   ├── 📄 nutrition_cache.py   # Smart caching system
│   │   └── 📄 chroma_session.py    # Session management
│   │
│   ├── 📂 templates/               # HTML templates (Jinja2)
│   │   ├── 📄 base.html            # Base template
│   │   ├── 📄 login.html           # Login page
│   │   ├── 📄 register.html        # Registration page
│   │   ├── 📄 chat.html            # Chat interface
│   │   └── 📄 calendar.html        # Calendar view
│   │
│   ├── 📂 static/                  # Static assets
│   │   ├── 📂 css/
│   │   │   └── 📄 style.css        # Main stylesheet
│   │   ├── 📂 js/
│   │   │   └── 📄 app.js           # Frontend JavaScript
│   │   └── 📂 images/
│   │       └── 📄 logo.png
│   │
│   ├── 📂 chroma_data/             # ChromaDB storage (not in git)
│   │   └── (vector database files)
│   │
│   ├── 📂 chat_logs/               # Chat interaction logs (not in git)
│   │   └── (JSON log files)
│   │
│   └── 📂 venv39/                  # Python virtual environment (not in git)
│       └── (Python packages)
│
├── 📂 docs/                        # Documentation
│   ├── 📄 ARCHITECTURE.md          # System architecture documentation
│   ├── 📄 API.md                   # Complete API reference
│   ├── 📄 PROJECT_SUMMARY.md       # Quick reference guide
│   ├── 📄 CHROMADB_SETUP.md        # ChromaDB setup guide
│   ├── 📄 GEMINI_INTEGRATION.md    # Gemini AI integration guide
│   ├── 📄 MIGRATION_COMPLETE.md    # Migration documentation
│   ├── 📄 SETUP_GUIDE.md           # Setup instructions
│   ├── 📄 REPORT_ARTIFACTS.md      # Report artifacts index
│   │
│   ├── 📄 final_report.tex         # LaTeX source for report
│   ├── 📄 final_report.pdf         # Compiled final report
│   ├── 📄 final_report.aux         # LaTeX auxiliary files
│   ├── 📄 final_report.toc
│   ├── 📄 final_report.out
│   ├── 📄 final_report.log
│   │
│   ├── 📄 slides.tex               # Presentation slides (LaTeX)
│   │
│   ├── 📄 network_diagram_image.png
│   ├── 📄 wbs_img_1.png
│   ├── 📄 wbs_img_2.png
│   ├── 📄 costEst-1.png
│   ├── 📄 costEst-2.png
│   ├── 📄 costEst-3.png
│   ├── 📄 earnedVal-1.png
│   ├── 📄 earnedVal-2.png
│   ├── 📄 earnedVal-3.png
│   │
│   └── 📂 Assignment04/            # Project management artifacts
│       ├── 📄 README.md
│       ├── 📄 Assignment04_Report.md
│       ├── 📄 COVER_PAGE.md
│       ├── 📄 DELIVERABLES_CHECKLIST.md
│       ├── 📄 FINAL_SUBMISSION_CHECKLIST.md
│       │
│       ├── 📄 Assignment04_Final_Report.tex
│       ├── 📄 Assignment04_Final_Report.pdf
│       ├── 📄 Assignment04_Final_Report.aux
│       ├── 📄 Assignment04_Final_Report.toc
│       ├── 📄 Assignment04_Final_Report.out
│       ├── 📄 Assignment04_Final_Report.log
│       │
│       ├── 📄 updated_wbs.csv
│       ├── 📄 updated_wbs.drawio
│       ├── 📄 updated_wbs.drawio.png
│       │
│       ├── 📄 updated_schedule.csv
│       ├── 📄 gantt_chart_visio.csv
│       ├── 📄 GanttChartUpdated.png
│       │
│       ├── 📄 updated_network_diagram.txt
│       ├── 📄 updated_network_diagram.drawio
│       ├── 📄 updated_network_diagram.png
│       │
│       ├── 📄 resource_assignment_matrix.csv
│       ├── 📄 initial_resource_loading.csv
│       ├── 📄 leveled_resource_loading.csv
│       ├── 📄 resource_conflicts_analysis.md
│       │
│       ├── 📄 initial_individual_histograms.png
│       ├── 📄 leveled_individual_histograms.png
│       ├── 📄 project_level_comparison.png
│       ├── 📄 stacked_comparison.png
│       │
│       ├── 📄 generate_histograms.py
│       ├── 📄 compile_report.bat
│       └── 📄 README_LATEX.md
│
└── 📂 tests/                       # Test suite
    ├── 📄 test_chromadb.py         # ChromaDB tests
    ├── 📄 test_integration.py      # Integration tests
    ├── 📄 test_simple.py           # Simple unit tests
    ├── 📄 test_local_chroma.py     # Local ChromaDB tests
    └── 📄 test_imports.py          # Import validation tests
```

---

## 📊 File Count Summary

| Category | Count | Description |
|----------|-------|-------------|
| **Python Files** | 15+ | Application code, agents, utilities |
| **Documentation** | 10+ | Markdown and LaTeX documents |
| **Templates** | 5 | HTML templates for web interface |
| **Tests** | 5 | Test files for validation |
| **Config Files** | 5 | Environment, requirements, gitignore |
| **PM Artifacts** | 20+ | WBS, Gantt, network diagrams, etc. |
| **Images** | 15+ | Diagrams, charts, screenshots |
| **Scripts** | 4 | Startup and setup scripts |

**Total Files**: ~80+ (excluding virtual environment and generated files)

---

## 🔑 Key Files Description

### Root Level

| File | Purpose | Size |
|------|---------|------|
| `README.md` | Main project documentation, installation guide | ~15 KB |
| `start-fullstack.cmd` | One-command startup script for Windows | ~3 KB |
| `.gitignore` | Git ignore rules for Python, databases, etc. | ~1 KB |
| `SUBMISSION_CHECKLIST.md` | Final submission verification | ~10 KB |
| `PROJECT_STRUCTURE.md` | This file - directory layout | ~8 KB |

### Backend Core

| File | Purpose | Lines of Code |
|------|---------|---------------|
| `app.py` | Flask application, routes, API endpoints | ~900 |
| `agent.py` | LangGraph agent orchestration | ~400 |
| `agent_chat.py` | Conversational agent logic | ~300 |
| `agent_gemini.py` | Gemini AI integration | ~200 |
| `requirements.txt` | Python dependencies | ~15 |

### Backend Utilities

| File | Purpose | Lines of Code |
|------|---------|---------------|
| `chromadb_client.py` | ChromaDB operations (CRUD) | ~500 |
| `gemini_nutrition.py` | Gemini AI nutrition lookup | ~250 |
| `nutrition_cache.py` | 3-tier caching system | ~200 |
| `chroma_session.py` | Custom session interface | ~150 |

### Documentation

| File | Purpose | Pages/Size |
|------|---------|------------|
| `docs/final_report.pdf` | Complete project report | ~18 pages |
| `docs/ARCHITECTURE.md` | System architecture details | ~50 KB |
| `docs/API.md` | Complete API reference | ~40 KB |
| `docs/PROJECT_SUMMARY.md` | Quick reference guide | ~15 KB |

### Project Management

| File | Purpose | Format |
|------|---------|--------|
| `updated_wbs.csv` | Work Breakdown Structure | CSV |
| `updated_schedule.csv` | Project schedule | CSV |
| `GanttChartUpdated.png` | Gantt chart visualization | PNG |
| `updated_network_diagram.png` | Network diagram | PNG |
| `resource_assignment_matrix.csv` | RACI matrix | CSV |

---

## 🎯 Important Directories

### `/backend/`
**Purpose**: Main application code  
**Key Files**: `app.py`, `agent.py`, `requirements.txt`  
**Size**: ~50 MB (with virtual environment)  
**Excluded from Git**: `venv39/`, `chroma_data/`, `chat_logs/`, `.env`

### `/docs/`
**Purpose**: All documentation and reports  
**Key Files**: `final_report.pdf`, `ARCHITECTURE.md`, `API.md`  
**Size**: ~20 MB (with images)  
**Included in Git**: All files except LaTeX auxiliary files

### `/tests/`
**Purpose**: Test suite for validation  
**Key Files**: `test_integration.py`, `test_chromadb.py`  
**Size**: ~100 KB  
**Included in Git**: All test files

### `/docs/Assignment04/`
**Purpose**: Project management artifacts  
**Key Files**: WBS, Gantt, network diagrams, resource analysis  
**Size**: ~10 MB  
**Included in Git**: All files

---

## 🚫 Excluded from Git

### Large Files
- `backend/venv39/` - Virtual environment (~200 MB)
- `backend/chroma_data/` - Database files (~50 MB)

### Generated Files
- `backend/chat_logs/` - Runtime logs
- `*.pyc`, `__pycache__/` - Python bytecode
- `*.aux`, `*.toc`, `*.out` - LaTeX auxiliary files

### Sensitive Files
- `backend/.env` - Environment variables with API keys

---

## 📦 Submission Package Structure

### For ZIP Submission

```
ai-mindful-eating-agent.zip
│
├── backend/                # All source code
│   ├── (exclude venv39/)
│   ├── (exclude chroma_data/)
│   ├── (exclude chat_logs/)
│   └── (exclude .env - provide .env.example)
│
├── docs/                   # All documentation
│   └── (include all files)
│
├── tests/                  # All test files
│   └── (include all files)
│
├── README.md
├── start-fullstack.cmd
├── .gitignore
├── SUBMISSION_CHECKLIST.md
└── PROJECT_STRUCTURE.md
```

**Estimated ZIP Size**: ~15-20 MB

### For GitHub Submission

**Repository URL**: `https://github.com/your-org/ai-mindful-eating-agent`

**Branches**:
- `main` - Production-ready code
- `development` - Development branch
- `feature/*` - Feature branches

**Tags**:
- `v1.0-final-submission` - Final submission version

---

## 🔍 File Search Quick Reference

### Find a specific file type:

**Python files**:
```bash
find . -name "*.py" -not -path "*/venv39/*"
```

**Documentation**:
```bash
find docs/ -name "*.md"
```

**Tests**:
```bash
find tests/ -name "test_*.py"
```

**Images**:
```bash
find docs/ -name "*.png"
```

---

## 📈 Code Statistics

### Lines of Code (excluding comments and blank lines)

| Component | Lines | Percentage |
|-----------|-------|------------|
| Flask Application | ~900 | 35% |
| LangGraph Agents | ~900 | 35% |
| Utilities | ~1,100 | 43% |
| Tests | ~500 | 19% |
| **Total** | **~2,600** | **100%** |

### File Type Distribution

| Type | Count | Percentage |
|------|-------|------------|
| Python (.py) | 20 | 25% |
| Markdown (.md) | 15 | 19% |
| Images (.png) | 15 | 19% |
| CSV (.csv) | 8 | 10% |
| HTML (.html) | 5 | 6% |
| LaTeX (.tex) | 3 | 4% |
| Other | 14 | 17% |
| **Total** | **80** | **100%** |

---

## 🛠️ Maintenance

### Adding New Files

**Python Module**:
```
backend/utils/new_module.py
```

**Test File**:
```
tests/test_new_feature.py
```

**Documentation**:
```
docs/NEW_FEATURE.md
```

### Updating Structure

1. Update this file (`PROJECT_STRUCTURE.md`)
2. Update `.gitignore` if needed
3. Update `README.md` if structure changes affect setup
4. Commit changes with descriptive message

---

## 📝 Notes

### Virtual Environment
- **Location**: `backend/venv39/`
- **Python Version**: 3.9.13
- **Size**: ~200 MB
- **Excluded from Git**: Yes
- **Recreate with**: `python3.9 -m venv backend/venv39`

### Database
- **Type**: ChromaDB (Vector Database)
- **Location**: `backend/chroma_data/`
- **Size**: ~50 MB (grows with usage)
- **Excluded from Git**: Yes
- **Recreate**: Automatically on first run

### Logs
- **Location**: `backend/chat_logs/`
- **Format**: JSON files
- **Retention**: Manual cleanup
- **Excluded from Git**: Yes

---

## ✅ Structure Validation

### Checklist

- [x] All source code in `backend/`
- [x] All documentation in `docs/`
- [x] All tests in `tests/`
- [x] Root level clean (only essential files)
- [x] `.gitignore` properly configured
- [x] No sensitive files in repository
- [x] No large binary files in repository
- [x] Clear directory hierarchy
- [x] Consistent naming conventions

---

**Document Version**: 1.0  
**Last Updated**: November 25, 2025  
**Maintained by**: Team Mindful Eating
