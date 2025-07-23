// React Query hooks for API integration
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from './api';

// Query keys
export const queryKeys = {
  ping: ['ping'] as const,
  dashboardStats: ['dashboard', 'stats'] as const,
  products: (limit?: number, offset?: number) => ['products', { limit, offset }] as const,
  product: (name: string) => ['product', name] as const,
};

// Test connectivity
export function usePing() {
  return useQuery({
    queryKey: queryKeys.ping,
    queryFn: () => apiClient.ping(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
  });
}

// Dashboard stats
export function useDashboardStats() {
  return useQuery({
    queryKey: queryKeys.dashboardStats,
    queryFn: () => apiClient.getDashboardStats(),
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  });
}

// Products
export function useProducts(limit: number = 20, offset: number = 0) {
  return useQuery({
    queryKey: queryKeys.products(limit, offset),
    queryFn: () => apiClient.getProducts(limit, offset),
    staleTime: 1 * 60 * 1000, // 1 minute
  });
}

export function useProduct(name: string) {
  return useQuery({
    queryKey: queryKeys.product(name),
    queryFn: () => apiClient.getProduct(name),
    enabled: !!name,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Authentication
export function useLogin() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ username, password }: { username: string; password: string }) =>
      apiClient.login(username, password),
    onSuccess: () => {
      // Invalidate all queries on successful login
      queryClient.invalidateQueries();
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: () => apiClient.logout(),
    onSuccess: () => {
      // Clear all queries on logout
      queryClient.clear();
    },
  });
}
