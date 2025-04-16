import { create } from 'zustand';
import { productApi } from '../api/api';

const useSearchStore = create((set, get) => ({
  // 状态
  searchQuery: '',
  searchResults: [],
  isLoading: false,
  error: null,
  currentPage: 1,
  totalPages: 1,
  totalResults: 0,
  
  // 动作
  search: async (query) => {
    // 新搜索时重置页码
    set({ 
      searchQuery: query, 
      isLoading: true, 
      error: null,
      currentPage: 1
    });
    
    try {
      const data = await productApi.searchProducts(query, 1);
      set({
        searchResults: data.items || [],
        totalResults: data.total || 0,
        totalPages: data.pages || 1,
        isLoading: false
      });
    } catch (err) {
      console.error('搜索失败:', err);
      set({
        error: '搜索失败，请稍后再试',
        searchResults: [],
        isLoading: false
      });
    }
  },
  
  loadNextPage: async () => {
    const { searchQuery, currentPage, totalPages } = get();
    if (currentPage >= totalPages) return;
    
    const nextPage = currentPage + 1;
    set({ isLoading: true, error: null });
    
    try {
      const data = await productApi.searchProducts(searchQuery, nextPage);
      set({
        searchResults: data.items || [],
        currentPage: nextPage,
        isLoading: false
      });
    } catch (err) {
      console.error('加载下一页失败:', err);
      set({
        error: '加载更多产品失败，请稍后再试',
        isLoading: false
      });
    }
  },
  
  loadPrevPage: async () => {
    const { searchQuery, currentPage } = get();
    if (currentPage <= 1) return;
    
    const prevPage = currentPage - 1;
    set({ isLoading: true, error: null });
    
    try {
      const data = await productApi.searchProducts(searchQuery, prevPage);
      set({
        searchResults: data.items || [],
        currentPage: prevPage,
        isLoading: false
      });
    } catch (err) {
      console.error('加载上一页失败:', err);
      set({
        error: '加载产品失败，请稍后再试',
        isLoading: false
      });
    }
  },
  
  // 重置搜索状态
  resetSearch: () => {
    set({
      searchQuery: '',
      searchResults: [],
      isLoading: false,
      error: null,
      currentPage: 1,
      totalPages: 1,
      totalResults: 0
    });
  }
}));

export default useSearchStore;