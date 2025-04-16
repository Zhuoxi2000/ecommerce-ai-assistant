import React from 'react';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';

const Header = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-blue-600 mb-4 md:mb-0">
          AI电商助手
        </Link>
        
        <div className="w-full md:w-2/3 lg:w-1/2">
          <SearchBar />
        </div>
      </div>
    </header>
  );
};

export default Header;