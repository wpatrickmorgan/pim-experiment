"use client";

import { useQuery } from "@tanstack/react-query";
import { AppLayout } from "@/components/layout/app-layout";
import { MetricCard } from "@/components/dashboard/metric-card";
import { RecentProducts } from "@/components/dashboard/recent-products";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { Package, FolderTree, AlertTriangle, TrendingDown, Loader2 } from "lucide-react";
import { frappeAPI } from "@/lib/api";
import { formatNumber } from "@/lib/utils";

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading, error: statsError } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => frappeAPI.getDashboardStats(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  return (
    <AppLayout>
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">
            Overview of your product information management system
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statsLoading ? (
            <div className="col-span-4 flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              <span className="ml-2 text-gray-600">Loading dashboard...</span>
            </div>
          ) : statsError ? (
            <div className="col-span-4 text-center py-12">
              <p className="text-red-600 mb-2">Error loading dashboard stats</p>
              <p className="text-sm text-gray-500">{statsError.message}</p>
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
