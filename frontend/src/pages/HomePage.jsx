import React, { useEffect, useState } from 'react';
import ProductList from '../components/ProductList';
import { productApi } from '../api/api';

const HomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      try {
        setLoading(true);
        const data = await productApi.getFeaturedProducts();
        setFeaturedProducts(data.items || []);
        setLoading(false);
      } catch (err) {
        console.error('获取推荐产品失败:', err);
        setError('获取推荐产品失败，请稍后再试');
        setLoading(false);
      }
    };
    
    fetchFeaturedProducts();
  }, []);
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-blue-50 p-8 rounded-lg mb-8 text-center">
        <h1 className="text-3xl font-bold text-blue-800 mb-4">
          欢迎使用AI电商助手
        </h1>
        <p className="text-lg text-blue-600 mb-6">
          使用自然语言描述你想要的产品，我们的AI助手会为你找到最匹配的商品
        </p>
        <p className="text-gray-600">
          试试输入: "找一款价格在5000元以下的轻薄笔记本电脑" 或 "我需要一台性价比高的相机"
        </p>
      </div>
      
      <div className="mb-6">
        <h2 className="text-2xl font-semibold mb-4">推荐产品</h2>
        <ProductList 
          products={featuredProducts} 
          loading={loading} 
          error={error} 
        />
      </div>
    </div>
  );
};

export default HomePage;