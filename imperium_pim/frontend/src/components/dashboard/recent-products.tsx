"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MoreHorizontal, Loader2 } from "lucide-react";
import { frappeAPI } from "@/lib/api";
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

export function RecentProducts() {
  const { data: productsData, isLoading, error } = useQuery({
    queryKey: ['recent-products'],
    queryFn: () => frappeAPI.getProducts({ limit: 5 }),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const products = productsData?.products || [];

  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Products</CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
            <span className="ml-2 text-gray-600">Loading...</span>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-600 mb-1">Error loading products</p>
            <p className="text-sm text-gray-500">{error.message}</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-6 gap-4 text-sm font-medium text-gray-500 border-b pb-2">
              <div>Product</div>
              <div>SKU</div>
              <div>Status</div>
              <div>Stock</div>
              <div>Price</div>
              <div>Modified</div>
            </div>
            {products.map((product) => (
              <div
                key={product.name}
                className="grid grid-cols-6 gap-4 items-center py-2 hover:bg-gray-50 rounded-md px-2"
              >
                <div className="font-medium text-gray-900 truncate">{product.item_name}</div>
                <div className="text-gray-600">{product.item_code}</div>
                <div>
                  <Badge variant={getStatusVariant(product.status) as any}>
                    {product.status}
                  </Badge>
                </div>
                <div className="text-gray-600">{product.stock_qty}</div>
                <div className="text-gray-900 font-medium">{formatCurrency(product.standard_rate)}</div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-500 text-sm">{formatDate(product.modified)}</span>
                  <MoreHorizontal className="h-4 w-4 text-gray-400" />
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
