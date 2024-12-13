import React from 'react';
import { Outlet } from 'react-router-dom'; // React Router's Outlet for nested routing
import Sidebar from '@/components/Sidebar'; // Adjust path to Sidebar component if needed
import { ShoppingCart } from 'lucide-react';
import '@/global.css'; // Import global styles

export default function Layout() { // Exported as Layout to match AppRoutes usage
  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar component */}
      <Sidebar />
      
      <div className="flex-1">
        {/* Header */}
        <header className="bg-primary text-primary-foreground shadow-md py-2">
          <div className="container mx-auto px-4 flex items-center">
            <ShoppingCart className="w-6 h-6 mr-2" />
            <h1 className="text-xl font-bold">AutoCart</h1>
          </div>
        </header>

        {/* Main content */}
        <main className="container mx-auto px-4 py-6">
          {/* Outlet renders the child routes */}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
