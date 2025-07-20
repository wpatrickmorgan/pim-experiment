// Frappe API client utilities
import { getCookie } from './utils';

export interface FrappeResponse<T = any> {
  message: T;
  exc?: string;
  exc_type?: string;
}

export interface Product {
  name: string;
  item_name: string;
  item_code: string;
  item_group: string;
  status: string;
  stock_qty: number;
  standard_rate: number;
  image_count: number;
  modified: string;
  is_starred: boolean;
}

export interface ProductsResponse {
  products: Product[];
  total_count: number;
  has_more: boolean;
}

export interface DashboardStats {
  total_products: number;
  active_products: number;
  draft_products: number;
  low_stock_products: number;
  total_categories: number;
  recent_orders: number;
  revenue_this_month: number;
  revenue_growth: number;
}

class FrappeAPI {
  private baseURL = '';
  
  private async makeRequest<T>(
    method: string,
    endpoint: string,
    data?: any
  ): Promise<T> {
    const url = `${this.baseURL}/api/method/${endpoint}`;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    
    // Add CSRF token for non-GET requests
    if (method !== 'GET') {
      const csrfToken = getCookie('csrf_token');
      if (csrfToken) {
        headers['X-Frappe-CSRF-Token'] = csrfToken;
      }
    }
    
    const config: RequestInit = {
      method,
      headers,
      credentials: 'include', // Include cookies for session management
    };
    
    if (data && method !== 'GET') {
      config.body = JSON.stringify(data);
    } else if (data && method === 'GET') {
      const params = new URLSearchParams();
      Object.keys(data).forEach(key => {
        if (data[key] !== undefined && data[key] !== null) {
          params.append(key, String(data[key]));
        }
      });
      const queryString = params.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }
    
    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result: FrappeResponse<T> = await response.json();
      
      if (result.exc) {
        throw new Error(result.exc);
      }
      
      return result.message;
    } catch (error) {
      console.error(`API Error (${method} ${endpoint}):`, error);
      throw error;
    }
  }
  
  // Products API
  async getProducts(params?: {
    filters?: Record<string, any>;
    limit?: number;
    offset?: number;
    search_term?: string;
  }): Promise<ProductsResponse> {
    return this.makeRequest<ProductsResponse>(
      'GET',
      'imperium_pim.api.get_products',
      params
    );
  }
  
  async getProductCategories(): Promise<Array<{name: string; count: number}>> {
    return this.makeRequest<Array<{name: string; count: number}>>(
      'GET',
      'imperium_pim.api.get_product_categories'
    );
  }
  
  async toggleProductStar(productName: string): Promise<{success: boolean; message: string}> {
    return this.makeRequest<{success: boolean; message: string}>(
      'POST',
      'imperium_pim.api.toggle_product_star',
      { product_name: productName }
    );
  }
  
  async bulkUpdateProducts(
    productNames: string[],
    action: string,
    value?: any
  ): Promise<{success: boolean; message: string}> {
    return this.makeRequest<{success: boolean; message: string}>(
      'POST',
      'imperium_pim.api.bulk_update_products',
      { product_names: productNames, action, value }
    );
  }
  
  // Dashboard API
  async getDashboardStats(): Promise<DashboardStats> {
    return this.makeRequest<DashboardStats>(
      'GET',
      'imperium_pim.api.get_dashboard_stats'
    );
  }
  
  // Auth API
  async getCurrentUser(): Promise<any> {
    return this.makeRequest<any>(
      'GET',
      'frappe.auth.get_logged_user'
    );
  }
}

export const frappeAPI = new FrappeAPI();

