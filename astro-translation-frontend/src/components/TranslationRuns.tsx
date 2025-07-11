import React, { useState, useEffect } from 'react';
import { makeApiCall, getCurrentUserId } from '../lib/supabase';

interface TranslationRun {
  id: string;
  job_id: string;
  book_path: string;
  model: string;
  language: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  created_at: string;
  started_at?: string;
  completed_at?: string;
  error?: string;
  output_file?: string;
  config?: any;
}

interface TranslationRunsProps {
  refreshTrigger?: number;
}

export default function TranslationRuns({ refreshTrigger }: TranslationRunsProps) {
  const [runs, setRuns] = useState<TranslationRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [downloadingJobs, setDownloadingJobs] = useState<Set<string>>(new Set());

  const fetchTranslationRuns = async () => {
    try {
      setError('');
      const userId = await getCurrentUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const response = await makeApiCall(`/translate/user/${userId}/translations?limit=50`);
      setRuns(response.translations || []);
    } catch (error: any) {
      setError(error.message || 'Failed to fetch translation runs');
    } finally {
      setLoading(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    try {
      const userId = await getCurrentUserId();
      if (!userId) return;

      const response = await makeApiCall(`/translate/jobs/${jobId}?user_id=${userId}`);
      
      setRuns(prevRuns => 
        prevRuns.map(run => 
          run.job_id === jobId 
            ? { ...run, status: response.status, completed_at: response.completed_at }
            : run
        )
      );
    } catch (error) {
      console.error('Failed to poll job status:', error);
    }
  };

  const handleDownload = async (jobId: string) => {
    try {
      setDownloadingJobs(prev => new Set(prev).add(jobId));
      
      const userId = await getCurrentUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const response = await makeApiCall(`/translate/download/${jobId}?user_id=${userId}`);
      
      if (response.download_url) {
        // Create a temporary anchor element to trigger download
        const link = document.createElement('a');
        link.href = response.download_url;
        link.download = response.filename || 'translation.txt';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    } catch (error: any) {
      setError(error.message || 'Failed to download file');
    } finally {
      setDownloadingJobs(prev => {
        const newSet = new Set(prev);
        newSet.delete(jobId);
        return newSet;
      });
    }
  };

  const handleDelete = async (jobId: string) => {
    if (!confirm('Are you sure you want to delete this translation job?')) {
      return;
    }

    try {
      const userId = await getCurrentUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      await makeApiCall(`/translate/jobs/${jobId}?user_id=${userId}`, {
        method: 'DELETE'
      });

      setRuns(prevRuns => prevRuns.filter(run => run.job_id !== jobId));
    } catch (error: any) {
      setError(error.message || 'Failed to delete translation job');
    }
  };

  useEffect(() => {
    fetchTranslationRuns();
  }, [refreshTrigger]);

  // Poll for status updates on running jobs
  useEffect(() => {
    const runningJobs = runs.filter(run => run.status === 'running' || run.status === 'pending');
    
    if (runningJobs.length === 0) return;

    const interval = setInterval(() => {
      runningJobs.forEach(job => {
        pollJobStatus(job.job_id);
      });
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, [runs]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800 border-green-200';
      case 'failed': return 'bg-red-100 text-red-800 border-red-200';
      case 'running': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'pending': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅';
      case 'failed': return '❌';
      case 'running': return '⏳';
      case 'pending': return '⏸️';
      default: return '❓';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-sm text-red-800">{error}</p>
        <button
          onClick={fetchTranslationRuns}
          className="mt-2 text-sm text-red-600 hover:text-red-500"
        >
          Try again
        </button>
      </div>
    );
  }

  if (runs.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No translation jobs found.</p>
        <p className="text-sm mt-2">Upload a file to start your first translation!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">
          Recent Translations ({runs.length})
        </h3>
        <button
          onClick={fetchTranslationRuns}
          className="text-sm text-blue-600 hover:text-blue-500"
        >
          Refresh
        </button>
      </div>

      <div className="space-y-3">
        {runs.map((run) => (
          <div key={run.job_id} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <span className="text-lg">{getStatusIcon(run.status)}</span>
                <div>
                  <h4 className="font-medium text-gray-900">
                    {run.book_path.split('/').pop() || 'Unknown File'}
                  </h4>
                  <p className="text-sm text-gray-500">
                    {run.model} → {run.language}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getStatusColor(run.status)}`}>
                  {run.status.charAt(0).toUpperCase() + run.status.slice(1)}
                </span>
                {run.status === 'completed' && (
                  <button
                    onClick={() => handleDownload(run.job_id)}
                    disabled={downloadingJobs.has(run.job_id)}
                    className="px-3 py-1 text-xs font-medium text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50"
                  >
                    {downloadingJobs.has(run.job_id) ? 'Downloading...' : 'Download'}
                  </button>
                )}
                <button
                  onClick={() => handleDelete(run.job_id)}
                  className="px-3 py-1 text-xs font-medium text-white bg-red-600 hover:bg-red-700 rounded-md"
                >
                  Delete
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
              <div>
                <span className="font-medium">Created:</span> {formatDate(run.created_at)}
              </div>
              {run.started_at && (
                <div>
                  <span className="font-medium">Started:</span> {formatDate(run.started_at)}
                </div>
              )}
              {run.completed_at && (
                <div>
                  <span className="font-medium">Completed:</span> {formatDate(run.completed_at)}
                </div>
              )}
            </div>

            {run.status === 'running' && (
              <div className="mt-3">
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{ width: '45%' }}></div>
                  </div>
                  <span className="text-sm text-gray-600">Processing...</span>
                </div>
              </div>
            )}

            {run.error && (
              <div className="mt-3 bg-red-50 border border-red-200 rounded-md p-3">
                <p className="text-sm text-red-800">
                  <span className="font-medium">Error:</span> {run.error}
                </p>
              </div>
            )}

            {run.config && (
              <details className="mt-3">
                <summary className="text-sm text-gray-600 cursor-pointer hover:text-gray-800">
                  View Configuration
                </summary>
                <div className="mt-2 text-xs text-gray-500 bg-gray-100 rounded-md p-2">
                  <pre>{JSON.stringify(run.config, null, 2)}</pre>
                </div>
              </details>
            )}
          </div>
        ))}
      </div>

      {runs.length >= 50 && (
        <div className="text-center py-4">
          <p className="text-sm text-gray-600">
            Showing latest 50 translations. Older translations may be available in your account.
          </p>
        </div>
      )}
    </div>
  );
}