import json
from typing import Dict, Any, List, Optional
import logging
from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI服务，用于处理自然语言理解任务"""
    
    def __init__(self):
        """初始化AI服务"""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
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
            
            response = await self.client.chat.completions.create(
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
        """生成模拟意图数据"""
        # 简单的关键词提取
        words = query.lower().split()
        
        # 识别可能的产品类型
        product_types = ["手机", "电脑", "相机", "耳机", "衣服", "鞋子", "家具", "食品"]
        product_type = next((w for w in words if w in product_types), "其他")
        
        # 识别可能的价格范围
        price_range = {"min": 0, "max": 0}
        for i, word in enumerate(words):
            if "元" in word or "¥" in word or "rmb" in word:
                try:
                    price = float(word.replace("元", "").replace("¥", "").replace("rmb", ""))
                    if i > 0 and words[i-1] in ["低于", "小于", "不超过"]:
                        price_range["max"] = price
                    elif i > 0 and words[i-1] in ["高于", "大于", "至少"]:
                        price_range["min"] = price
                    else:
                        # 猜测这可能是一个基准价格
                        price_range["min"] = price * 0.8
                        price_range["max"] = price * 1.2
                except (ValueError, IndexError):
                    pass
        
        return {
            "product_type": product_type,
            "price_range": price_range,
            "brands": [],
            "keywords": [w for w in words if len(w) > 1 and w not in product_types],
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