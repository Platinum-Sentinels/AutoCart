import "@/styles/globals.css";
import { Inter } from "next/font/google";
import Sidebar from "@/components/Sidebar";
import { ShoppingCart } from "lucide-react";
import { QueryClient, QueryClientProvider } from "react-query";
import { Toaster } from "sonner";
import { Auth0Provider } from "@auth0/auth0-react";

const inter = Inter({ subsets: ["latin"] });

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" style={{ height: "100%" }}>
      <Auth0Provider
        domain="YOUR_AUTH0_DOMAIN"
        clientId="YOUR_AUTH0_CLIENT_ID"
        authorizationParams={{
          redirect_uri:
            typeof window !== "undefined" ? window.location.origin : "",
        }}
      >
        <QueryClientProvider client={queryClient}>
          <body
            className={inter.className}
            style={{ height: "100%", margin: 0 }}
          >
            <div
              className="flex min-h-screen bg-background"
              style={{ height: "100%" }}
            >
              <Sidebar />
              <div className="flex-1 flex flex-col">
                <header className="bg-primary text-primary-foreground shadow-md py-2">
                  <div className="container mx-auto px-4 flex items-center">
                    <ShoppingCart className="w-6 h-6 mr-2" />
                    <h1 className="text-xl font-bold">AutoCart</h1>
                  </div>
                </header>
                <main className="container mx-auto px-4 py-6 flex-1">
                  {children}
                </main>
              </div>
            </div>
            <Toaster visibleToasts={1} position="top-right" richColors />
          </body>
        </QueryClientProvider>
      </Auth0Provider>
    </html>
  );
}
