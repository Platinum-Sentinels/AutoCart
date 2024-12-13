import { useState, useEffect } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, ArrowRight } from 'lucide-react'

interface Product {
  id: string
  name: string
  price: number
  discountedPrice: number
  imageUrl: string
}

export default function LatestProductsBanner() {
  const [products, setProducts] = useState<Product[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    // In a real application, you would fetch this data from an API
    const mockProducts: Product[] = [
      {
        id: '1',
        name: 'Wireless Earbuds',
        price: 129.99,
        discountedPrice: 99.99,
        imageUrl: '/placeholder.svg?height=200&width=200'
      },
      {
        id: '2',
        name: 'Smart Watch',
        price: 249.99,
        discountedPrice: 199.99,
        imageUrl: '/placeholder.svg?height=200&width=200'
      },
      {
        id: '3',
        name: 'Noise-Cancelling Headphones',
        price: 299.99,
        discountedPrice: 249.99,
        imageUrl: '/placeholder.svg?height=200&width=200'
      },
    ]
    setProducts(mockProducts)
  }, [])

  const nextProduct = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % products.length)
  }

  const prevProduct = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + products.length) % products.length)
  }

  if (products.length === 0) {
    return null
  }

  const currentProduct = products[currentIndex]

  return (
    <Card className="w-full overflow-hidden">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold mb-4">Latest Deals</h2>
          <div className="space-x-2">
            <Button variant="outline" size="icon" onClick={prevProduct}>
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" onClick={nextProduct}>
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <div className="flex items-center space-x-6">
          <div className="flex-shrink-0">
            {/* Use a standard img tag instead of next/image */}
            <img
              src={currentProduct.imageUrl}
              alt={currentProduct.name}
              width={200}
              height={200}
              className="rounded-lg"
            />
          </div>
          <div className="flex-grow">
            <h3 className="text-xl font-semibold mb-2">{currentProduct.name}</h3>
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-2xl font-bold text-green-600">
                ${currentProduct.discountedPrice.toFixed(2)}
              </span>
              <span className="text-lg text-gray-500 line-through">
                ${currentProduct.price.toFixed(2)}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-4">
              Save ${(currentProduct.price - currentProduct.discountedPrice).toFixed(2)} on this amazing deal!
            </p>
            <Button>Shop Now</Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
