"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface UserInfo {
  name: string;
  email: string;
  avatar: string;
  searchCount: number;
  joinDate: string;
  preferences: {
    categories: string[];
    priceRange: string;
  };
}

export default function UserInfoPage() {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);

  useEffect(() => {
    setUserInfo({
      name: "John Doe",
      email: "john@example.com",
      avatar: "https://api.dicebear.com/6.x/avataaars/svg?seed=John",
      searchCount: 15,
      joinDate: "2023-01-15",
      preferences: {
        categories: ["Electronics", "Books", "Home & Kitchen"],
        priceRange: "$50 - $500",
      },
    });
  }, []);

  const handleLogout = () => {
    console.log("User logged out");
  };

  if (!userInfo) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto">
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-4">
            <Avatar className="w-16 h-16">
              <AvatarImage src={userInfo.avatar} alt={userInfo.name} />
              <AvatarFallback>{userInfo.name.charAt(0)}</AvatarFallback>
            </Avatar>
            <div>
              <CardTitle className="text-2xl">{userInfo.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{userInfo.email}</p>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="profile" className="w-full">
            <TabsList className="w-full">
              <TabsTrigger value="profile" className="flex-1">
                Profile
              </TabsTrigger>
              <TabsTrigger value="preferences" className="flex-1">
                Preferences
              </TabsTrigger>
            </TabsList>
            <TabsContent value="profile" className="space-y-4 mt-4">
              <div>
                <h3 className="font-semibold">Member Since</h3>
                <p>{userInfo.joinDate}</p>
              </div>
              <div>
                <h3 className="font-semibold">Total Searches</h3>
                <p>{userInfo.searchCount}</p>
              </div>
            </TabsContent>
            <TabsContent value="preferences" className="space-y-4 mt-4">
              <div>
                <h3 className="font-semibold">Favorite Categories</h3>
                <ul className="list-disc list-inside">
                  {userInfo.preferences.categories.map((category, index) => (
                    <li key={index}>{category}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="font-semibold">Preferred Price Range</h3>
                <p>{userInfo.preferences.priceRange}</p>
              </div>
            </TabsContent>
          </Tabs>
          <div className="mt-6 space-x-2">
            <Button onClick={handleLogout} size="sm">
              Logout
            </Button>
            <Button variant="outline" size="sm">
              Edit Profile
            </Button>
            <Button variant="ghost" size="sm">
              Change Password
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
