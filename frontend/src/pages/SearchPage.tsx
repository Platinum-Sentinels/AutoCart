import SearchForm from '@/components/SearchForm'
import ResultsList from '@/components/ResultsList'

export default function SearchPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">Search Products</h1>
      <SearchForm />
      <ResultsList />
    </div>
  )
}
