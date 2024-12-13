import { Link } from 'react-router-dom'
import { Button } from "@/components/ui/button"
import LatestProductsBanner from '@/components/LatestProductsBanner'

export default function HomePage() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold mb-4">Welcome to AutoCart</h1>
        <p className="text-lg mb-4">Experience the future of shopping with our AI-powered platform.</p>
        <div className="space-x-2">
          <Button asChild size="sm">
            <Link to="/search">Start Shopping</Link>
          </Button>
          <Button asChild size="sm" variant="outline">
            <Link to="/about">Learn More</Link>
          </Button>
        </div>
      </div>
      <LatestProductsBanner />
    </div>
  )
}

