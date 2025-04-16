import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useSearchStore from '../store/searchStore';

const SearchBar = () => {
  const navigate = useNavigate();
  const search = useSearchStore((state) => state.search);
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      search(query);
      navigate('/search');
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="flex w-full">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="输入商品描述、需求或关键词..."
        className="flex-grow px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded-r-md hover:bg-blue-700 transition-colors"
      >
        搜索
      </button>
    </form>
  );
};

export default SearchBar;