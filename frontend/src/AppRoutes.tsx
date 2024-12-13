import { Navigate, Route, Routes } from 'react-router-dom';
import Layout from './layouts/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SearchPage from './pages/SearchPage';
import SearchHistoryPage from './pages/SearchHistoryPage';
import SignUpPage from './pages/SignupPage';
import UserInfoPage from './pages/UserInfoPage';

const AppRoutes = () => {
  return (
    <Routes>
      {/* Main Layout Route */}
      <Route path="/" element={<Layout children={undefined} />}>
        <Route index element={<HomePage />} /> {/* Default home route */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/search-history" element={<SearchHistoryPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/user-profile" element={<UserInfoPage />} />
      </Route>

      {/* Redirect for unmatched routes */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
