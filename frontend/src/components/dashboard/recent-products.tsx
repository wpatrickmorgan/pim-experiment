import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MoreHorizontal, Loader2 } from "lucide-react";
import { useProducts } from "@/lib/hooks";

function formatCurrency(amount: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

function formatDate(dateString: string) {
  const date = new Date(dateString);
  const now = new Date();
  const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
  
  if (diffInHours < 1) return 'Just now';
  if (diffInHours < 24) return `${diffInHours} hours ago`;
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays === 1) return '1 day ago';
  if (diffInDays < 7) return `${diffInDays} days ago`;
  
  return date.toLocaleDateString();
}

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
  const { data: products, isLoading, error } = useProducts(10, 0);

  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Products</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-6 gap-4 text-sm font-medium text-gray-500 border-b pb-2">
            <div>Product</div>
            <div>Code</div>
            <div>Group</div>
            <div>Stock</div>
            <div>Rate</div>
            <div>Modified</div>
          </div>
          
          {isLoading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin text-gray-400" />
              <span className="ml-2 text-gray-500">Loading products...</span>
            </div>
          )}
          
          {error && (
            <div className="text-center py-8 text-red-500">
              Failed to load products. Please check your connection.
            </div>
          )}
          
          {products && products.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No products found.
            </div>
          )}
          
          {products && products.map((product) => (
            <div
              key={product.name}
              className="grid grid-cols-6 gap-4 items-center py-2 hover:bg-gray-50 rounded-md px-2"
            >
              <div className="font-medium text-gray-900">{product.item_name}</div>
              <div className="text-gray-600">{product.item_code}</div>
              <div>
                <Badge variant="default">
                  {product.item_group}
                </Badge>
              </div>
              <div className="text-gray-600">{product.stock_qty || 0}</div>
              <div className="text-gray-900 font-medium">
                {product.standard_rate ? formatCurrency(product.standard_rate) : 'N/A'}
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-500">{formatDate(product.modified)}</span>
                <MoreHorizontal className="h-4 w-4 text-gray-400" />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
