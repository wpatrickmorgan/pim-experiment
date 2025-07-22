"use client";

import { usePathname } from "next/navigation";
import { Bell, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";

function getPageTitle(pathname: string) {
  switch (pathname) {
    case "/":
      return "Dashboard";
    case "/products":
      return "Products";
    case "/categories":
      return "Categories";
    case "/catalog":
      return "Catalog";
    default:
      return "Dashboard";
  }
}

export function Header() {
  const pathname = usePathname();
  const pageTitle = getPageTitle(pathname);

  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6">
      <div className="flex items-center space-x-4">
        <h2 className="text-lg font-semibold text-gray-900">{pageTitle}</h2>
      </div>

      <div className="flex items-center space-x-4">
        <Button variant="outline" size="sm">
          View Catalog
        </Button>
        <Button size="sm">Add Product</Button>

        <div className="relative">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
            <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-red-500 text-xs text-white flex items-center justify-center">
              3
            </span>
          </Button>
        </div>

        <div className="flex items-center space-x-2">
          <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
            <span className="text-sm font-medium text-white">JD</span>
          </div>
          <span className="text-sm font-medium text-gray-700">John Doe</span>
          <ChevronDown className="h-4 w-4 text-gray-500" />
        </div>
      </div>
    </header>
  );
}
