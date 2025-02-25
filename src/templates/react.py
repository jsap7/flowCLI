from pathlib import Path
from typing import List
from .base import BaseTemplate

class ReactTemplate(BaseTemplate):
    def generate(self):
        """Generate a React project using Vite."""
        # Create project using Vite in the parent directory
        parent_dir = self.target_dir.parent
        template = "react-ts" if "TypeScript" in self.features else "react"
        
        # Ensure parent directory exists
        parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Run create-vite in the parent directory
        success = self._run_command([
            "npm",
            "create",
            "vite@latest",
            str(self.project_name),  # Use string path to avoid Path object issues
            "--",
            "--template",
            template
        ], cwd=parent_dir)
        
        if not success:
            return False
            
        # Install dependencies
        success = self._run_command(["npm", "install"], self.target_dir)
        if not success:
            return False
            
        # Add selected features
        if "Tailwind CSS" in self.features:
            success = self._setup_tailwind()
            if not success:
                return False
            
        if "ESLint" in self.features or "Prettier" in self.features:
            self._setup_linting()
        
        return True
    
    def _setup_tailwind(self):
        """Set up Tailwind CSS."""
        try:
            # Create src directory if it doesn't exist
            src_dir = self.target_dir / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            
            # Add Tailwind CSS configuration
            css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
            self._write_file(self.target_dir / "src" / "index.css", css_content)
            
            # Install Tailwind and its dependencies
            self._run_command([
                "npm",
                "install",
                "-D",
                "tailwindcss",
                "postcss",
                "autoprefixer"
            ])
            
            # Initialize Tailwind
            self._run_command(["npx", "tailwindcss", "init", "-p"])
            
            # Update tailwind.config.js
            config_content = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
            self._write_file(self.target_dir / "tailwind.config.js", config_content)
            return True
        except (PermissionError, OSError):
            return False
    
    def _setup_linting(self):
        """Set up ESLint and Prettier."""
        packages = []
        
        if "ESLint" in self.features:
            packages.extend([
                "eslint",
                "@typescript-eslint/parser",
                "@typescript-eslint/eslint-plugin",
                "eslint-plugin-react",
                "eslint-plugin-react-hooks"
            ])
            
            # Create ESLint config
            eslint_config = """{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true
    },
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": ["react", "@typescript-eslint"],
  "settings": {
    "react": {
      "version": "detect"
    }
  },
  "rules": {}
}"""
            self._write_file(self.target_dir / ".eslintrc.json", eslint_config)
        
        if "Prettier" in self.features:
            packages.extend([
                "prettier",
                "eslint-config-prettier",
                "eslint-plugin-prettier"
            ])
            
            # Create Prettier config
            prettier_config = """{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "tabWidth": 2,
  "useTabs": false
}"""
            self._write_file(self.target_dir / ".prettierrc", prettier_config)
        
        if packages:
            self._run_command([
                "npm",
                "install",
                "-D",
                *packages
            ])
            
            # Add scripts to package.json
            scripts = {
                "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
                "format": "prettier --write \"src/**/*.{ts,tsx}\""
            }
            
            # TODO: Update package.json with new scripts
