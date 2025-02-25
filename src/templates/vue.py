from pathlib import Path
from typing import List
from .base import BaseTemplate

class VueTemplate(BaseTemplate):
    def generate(self):
        """Generate a Vue 3 project using Vite."""
        # Create project using create-vue in the parent directory
        parent_dir = self.target_dir.parent
        
        # Ensure parent directory exists
        parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Build create-vue command with selected features
        cmd = [
            "npm",
            "create",
            "vue@latest",
            str(self.project_name),
            "--",
            "--typescript" if "TypeScript" in self.features else "",
            "--jsx" if "JSX" in self.features else "",
            "--router" if "Vue Router" in self.features else "",
            "--pinia" if "Pinia" in self.features else "",
            "--vitest" if "Vitest" in self.features else "",
            "--cypress" if "Cypress" in self.features else "",
            "--eslint" if "ESLint" in self.features else "",
            "--prettier" if "Prettier" in self.features else "",
        ]
        
        # Filter out empty strings
        cmd = [arg for arg in cmd if arg]
        
        success = self._run_command(cmd, cwd=parent_dir)
        if not success:
            return False
        
        # Install dependencies
        self._run_command(["npm", "install"], self.target_dir)
        
        # Add additional features
        if "Tailwind CSS" in self.features:
            self._setup_tailwind()
            
        if "PWA" in self.features:
            self._setup_pwa()
            
        if "i18n" in self.features:
            self._setup_i18n()
        
        return True
    
    def _setup_tailwind(self):
        """Set up Tailwind CSS."""
        # Create src directory if it doesn't exist
        src_dir = self.target_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        # Add Tailwind CSS configuration
        css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
        self._write_file(self.target_dir / "src" / "style.css", css_content)
        
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
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        self._write_file(self.target_dir / "tailwind.config.js", config_content)
    
    def _setup_pwa(self):
        """Set up PWA support."""
        # Install Vite PWA plugin
        self._run_command([
            "npm",
            "install",
            "-D",
            "vite-plugin-pwa"
        ])
        
        # Update vite.config.ts/js
        vite_config = """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'Vue App',
        short_name: 'Vue',
        description: 'Vue 3 application with PWA support',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ]
})
"""
        self._write_file(
            self.target_dir / ("vite.config.ts" if "TypeScript" in self.features else "vite.config.js"),
            vite_config
        )
    
    def _setup_i18n(self):
        """Set up Vue I18n for internationalization."""
        # Install Vue I18n
        self._run_command([
            "npm",
            "install",
            "vue-i18n@9"
        ])
        
        # Create i18n configuration
        i18n_config = """import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    message: {
      hello: 'Hello World'
    }
  },
  es: {
    message: {
      hello: 'Hola Mundo'
    }
  }
}

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages,
})
"""
        self._write_file(
            self.target_dir / "src" / "i18n" / ("index.ts" if "TypeScript" in self.features else "index.js"),
            i18n_config
        )
        
        # Update main.ts/js to use i18n
        main_content = """import { createApp } from 'vue'
import App from './App.vue'
import { i18n } from './i18n'

const app = createApp(App)
app.use(i18n)
app.mount('#app')
"""
        self._write_file(
            self.target_dir / "src" / ("main.ts" if "TypeScript" in self.features else "main.js"),
            main_content
        ) 