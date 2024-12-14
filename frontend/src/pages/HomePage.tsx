import { Link } from 'react-router-dom'; // Replace Next.js Link with React Router's Link
import { Button } from "@/components/ui/button"; // Ensure your component paths are adjusted
import LatestProductsBanner from '@/components/LatestProductsBanner';

export default function HomePage() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold mb-4">Welcome to AutoCart</h1>
        <p className="text-lg mb-4">Experience the future of shopping with our AI-powered platform.</p>
        <div className="space-x-2">
          <Button size="sm">
            <Link to="/search">Start Shopping</Link>
          </Button>
          <Button size="sm" variant="outline">
            <Link to="/about">Learn More</Link>
          </Button>
        </div>
      </div>
      <LatestProductsBanner />
    </div>
  );
}
