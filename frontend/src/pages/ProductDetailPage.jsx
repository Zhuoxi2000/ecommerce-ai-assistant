import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { productApi } from '../api/api';

const ProductDetailPage = () => {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchProductDetail = async () => {
      try {
        setLoading(true);
        const data = await productApi.getProductDetail(productId);
        setProduct(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    
    fetchProductDetail();
  }, [productId]);
  
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <div className="inline-block h-10 w-10 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
        <p className="mt-4 text-gray-600">加载产品信息...</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p className="text-red-500">加载出错: {error}</p>
        <Link to="/" className="mt-4 inline-block text-blue-500 hover:underline">
          返回首页
        </Link>
      </div>
    );
  }
  
  if (!product) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p className="text-gray-600">未找到该产品</p>
        <Link to="/" className="mt-4 inline-block text-blue-500 hover:underline">
          返回首页
        </Link>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <Link to="/" className="text-blue-500 hover:underline mb-6 inline-block">
        &larr; 返回首页
      </Link>
      
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="md:flex">
          {/* 产品图片 */}
          <div className="md:w-1/2 bg-gray-100">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.title}
                className="w-full h-96 object-contain"
              />
            ) : (
              <div className="w-full h-96 flex items-center justify-center">
                <span className="text-gray-400">无图片</span>
              </div>
            )}
          </div>
          
          {/* 产品信息 */}
          <div className="md:w-1/2 p-6">
            <h1 className="text-2xl font-bold mb-2">{product.title}</h1>
            
            <div className="mb-4">
              <span className="text-gray-500">{product.brand}</span>
              <span className="mx-2">|</span>
              <span className="text-gray-500">{product.category}</span>
              {product.subcategory && (
                <>
                  <span className="mx-2">|</span>
                  <span className="text-gray-500">{product.subcategory}</span>
                </>
              )}
            </div>
            
            {/* 评分 */}
            <div className="flex items-center mb-4">
              <div className="flex text-yellow-500">
                {[...Array(5)].map((_, i) => (
                  <span key={i}>
                    {i < Math.floor(product.rating) ? '★' : '☆'}
                  </span>
                ))}
              </div>
              <span className="ml-2 text-gray-600">
                {product.rating.toFixed(1)} ({product.review_count} 评论)
              </span>
            </div>
            
            {/* 价格 */}
            <div className="text-2xl font-bold text-blue-600 mb-4">
              {product.currency} {product.price.toFixed(2)}
            </div>
            
            {/* 描述 */}
            <div className="mb-6">
              <h2 className="text-lg font-semibold mb-2">产品描述</h2>
              <p className="text-gray-700">{product.description}</p>
            </div>
            
            {/* 产品特性 */}
            {product.features && Object.keys(product.features).length > 0 && (
              <div className="mb-6">
                <h2 className="text-lg font-semibold mb-2">产品特性</h2>
                <ul className="list-disc pl-5">
                  {Object.entries(product.features).map(([key, value]) => (
                    <li key={key} className="text-gray-700">
                      <span className="font-semibold">{key}:</span> {value}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {/* 购买按钮 */}
            <button className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors">
              模拟购买
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;