from pathlib import Path
from typing import List
from .base import BaseTemplate

class T3Template(BaseTemplate):
    def generate(self):
        """Generate a T3 Stack project."""
        try:
            # Create project using create-t3-app
            cmd = [
                "npx",
                "create-t3-app@latest",
                str(self.project_name),
                "--noGit",  # We'll handle git ourselves
                "--CI",  # Run in CI mode for automated setup
            ]

            # Add feature flags when running in CI mode
            if "NextAuth" in self.features:
                cmd.extend(["--nextAuth", "true"])
            if "Prisma" in self.features:
                cmd.extend(["--prisma", "true"])
            
            # Always include these core features
            cmd.extend([
                "--tailwind", "true",
                "--trpc", "true",
                "--appRouter", "true"
            ])

            success = self._run_command(cmd, cwd=self.target_dir.parent)
            
            if not success:
                return False

            # Create project directory if it doesn't exist
            self._create_directory(self.target_dir)
            
            # Install additional dependencies
            packages = []
            dev_packages = []
            
            if "PWA" in self.features:
                packages.extend([
                    "next-pwa"
                ])
                if not self._setup_pwa():
                    return False
            
            if "Jest" in self.features:
                dev_packages.extend([
                    "@testing-library/react",
                    "@testing-library/jest-dom",
                    "jest",
                    "@types/jest",
                    "ts-jest"
                ])
                if not self._setup_testing():
                    return False
            
            if "tRPC-Sub" in self.features:
                packages.extend([
                    "@trpc/server",
                    "@trpc/client",
                    "ws",
                    "@trpc/react-query"
                ])
                if not self._setup_trpc_subscriptions():
                    return False
            
            # Install packages
            if packages:
                success = self._run_command([
                    "npm",
                    "install",
                    *packages
                ], self.target_dir)
                if not success:
                    return False
            
            if dev_packages:
                success = self._run_command([
                    "npm",
                    "install",
                    "-D",
                    *dev_packages
                ], self.target_dir)
                if not success:
                    return False
            
            # Set up additional configurations
            if not self._setup_config_files():
                return False
            
            return True
        except Exception as e:
            print(f"Error during project generation: {e}")
            self._cleanup()
            return False
    
    def _setup_config_files(self) -> bool:
        """Set up additional configuration files."""
        try:
            # Update tsconfig.json with better defaults
            tsconfig = """{
  "compilerOptions": {
    "target": "es2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "checkJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "~/*": ["./src/*"]
    }
  },
  "include": [
    ".eslintrc.cjs",
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    "**/*.cjs",
    "**/*.mjs"
  ],
  "exclude": ["node_modules"]
}"""
            self._write_file(self.target_dir / "tsconfig.json", tsconfig)
            return True
        except Exception:
            return False
    
    def _setup_pwa(self) -> bool:
        """Set up PWA configuration."""
        try:
            # Create necessary directories
            self._create_directory(self.target_dir / "public")
            
            next_config = """import { withPWA } from 'next-pwa';

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your existing config here
};

export default withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
})(nextConfig);
"""
            self._write_file(self.target_dir / "next.config.mjs", next_config)
            
            manifest = """{
  "name": "T3 App",
  "short_name": "T3 App",
  "description": "Full-stack application built with the T3 Stack",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""
            self._write_file(self.target_dir / "public" / "manifest.json", manifest)
            return True
        except Exception:
            return False
    
    def _setup_testing(self) -> bool:
        """Set up Jest testing configuration."""
        try:
            # Create necessary directories
            self._create_directory(self.target_dir / "src" / "test")
            
            jest_config = """/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^~/(.*)$': '<rootDir>/src/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
};"""
            self._write_file(self.target_dir / "jest.config.js", jest_config)
            
            test_setup = """import '@testing-library/jest-dom';"""
            self._write_file(self.target_dir / "src" / "test" / "setup.ts", test_setup)
            return True
        except Exception:
            return False
    
    def _setup_trpc_subscriptions(self) -> bool:
        """Set up tRPC subscriptions."""
        try:
            # Create necessary directories
            self._create_directory(self.target_dir / "src" / "utils")
            
            ws_context = """import { createWSClient, wsLink } from '@trpc/client';
import { createTRPCNext } from '@trpc/next';
import { type AppRouter } from '~/server/api/root';

const getBaseUrl = () => {
  if (typeof window !== 'undefined') return ''; // browser should use relative url
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`; // SSR should use vercel url
  return `http://localhost:${process.env.PORT ?? 3000}`; // dev SSR should use localhost
};

const getWsUrl = () => {
  if (typeof window !== 'undefined') {
    return `ws://${window.location.host}`;
  }
  return `ws://localhost:${process.env.PORT ?? 3000}`;
};

export const api = createTRPCNext<AppRouter>({
  config() {
    return {
      links: [
        wsLink({
          client: createWSClient({
            url: getWsUrl(),
          }),
        }),
      ],
    };
  },
  ssr: false,
});"""
            self._write_file(self.target_dir / "src" / "utils" / "api.ts", ws_context)
            return True
        except Exception:
            return False 