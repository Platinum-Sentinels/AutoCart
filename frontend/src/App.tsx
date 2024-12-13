import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import SearchPage from './pages/SearchPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import UserInfoPage from './pages/UserInfoPage'
import SearchHistoryPage from './pages/SearchHistoryPage'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/user-info" element={<UserInfoPage />} />
        <Route path="/search-history" element={<SearchHistoryPage />} />
      </Routes>
    </Layout>
  )
}

export default App

