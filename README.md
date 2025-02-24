# 🌊 Flow CLI

A modern CLI tool for creating development projects with best practices and common features baked in.

## Features

- 🎯 Interactive project creation with beautiful UI
- 📦 Multiple project templates with modern stack options
- 🛠️ Customizable features per template
- 🚀 Automatic IDE integration (Cursor)
- 🧹 Clean interruption handling (Ctrl+C safe)

## 🎨 Project Templates

### ⚛️ React Frontend
Modern React application with choice of frameworks:
- 📦 Next.js (App Router, SSR, file-based routing)
- ⚡ Vite (Fast SPA development)

Features:
- TypeScript
- Tailwind CSS
- ESLint + Prettier
- PWA Support (Next.js)
- API Routes (Next.js)
- MongoDB + Prisma (Next.js)

### 🚀 T3 Stack
Full-stack application with:
- Next.js (App Router)
- tRPC
- Prisma
- Tailwind CSS
- TypeScript

Optional features:
- NextAuth.js
- PWA Support
- Jest Testing
- tRPC Subscriptions
- Prisma Studio UI

### ⚡ React + Supabase
Full-stack React with Supabase backend:
- All React Frontend features
- Authentication
- Database Helpers
- Storage Helpers
- Real-time subscriptions

### ⚡ FastAPI Backend
Modern Python API with:
- SQLAlchemy ORM
- Pydantic Models
- Auto-generated OpenAPI docs
- JWT Authentication
- pytest
- Black + Flake8

Optional features:
- Poetry dependency management
- Docker setup
- Alembic Migrations
- Prometheus Metrics
- Enhanced API Documentation

### 🛠️ Express API
TypeScript API with:
- Prisma ORM
- OpenAPI/Swagger
- JWT Authentication
- Jest Testing
- ESLint + Prettier

Optional features:
- Docker setup
- Prometheus Metrics
- Rate Limiting

### 🐍 Python Project
Production-ready Python project structure:
- Black (formatter)
- Flake8 (linter)
- pytest
- pre-commit hooks
- Docker setup

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flow.git
cd flow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📝 Usage

Create a new project:
```bash
python -m src.main new project
```

This will start an interactive process where you can:
1. Enter your project name
2. Choose your project template
3. Select framework (for React projects)
4. Configure desired features
5. Automatically open in Cursor

## ⚙️ Configuration

Flow stores its configuration in `~/.flow/config.json`. Current options:
- `dev_folder`: Where to create new projects (default: "~/Development")
- `ide`: Which IDE to open projects in (default: "cursor")

## 🛠️ Development

### Project Structure
```
flow/
├── src/
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── ui.py               # UI components and prompts
│   └── templates/          # Project templates
│       ├── base.py         # Base template class
│       ├── react.py        # React template
│       ├── nextjs.py       # Next.js template
│       ├── t3.py           # T3 Stack template
│       ├── fastapi.py      # FastAPI template
│       ├── express.py      # Express API template
│       ├── python.py       # Python template
│       └── react_supabase.py # React + Supabase
└── requirements.txt        # Python dependencies
```

### Adding New Templates

1. Create a new template class in `src/templates/`
2. Inherit from `BaseTemplate`
3. Implement the `generate()` method
4. Add template to `__init__.py`
5. Update UI choices in `ui.py`

## 📄 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 