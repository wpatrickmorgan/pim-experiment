"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MoreHorizontal, Star, Image, Loader2 } from "lucide-react";
import { frappeAPI, type Product } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

function getStatusVariant(status: string) {
  switch (status) {
    case "Active":
      return "success";
    case "Draft":
      return "draft";
    case "Review":
      return "warning";
    default:
      return "default";
  }
}

export function ProductsTable() {
  const [selectedProducts, setSelectedProducts] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  
  const queryClient = useQueryClient();
  
  // Fetch products with React Query
  const { data: productsData, isLoading, error } = useQuery({
    queryKey: ['products', { search_term: searchTerm, status: statusFilter }],
    queryFn: () => frappeAPI.getProducts({
      search_term: searchTerm || undefined,
      filters: statusFilter ? { status: statusFilter } : undefined,
      limit: 50
    }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
  
  // Star toggle mutation
  const starMutation = useMutation({
    mutationFn: (productName: string) => frappeAPI.toggleProductStar(productName),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });

  const products = productsData?.products || [];

  const toggleProductSelection = (productName: string) => {
    setSelectedProducts((prev) =>
      prev.includes(productName)
        ? prev.filter((name) => name !== productName)
        : [...prev, productName],
    );
  };

  const toggleAllProducts = () => {
    setSelectedProducts((prev) =>
      prev.length === products.length ? [] : products.map((p) => p.name),
    );
  };
  
  const handleStarToggle = (productName: string) => {
    starMutation.mutate(productName);
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          <span className="ml-2 text-gray-600">Loading products...</span>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <p className="text-red-600 mb-2">Error loading products</p>
            <p className="text-sm text-gray-500">{error.message}</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">
            Product Catalog
          </CardTitle>
          <span className="text-sm text-gray-500">
            Showing {products.length} products
            {productsData?.total_count && ` of ${productsData.total_count}`}
          </span>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="w-12 px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={selectedProducts.length === products.length && products.length > 0}
                    onChange={toggleAllProducts}
                    className="rounded border-gray-300"
                  />
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Product
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  SKU
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Stock
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Images
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Modified
                </th>
                <th className="w-12 px-6 py-3"></th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {products.map((product) => (
                <tr key={product.name} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedProducts.includes(product.name)}
                      onChange={() => toggleProductSelection(product.name)}
                      className="rounded border-gray-300"
                    />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-3">
                      <button
                        onClick={() => handleStarToggle(product.name)}
                        disabled={starMutation.isPending}
                        className="p-1 hover:bg-gray-100 rounded"
                      >
                        <Star 
                          className={`h-4 w-4 ${
                            product.is_starred 
                              ? 'text-yellow-400 fill-current' 
                              : 'text-gray-300 hover:text-yellow-400'
                          }`} 
                        />
                      </button>
                      <div className="font-medium text-gray-900 text-sm">
                        {product.item_name}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {product.item_code}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {product.item_group}
                  </td>
                  <td className="px-6 py-4">
                    <Badge
                      variant={getStatusVariant(product.status) as any}
                      className="text-xs"
                    >
                      {product.status}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {product.stock_qty}
                  </td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {formatCurrency(product.standard_rate)}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-1">
                      <Image className="h-4 w-4 text-blue-600" />
                      <span className="text-sm text-blue-600">
                        {product.image_count}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {formatDate(product.modified)}
                  </td>
                  <td className="px-6 py-4">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
