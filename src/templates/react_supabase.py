from pathlib import Path
from typing import List
from .react import ReactTemplate

class ReactSupabaseTemplate(ReactTemplate):
    def generate(self):
        """Generate a React + Supabase project."""
        # First generate the base React project
        if not super().generate():
            return False
            
        # Install Supabase client
        if not self._run_command([
            "npm",
            "install",
            "@supabase/supabase-js"
        ]):
            return False
        
        try:
            # Create Supabase client configuration
            self._setup_supabase_client()
            
            # Add selected Supabase features
            if "Authentication" in self.features:
                self._setup_auth()
                
            if "Database Helpers" in self.features:
                self._setup_database_helpers()
                
            if "Storage Helpers" in self.features:
                self._setup_storage_helpers()
                
            return True
        except Exception:
            self._cleanup()
            return False
    
    def _setup_supabase_client(self):
        """Set up Supabase client configuration."""
        # Create src directory if it doesn't exist
        src_dir = self.target_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        # Create .env file
        env_content = """VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_ANON_KEY=your-anon-key
"""
        self._write_file(self.target_dir / ".env", env_content)
        
        # Create Supabase client file
        client_content = """import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
"""
        self._write_file(self.target_dir / "src" / "supabase.ts", client_content)
    
    def _setup_auth(self):
        """Set up authentication components."""
        # Create Auth context
        auth_context = """import { createContext, useContext, useState, useEffect } from 'react'
import { supabase } from './supabase'
import type { User } from '@supabase/supabase-js'

const AuthContext = createContext<{
  user: User | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}>({
  user: null,
  signIn: async () => {},
  signOut: async () => {},
})

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) throw error
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
  }

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
"""
        self._write_file(self.target_dir / "src" / "auth.tsx", auth_context)
    
    def _setup_database_helpers(self):
        """Set up database helper functions."""
        db_helpers = """import { supabase } from './supabase'

export async function fetchData<T>(
  table: string,
  query: { [key: string]: any } = {}
): Promise<T[]> {
  let queryBuilder = supabase.from(table).select('*')
  
  Object.entries(query).forEach(([key, value]) => {
    queryBuilder = queryBuilder.eq(key, value)
  })
  
  const { data, error } = await queryBuilder
  
  if (error) throw error
  return data as T[]
}

export async function insertData<T>(
  table: string,
  data: Partial<T>
): Promise<T> {
  const { data: inserted, error } = await supabase
    .from(table)
    .insert(data)
    .select()
    .single()
    
  if (error) throw error
  return inserted as T
}

export async function updateData<T>(
  table: string,
  id: string | number,
  data: Partial<T>
): Promise<T> {
  const { data: updated, error } = await supabase
    .from(table)
    .update(data)
    .eq('id', id)
    .select()
    .single()
    
  if (error) throw error
  return updated as T
}

export async function deleteData(
  table: string,
  id: string | number
): Promise<void> {
  const { error } = await supabase
    .from(table)
    .delete()
    .eq('id', id)
    
  if (error) throw error
}
"""
        self._write_file(self.target_dir / "src" / "db.ts", db_helpers)
    
    def _setup_storage_helpers(self):
        """Set up storage helper functions."""
        storage_helpers = """import { supabase } from './supabase'

export async function uploadFile(
  bucket: string,
  path: string,
  file: File
): Promise<string> {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file)
    
  if (error) throw error
  return data.path
}

export async function downloadFile(
  bucket: string,
  path: string
): Promise<string> {
  const { data, error } = await supabase.storage
    .from(bucket)
    .download(path)
    
  if (error) throw error
  return URL.createObjectURL(data)
}

export async function deleteFile(
  bucket: string,
  path: string
): Promise<void> {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path])
    
  if (error) throw error
}

export function getPublicUrl(
  bucket: string,
  path: string
): string {
  const { data } = supabase.storage
    .from(bucket)
    .getPublicUrl(path)
    
  return data.publicUrl
}
"""
        self._write_file(self.target_dir / "src" / "storage.ts", storage_helpers) 