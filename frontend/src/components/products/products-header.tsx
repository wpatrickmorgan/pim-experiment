import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Upload, Download, Plus, Filter } from "lucide-react";

export function ProductsHeader() {
  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Products</h1>
          <p className="text-gray-600">
            Manage your product catalog and inventory
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <Upload className="h-4 w-4 mr-2" />
            Import
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Add Product
          </Button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input placeholder="Search products..." className="pl-10" />
        </div>

        <select className="h-10 rounded-md border border-input bg-background px-3 py-2 text-sm text-gray-700 min-w-[120px]">
          <option value="" className="text-gray-500">
            Category
          </option>
          <option value="electronics">Electronics</option>
          <option value="accessories">Accessories</option>
          <option value="furniture">Furniture</option>
        </select>

        <select className="h-10 rounded-md border border-input bg-background px-3 py-2 text-sm text-gray-700 min-w-[100px]">
          <option value="" className="text-gray-500">
            Status
          </option>
          <option value="active">Active</option>
          <option value="draft">Draft</option>
          <option value="review">Under Review</option>
        </select>

        <Button variant="outline" size="sm">
          <Filter className="h-4 w-4 mr-2" />
          Filter
        </Button>
      </div>
    </div>
  );
}
