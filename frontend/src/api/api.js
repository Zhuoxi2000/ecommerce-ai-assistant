import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8001/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 产品API
export const productApi = {
  // 获取推荐产品
  getFeaturedProducts: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/search/featured?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('获取推荐产品失败', error);
      throw error;
    }
  },
  
  // 根据ID获取产品详情
  getProductDetail: async (productId) => {
    try {
      const response = await apiClient.get(`/products/${productId}`);
      return response.data;
    } catch (error) {
      console.error('获取产品详情失败', error);
      throw error;
    }
  },
  
  // 自然语言搜索产品
  searchProducts: async (query, page = 1, limit = 10) => {
    try {
      const response = await apiClient.post('/search/natural', {
        query,
        page,
        limit
      });
      return response.data;
    } catch (error) {
      console.error('搜索产品失败', error);
      throw error;
    }
  }
};