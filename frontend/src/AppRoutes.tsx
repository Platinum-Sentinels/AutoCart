import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./layouts/layout";
import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/LoginPage";
import SearchPage from "@/pages/SearchPage";
import SearchHistoryPage from "@/pages/SearchHistoryPage";
import SignUpPage from "@/pages/SignUpPage";
import UserInfoPage from "@/pages/UserInfoPage";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/search-history" element={<SearchHistoryPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/user-profile" element={<UserInfoPage />} /> {/* Fixed here */}
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
