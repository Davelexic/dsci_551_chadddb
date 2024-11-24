import React, { useState } from 'react';
import { AlertCircle, Database, PlayCircle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';


const ChatDB = () => {
  const [selectedDatabase, setSelectedDatabase] = useState('');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Handle database selection
  const handleDatabaseSelect = async (dbType) => {
    try {
      setLoading(true);
      setSelectedDatabase(dbType);

      // Replace with actual backend endpoint
      const response = await fetch('/api/database/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ databaseType: dbType }),
      });

      if (!response.ok) throw new Error('Failed to connect to database');
      const data = await response.json();
      addMessage('system', `Connected to ${dbType}. Available tables: ${data.tables.join(', ')}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle query submission
  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setLoading(true);
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          databaseType: selectedDatabase,
        }),
      });

      if (!response.ok) throw new Error('Failed to execute query');
      const data = await response.json();

      addMessage('user', query);
      addMessage('system', data.response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  // Handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('databaseType', selectedDatabase);

      const response = await fetch('/api/database/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to upload file');
      const data = await response.json();
      addMessage('system', `Uploaded ${file.name} to ${selectedDatabase}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Add message to chat
  const addMessage = (type, content) => {
    setMessages((prev) => [...prev, { type, content }]);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto space-y-4">
        {/* Header */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">ChatDB</CardTitle>
          </CardHeader>
        </Card>

        {/* Database Selection */}
        <Card>
          <CardHeader>
            <CardTitle>Select Database</CardTitle>
          </CardHeader>
          <CardContent className="flex gap-4">
            <button
              onClick={() => handleDatabaseSelect('MySQL')}
              className={`p-3 rounded ${selectedDatabase === 'MySQL' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100'}`}
            >
              <Database size={20} /> MySQL
            </button>
            <button
              onClick={() => handleDatabaseSelect('MongoDB')}
              className={`p-3 rounded ${selectedDatabase === 'MongoDB' ? 'bg-green-100 text-green-700' : 'bg-gray-100'}`}
            >
              <Database size={20} /> MongoDB
            </button>
          </CardContent>
        </Card>

        {/* File Upload */}
        {selectedDatabase && (
          <Card>
            <CardHeader>
              <CardTitle>Upload Dataset</CardTitle>
            </CardHeader>
            <CardContent>
              <input type="file" onChange={handleFileUpload} />
            </CardContent>
          </Card>
        )}

        {/* Query Input */}
        <Card>
          <CardContent>
            <form onSubmit={handleQuerySubmit} className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter query..."
                className="flex-1 p-3 border rounded-lg"
                disabled={!selectedDatabase || loading}
              />
              <button type="submit" disabled={!selectedDatabase || loading} className="p-3 bg-blue-600 text-white rounded-lg">
                <PlayCircle size={20} /> Send
              </button>
            </form>
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Chat Messages */}
        <Card>
          <CardHeader>
            <CardTitle>Chat History</CardTitle>
          </CardHeader>
          <CardContent>
            {messages.map((msg, idx) => (
              <div key={idx} className={`p-3 ${msg.type === 'user' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                <strong>{msg.type === 'user' ? 'You' : 'ChatDB'}:</strong> {msg.content}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ChatDB;
