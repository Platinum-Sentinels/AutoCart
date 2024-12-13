import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./layouts/layout"; // Adjusted import path for Layout component
import HomePage from "@/pages/HomePage"; // Correct path for HomePage
import LoginPage from "@/pages/LoginPage"; // Ensure LoginPage path is correct
import SearchPage from "@/pages/SearchPage"; // Adjust for SearchPage
import SearchHistoryPage from "@/pages/SearchHistoryPage"; // Adjust for SearchHistoryPage
import SignUpPage from "@/pages/SignUpPage"; // Adjust for SignUpPage
import UserInfoPage from "@/pages/UserInfoPage"; // Adjust for UserInfoPage

const AppRoutes = () => {
  return (
    <Routes>
      {/* Main Layout Route */}
      <Route path="/" element={<Layout />}>
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
