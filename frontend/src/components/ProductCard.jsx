import React from 'react';
import { Link } from 'react-router-dom';

const ProductCard = ({ product }) => {
  if (!product) return null;
  
  // 处理可能的不同字段名称
  const id = product.id;
  const name = product.name || product.title;
  const description = product.description;
  const price = product.price;
  const currency = product.currency || 'CNY';
  const category = product.category;
  const imageUrl = product.image_url;
  
  return (
    <Link 
      to={`/product/${id}`}
      className="block bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
    >
      {/* 商品图片 */}
      <div className="bg-gray-100 h-48">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-full object-contain"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <span className="text-gray-400">无图片</span>
          </div>
        )}
      </div>
      
      {/* 商品信息 */}
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-1 truncate">{name}</h3>
        
        <div className="mb-2 flex items-center">
          <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
            {category}
          </span>
        </div>
        
        {description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {description}
          </p>
        )}
        
        <div className="text-blue-600 font-bold">
          {currency} {price ? price.toFixed(2) : '0.00'}
        </div>
      </div>
    </Link>
  );
};

export default ProductCard;