'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Star } from 'lucide-react'

interface Product {
  id: string
  name: string
  price: number
  description: string
  store: string
  link: string
  youtubeLink?: string
  rating: number
  reviewCount: number
}

export default function ResultsList() {
  const [products, setProducts] = useState<Product[]>([
    {
      id: '1',
      name: 'Sony WH-1000XM4',
      price: 349.99,
      description: 'Wireless noise-cancelling headphones with exceptional sound quality.',
      store: 'Amazon',
      link: 'https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B0863TXGM3',
      youtubeLink: 'https://www.youtube.com/watch?v=vjVYKRzlLnw',
      rating: 4.7,
      reviewCount: 28945
    },
    {
      id: '2',
      name: 'Bose QuietComfort 45',
      price: 329.00,
      description: 'Premium noise-cancelling headphones with balanced sound and comfort.',
      store: 'Best Buy',
      link: 'https://www.bestbuy.com/site/bose-quietcomfort-45-wireless-noise-cancelling-over-the-ear-headphones-triple-black/6471291.p',
      youtubeLink: 'https://www.youtube.com/watch?v=6j8MXjpVgdI',
      rating: 4.5,
      reviewCount: 12763
    }
  ])

  const renderRating = (rating: number) => {
    return (
      <div className="flex items-center">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`h-4 w-4 ${
              star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
          />
        ))}
        <span className="ml-2 text-sm">{rating.toFixed(1)}</span>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Search Results</h2>
      {products.map((product) => (
        <Card key={product.id}>
          <CardHeader>
            <CardTitle>{product.name}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">{product.description}</p>
            <p className="font-bold mt-2">Price: ${product.price.toFixed(2)}</p>
            <p className="text-sm">Store: {product.store}</p>
            <div className="mt-2">
              {renderRating(product.rating)}
              <span className="text-xs text-gray-500 ml-2">({product.reviewCount} reviews)</span>
            </div>
            <div className="mt-4 space-x-2">
              <Button asChild size="sm">
                <a href={product.link} target="_blank" rel="noopener noreferrer">View on {product.store}</a>
              </Button>
              {product.youtubeLink && (
                <Button variant="outline" size="sm" asChild>
                  <a href={product.youtubeLink} target="_blank" rel="noopener noreferrer">Watch Review</a>
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

