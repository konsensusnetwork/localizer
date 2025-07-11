import React, { useState, useRef } from 'react';
import { makeApiCall, getCurrentUserId } from '../lib/supabase';

interface FileUploadProps {
  onTranslationStart?: (jobId: string) => void;
}

export default function FileUpload({ onTranslationStart }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Translation parameters
  const [model, setModel] = useState('gpt-4');
  const [language, setLanguage] = useState('Chinese');
  const [singleTranslate, setSingleTranslate] = useState(false);
  const [testMode, setTestMode] = useState(false);
  const [testNum, setTestNum] = useState(10);
  const [temperature, setTemperature] = useState(1.0);
  const [useContext, setUseContext] = useState(false);
  const [reasoningEffort, setReasoningEffort] = useState('medium');

  // Available models and languages
  const models = [
    'gpt-4', 'gpt-4-turbo', 'gpt-4o', 'gpt-4o-mini',
    'gpt-3.5-turbo', 'claude-3-opus', 'claude-3-sonnet',
    'claude-3-haiku', 'gemini-pro', 'o1-preview', 'o1-mini'
  ];

  const languages = [
    'Chinese', 'Spanish', 'French', 'German', 'Japanese',
    'Korean', 'Italian', 'Portuguese', 'Russian', 'Arabic',
    'Dutch', 'Swedish', 'Norwegian', 'Danish', 'Finnish'
  ];

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError('');
      setSuccess('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const userId = await getCurrentUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      // Create a temporary file path (in a real app, you'd upload to storage first)
      const tempFilePath = `/tmp/${selectedFile.name}`;
      
      // Start translation job
      const response = await makeApiCall('/translate/start', {
        method: 'POST',
        body: JSON.stringify({
          book_path: tempFilePath,
          model,
          language,
          single_translate: singleTranslate,
          test_mode: testMode,
          test_num: testNum,
          temperature,
          use_context: useContext,
          reasoning_effort: reasoningEffort,
          user_id: userId
        })
      });

      if (response.job_id) {
        setSuccess(`Translation started! Job ID: ${response.job_id}`);
        onTranslationStart?.(response.job_id);
        
        // Reset form
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      } else {
        throw new Error('Failed to start translation job');
      }
    } catch (error: any) {
      setError(error.message || 'Failed to start translation');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Book File
          </label>
          <div className="flex items-center justify-center w-full">
            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                {selectedFile ? (
                  <>
                    <p className="mb-2 text-sm text-gray-500">
                      <span className="font-semibold">Selected:</span> {selectedFile.name}
                    </p>
                    <p className="text-xs text-gray-400">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </p>
                  </>
                ) : (
                  <>
                    <svg className="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                      <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                    </svg>
                    <p className="mb-2 text-sm text-gray-500">
                      <span className="font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-xs text-gray-400">
                      TXT, MD, EPUB, PDF (MAX. 10MB)
                    </p>
                  </>
                )}
              </div>
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept=".txt,.md,.epub,.pdf"
                onChange={handleFileSelect}
              />
            </label>
          </div>
        </div>

        {/* Translation Parameters */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              AI Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              {models.map(m => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              {languages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Temperature ({temperature})
            </label>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Conservative</span>
              <span>Creative</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Reasoning Effort
            </label>
            <select
              value={reasoningEffort}
              onChange={(e) => setReasoningEffort(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        {/* Advanced Options */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-900">Advanced Options</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center">
              <input
                id="single-translate"
                type="checkbox"
                checked={singleTranslate}
                onChange={(e) => setSingleTranslate(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="single-translate" className="ml-2 block text-sm text-gray-700">
                Single Translation Mode
              </label>
            </div>

            <div className="flex items-center">
              <input
                id="use-context"
                type="checkbox"
                checked={useContext}
                onChange={(e) => setUseContext(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="use-context" className="ml-2 block text-sm text-gray-700">
                Use Context
              </label>
            </div>

            <div className="flex items-center">
              <input
                id="test-mode"
                type="checkbox"
                checked={testMode}
                onChange={(e) => setTestMode(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="test-mode" className="ml-2 block text-sm text-gray-700">
                Test Mode
              </label>
            </div>

            {testMode && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Test Sentences
                </label>
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={testNum}
                  onChange={(e) => setTestNum(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            )}
          </div>
        </div>

        {/* Status Messages */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {success && (
          <div className="bg-green-50 border border-green-200 rounded-md p-3">
            <p className="text-sm text-green-800">{success}</p>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={uploading || !selectedFile}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {uploading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Starting Translation...
            </>
          ) : (
            'Start Translation'
          )}
        </button>
      </form>
    </div>
  );
}