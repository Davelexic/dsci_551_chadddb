import React, { useState } from 'react';
import { AlertCircle, Database, PlayCircle, Code } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import './App.css' 

const ChatDB = () => {
  const [selectedDatabase, setSelectedDatabase] = useState('');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);
  const [databaseType, setDatabaseType] = useState('');

  // Format DBHub.io response
  const formatDbHubResponse = (data) => {
    if (!Array.isArray(data)) return [];
    
    return data.map(row => 
      Array.isArray(row) 
        ? row.map(cell => cell?.Value !== undefined ? cell.Value : cell).filter(cell => cell !== null)
        : []
    );
  };

  // Handle database selection
  const handleDatabaseSelect = (dbType) => {
    setSelectedDatabase(dbType);
    addMessage('system', `Connected to ${dbType}`);
  };

  // Handle query submission
  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/query/table', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          database_type: selectedDatabase.toLowerCase()
        }),
      });

      const data = await response.json();

      if (data.status === 'error') {
        throw new Error(data.message || 'Failed to execute query');
      }

      // Add user's natural language query
      addMessage('user', query);
      
      // Add system's SQL query if available in the response
      if(data.database_used === 'mongodb'){
        if(data.sql_query){
          addMessage('sql',JSON.stringify(data.sql_query))
        }
      }
      else{
        if (data.sql_query) {
          addMessage('sql', data.sql_query);
        }
      }

      // Set database type for rendering
      setDatabaseType(selectedDatabase.toLowerCase());
      
      // Format the response data
      let formattedData;
      if(data.database_used === 'mongodb'){
        formattedData = (data.data)
      }
      else{
        formattedData = formatDbHubResponse(data.data);
      }
      setResults(formattedData);
      
      // Format the results for chat display
      const resultMessage = formattedData.length > 0
      ? (data.database_used === 'mongodb' 
         ? `Query executed successfully. Found ${formattedData.length} results.`
         : `Query executed successfully. Found ${formattedData.length - 1} results.`)
      : 'Query executed successfully. No results found.';
      
      addMessage('system', resultMessage);
    } catch (err) {
      setError(err.message);
      addMessage('system', `Error: ${err.message}`);
    } finally {
      setLoading(false);
      setQuery('');
    }
  };

  // Add message to chat
  const addMessage = (type, content) => {
    setMessages((prev) => [...prev, { type, content, timestamp: new Date() }]);
  };

  const renderResults = (results) => {
    if (!results || results.length === 0) return null;
    
    if (databaseType === 'mongodb') {
      return (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg">
          <pre className="whitespace-pre-wrap text-sm overflow-x-auto">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      );
    }

    return (
      <div className="overflow-x-auto mt-4">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              {results[0].map((header, i) => (
                <th key={i} className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {String(header)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {results.slice(1).map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <td key={j} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  // Render message based on type
  const renderMessage = (msg, idx, isLast) => {
    const messageClasses = {
      user: 'bg-blue-100',
      system: 'bg-gray-100',
      sql: 'bg-gray-800 text-white font-mono',
    };

    return (
      <div 
        key={idx} 
        className={`p-3 rounded-lg ${messageClasses[msg.type] || 'bg-gray-100'}`}
      >
        <div className="flex justify-between items-start">
          <strong className="flex items-center gap-2">
            {msg.type === 'user' ? 'You' : 
             msg.type === 'sql' ? <><Code size={16} /> SQL Query</> : 
             'ChatDB'}:
          </strong>
          <span className="text-xs text-gray-500">
            {msg.timestamp.toLocaleTimeString()}
          </span>
        </div>
        <div className="mt-1">
          {msg.type === 'sql' ? (
            <pre className="whitespace-pre-wrap text-sm">{msg.content}</pre>
          ) : (
            msg.content
          )}
        </div>
        {isLast && msg.type === 'system' && results && renderResults(results)}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto space-y-4">
        {/* Header */}
        {/* <Card>
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">ChatDB</CardTitle>
          </CardHeader>
        </Card> */}
        <h1 className="page-title">ChatDB</h1>

        {/* Database Selection */}
        <Card>
          <CardHeader>
            <CardTitle>Select Database</CardTitle>
          </CardHeader>
          <CardContent className="flex gap-4">
            <button
              onClick={() => handleDatabaseSelect('SQLite')}
              className={`p-3 rounded flex items-center gap-2 ${
                selectedDatabase === 'SQLite' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100'
              }`}
            >
              <Database size={20} /> SQLite
            </button>
            <button
              onClick={() => handleDatabaseSelect('MongoDB')}
              className={`p-3 rounded flex items-center gap-2 ${
                selectedDatabase === 'MongoDB' ? 'bg-green-100 text-green-700' : 'bg-gray-100'
              }`}
            >
              <Database size={20} /> MongoDB
            </button>
          </CardContent>
        </Card>

        {/* Query Input */}
        <Card>
          <CardContent>
            <form onSubmit={handleQuerySubmit} className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your question (e.g., 'Show me today's sales')"
                className="flex-1 p-3 border rounded-lg"
                disabled={!selectedDatabase || loading}
              />
              <button 
                type="submit" 
                disabled={!selectedDatabase || loading} 
                className="p-3 bg-blue-600 text-white rounded-lg flex items-center gap-2 hover:bg-blue-700 disabled:bg-blue-300"
              >
                <PlayCircle size={20} />
                {loading ? 'Sending...' : 'Send'}
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

        {/* Chat Messages and Results */}
        <Card>
          <CardHeader>
            <CardTitle>Chat History</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {messages.map((msg, idx) => 
              renderMessage(msg, idx, idx === messages.length - 1)
            )}
            {messages.length === 0 && (
              <div className="text-center text-gray-500">
                No messages yet. Start by selecting a database and asking a question!
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ChatDB;