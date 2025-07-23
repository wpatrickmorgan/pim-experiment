'use client';

import { useEffect, useState } from 'react';

export default function DebugPage() {
  const [apiConfig, setApiConfig] = useState<any>({});
  const [testResults, setTestResults] = useState<any>({});

  useEffect(() => {
    // Get API configuration
    const config = {
      NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
      NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL,
      NODE_ENV: process.env.NODE_ENV,
      currentUrl: window.location.href,
      userAgent: navigator.userAgent
    };
    setApiConfig(config);

    // Test API endpoints
    testApiEndpoints();
  }, []);

  const testApiEndpoints = async () => {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';
    const endpoints = [
      '/method/imperium_pim.api.ping.ping',
      '/method/imperium_pim.api.dashboard.get_dashboard_stats',
      '/method/imperium_pim.api.items.get_item_list'
    ];

    const results: any = {};

    for (const endpoint of endpoints) {
      const fullUrl = `${baseUrl}${endpoint}`;
      try {
        console.log(`Testing: ${fullUrl}`);
        const response = await fetch(fullUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          mode: 'cors',
          credentials: 'include'
        });

        results[endpoint] = {
          url: fullUrl,
          status: response.status,
          statusText: response.statusText,
          headers: Object.fromEntries(response.headers.entries()),
          success: response.ok
        };

        if (response.ok) {
          try {
            const data = await response.json();
            results[endpoint].data = data;
          } catch (e) {
            results[endpoint].parseError = 'Failed to parse JSON';
          }
        } else {
          try {
            const errorText = await response.text();
            results[endpoint].error = errorText;
          } catch (e) {
            results[endpoint].error = 'Failed to read error response';
          }
        }
      } catch (error) {
        results[endpoint] = {
          url: fullUrl,
          error: error instanceof Error ? error.message : 'Unknown error',
          success: false
        };
      }
    }

    setTestResults(results);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">API Debug Information</h1>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Environment Configuration</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-auto">
          {JSON.stringify(apiConfig, null, 2)}
        </pre>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">API Endpoint Tests</h2>
        {Object.entries(testResults).map(([endpoint, result]: [string, any]) => (
          <div key={endpoint} className="mb-4 p-4 border rounded">
            <h3 className="font-semibold text-lg mb-2">{endpoint}</h3>
            <div className={`p-2 rounded mb-2 ${result.success ? 'bg-green-100' : 'bg-red-100'}`}>
              Status: {result.success ? '✅ SUCCESS' : '❌ FAILED'}
            </div>
            <pre className="bg-gray-50 p-2 rounded text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        ))}
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Manual Test URLs</h2>
        <p className="mb-2">Try these URLs directly in your browser:</p>
        <ul className="list-disc pl-6">
          <li>
            <a 
              href="http://138.197.71.50:8000/api/method/imperium_pim.api.ping.ping" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Ping Endpoint (HTTP)
            </a>
          </li>
          <li>
            <a 
              href="https://138.197.71.50:8000/api/method/imperium_pim.api.ping.ping" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Ping Endpoint (HTTPS)
            </a>
          </li>
          <li>
            <a 
              href="http://138.197.71.50:8000/api/method/imperium_pim.api.dashboard.get_dashboard_stats" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Dashboard Stats (HTTP)
            </a>
          </li>
        </ul>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Recommended Fixes</h2>
        <div className="bg-yellow-50 p-4 rounded">
          <p className="mb-2"><strong>If you see HTTPS errors:</strong></p>
          <p className="mb-4">Set your Vercel environment variable to:</p>
          <code className="bg-gray-200 px-2 py-1 rounded">
            NEXT_PUBLIC_API_BASE_URL=http://138.197.71.50:8000/api
          </code>
          
          <p className="mt-4 mb-2"><strong>If you see CORS errors:</strong></p>
          <p>Make sure your backend CORS configuration includes your Vercel domain.</p>
        </div>
      </div>
    </div>
  );
}
