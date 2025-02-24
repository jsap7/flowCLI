from pathlib import Path
from typing import List
from .base import BaseTemplate

class FastAPITemplate(BaseTemplate):
    def generate(self):
        """Generate a FastAPI project."""
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
            self._setup_poetry()
        else:
            self._setup_requirements()
        
        # Create main FastAPI application
        self._setup_main_app()
        
        # Set up database with SQLAlchemy if selected
        if "SQLAlchemy" in self.features:
            self._setup_database()
            
            if "Alembic" in self.features:
                self._setup_alembic()
        
        # Set up authentication if selected
        if "JWT" in self.features:
            self._setup_auth()
        
        # Set up Docker if selected
        if "Docker" in self.features:
            self._setup_docker()
        
        # Set up Prometheus metrics if selected
        if "Prometheus" in self.features:
            self._setup_metrics()
        
        # Set up API documentation if selected
        if "API-Docs" in self.features:
            self._setup_api_docs()
        
        return True
    
    def _setup_poetry(self):
        """Set up Poetry for dependency management."""
        # Initialize Poetry
        self._run_command(["poetry", "init", "--no-interaction"], self.target_dir)
        
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
        self._run_command(["poetry", "add", *dependencies], self.target_dir)
        self._run_command(["poetry", "add", "--group", "dev", *dev_dependencies], self.target_dir)
    
    def _setup_requirements(self):
        """Set up requirements.txt."""
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
    
    def _setup_main_app(self):
        """Set up the main FastAPI application."""
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
    
    def _setup_database(self):
        """Set up SQLAlchemy database configuration."""
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
    
    def _setup_alembic(self):
        """Set up Alembic migrations."""
        # Initialize Alembic
        self._run_command(["alembic", "init", "migrations"], self.target_dir)
        
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
    
    def _setup_auth(self):
        """Set up JWT authentication."""
        auth_utils = """from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Security configuration
SECRET_KEY = "your-secret-key"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Get user from database here
    return username
"""
        self._write_file(self.target_dir / "src" / "core" / "auth.py", auth_utils)
    
    def _setup_docker(self):
        """Set up Docker configuration."""
        dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Run the application
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        self._write_file(self.target_dir / "Dockerfile", dockerfile)
        
        docker_compose = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:password@db/dbname
    depends_on:
      - db
    
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
        self._write_file(self.target_dir / "docker-compose.yml", docker_compose)
    
    def _setup_metrics(self):
        """Set up Prometheus metrics."""
        metrics_config = """from prometheus_fastapi_instrumentator import Instrumentator

def setup_metrics(app):
    Instrumentator().instrument(app).expose(app)
"""
        self._write_file(self.target_dir / "src" / "core" / "metrics.py", metrics_config)
    
    def _setup_api_docs(self):
        """Set up enhanced API documentation."""
        openapi_config = """from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="FastAPI App",
        version="1.0.0",
        description="Modern FastAPI application with SQLAlchemy and auto-docs",
        routes=app.routes,
    )
    
    # Custom documentation settings
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
"""
        self._write_file(self.target_dir / "src" / "core" / "docs.py", openapi_config) 