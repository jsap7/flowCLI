from pathlib import Path
from typing import List
from .base import BaseTemplate

class NextjsTemplate(BaseTemplate):
    def generate(self):
        """Generate a Next.js project."""
        try:
            # Create project using create-next-app
            success = self._run_command([
                "npx",
                "create-next-app@latest",
                str(self.project_name),
                "--ts" if "TypeScript" in self.features else "--js",
                "--tailwind" if "Tailwind CSS" in self.features else "--no-tailwind",
                "--eslint" if "ESLint" in self.features else "--no-eslint",
                "--app",  # Use App Router
                "--src-dir",  # Use src/ directory
                "--import-alias", "@/*",  # Modern import alias
                "--no-git",  # We'll handle git ourselves
            ], cwd=self.target_dir.parent)
            
            if not success:
                return False
            
            # Install additional dependencies
            packages = []
            
            if "Prettier" in self.features:
                packages.extend([
                    "prettier",
                    "prettier-plugin-tailwindcss",
                    "eslint-config-prettier",
                    "eslint-plugin-prettier"
                ])
            
            if "PWA" in self.features:
                packages.extend([
                    "next-pwa"
                ])
            
            if "MongoDB" in self.features:
                packages.extend([
                    "@prisma/client",
                    "prisma"
                ])
            
            if packages:
                success = self._run_command([
                    "npm",
                    "install",
                    "-D",
                    *packages
                ], self.target_dir)
                
                if not success:
                    return False
            
            # Set up configuration files
            if not self._setup_config_files():
                return False
            
            # Set up PWA if selected
            if "PWA" in self.features:
                if not self._setup_pwa():
                    return False
            
            # Set up MongoDB if selected
            if "MongoDB" in self.features:
                if not self._setup_mongodb():
                    return False
            
            return True
        except Exception as e:
            print(f"Error during project generation: {e}")
            self._cleanup()
            return False
    
    def _setup_config_files(self) -> bool:
        """Set up configuration files for the project."""
        try:
            if "Prettier" in self.features:
                self._create_directory(self.target_dir)
                prettier_config = """{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "plugins": ["prettier-plugin-tailwindcss"]
}"""
                self._write_file(self.target_dir / ".prettierrc", prettier_config)
                
                # Add format scripts to package.json
                # TODO: Update package.json with format scripts
            return True
        except Exception:
            return False
    
    def _setup_pwa(self) -> bool:
        """Set up PWA configuration."""
        try:
            # Create necessary directories
            self._create_directory(self.target_dir / "public")
            
            next_config = """const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development'
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your existing config here
}

module.exports = withPWA(nextConfig)
"""
            self._write_file(self.target_dir / "next.config.js", next_config)
            
            manifest = """{
  "name": "Your App",
  "short_name": "App",
  "description": "Your app description",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""
            self._write_file(self.target_dir / "public" / "manifest.json", manifest)
            return True
        except Exception:
            return False
    
    def _setup_mongodb(self) -> bool:
        """Set up MongoDB with Prisma."""
        try:
            # Create necessary directories
            self._create_directory(self.target_dir / "prisma")
            self._create_directory(self.target_dir / "src" / "lib")
            
            # Initialize Prisma
            success = self._run_command(["npx", "prisma", "init"], self.target_dir)
            if not success:
                return False
            
            # Create basic schema
            schema = """datasource db {
  provider = "mongodb"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

// Add your models here
model Example {
  id        String   @id @default(auto()) @map("_id") @db.ObjectId
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}"""
            self._write_file(self.target_dir / "prisma" / "schema.prisma", schema)
            
            # Create database helper
            db_utils = """import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma"""
            self._write_file(self.target_dir / "src" / "lib" / "db.ts", db_utils)
            return True
        except Exception:
            return False 