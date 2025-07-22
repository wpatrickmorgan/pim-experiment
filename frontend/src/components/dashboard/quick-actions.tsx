import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, Upload, Download, Archive } from "lucide-react";

const actions = [
  {
    title: "Add New Product",
    description: "Create a new product listing",
    icon: Plus,
    color: "bg-blue-500 hover:bg-blue-600",
  },
  {
    title: "Import Products",
    description: "Bulk import from CSV/Excel",
    icon: Upload,
    color: "bg-green-500 hover:bg-green-600",
  },
  {
    title: "Export Catalog",
    description: "Download product catalog",
    icon: Download,
    color: "bg-purple-500 hover:bg-purple-600",
  },
  {
    title: "Manage Categories",
    description: "Organize product categories",
    icon: Archive,
    color: "bg-orange-500 hover:bg-orange-600",
  },
];

export function QuickActions() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {actions.map((action, index) => (
          <div key={index} className="flex items-start space-x-3">
            <div className={`p-2 rounded-md ${action.color}`}>
              <action.icon className="h-4 w-4 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">
                {action.title}
              </p>
              <p className="text-xs text-gray-500">{action.description}</p>
            </div>
          </div>
        ))}

        <div className="pt-4 border-t">
          <h4 className="text-sm font-medium text-gray-900 mb-3">
            System Status
          </h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-600">Data Quality</span>
              <div className="w-16 bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-green-500 h-1.5 rounded-full"
                  style={{ width: "78%" }}
                ></div>
              </div>
              <span className="text-xs text-gray-500">78%</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
