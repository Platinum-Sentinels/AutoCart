import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface SearchHistoryItem {
  id: string;
  query: string;
  date: string;
  results: number;
}

export default function SearchHistoryPage() {
  const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);

  useEffect(() => {
    setSearchHistory([
      {
        id: "1",
        query: "Wireless headphones",
        date: "2023-06-01",
        results: 15,
      },
      {
        id: "2",
        query: "Smartphone under $500",
        date: "2023-05-28",
        results: 23,
      },
      {
        id: "3",
        query: "Best laptop for programming",
        date: "2023-05-25",
        results: 18,
      },
    ]);
  }, []);

  const handleClearHistory = () => {
    setSearchHistory([]);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-2xl">Search History</CardTitle>
      </CardHeader>
      <CardContent>
        {searchHistory.length === 0 ? (
          <p>No search history available.</p>
        ) : (
          <ul className="space-y-4">
            {searchHistory.map((item, index) => (
              <li key={item.id}>
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">{item.query}</h3>
                    <p className="text-sm text-muted-foreground">
                      {item.date} • {item.results} results
                    </p>
                  </div>
                  <div className="space-x-2">
                    <Button variant="outline" size="sm">
                      Repeat Search
                    </Button>
                    <Button variant="ghost" size="sm">
                      Delete
                    </Button>
                  </div>
                </div>
                {index < searchHistory.length - 1 && (
                  <Separator className="mt-4" />
                )}
              </li>
            ))}
          </ul>
        )}
        <div className="mt-6 space-x-2 text-right">
          <Button onClick={handleClearHistory} size="sm" variant="destructive">
            Clear History
          </Button>
          <Button size="sm" variant="outline">
            Export History
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

