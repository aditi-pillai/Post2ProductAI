import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import PrivateRoute from './components/PrivateRoute';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import InstagramPosts from './pages/InstagramPosts';
import ProductCreation from './pages/ProductCreation';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Register from './pages/Register';
import InstagramAuth from './components/InstaConnect/InstagramAuth';
import MediaGallery from './components/InstaConnect/MediaGallery';
import InstagramCallback from './pages/InstagramCallback';
import ShopifySettings from './pages/ShopifySettings';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected Routes */}
            <Route element={<PrivateRoute />}>
              <Route element={<Layout />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/instagram" element={<InstagramPosts />} />
                <Route path="/product/create" element={<ProductCreation />} />
                <Route path="/instagram/callback" element={<InstagramCallback />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="/shopify" element={<ShopifySettings />} />
              </Route>
            </Route>

            {/* New Instagram Connect routes */}
            <Route path="/instagram/connect" element={<InstagramAuth />} />
            <Route path="/instagram/media" element={<MediaGallery />} />

            {/* Redirect any unknown routes to dashboard */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 