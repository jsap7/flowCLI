from pathlib import Path
from typing import List
from .base import BaseTemplate

class FastAPITemplate(BaseTemplate):
    def generate(self):
        """Generate a FastAPI project."""
        try:
            # Create project structure
            src_dir = self.target_dir / "src"
            tests_dir = self.target_dir / "tests"
            
            for dir in [
                src_dir,
                tests_dir,
                src_dir / "api",
                src_dir / "core",
                src_dir / "db",
                src_dir / "models",
                src_dir / "schemas",
                src_dir / "services",
            ]:
                self._create_directory(dir)
            
            # Set up Poetry if selected
            if "Poetry" in self.features:
                if not self._setup_poetry():
                    self._cleanup()
                    return False
            else:
                if not self._setup_requirements():
                    self._cleanup()
                    return False
            
            # Create main FastAPI application
            if not self._setup_main_app():
                self._cleanup()
                return False
            
            # Set up database with SQLAlchemy if selected
            if "SQLAlchemy" in self.features:
                if not self._setup_database():
                    self._cleanup()
                    return False
                
                if "Alembic" in self.features:
                    if not self._setup_alembic():
                        self._cleanup()
                        return False
            
            # Set up authentication if selected
            if "JWT" in self.features:
                if not self._setup_auth():
                    self._cleanup()
                    return False
            
            # Set up Docker if selected
            if "Docker" in self.features:
                if not self._setup_docker():
                    self._cleanup()
                    return False
            
            # Set up Prometheus metrics if selected
            if "Prometheus" in self.features:
                if not self._setup_metrics():
                    self._cleanup()
                    return False
            
            # Set up API documentation if selected
            if "API-Docs" in self.features:
                if not self._setup_api_docs():
                    self._cleanup()
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error during project generation: {e}")
            self._cleanup()
            return False
    
    def _setup_poetry(self) -> bool:
        """Set up Poetry for dependency management."""
        try:
            # Initialize Poetry
            if not self._run_command(["poetry", "init", "--no-interaction"]):
                return False
            
            # Add dependencies
            dependencies = [
                "fastapi",
                "uvicorn[standard]",
                "pydantic[email]",
                "python-dotenv",
            ]
            
            if "SQLAlchemy" in self.features:
                dependencies.extend([
                    "sqlalchemy",
                    "asyncpg",  # For PostgreSQL
                ])
            
            if "JWT" in self.features:
                dependencies.extend([
                    "python-jose[cryptography]",
                    "passlib[bcrypt]",
                ])
            
            if "Prometheus" in self.features:
                dependencies.append("prometheus-fastapi-instrumentator")
            
            # Add development dependencies
            dev_dependencies = [
                "black",
                "flake8",
                "pytest",
                "pytest-asyncio",
                "httpx",
            ]
            
            # Install dependencies
            if not self._run_command(["poetry", "add", *dependencies]):
                return False
            if not self._run_command(["poetry", "add", "--group", "dev", *dev_dependencies]):
                return False
            
            return True
        except Exception:
            return False
    
    def _setup_requirements(self) -> bool:
        """Set up requirements.txt."""
        try:
            requirements = """fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic[email]>=2.0.0
python-dotenv>=1.0.0
"""
            if "SQLAlchemy" in self.features:
                requirements += """sqlalchemy>=2.0.0
asyncpg>=0.28.0  # For PostgreSQL
"""
            
            if "JWT" in self.features:
                requirements += """python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
"""
            
            if "Prometheus" in self.features:
                requirements += "prometheus-fastapi-instrumentator>=6.0.0\n"
            
            self._write_file(self.target_dir / "requirements.txt", requirements)
            
            # Development requirements
            dev_requirements = """black>=23.0.0
flake8>=6.0.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
"""
            self._write_file(self.target_dir / "requirements-dev.txt", dev_requirements)
            
            return True
        except Exception:
            return False
    
    def _setup_main_app(self) -> bool:
        """Set up the main FastAPI application."""
        try:
            main_app = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI App",
    description="Modern FastAPI application with SQLAlchemy and auto-docs",
    version="1.0.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""
            self._write_file(self.target_dir / "src" / "main.py", main_app)
            return True
        except Exception:
            return False
    
    def _setup_database(self) -> bool:
        """Set up SQLAlchemy database configuration."""
        try:
            db_config = """from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

# Create async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/dbname",
    echo=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
"""
            self._write_file(self.target_dir / "src" / "db" / "database.py", db_config)
            
            # Create example model
            example_model = """from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ..db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
"""
            self._write_file(self.target_dir / "src" / "models" / "user.py", example_model)
            return True
        except Exception:
            return False
    
    def _setup_alembic(self) -> bool:
        """Set up Alembic migrations."""
        try:
            # Initialize Alembic
            if not self._run_command(["alembic", "init", "migrations"]):
                return False
            
            # Update alembic.ini
            alembic_ini = """[alembic]
script_location = migrations
sqlalchemy.url = postgresql+asyncpg://user:password@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
            self._write_file(self.target_dir / "alembic.ini", alembic_ini)
            return True
        except Exception:
            return False
    
    def _setup_auth(self) -> bool:
        """Set up JWT authentication."""
        try:
            auth_utils = """from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# JWT configuration
SECRET_KEY = "your-secret-key"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
"""
            self._write_file(self.target_dir / "src" / "core" / "auth.py", auth_utils)
            return True
        except Exception:
            return False
    
    def _setup_docker(self) -> bool:
        """Set up Docker configuration."""
        try:
            # Create Dockerfile
            dockerfile = """FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            self._write_file(self.target_dir / "Dockerfile", dockerfile)
            
            # Create docker-compose.yml
            compose = """version: '3.8'

services:
  web:
    build: .
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=fastapi
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
"""
            self._write_file(self.target_dir / "docker-compose.yml", compose)
            return True
        except Exception:
            return False
    
    def _setup_metrics(self) -> bool:
        """Set up Prometheus metrics."""
        try:
            metrics_config = """from prometheus_fastapi_instrumentator import Instrumentator

def setup_metrics(app):
    Instrumentator().instrument(app).expose(app)
"""
            self._write_file(self.target_dir / "src" / "core" / "metrics.py", metrics_config)
            return True
        except Exception:
            return False
    
    def _setup_api_docs(self) -> bool:
        """Set up API documentation."""
        try:
            # Update main.py to include better OpenAPI configuration
            main_app = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI App",
        version="1.0.0",
        description="Modern FastAPI application with SQLAlchemy and auto-docs",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
"""
            self._write_file(self.target_dir / "src" / "main.py", main_app)
            return True
        except Exception:
            return False 