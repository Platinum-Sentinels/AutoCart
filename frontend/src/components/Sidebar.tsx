'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Home, Search, User, LogIn, UserPlus, Clock } from 'lucide-react'

export default function Sidebar() {
  const pathname = usePathname()

  const links = [
    { href: '/', label: 'Home', icon: Home },
    { href: '/search', label: 'Search', icon: Search },
    { href: '/search-history', label: 'Search History', icon: Clock },
    { href: '/user-info', label: 'User Info', icon: User },
    { href: '/login', label: 'Login', icon: LogIn },
    { href: '/signup', label: 'Sign Up', icon: UserPlus },
  ]

  return (
    <div className="w-64 bg-card text-card-foreground h-screen p-4 border-r">
      <nav className="space-y-2">
        {links.map((link) => (
          <Button
            key={link.href}
            asChild
            variant={pathname === link.href ? "secondary" : "ghost"}
            className="w-full justify-start"
            size="sm"
          >
            <Link href={link.href}>
              <link.icon className="mr-2 h-4 w-4" />
              {link.label}
            </Link>
          </Button>
        ))}
      </nav>
    </div>
  )
}

