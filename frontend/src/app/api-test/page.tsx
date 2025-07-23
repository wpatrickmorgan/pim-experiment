'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

interface TestResult {
  name: string;
  status: 'pending' | 'success' | 'error';
  result?: unknown;
  error?: string;
  duration?: number;
}

export default function ApiTestPage() {
  const [tests, setTests] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const runTest = async (name: string, testFn: () => Promise<unknown>) => {
    const startTime = Date.now();
    setTests(prev => prev.map(t => t.name === name ? { ...t, status: 'pending' as const } : t));
    
    try {
      const result = await testFn();
      const duration = Date.now() - startTime;
      setTests(prev => prev.map(t => 
        t.name === name 
          ? { ...t, status: 'success' as const, result, duration }
          : t
      ));
    } catch (error) {
      const duration = Date.now() - startTime;
      setTests(prev => prev.map(t => 
        t.name === name 
          ? { 
              ...t, 
              status: 'error' as const, 
              error: error instanceof Error ? error.message : 'Unknown error',
              duration 
            }
          : t
      ));
    }
  };

  const runAllTests = async () => {
    setIsRunning(true);
    
    // Initialize test results
    const testList: TestResult[] = [
      { name: 'Health Check', status: 'pending' },
      { name: 'Ping API', status: 'pending' },
      { name: 'Dashboard Stats', status: 'pending' },
      { name: 'Get Items', status: 'pending' },
    ];
    setTests(testList);

    // Run tests sequentially
    await runTest('Health Check', () => api.healthCheck());
    await runTest('Ping API', () => api.ping());
    await runTest('Dashboard Stats', () => api.getDashboardStats());
    await runTest('Get Items', () => api.getProducts(5));
    
    setIsRunning(false);
  };

  const getStatusColor = (status: TestResult['status']) => {
    switch (status) {
      case 'pending': return 'text-yellow-600';
      case 'success': return 'text-green-600';
      case 'error': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: TestResult['status']) => {
    switch (status) {
      case 'pending': return '⏳';
      case 'success': return '✅';
      case 'error': return '❌';
      default: return '⚪';
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">API Connectivity Test</h1>
      
      <div className="mb-6">
        <button
          onClick={runAllTests}
          disabled={isRunning}
          className="bg-blue-500 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded"
        >
          {isRunning ? 'Running Tests...' : 'Run API Tests'}
        </button>
      </div>

      <div className="space-y-4">
        {tests.map((test) => (
          <div key={test.name} className="border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <span>{getStatusIcon(test.status)}</span>
                {test.name}
              </h3>
              <span className={`text-sm ${getStatusColor(test.status)}`}>
                {test.status.toUpperCase()}
                {test.duration && ` (${test.duration}ms)`}
              </span>
            </div>
            
            {test.error && (
              <div className="bg-red-50 border border-red-200 rounded p-3 mb-2">
                <p className="text-red-800 text-sm font-medium">Error:</p>
                <p className="text-red-700 text-sm">{test.error}</p>
              </div>
            )}
            
            {test.result && (
              <div className="bg-green-50 border border-green-200 rounded p-3">
                <p className="text-green-800 text-sm font-medium">Result:</p>
                <pre className="text-green-700 text-xs mt-1 overflow-x-auto">
                  {JSON.stringify(test.result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-8 bg-gray-50 border rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-2">Configuration Info</h3>
        <div className="text-sm space-y-1">
          <p><strong>API Base URL:</strong> {process.env.NEXT_PUBLIC_API_BASE_URL || '/api'}</p>
          <p><strong>Backend URL:</strong> {process.env.NEXT_PUBLIC_BACKEND_URL || 'Not set'}</p>
          <p><strong>Environment:</strong> {process.env.NODE_ENV}</p>
          <p><strong>Cross-Origin Mode:</strong> {(process.env.NEXT_PUBLIC_API_BASE_URL || '/api').startsWith('http') ? 'Yes' : 'No'}</p>
        </div>
      </div>
    </div>
  );
}
