"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();

  useEffect(() => {
    console.log('🔄 Root Dashboard: Redirecting to /pim');
    // Redirect to the /pim route where the actual dashboard is located
    router.push('/pim');
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Redirecting to PIM Dashboard...</p>
      </div>
    </div>
  );
}
