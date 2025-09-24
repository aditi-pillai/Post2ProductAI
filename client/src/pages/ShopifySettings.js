import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

function ShopifySettings() {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [connectionStatus, setConnectionStatus] = useState({
    connected: false,
    shop_domain: '',
    last_sync: null
  });

  const [formData, setFormData] = useState({
    shop_domain: '',
    access_token: ''
  });

  useEffect(() => {
    if (user?.shopify_connected) {
      setConnectionStatus({
        connected: true,
        shop_domain: user.shopify_shop_domain || '',
        last_sync: user.last_sync || null
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleConnect = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      await axios.post('/api/shopify/connect', formData);
      setSuccess('Shopify store connected successfully!');
      setConnectionStatus({
        connected: true,
        shop_domain: formData.shop_domain,
        last_sync: new Date().toISOString()
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to connect Shopify store');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    if (!window.confirm('Are you sure you want to disconnect your Shopify store?')) {
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      await axios.delete('/api/shopify/connect');
      setSuccess('Shopify store disconnected successfully!');
      setConnectionStatus({
        connected: false,
        shop_domain: '',
        last_sync: null
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to disconnect Shopify store');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestConnection = async () => {
    setIsLoading(true);
    setError('');

    try {
      await axios.post('/api/shopify/test-connection');
      setSuccess('Connection test successful!');
    } catch (err) {
      setError(err.response?.data?.error || 'Connection test failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Shopify Integration</h1>
        <p className="text-gray-600 mt-2">
          Connect your Shopify store to automatically publish products from Instagram posts.
        </p>
      </div>

      {/* Connection Status */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Connection Status</h2>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className={`w-4 h-4 rounded-full mr-3 ${
              connectionStatus.connected ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <div>
              <p className="font-medium text-gray-900">
                {connectionStatus.connected ? 'Connected' : 'Not Connected'}
              </p>
              {connectionStatus.connected && (
                <p className="text-sm text-gray-600">
                  Store: {connectionStatus.shop_domain}
                </p>
              )}
            </div>
          </div>
          
          {connectionStatus.connected && (
            <div className="flex space-x-2">
              <button
                onClick={handleTestConnection}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                Test Connection
              </button>
              <button
                onClick={handleDisconnect}
                disabled={isLoading}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                Disconnect
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Connection Form */}
      {!connectionStatus.connected && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Connect Shopify Store</h2>
          
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          {success && (
            <div className="mb-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
              {success}
            </div>
          )}

          <form onSubmit={handleConnect} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Shopify Shop Domain
              </label>
              <input
                type="text"
                name="shop_domain"
                value={formData.shop_domain}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="your-store (without .myshopify.com)"
              />
              <p className="text-sm text-gray-500 mt-1">
                Enter your Shopify store domain without .myshopify.com
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Admin API Access Token
              </label>
              <input
                type="password"
                name="access_token"
                value={formData.access_token}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter your Shopify Admin API access token"
              />
              <p className="text-sm text-gray-500 mt-1">
                Get this from your Shopify Admin → Apps → Develop apps → Create app
              </p>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className={`px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isLoading ? 'Connecting...' : 'Connect Store'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Setup Instructions */}
      <div className="bg-blue-50 rounded-lg p-6 mt-8">
        <h3 className="text-lg font-semibold text-blue-900 mb-4">Setup Instructions</h3>
        <div className="space-y-4 text-sm text-blue-800">
          <div>
            <h4 className="font-medium">1. Create a Custom App in Shopify</h4>
            <p>Go to your Shopify Admin → Settings → Apps and sales channels → Develop apps → Create app</p>
          </div>
          <div>
            <h4 className="font-medium">2. Configure API Access Scopes</h4>
            <p>Enable the following scopes: <code className="bg-blue-100 px-1 rounded">read_products</code>, <code className="bg-blue-100 px-1 rounded">write_products</code>, <code className="bg-blue-100 px-1 rounded">read_inventory</code>, <code className="bg-blue-100 px-1 rounded">write_inventory</code></p>
          </div>
          <div>
            <h4 className="font-medium">3. Install and Get Access Token</h4>
            <p>Install the app and copy the Admin API access token</p>
          </div>
          <div>
            <h4 className="font-medium">4. Enter Credentials Above</h4>
            <p>Enter your shop domain and access token in the form above</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ShopifySettings;
