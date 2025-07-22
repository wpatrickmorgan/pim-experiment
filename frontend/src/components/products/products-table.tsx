"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MoreHorizontal, Star, Image } from "lucide-react";

const products = [
  {
    id: 1,
    name: "Wireless Bluetooth Headphones",
    sku: "WBH-001-BLK",
    category: "Electronics",
    status: "Active",
    stock: 156,
    price: "$79.99",
    images: 4,
    modified: "Jan 15, 02:35 AM",
    starred: true,
  },
  {
    id: 2,
    name: "Smartphone Case - Clear Protective",
    sku: "SPC-002-CLR",
    category: "Accessories",
    status: "Draft",
    stock: 23,
    price: "$14.99",
    images: 2,
    modified: "Jan 15, 03:12 AM",
    starred: false,
  },
  {
    id: 3,
    name: "USB-C Fast Charger 65W",
    sku: "UFC-003-65W",
    category: "Electronics",
    status: "Active",
    stock: 8,
    price: "$24.99",
    images: 3,
    modified: "Jan 15, 01:48 AM",
    starred: false,
  },
  {
    id: 4,
    name: "Wireless Mouse - Ergonomic Design",
    sku: "WME-004-ERG",
    category: "Accessories",
    status: "Review",
    stock: 92,
    price: "$34.99",
    images: 5,
    modified: "Jan 14, 11:02 AM",
    starred: true,
  },
  {
    id: 5,
    name: "Laptop Stand Adjustable Aluminum",
    sku: "LSA-005-ALU",
    category: "Furniture",
    status: "Active",
    stock: 67,
    price: "$49.99",
    images: 6,
    modified: "Jan 14, 09:18 AM",
    starred: false,
  },
  {
    id: 6,
    name: "Mechanical Keyboard RGB Backlit",
    sku: "MKB-006-RGB",
    category: "Electronics",
    status: "Active",
    stock: 134,
    price: "$89.99",
    images: 8,
    modified: "Jan 14, 07:05 AM",
    starred: false,
  },
  {
    id: 7,
    name: "Desk Lamp LED Adjustable",
    sku: "DLA-007-LED",
    category: "Furniture",
    status: "Active",
    stock: 45,
    price: "$39.99",
    images: 4,
    modified: "Jan 14, 06:42 AM",
    starred: false,
  },
];

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
  const [selectedProducts, setSelectedProducts] = useState<number[]>([]);

  const toggleProductSelection = (productId: number) => {
    setSelectedProducts((prev) =>
      prev.includes(productId)
        ? prev.filter((id) => id !== productId)
        : [...prev, productId],
    );
  };

  const toggleAllProducts = () => {
    setSelectedProducts((prev) =>
      prev.length === products.length ? [] : products.map((p) => p.id),
    );
  };

  return (
    <Card>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">
            Product Catalog
          </CardTitle>
          <span className="text-sm text-gray-500">
            Showing {products.length} products
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
                    checked={selectedProducts.length === products.length}
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
                <tr key={product.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedProducts.includes(product.id)}
                      onChange={() => toggleProductSelection(product.id)}
                      className="rounded border-gray-300"
                    />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-3">
                      {product.starred && (
                        <Star className="h-4 w-4 text-yellow-400 fill-current" />
                      )}
                      <div className="font-medium text-gray-900 text-sm">
                        {product.name}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {product.sku}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {product.category}
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
                    {product.stock}
                  </td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {product.price}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-1">
                      <Image className="h-4 w-4 text-blue-600" />
                      <span className="text-sm text-blue-600">
                        {product.images}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {product.modified}
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
