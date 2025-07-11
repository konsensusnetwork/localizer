import React, { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import type { User } from '@supabase/supabase-js';
import AuthComponent from './AuthComponent';
import FileUpload from './FileUpload';
import TranslationRuns from './TranslationRuns';

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    // Get initial user
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user);
      setLoading(false);
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const handleAuthChange = (newUser: User | null) => {
    setUser(newUser);
    if (newUser) {
      // Refresh translation runs when user signs in
      setRefreshTrigger(prev => prev + 1);
    }
  };

  const handleTranslationStart = (jobId: string) => {
    // Refresh translation runs when new job starts
    setRefreshTrigger(prev => prev + 1);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="max-w-md mx-auto">
        <AuthComponent onAuthChange={handleAuthChange} />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* User Welcome */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
              <span className="text-white font-medium">
                {user.email?.charAt(0).toUpperCase()}
              </span>
            </div>
            <div>
              <p className="font-medium text-gray-900">Welcome back!</p>
              <p className="text-sm text-gray-600">{user.email}</p>
            </div>
          </div>
          <button
            onClick={() => supabase.auth.signOut()}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Sign Out
          </button>
        </div>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-900">Upload & Translate</h2>
        <FileUpload onTranslationStart={handleTranslationStart} />
      </div>

      {/* Translation Runs */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-6 text-gray-900">Translation History</h2>
        <TranslationRuns refreshTrigger={refreshTrigger} />
      </div>
    </div>
  );
}