import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import ProductList from '../components/ProductList';
import useSearchStore from '../store/searchStore';

const SearchResultsPage = () => {
  const searchQuery = useSearchStore((state) => state.searchQuery);
  const searchResults = useSearchStore((state) => state.searchResults);
  const isLoading = useSearchStore((state) => state.isLoading);
  const error = useSearchStore((state) => state.error);
  const currentPage = useSearchStore((state) => state.currentPage);
  const totalPages = useSearchStore((state) => state.totalPages);
  const totalResults = useSearchStore((state) => state.totalResults);
  const loadNextPage = useSearchStore((state) => state.loadNextPage);
  const loadPrevPage = useSearchStore((state) => state.loadPrevPage);
  const navigate = useNavigate();
  useEffect(() => {
    // 如果没有搜索查询，重定向到首页
    if (!searchQuery) {
      navigate('/');
    }
  }, [searchQuery, navigate]);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <SearchBar />
      </div>
      
      {searchQuery && (
        <div className="mb-4">
          <h1 className="text-2xl font-semibold">搜索结果: "{searchQuery}"</h1>
          {totalResults > 0 && (
            <p className="text-gray-600">找到 {totalResults} 个相关产品</p>
          )}
        </div>
      )}
      
      <ProductList
        products={searchResults}
        loading={isLoading}
        error={error}
      />
      
      {/* 分页控制 */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-4 mt-8">
          <button
            onClick={loadPrevPage}
            disabled={currentPage === 1 || isLoading}
            className={`px-4 py-2 rounded ${
              currentPage === 1 || isLoading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            上一页
          </button>
          
          <span className="text-gray-600">
            {currentPage} / {totalPages}
          </span>
          
          <button
            onClick={loadNextPage}
            disabled={currentPage === totalPages || isLoading}
            className={`px-4 py-2 rounded ${
              currentPage === totalPages || isLoading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            下一页
          </button>
        </div>
      )}
    </div>
  );
};

export default SearchResultsPage;