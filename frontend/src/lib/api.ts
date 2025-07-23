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

export interface FrappeResponse<T = unknown> {
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
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        let errorDetails = '';
        
        if (response.status === 0) {
          errorMessage = 'Network Error';
          errorDetails = isCrossOrigin 
            ? 'Cannot reach backend server. Check if the backend URL is correct and the server is running.'
            : 'Network request failed. Check your internet connection.';
        } else if (response.status === 404) {
          errorDetails = isCrossOrigin 
            ? 'API endpoint not found. Check if the backend server is running and the endpoint path is correct.'
            : 'API endpoint not found. Check if the endpoint exists.';
        } else if (response.status === 403) {
          errorDetails = 'Access forbidden. This could be due to CORS policy, authentication, or authorization issues.';
        } else if (response.status === 500) {
          errorDetails = 'Internal server error. Check backend logs for details.';
        } else if (response.status >= 400 && response.status < 500) {
          errorDetails = 'Client error. Check request parameters and authentication.';
        } else if (response.status >= 500) {
          errorDetails = 'Server error. The backend service may be experiencing issues.';
        }
        
        // Try to get error details from response body
        try {
          const errorBody = await response.text();
          if (errorBody) {
            errorDetails += ` Response: ${errorBody.substring(0, 200)}`;
          }
        } catch (e) {
          // Ignore if we can't read the response body
        }
        
        const fullError = errorDetails ? `${errorMessage} - ${errorDetails}` : errorMessage;
        throw new Error(fullError);
      }

      const data: FrappeResponse<T> = await response.json();
      
      if (data.exc) {
        throw new Error(`Backend Error: ${data.exc}`);
      }

      return data.message;
    } catch (error) {
      // Enhanced error logging
      const errorInfo = {
        url,
        method: config.method || 'GET',
        isCrossOrigin,
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
        config: {
          credentials: config.credentials,
          mode: config.mode,
          headers: config.headers
        }
      };
      
      console.error('API request failed:', errorInfo);
      
      // Re-throw with additional context for network errors
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error(`Network Error: Unable to connect to ${this.baseUrl}. Check if the backend server is running and accessible.`);
      }
      
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
    return this.request<{ status: string; message: string; timestamp: string }>('/method/imperium_pim.api.ping.ping');
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
        pingResult: result
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
    return this.request<DashboardStats>('/method/imperium_pim.api.dashboard.get_dashboard_stats');
  }

  // Products
  async getProducts(limit: number = 20, offset: number = 0): Promise<Product[]> {
    return this.request<Product[]>(`/method/imperium_pim.api.items.get_item_list?limit=${limit}&offset=${offset}`);
  }

  async getProduct(name: string): Promise<Product> {
    return this.request<Product>(`/method/imperium_pim.api.items.get_item_details?item_id=${encodeURIComponent(name)}`);
  }

  // Generic DocType operations
  async getDoc(doctype: string, name: string) {
    return this.request(`/method/frappe.client.get?doctype=${doctype}&name=${encodeURIComponent(name)}`);
  }

  async getList(doctype: string, options: {
    fields?: string[];
    filters?: Record<string, unknown>;
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
export const api = apiClient; // Alias for convenience

// React Query hooks
export const useApi = () => apiClient;
