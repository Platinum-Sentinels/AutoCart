'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Textarea } from "@/components/ui/textarea"
import VoiceInput from './VoiceInput'
import { Upload } from 'lucide-react'

export default function SearchForm() {
  const [searchParams, setSearchParams] = useState({
    query: '',
    features: '',
    brands: '',
    budget: 1000,
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setSearchParams({ ...searchParams, [e.target.name]: e.target.value })
  }

  const handleBudgetChange = (value: number[]) => {
    setSearchParams({ ...searchParams, budget: value[0] })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Search params:', searchParams)
    // Here you would typically send the search params to your backend
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // Here you would typically send the file to your backend for processing
      console.log('File uploaded:', file.name)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <Label htmlFor="query">What are you looking for?</Label>
        <div className="flex space-x-2">
          <Input
            id="query"
            name="query"
            value={searchParams.query}
            onChange={handleInputChange}
            placeholder="e.g. Wireless headphones with noise cancellation"
            className="flex-grow"
          />
          <VoiceInput onTranscript={(transcript) => setSearchParams({ ...searchParams, query: transcript })} />
        </div>
      </div>
      <div>
        <Label htmlFor="features">Desired features</Label>
        <Textarea
          id="features"
          name="features"
          value={searchParams.features}
          onChange={handleInputChange}
          placeholder="e.g. Waterproof, Long battery life"
          rows={3}
        />
      </div>
      <div>
        <Label htmlFor="brands">Preferred brands</Label>
        <Input
          id="brands"
          name="brands"
          value={searchParams.brands}
          onChange={handleInputChange}
          placeholder="e.g. Sony, Bose, Apple"
        />
      </div>
      <div>
        <Label htmlFor="budget">Budget (USD)</Label>
        <Slider
          id="budget"
          min={0}
          max={5000}
          step={50}
          value={[searchParams.budget]}
          onValueChange={handleBudgetChange}
        />
        <div className="text-right mt-2">${searchParams.budget}</div>
      </div>
      <div>
        <Label htmlFor="file">Upload a document with requirements</Label>
        <div className="flex items-center space-x-2">
          <Input id="file" type="file" accept=".txt,.pdf,.doc,.docx" onChange={handleFileUpload} className="flex-grow" />
          <Button type="button" size="icon" variant="outline">
            <Upload className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <Button type="submit" className="w-full">Search Products</Button>
    </form>
  )
}

