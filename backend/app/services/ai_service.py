import json
from typing import Dict, Any, List, Optional
import logging
from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI服务，用于处理自然语言理解任务"""
    
    def __init__(self):
        """初始化AI服务"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_AI_MODEL
    
    async def parse_search_intent(self, query: str) -> Dict[str, Any]:
        """
        解析用户搜索意图
        
        Args:
            query: 用户的自然语言查询字符串
            
        Returns:
            解析后的意图数据，包含产品类型、价格范围、品牌等信息
        """
        try:
            if not settings.OPENAI_API_KEY:
                logger.warning("未设置OpenAI API密钥，使用模拟数据")
                return self._mock_intent_data(query)
            
            prompt = self._build_intent_prompt(query)
            
            # 使用同步API调用
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的电商搜索意图分析助手，可以从用户的自然语言查询中提取关键信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            # 从回复中提取JSON
            try:
                # 尝试直接解析整个回复
                intent_data = json.loads(content)
            except json.JSONDecodeError:
                # 如果失败，尝试提取内容中的JSON部分
                start_index = content.find('{')
                end_index = content.rfind('}') + 1
                if start_index >= 0 and end_index > start_index:
                    json_str = content[start_index:end_index]
                    intent_data = json.loads(json_str)
                else:
                    # 无法提取JSON，使用模拟数据
                    logger.warning(f"无法从AI回复中提取JSON: {content}")
                    intent_data = self._mock_intent_data(query)
            
            return intent_data
        
        except Exception as e:
            logger.error(f"解析搜索意图失败: {str(e)}")
            # 出错时使用简单的模拟数据
            return self._mock_intent_data(query)
    
    def _build_intent_prompt(self, query: str) -> str:
        """构建提示信息"""
        return f"""
        请分析以下电商搜索查询，提取关键信息，并以JSON格式返回：

        用户查询: "{query}"

        请提取以下字段:
        1. 产品类型 (比如"手机"、"衣服"、"家具"等)
        2. 价格范围 (如果有提及)
        3. 品牌 (如果有提及)
        4. 关键词 (描述产品特性的词，如"轻薄"、"防水"等)
        5. 排序偏好 (如"价格从低到高"、"评分最高"等)

        仅返回一个有效的JSON对象，格式如下:
        {{
            "product_type": "产品类别",
            "price_range": {{"min": 最低价格, "max": 最高价格}},
            "brands": ["品牌1", "品牌2"],
            "keywords": ["关键词1", "关键词2"],
            "sort_preference": "排序偏好"
        }}

        如果某个字段未提及，请使用null或空列表。
        """
    
    def _mock_intent_data(self, query: str) -> Dict[str, Any]:
        """生成模拟意图数据，增强对价格区间和产品类型的理解"""
        # 转换为小写并分词
        query_lower = query.lower()
        words = query_lower.split()
        
        # 识别可能的产品类型
        product_categories = {
            "手机": ["手机", "智能手机", "phone", "iphone", "华为", "小米", "三星", "oppo", "vivo"],
            "电脑": ["电脑", "笔记本", "台式机", "平板", "laptop", "macbook", "surface", "thinkpad"],
            "相机": ["相机", "单反", "微单", "camera", "gopro", "佳能", "尼康", "索尼"],
            "耳机": ["耳机", "airpods", "蓝牙耳机", "headphone", "earphone", "耳麦"],
            "服装": ["衣服", "裤子", "鞋子", "外套", "连衣裙", "t恤", "牛仔裤", "夹克"],
            "家具": ["家具", "桌子", "椅子", "沙发", "床", "柜子", "书架"],
            "食品": ["食品", "零食", "饮料", "水果", "蔬菜", "肉类", "海鲜", "糕点"]
        }
        
        # 检查产品类型
        identified_category = "其他"
        for category, keywords in product_categories.items():
            for keyword in keywords:
                if keyword in query_lower:
                    identified_category = category
                    break
            if identified_category != "其他":
                break
        
        # 识别可能的品牌
        common_brands = {
            "手机": ["苹果", "华为", "小米", "三星", "oppo", "vivo", "荣耀"],
            "电脑": ["苹果", "联想", "戴尔", "惠普", "华硕", "微软", "宏碁"],
            "相机": ["佳能", "尼康", "索尼", "富士", "松下", "奥林巴斯", "徕卡", "gopro"],
            "耳机": ["苹果", "索尼", "bose", "森海塞尔", "beats", "华为", "小米"]
        }
        
        identified_brands = []
        relevant_brands = common_brands.get(identified_category, [])
        for brand in relevant_brands:
            if brand.lower() in query_lower:
                identified_brands.append(brand)
        print(identified_brands, "identified_brands")
        # 增强的价格范围识别
        price_range = {"min": 0, "max": 0}
        
        # 1. 检查常见价格表达方式
        price_patterns = [
            # 模式1: "低于X元"、"不超过X元"、"X元以下"
            ("低于", lambda x: {"min": 0, "max": x}),
            ("不超过", lambda x: {"min": 0, "max": x}),
            ("小于", lambda x: {"min": 0, "max": x}),
            ("以下", lambda x: {"min": 0, "max": x}),
            
            # 模式2: "高于X元"、"超过X元"、"X元以上"
            ("高于", lambda x: {"min": x, "max": 0}),
            ("超过", lambda x: {"min": x, "max": 0}),
            ("大于", lambda x: {"min": x, "max": 0}),
            ("以上", lambda x: {"min": x, "max": 0}),
            
            # 模式3: "X元到Y元之间"、"X元-Y元"
            ("到", lambda x, y: {"min": x, "max": y}),
            ("至", lambda x, y: {"min": x, "max": y}),
            ("-", lambda x, y: {"min": x, "max": y}),
            ("~", lambda x, y: {"min": x, "max": y}),
            
            # 模式4: "大约X元"、"X元左右"
            ("大约", lambda x: {"min": x * 0.8, "max": x * 1.2}),
            ("左右", lambda x: {"min": x * 0.8, "max": x * 1.2}),
            ("附近", lambda x: {"min": x * 0.8, "max": x * 1.2})
        ]
        
        # 提取数字函数
        def extract_number(text):
            import re
            nums = re.findall(r'\d+', text)
            return float(nums[0]) if nums else 0
        
        # 遍历文本查找价格表达
        for i, word in enumerate(words):
            # 检查是否包含数字和货币符号
            if any(char.isdigit() for char in word):
                price_value = extract_number(word)
                
                # 检查价格模式
                for pattern, handler in price_patterns:
                    # 检查当前词
                    if pattern in word:
                        if handler.__code__.co_argcount == 1:
                            price_dict = handler(price_value)
                            price_range.update(price_dict)
                            break
                    
                    # 检查相邻词的组合
                    if i > 0 and pattern in words[i-1]:
                        if handler.__code__.co_argcount == 1:
                            price_dict = handler(price_value)
                            price_range.update(price_dict)
                            break
                    elif i < len(words) - 1 and pattern in words[i+1]:
                        if handler.__code__.co_argcount == 1:
                            price_dict = handler(price_value)
                            price_range.update(price_dict)
                            break
        
        # 如果找到了数字但没有找到明确的价格范围模式，假设这是一个具体价格
        if price_range["min"] == 0 and price_range["max"] == 0:
            for word in words:
                if any(char.isdigit() for char in word):
                    try:
                        # 提取价格数字
                        price = extract_number(word)
                        if price > 0:
                            # 设置一个默认范围
                            price_range["min"] = price * 0.8
                            price_range["max"] = price * 1.2
                            break
                    except (ValueError, IndexError):
                        pass
        
        # 返回最终的意图数据
        print("Return Mock result",{"product_type": identified_category,"price_range": price_range,"brands": identified_brands,"keywords": [w for w in words if len(w) > 1 and w not in product_categories.get(identified_category, [])],"sort_preference": None})
        return {
            "product_type": identified_category,
            "price_range": price_range,
            "brands": identified_brands,
            "keywords": [w for w in words if len(w) > 1 and w not in product_categories.get(identified_category, [])],
            "sort_preference": None
        }

    async def get_product_recommendations(self, 
                                         product_id: int, 
                                         user_preferences: Optional[Dict[str, Any]] = None
                                        ) -> List[Dict[str, Any]]:
        """
        获取产品推荐
        
        Args:
            product_id: 产品ID
            user_preferences: 用户偏好数据
            
        Returns:
            推荐产品列表
        """
        # 这里暂时返回模拟数据
        # 实际实现中，可能会基于产品属性和用户偏好调用AI进行推荐
        return [
            {
                "id": 101,
                "name": "推荐产品1",
                "price": 299,
                "category": "电子产品",
                "recommendation_score": 0.92
            },
            {
                "id": 102,
                "name": "推荐产品2",
                "price": 199,
                "category": "电子产品",
                "recommendation_score": 0.85
            }
        ]