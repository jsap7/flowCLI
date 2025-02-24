from pathlib import Path
from typing import List
from .base import BaseTemplate

class NextjsTemplate(BaseTemplate):
    def generate(self):
        """Generate a Next.js project."""
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
            self._setup_pwa()
        
        if "MongoDB" in self.features:
            packages.extend([
                "@prisma/client",
                "prisma"
            ])
            self._setup_mongodb()
        
        if packages:
            self._run_command([
                "npm",
                "install",
                "-D",
                *packages
            ], self.target_dir)
        
        # Set up configuration files
        self._setup_config_files()
        
        return True
    
    def _setup_config_files(self):
        """Set up configuration files for the project."""
        if "Prettier" in self.features:
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
    
    def _setup_pwa(self):
        """Set up PWA configuration."""
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
    
    def _setup_mongodb(self):
        """Set up MongoDB with Prisma."""
        # Initialize Prisma
        self._run_command(["npx", "prisma", "init"], self.target_dir)
        
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