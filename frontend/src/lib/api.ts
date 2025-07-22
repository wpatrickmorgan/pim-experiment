// API client for Frappe backend integration
// Support both relative URLs (monorepo) and absolute URLs (separate deployment)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || '';

// Determine if we're in cross-origin mode
const isCrossOrigin = API_BASE_URL.startsWith('http');

console.log('API Configuration:', {
  API_BASE_URL,
  BACKEND_URL,
  isCrossOrigin,
  environment: process.env.NODE_ENV
});

export interface FrappeResponse<T = any> {
  message: T;
  exc?: string;
  exc_type?: string;
}

export interface DashboardStats {
  total_products: number;
  total_categories: number;
  low_stock_items: number;
  pending_orders: number;
}

export interface Product {
  name: string;
  item_name: string;
  item_code: string;
  item_group: string;
  stock_qty: number;
  standard_rate: number;
  modified: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
      // Handle credentials based on deployment mode
      credentials: isCrossOrigin ? 'include' : 'include', // Always include for now, may need tokens later
      // Add CORS mode for cross-origin requests
      mode: isCrossOrigin ? 'cors' : 'same-origin',
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        // Enhanced error handling for cross-origin requests
        let errorMessage = `HTTP error! status: ${response.status}`;
        
        if (response.status === 0 || response.status === 404) {
          errorMessage += isCrossOrigin 
            ? ' - Check if backend server is running and CORS is configured'
            : ' - Check if API endpoint exists';
        } else if (response.status === 403) {
          errorMessage += ' - Authentication required or CORS blocked';
        }
        
        throw new Error(errorMessage);
      }

      const data: FrappeResponse<T> = await response.json();
      
      if (data.exc) {
        throw new Error(data.exc);
      }

      return data.message;
    } catch (error) {
      console.error('API request failed:', {
        url,
        error,
        isCrossOrigin,
        config: { ...config, headers: 'redacted' }
      });
      throw error;
    }
  }

  // Authentication
  async login(username: string, password: string) {
    return this.request('/method/login', {
      method: 'POST',
      body: JSON.stringify({
        usr: username,
        pwd: password,
      }),
    });
  }

  async logout() {
    return this.request('/method/logout', {
      method: 'POST',
    });
  }

  // Test connectivity
  async ping() {
    return this.request<{ status: string; message: string; timestamp: string }>('/method/imperium_pim.api.ping');
  }

  // Health check for separate deployment
  async healthCheck() {
    try {
      const result = await this.ping();
      return {
        status: 'healthy',
        backend: 'connected',
        timestamp: new Date().toISOString(),
        config: {
          apiBaseUrl: API_BASE_URL,
          isCrossOrigin,
          environment: process.env.NODE_ENV
        },
        ...result
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        backend: 'disconnected',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
        config: {
          apiBaseUrl: API_BASE_URL,
          isCrossOrigin,
          environment: process.env.NODE_ENV
        }
      };
    }
  }

  // Dashboard data
  async getDashboardStats(): Promise<DashboardStats> {
    return this.request<DashboardStats>('/method/imperium_pim.api.get_dashboard_stats');
  }

  // Products
  async getProducts(limit: number = 20, offset: number = 0): Promise<Product[]> {
    return this.request<Product[]>(`/method/imperium_pim.api.get_products?limit=${limit}&offset=${offset}`);
  }

  async getProduct(name: string): Promise<Product> {
    return this.request<Product>(`/method/imperium_pim.api.get_product?name=${encodeURIComponent(name)}`);
  }

  // Generic DocType operations
  async getDoc(doctype: string, name: string) {
    return this.request(`/method/frappe.client.get?doctype=${doctype}&name=${encodeURIComponent(name)}`);
  }

  async getList(doctype: string, options: {
    fields?: string[];
    filters?: Record<string, any>;
    limit?: number;
    offset?: number;
    order_by?: string;
  } = {}) {
    const params = new URLSearchParams();
    params.append('doctype', doctype);
    
    if (options.fields) {
      params.append('fields', JSON.stringify(options.fields));
    }
    if (options.filters) {
      params.append('filters', JSON.stringify(options.filters));
    }
    if (options.limit) {
      params.append('limit', options.limit.toString());
    }
    if (options.offset) {
      params.append('offset', options.offset.toString());
    }
    if (options.order_by) {
      params.append('order_by', options.order_by);
    }

    return this.request(`/method/frappe.client.get_list?${params.toString()}`);
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// React Query hooks
export const useApi = () => apiClient;
