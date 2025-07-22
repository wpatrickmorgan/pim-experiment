"use client";

import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { AppLayout } from "@/components/layout/app-layout";
import { MetricCard } from "@/components/dashboard/metric-card";
import { RecentProducts } from "@/components/dashboard/recent-products";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { Package, FolderTree, AlertTriangle, TrendingDown, Loader2, RefreshCw, Bug } from "lucide-react";
import { frappeAPI } from "@/lib/api";
import { formatNumber } from "@/lib/utils";

export default function Dashboard() {
  const [debugInfo, setDebugInfo] = useState<any>({});
  const [manualTestResult, setManualTestResult] = useState<string>('');
  const [timeoutReached, setTimeoutReached] = useState(false);

  // Enhanced useQuery with debugging
  const { data: stats, isLoading: statsLoading, error: statsError, refetch, fetchStatus } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      console.log('🚀 Dashboard useQuery: Starting API call...');
      console.log('🌐 API Base URL:', window.location.origin);
      console.log('🔗 Full API URL:', `${window.location.origin}/api/method/imperium_pim.api.get_dashboard_stats`);
      
      try {
        const result = await frappeAPI.getDashboardStats();
        console.log('✅ Dashboard useQuery: API call successful', result);
        return result;
      } catch (error) {
        console.error('❌ Dashboard useQuery: API call failed', error);
        throw error;
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
    retryDelay: 1000,
  });

  // Component mounting debug
  useEffect(() => {
    console.log('🎯 Dashboard Component: Mounted');
    console.log('🔧 Environment check:', {
      NODE_ENV: process.env.NODE_ENV,
      NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE,
      window_location: typeof window !== 'undefined' ? window.location.href : 'SSR',
      frappe_available: typeof window !== 'undefined' ? typeof (window as any).frappe : 'SSR'
    });

    return () => {
      console.log('🎯 Dashboard Component: Unmounting');
    };
  }, []);

  // Query state debugging
  useEffect(() => {
    const currentDebugInfo = {
      isLoading: statsLoading,
      fetchStatus,
      hasData: !!stats,
      hasError: !!statsError,
      errorMessage: statsError?.message,
      timestamp: new Date().toISOString()
    };
    
    setDebugInfo(currentDebugInfo);
    
    console.log('📊 Dashboard useQuery State Update:', currentDebugInfo);
    
    if (stats) {
      console.log('📈 Dashboard Data Received:', stats);
    }
    
    if (statsError) {
      console.error('🚨 Dashboard Query Error:', statsError);
    }
  }, [statsLoading, fetchStatus, stats, statsError]);

  // Timeout mechanism
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (statsLoading && !stats && !statsError) {
        console.warn('⏰ Dashboard: Query timeout reached (30s)');
        setTimeoutReached(true);
      }
    }, 30000); // 30 second timeout

    return () => clearTimeout(timeout);
  }, [statsLoading, stats, statsError]);

  // Manual API test function
  const testAPIManually = async () => {
    console.log('🧪 Manual API Test: Starting...');
    setManualTestResult('Testing...');
    
    try {
      // Test basic fetch
      const url = `${window.location.origin}/api/method/imperium_pim.api.get_dashboard_stats`;
      console.log('🧪 Manual API Test: Fetching', url);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include',
      });
      
      console.log('🧪 Manual API Test: Response status', response.status);
      console.log('🧪 Manual API Test: Response headers', Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('🧪 Manual API Test: Response data', data);
      
      setManualTestResult(`✅ Success: ${JSON.stringify(data, null, 2)}`);
    } catch (error) {
      console.error('🧪 Manual API Test: Failed', error);
      setManualTestResult(`❌ Error: ${error.message}`);
    }
  };

  return (
    <AppLayout>
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">
            Overview of your product information management system
          </p>
        </div>

        {/* Debug Panel */}
        <div className="mb-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-gray-700 flex items-center">
              <Bug className="h-4 w-4 mr-2" />
              Debug Information
            </h3>
            <div className="flex gap-2">
              <button
                onClick={() => refetch()}
                className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 flex items-center"
              >
                <RefreshCw className="h-3 w-3 mr-1" />
                Retry Query
              </button>
              <button
                onClick={testAPIManually}
                className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200"
              >
                Test API
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <p><strong>Query State:</strong> {JSON.stringify(debugInfo, null, 2)}</p>
            </div>
            <div>
              <p><strong>Manual Test Result:</strong></p>
              <pre className="mt-1 p-2 bg-white border rounded text-xs overflow-auto max-h-32">
                {manualTestResult || 'Click "Test API" to run manual test'}
              </pre>
            </div>
          </div>
          
          {timeoutReached && (
            <div className="mt-3 p-2 bg-yellow-100 border border-yellow-300 rounded">
              <p className="text-yellow-800 text-xs">
                ⚠️ Query timeout reached. The useQuery hook may not be executing properly.
              </p>
            </div>
          )}
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsLoading && !timeoutReached ? (
            <div className="col-span-4 flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              <span className="ml-2 text-gray-600">Loading dashboard...</span>
              <span className="ml-2 text-xs text-gray-400">
                (Status: {fetchStatus}, Loading: {statsLoading ? 'true' : 'false'})
              </span>
            </div>
          ) : timeoutReached && statsLoading ? (
            <div className="col-span-4 text-center py-12">
              <p className="text-orange-600 mb-2">Query timeout reached</p>
              <p className="text-sm text-gray-500 mb-4">
                The useQuery hook appears to be stuck. Check the debug panel above.
              </p>
              <button
                onClick={() => {
                  setTimeoutReached(false);
                  refetch();
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Retry Now
              </button>
            </div>
          ) : statsError ? (
            <div className="col-span-4 text-center py-12">
              <p className="text-red-600 mb-2">Error loading dashboard stats</p>
              <p className="text-sm text-gray-500 mb-4">{statsError.message}</p>
              <button
                onClick={() => refetch()}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Retry
              </button>
            </div>
          ) : (
            <>
              <MetricCard
                title="Total Products"
                value={formatNumber(stats?.total_products || 0)}
                subtitle={`${stats?.active_products || 0} active`}
                icon={Package}
                trend={{ value: `${stats?.revenue_growth || 0}%`, positive: (stats?.revenue_growth || 0) > 0 }}
              />
              <MetricCard
                title="Active Categories"
                value={formatNumber(stats?.total_categories || 0)}
                subtitle="Product categories"
                icon={FolderTree}
                trend={{ value: "8.3%", positive: true }}
              />
              <MetricCard
                title="Pending Reviews"
                value={formatNumber(stats?.recent_orders || 0)}
                subtitle="Recent orders"
                icon={AlertTriangle}
                trend={{ value: "8.3%", positive: false }}
              />
              <MetricCard
                title="Low Stock Items"
                value={formatNumber(stats?.low_stock_products || 0)}
                subtitle="Requires attention"
                icon={TrendingDown}
                trend={{ value: "12.1%", positive: false }}
              />
            </>
          )}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <RecentProducts />
          <QuickActions />
        </div>
      </div>
    </AppLayout>
  );
}
