import { ShoppingCart } from 'lucide-react'
import Sidebar from './Sidebar'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <div className="flex-1">
        <header className="bg-primary text-primary-foreground shadow-md py-2">
          <div className="container mx-auto px-4 flex items-center">
            <ShoppingCart className="w-6 h-6 mr-2" />
            <h1 className="text-xl font-bold">AutoCart</h1>
          </div>
        </header>
        <main className="container mx-auto px-4 py-6">
          {children}
        </main>
      </div>
    </div>
  )
}

