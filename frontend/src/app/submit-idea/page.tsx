'use client';
import { useState } from 'react';
import axios from 'axios';

const SubmitIdea = () => {
  const [idea, setIdea] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Update the URL to your backend
      const res = await axios.post('http://127.0.0.1:8000/validate', { idea });
      // console.log(res,"fenillll");
      
      setResponse(res.data);
    } catch (error) {
      console.error('Error submitting idea:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Submit Your Idea</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="Describe your SaaS idea..."
          rows={5}
          className="w-full p-3 border border-gray-300 rounded-md mb-4"
        ></textarea>
        <button
          type="submit"
          className="bg-blue-500 text-white p-3 rounded-md"
          disabled={loading}
        >
          {loading ? 'Validating...' : 'Validate Idea'}
        </button>
      </form>
      {response && (
        <div className="mt-6">
          <h2 className="text-2xl font-semibold">Validation Result</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default SubmitIdea;