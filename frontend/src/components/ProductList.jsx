import React from 'react';
import ProductCard from './ProductCard';

const ProductList = ({ products, loading, error }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
        <span className="ml-3 text-gray-600">加载中...</span>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">加载出错: {error}</p>
      </div>
    );
  }
  
  if (!products || products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">没有找到产品</p>
      </div>
    );
  }
  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};

export default ProductList;