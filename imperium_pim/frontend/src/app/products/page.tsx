import { AppLayout } from "@/components/layout/app-layout";
import { ProductsTable } from "@/components/products/products-table";
import { ProductsHeader } from "@/components/products/products-header";

export default function ProductsPage() {
  return (
    <AppLayout>
      <div className="p-6">
        <ProductsHeader />
        <ProductsTable />
      </div>
    </AppLayout>
  );
}
