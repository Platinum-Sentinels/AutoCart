import '@/styles/globals.css'
import { Inter } from 'next/font/google'
import Sidebar from '@/components/Sidebar'
import { ShoppingCart } from 'lucide-react'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'AutoCart - AI Shopping Assistant',
  description: 'Find the best products across multiple online stores',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
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
      </body>
    </html>
  )
}

