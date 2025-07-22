'use client';

import { AppLayout } from "@/components/layout/app-layout";
import { MetricCard } from "@/components/dashboard/metric-card";
import { RecentProducts } from "@/components/dashboard/recent-products";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { Package, FolderTree, AlertTriangle, TrendingDown, Loader2 } from "lucide-react";
import { useDashboardStats, usePing } from "@/lib/hooks";

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading, error: statsError } = useDashboardStats();
  const { data: pingData, isLoading: pingLoading, error: pingError } = usePing();

  return (
    <AppLayout>
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">
            Overview of your product information management system
          </p>
          
          {/* Connection Status */}
          <div className="mt-4 flex items-center gap-2">
            {pingLoading && (
              <div className="flex items-center text-gray-500">
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Connecting to backend...
              </div>
            )}
            {pingData && (
              <div className="flex items-center text-green-600">
                <div className="h-2 w-2 bg-green-500 rounded-full mr-2"></div>
                Backend connected - {pingData.message}
              </div>
            )}
            {pingError && (
              <div className="flex items-center text-red-600">
                <div className="h-2 w-2 bg-red-500 rounded-full mr-2"></div>
                Backend connection failed
              </div>
            )}
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsLoading ? (
            // Loading state
            Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="bg-white p-6 rounded-lg border animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-full"></div>
              </div>
            ))
          ) : statsError ? (
            // Error state - show static data
            <>
              <MetricCard
                title="Total Products"
                value="--"
                subtitle="Unable to load data"
                icon={Package}
              />
              <MetricCard
                title="Active Categories"
                value="--"
                subtitle="Unable to load data"
                icon={FolderTree}
              />
              <MetricCard
                title="Pending Orders"
                value="--"
                subtitle="Unable to load data"
                icon={AlertTriangle}
              />
              <MetricCard
                title="Low Stock Items"
                value="--"
                subtitle="Unable to load data"
                icon={TrendingDown}
              />
            </>
          ) : (
            // Real data
            <>
              <MetricCard
                title="Total Products"
                value={stats?.total_products?.toString() || "0"}
                subtitle="Active products in system"
                icon={Package}
              />
              <MetricCard
                title="Active Categories"
                value={stats?.total_categories?.toString() || "0"}
                subtitle="Product categories"
                icon={FolderTree}
              />
              <MetricCard
                title="Pending Orders"
                value={stats?.pending_orders?.toString() || "0"}
                subtitle="Orders awaiting processing"
                icon={AlertTriangle}
              />
              <MetricCard
                title="Low Stock Items"
                value={stats?.low_stock_items?.toString() || "0"}
                subtitle="Items below minimum stock"
                icon={TrendingDown}
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
