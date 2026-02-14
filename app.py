"""
分子风味配对实验室 (Molecular Flavor Lab) - V4.0 专业版
基于FlavorDB数据的饮食灵感引擎
新增功能：Vegan模式 + 汉化字典 + 多食材对比 + 权重评分 + 专业UI
"""

import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
import os
from itertools import combinations
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============== 页面配置 ==============
st.set_page_config(
    page_title="分子风味配对实验室",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== 自定义CSS ==============
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #faf8f5 0%, #f5f0e8 100%);
        color: #2c3e50;
    }
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 700;
        background: linear-gradient(90deg, #2D5A27, #4a7c43);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .ingredient-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .flavor-tag {
        display: inline-block;
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        color: #2e7d32;
        padding: 0.25rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        margin: 0.15rem;
        border: 1px solid #a5d6a7;
    }
    .flavor-tag-common {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        color: #e65100;
        border-color: #ffcc80;
        font-weight: 600;
    }
    .flavor-tag-unique {
        background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
        color: #757575;
        border-color: #bdbdbd;
    }
    .vegan-badge {
        display: inline-block;
        background: linear-gradient(135deg, #2D5A27, #4a7c43);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .score-excellent { color: #2D5A27 !important; font-weight: bold; }
    .score-good { color: #558b2f !important; }
    .score-average { color: #f9a825 !important; }
    .score-poor { color: #e65100 !important; }
    .comparison-table th { background: #f5f5f5 !important; }
    .comparison-table td { border-bottom: 1px solid #e0e0e0; }
    .highlight-common { background: #fff8e1 !important; font-weight: 600; }
    .highlight-unique { background: #fafafa !important; color: #9e9e9e; }
</style>
""", unsafe_allow_html=True)

# ============== Vegan 过滤配置 ==============
NON_VEGAN_CATEGORIES = ['Meat', 'Seafood', 'Fish', 'Poultry', 'Dairy', 'Egg']
WUXIN_KEYWORDS = ['onion', 'garlic', 'chive', 'leek', 'scallion', 'shallot', 'asafoetida', 'hing']

# ============== 风味汉化字典（化学→厨师语言）=============
FLAVOR_CHEF_TRANSLATIONS = {
    # 基础味觉
    'sweet': '甜味', 'bitter': '苦味', 'sour': '酸味', 'salty': '咸味', 'umami': '鲜味',
    # 果香类
    'fruity': '果香', 'citrus': '柑橘香', 'apple': '苹果香', 'pear': '梨香', 'peach': '桃香',
    'apricot': '杏香', 'plum': '李子香', 'cherry': '樱桃香', 'strawberry': '草莓香',
    'raspberry': '覆盆子香', 'blueberry': '蓝莓香', 'pineapple': '菠萝香', 'banana': '香蕉香',
    'grape': '葡萄香', 'grapefruit': '葡萄柚香', 'lemon': '柠檬香', 'lime': '青柠香',
    'orange': '橙香', 'melon': '甜瓜香', 'tropical': '热带果香', 'berry': '浆果香',
    # 花香类
    'floral': '花香', 'rose': '玫瑰香', 'jasmine': '茉莉香', 'lily': '百合香',
    'lavender': '薰衣草香', 'honeysuckle': '金银花香', 'violet': '紫罗兰香',
    'peony': '牡丹香', 'carnation': '康乃馨香',
    # 草本香料
    'herbal': '草本香', 'mint': '薄荷香', 'peppermint': '薄荷醇香', 'menthol': '清凉薄荷',
    'thyme': '百里香', 'cinnamon': '肉桂香', 'clove': '丁香', 'vanilla': '香草甜',
    'anise': '茴香', 'camphor': '樟脑', 'eucalyptus': '桉树香', 'green': '青草香',
    'grassy': '草香', 'leafy': '叶香', 'hay': '干草香',
    # 坚果谷物
    'nutty': '坚果香', 'almond': '杏仁香', 'hazelnut': '榛子香', 'walnut': '核桃香',
    'peanut': '花生香', 'coconut': '椰香', 'popcorn': '爆米花香', 'malt': '麦芽香',
    'bread': '面包香', 'bready': '烘焙香', 'cereal': '谷物香',
    # 烘焙焦糖
    'roasted': '烘焙香', 'caramel': '焦糖香', 'caramellic': '焦糖甜', 'butterscotch': '奶油糖',
    'butter': '黄油香', 'buttery': '黄油感', 'creamy': '奶油感', 'milky': '奶香',
    'cheese': '奶酪香', 'cheesy': '奶酪味', 'chocolate': '巧克力香', 'cocoa': '可可香',
    'coffee': '咖啡香', 'burnt': '焦香', 'smoky': '烟熏香', 'smoke': '烟味',
    'baked': '烘烤香', 'toasted': '烘烤香',
    # 木质泥土
    'woody': '木香', 'wood': '木质', 'earthy': '泥土香', 'mushroom': '蘑菇香',
    'musty': '霉味', 'moss': '苔藓香', 'balsam': '香脂', 'balsamic': '香醋',
    'resin': '树脂', 'resinous': '树脂味', 'pine': '松木香', 'cedar': '雪松香',
    'sandalwood': '檀香',
    # 其他
    'fresh': '清新', 'waxy': '蜡质', 'fatty': '油脂感', 'oily': '油润',
    'pungent': '辛辣', 'spicy': '香料', 'spice': '辛香', 'peppery': '胡椒',
    'warm': '温暖', 'cool': '清凉', 'medicinal': '药草', 'medical': '药香',
    'phenolic': '酚类', 'sulfur': '硫磺', 'sulfurous': '葱蒜辛香',  # 五辛类
    'sweat': '汗味', 'sweaty': '汗味', 'rancid': '酸败', 'fishy': '鱼腥',
    'meaty': '肉香', 'beef': '牛肉香', 'chicken': '鸡肉香', 'wine': '酒香',
    'alcoholic': '酒精', 'alcohol': '酒味', 'fermented': '发酵香', 'vinegar': '醋香',
    'acid': '酸性', 'acidic': '酸味', 'sharp': '尖锐', 'strong': '浓烈',
    'mild': '温和', 'faint': '微弱', 'odorless': '无味', 'fragrant': '芳香',
    'aromatic': '香气', 'perfume': '香水', 'powdery': '粉质', 'soapy': '皂香',
    'plastic': '塑料', 'rubber': '橡胶', 'chemical': '化学味', 'gasoline': '汽油',
    'ether': '乙醚', 'ethereal': '飘渺', 'solvent': '溶剂', 'metallic': '金属',
    'leather': '皮革', 'raw': '生青', 'green bean': '青豆', 'tomato': '番茄',
    'potato': '土豆', 'onion': '洋葱', 'garlic': '大蒜', 'cabbage': '卷心菜',
    'pea': '豌豆', 'cucumber': '黄瓜', 'seaweed': '海藻', 'truffle': '松露香',
    'egg': '蛋香', 'honey': '蜂蜜甜', 'maple': '枫糖', 'sugar': '糖甜',
    'jam': '果酱', 'candy': '糖果', 'cotton candy': '棉花糖', 'tutti frutti': '什锦果',
    # 稀有风味（高权重）
    'truffle': '松露香', 'saffron': '藏红花', 'caviar': '鱼子酱', 'matsutake': '松茸',
    'morel': '羊肚菌', 'chanterelle': '鸡油菌', 'porcini': '牛肝菌',
}

# ============== 稀有风味权重配置 ==============
RARE_FLAVORS = {
    'truffle': 3.0, 'saffron': 3.0, 'caviar': 3.0, 'matsutake': 3.0,
    'morel': 2.5, 'chanterelle': 2.5, 'porcini': 2.5,
    'vanilla': 2.0, 'sandalwood': 2.0, 'rose': 2.0, 'jasmine': 2.0,
    'popcorn': 1.8, 'caramel': 1.5, 'chocolate': 1.5, 'coffee': 1.5,
    'coconut': 1.3, 'almond': 1.3, 'hazelnut': 1.3,
}

# ============== 食材中英文映射 ==============
INGREDIENT_TRANSLATIONS = {
    # 水果
    'apple': '苹果', 'apricot': '杏', 'avocado': '牛油果', 'banana': '香蕉',
    'cherry': '樱桃', 'grape': '葡萄', 'grapefruit': '葡萄柚', 'kiwi': '猕猴桃',
    'lemon': '柠檬', 'lime': '青柠', 'lychee': '荔枝', 'mango': '芒果',
    'melon': '甜瓜', 'orange': '橙子', 'papaya': '木瓜', 'peach': '桃子',
    'pear': '梨', 'pineapple': '菠萝', 'plum': '李子', 'pomegranate': '石榴',
    'pomelo': '柚子', 'raspberry': '覆盆子', 'strawberry': '草莓', 'watermelon': '西瓜',
    'blackberry': '黑莓', 'blueberry': '蓝莓', 'mulberry': '桑葚',
    # 蔬菜
    'artichoke': '洋蓟', 'asparagus': '芦笋', 'broccoli': '西兰花',
    'cabbage': '卷心菜', 'carrot': '胡萝卜', 'cauliflower': '花椰菜',
    'celery': '芹菜', 'corn': '玉米', 'cucumber': '黄瓜', 'eggplant': '茄子',
    'fennel': '茴香', 'lettuce': '生菜', 'mushroom': '蘑菇',
    'pea': '豌豆', 'pepper': '辣椒', 'potato': '土豆', 'pumpkin': '南瓜',
    'radish': '萝卜', 'spinach': '菠菜', 'squash': '南瓜', 'tomato': '西红柿',
    'zucchini': '西葫芦', 'bamboo shoots': '竹笋', 'lotus root': '莲藕',
    'water chestnut': '荸荠', 'okra': '秋葵',
    # 香草香料
    'basil': '罗勒', 'bay leaf': '月桂叶', 'cinnamon': '肉桂', 'clove': '丁香',
    'coriander': '香菜籽', 'cumin': '孜然', 'dill': '莳萝', 'mint': '薄荷',
    'nutmeg': '肉豆蔻', 'oregano': '牛至', 'parsley': '欧芹', 'peppermint': '薄荷',
    'rosemary': '迷迭香', 'saffron': '藏红花', 'sage': '鼠尾草', 'thyme': '百里香',
    'turmeric': '姜黄', 'vanilla': '香草', 'cardamom': '豆蔻', 'star anise': '八角',
    'ginger': '姜', 'wasabi': '芥末', 'horseradish': '辣根',
    # 肉类（Vegan模式会过滤）
    'beef': '牛肉', 'chicken': '鸡肉', 'duck': '鸭肉', 'lamb': '羊肉',
    'pork': '猪肉', 'turkey': '火鸡肉', 'veal': '小牛肉', 'venison': '鹿肉',
    'bacon': '培根', 'ham': '火腿', 'sausage': '香肠',
    # 海鲜（Vegan模式会过滤）
    'anchovy': '凤尾鱼', 'clam': '蛤蜊', 'cod': '鳕鱼', 'crab': '蟹',
    'lobster': '龙虾', 'mackerel': '鲭鱼', 'mussel': '青口', 'octopus': '章鱼',
    'oyster': '生蚝', 'salmon': '三文鱼', 'sardine': '沙丁鱼', 'scallop': '扇贝',
    'shrimp': '虾', 'squid': '鱿鱼', 'tuna': '金枪鱼',
    # 乳制品（Vegan模式会过滤）
    'blue cheese': '蓝纹奶酪', 'butter': '黄油', 'cheese': '奶酪', 'cream': '奶油',
    'feta': '菲达奶酪', 'milk': '牛奶', 'mozzarella': '马苏里拉奶酪',
    'parmesan': '帕尔马干酪', 'yogurt': '酸奶', 'ice cream': '冰淇淋',
    # 烘焙
    'bread': '面包', 'croissant': '牛角包', 'bagel': '百吉饼', 'baguette': '法棍',
    'muffin': '马芬', 'pita': '皮塔饼', 'pretzel': '椒盐卷饼',
    # 坚果
    'almond': '杏仁', 'cashew': '腰果', 'chestnut': '栗子', 'coconut': '椰子',
    'hazelnut': '榛子', 'peanut': '花生', 'pistachio': '开心果', 'walnut': '核桃',
    'macadamia': '夏威夷果', 'pine nut': '松子', 'pecan': '山核桃',
    # 豆类
    'bean': '豆类', 'chickpea': '鹰嘴豆', 'lentil': '小扁豆', 'soybean': '大豆',
    'tofu': '豆腐', 'edamame': '毛豆', 'mung bean': '绿豆',
    # 饮品
    'beer': '啤酒', 'brandy': '白兰地', 'coffee': '咖啡', 'gin': '金酒',
    'green tea': '绿茶', 'black tea': '红茶', 'red wine': '红酒', 'rum': '朗姆酒',
    'sake': '清酒', 'vodka': '伏特加', 'whiskey': '威士忌', 'white wine': '白葡萄酒',
    'wine': '葡萄酒', 'champagne': '香槟', 'cider': '苹果酒',
    # 其他
    'egg': '鸡蛋', 'honey': '蜂蜜', 'sugar': '糖', 'vinegar': '醋',
    'maple syrup': '枫糖浆', 'molasses': '糖蜜', 'yeast': '酵母',
}

INGREDIENT_TRANSLATIONS_REVERSE = {v: k for k, v in INGREDIENT_TRANSLATIONS.items()}

CATEGORY_TRANSLATIONS = {
    'Fruit': '水果', 'Berry': '浆果', 'Vegetable': '蔬菜',
    'Vegetable Root': '根茎蔬菜', 'Vegetable Fruit': '果菜',
    'Herb': '香草', 'Spice': '香料', 'Meat': '肉类', 'Fish': '鱼类',
    'Seafood': '海鲜', 'Dairy': '乳制品', 'Bakery': '烘焙', 'Cereal': '谷物',
    'Nut': '坚果', 'Legume': '豆类', 'Beverage': '饮品',
    'Beverage Alcoholic': '酒精饮品', 'Beverage Caffeinated': '咖啡因饮品',
    'Essential Oil': '精油', 'Egg': '蛋品',
}

# ============== 核心配对类 ==============
class MolecularFlavorLab:
    def __init__(self, csv_path='flavordb_data.csv', vegan_mode=True):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, csv_path)
        self.df = pd.read_csv(full_path)
        self.vegan_mode = vegan_mode
        self.parsed_data = self._parse_and_filter_data()
        self.name_index = self._build_name_index()
        
    def _parse_and_filter_data(self):
        """解析数据并根据Vegan模式过滤"""
        parsed = []
        for idx, row in self.df.iterrows():
            # Vegan过滤
            if self.vegan_mode:
                # 过滤肉类类别
                if row['category'] in NON_VEGAN_CATEGORIES:
                    continue
                # 过滤五辛关键词
                name_lower = row['name'].lower()
                if any(w in name_lower for w in WUXIN_KEYWORDS):
                    continue
            
            molecules = self._extract_molecules(row)
            if molecules:
                parsed.append({
                    'id': row['id'],
                    'name': row['name'],
                    'cn_name': INGREDIENT_TRANSLATIONS.get(row['name'].lower(), row['name']),
                    'category': row['category'],
                    'cn_category': CATEGORY_TRANSLATIONS.get(row['category'], row['category']),
                    'molecules': molecules,
                    'molecule_set': set(molecules),
                    'molecule_count': len(molecules)
                })
        return parsed
    
    def _extract_molecules(self, row):
        """提取风味分子"""
        molecules = []
        if pd.notna(row.get('sample_molecules')):
            mol_str = str(row['sample_molecules'])
            molecules = [m.strip() for m in mol_str.split(',') if m.strip()]
        elif pd.notna(row.get('flavors')):
            flavor_str = str(row['flavors'])
            groups = flavor_str.split(',')
            for group in groups:
                flavors = group.strip().split('@')
                molecules.extend([f.strip().lower() for f in flavors if f.strip()])
        elif pd.notna(row.get('flavor_profiles')):
            profile_str = str(row['flavor_profiles'])
            molecules = [p.strip() for p in profile_str.split(',') if p.strip()]
        return molecules
    
    def _build_name_index(self):
        """构建名称索引"""
        index = {}
        for item in self.parsed_data:
            en_name = item['name'].lower()
            index[en_name] = item
            cn_name = item['cn_name']
            if cn_name and cn_name != item['name']:
                index[cn_name.lower()] = item
        return index
    
    def search_ingredients(self, query, limit=20):
        """搜索食材（支持中英文）"""
        if not query:
            return []
        query_lower = query.lower().strip()
        results = []
        matched_ids = set()
        
        # 精确匹配中文名
        if query_lower in INGREDIENT_TRANSLATIONS_REVERSE:
            en_name = INGREDIENT_TRANSLATIONS_REVERSE[query_lower]
            for item in self.parsed_data:
                if item['name'].lower() == en_name.lower() and item['id'] not in matched_ids:
                    results.append(item)
                    matched_ids.add(item['id'])
        
        # 精确匹配英文名
        for item in self.parsed_data:
            if item['name'].lower() == query_lower and item['id'] not in matched_ids:
                results.append(item)
                matched_ids.add(item['id'])
        
        # 模糊匹配英文名
        for item in self.parsed_data:
            if query_lower in item['name'].lower() and item['id'] not in matched_ids:
                results.append(item)
                matched_ids.add(item['id'])
            if len(results) >= limit:
                break
        
        # 模糊匹配中文名
        for cn_name, en_name in INGREDIENT_TRANSLATIONS_REVERSE.items():
            if query_lower in cn_name.lower() and len(results) < limit:
                for item in self.parsed_data:
                    if item['name'].lower() == en_name.lower() and item['id'] not in matched_ids:
                        results.append(item)
                        matched_ids.add(item['id'])
        
        return results[:limit]
    
    def get_ingredient_by_name(self, name):
        """根据名称获取食材"""
        name_lower = name.lower().strip()
        if name_lower in self.name_index:
            return self.name_index[name_lower]
        if name_lower in INGREDIENT_TRANSLATIONS_REVERSE:
            en_name = INGREDIENT_TRANSLATIONS_REVERSE[name_lower]
            if en_name.lower() in self.name_index:
                return self.name_index[en_name.lower()]
        return None
    
    def translate_flavor(self, flavor):
        """翻译风味为厨师语言"""
        return FLAVOR_CHEF_TRANSLATIONS.get(flavor.lower(), flavor.title())
    
    def calculate_weighted_score(self, ing1, ing2):
        """计算加权配对得分（稀有风味权重更高）"""
        set1 = ing1['molecule_set']
        set2 = ing2['molecule_set']
        common = set1 & set2
        
        if not common:
            return 0, 0, []
        
        # 计算加权分数
        weighted_common = 0
        for mol in common:
            weight = RARE_FLAVORS.get(mol.lower(), 1.0)
            weighted_common += weight
        
        # 基础分数
        common_count = len(common)
        total_count = len(set1) + len(set2)
        base_score = (common_count * 2) / total_count * 100
        
        # 加权分数
        weighted_score = base_score * (1 + weighted_common / common_count * 0.3)
        
        return min(weighted_score, 100), common_count, list(common)
    
    def pair_two_ingredients(self, name1, name2):
        """配对两个食材"""
        ing1 = self.get_ingredient_by_name(name1)
        ing2 = self.get_ingredient_by_name(name2)
        
        if not ing1 or not ing2:
            return None
        
        score, common_count, common_molecules = self.calculate_weighted_score(ing1, ing2)
        
        return {
            'ingredient1': ing1,
            'ingredient2': ing2,
            'score': score,
            'common_count': common_count,
            'common_molecules': common_molecules,
        }
    
    def compare_multiple_ingredients(self, ingredient_names):
        """对比多个食材（2-5种）"""
        ingredients = []
        for name in ingredient_names:
            ing = self.get_ingredient_by_name(name)
            if ing:
                ingredients.append(ing)
        
        if len(ingredients) < 2:
            return None
        
        # 计算交集（共有分子）
        all_sets = [ing['molecule_set'] for ing in ingredients]
        intersection = set.intersection(*all_sets)
        
        # 计算并集（风味宽度）
        union = set.union(*all_sets)
        
        # 计算每对配对的分数
        pair_scores = []
        for i in range(len(ingredients)):
            for j in range(i + 1, len(ingredients)):
                score, common, _ = self.calculate_weighted_score(ingredients[i], ingredients[j])
                pair_scores.append({
                    'ing1': ingredients[i],
                    'ing2': ingredients[j],
                    'score': score,
                    'common_count': common
                })
        
        # 计算平均分数
        avg_score = sum(p['score'] for p in pair_scores) / len(pair_scores) if pair_scores else 0
        
        return {
            'ingredients': ingredients,
            'intersection': intersection,
            'union': union,
            'pair_scores': pair_scores,
            'avg_score': avg_score,
            'intersection_count': len(intersection),
            'union_count': len(union)
        }
    
    def get_score_level(self, score):
        """获取分数等级"""
        if score >= 70:
            return 'excellent', '绝佳', '#2D5A27'
        elif score >= 50:
            return 'good', '优秀', '#558b2f'
        elif score >= 30:
            return 'average', '良好', '#f9a825'
        else:
            return 'poor', '一般', '#e65100'

# ============== 初始化 ==============
@st.cache_resource
def get_lab(vegan_mode=True):
    return MolecularFlavorLab('flavordb_data.csv', vegan_mode=vegan_mode)

# ============== 侧边栏 ==============
with st.sidebar:
    st.markdown("## 🧪 分子风味配对实验室")
    st.markdown("---")
    
    # Vegan 模式开关（默认开启）
    vegan_mode = st.toggle("🌱 Vegan 纯素模式（含五辛过滤）", value=True)
    
    if vegan_mode:
        st.markdown("<span class='vegan-badge'>✓ 已过滤肉类、蛋奶、五辛</span>", unsafe_allow_html=True)
        st.caption("五辛：葱、蒜、韭菜、洋葱、兴渠")
    
    st.markdown("---")
    
    # 初始化数据
    try:
        lab = get_lab(vegan_mode=vegan_mode)
        data_loaded = True
        st.markdown(f"**📊 数据概览**")
        st.markdown(f"- 可用食材: `{len(lab.parsed_data)}` 种")
        if vegan_mode:
            st.markdown(f"- 过滤后: 纯素安全")
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        data_loaded = False
    
    st.markdown("---")
    st.markdown("### 🔍 功能模式")
    
    mode = st.radio(
        "选择功能:",
        ["🔄 双食材配对", "📊 多食材对比 (2-5种)", "🎯 最佳组合推荐"]
    )

# ============== 主页面 ==============
st.markdown('<h1 class="main-title">🧪 分子风味配对实验室</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">专业级饮食灵感引擎 | Vegan友好 | 分子级精准匹配</p>', unsafe_allow_html=True)

if not data_loaded:
    st.stop()

# ============== 双食材配对模式 ==============
if mode == "🔄 双食材配对":
    st.markdown("### 🔍 选择两种食材进行配对分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search1 = st.text_input("食材 A", placeholder="输入食材名称（如：西红柿、罗勒）", key="search1")
    
    with col2:
        search2 = st.text_input("食材 B", placeholder="输入食材名称（如：土豆、迷迭香）", key="search2")
    
    ing1, ing2 = None, None
    
    if search1:
        results1 = lab.search_ingredients(search1, limit=5)
        if results1:
            options1 = [f"{r['cn_name']} ({r['name']})" for r in results1]
            selected1 = st.selectbox("选择食材 A:", options1, key="sel1")
            name1 = selected1.split("(")[1].rstrip(")")
            ing1 = lab.get_ingredient_by_name(name1)
    
    if search2:
        results2 = lab.search_ingredients(search2, limit=5)
        if results2:
            options2 = [f"{r['cn_name']} ({r['name']})" for r in results2]
            selected2 = st.selectbox("选择食材 B:", options2, key="sel2")
            name2 = selected2.split("(")[1].rstrip(")")
            ing2 = lab.get_ingredient_by_name(name2)
    
    if ing1 and ing2:
        st.markdown("---")
        result = lab.pair_two_ingredients(ing1['name'], ing2['name'])
        
        if result:
            score = result['score']
            level, level_text, color = lab.get_score_level(score)
            
            # 分数卡片
            score_col, detail_col = st.columns([1, 2])
            
            with score_col:
                st.metric(label="风味契合度", value=f"{score:.1f}/100")
                st.progress(min(score / 100, 1.0))
                
                if level == 'excellent':
                    st.success(f"⭐⭐⭐⭐⭐ {level_text}")
                elif level == 'good':
                    st.info(f"⭐⭐⭐⭐ {level_text}")
                elif level == 'average':
                    st.warning(f"⭐⭐⭐ {level_text}")
                else:
                    st.error(f"⭐⭐ {level_text}")
            
            with detail_col:
                st.markdown(f"**配对详情**")
                st.markdown(f"### {ing1['cn_name']} × {ing2['cn_name']}")
                st.markdown(f"共有风味分子: **{result['common_count']}** 个")
            
            # 共有风味标签云
            if result['common_molecules']:
                st.markdown("**共有风味特征:**")
                mol_html = ""
                for mol in result['common_molecules'][:15]:
                    cn_name = lab.translate_flavor(mol)
                    mol_html += f'<span class="flavor-tag flavor-tag-common">{cn_name}</span>'
                st.markdown(mol_html, unsafe_allow_html=True)

# ============== 多食材对比模式 ==============
elif mode == "📊 多食材对比 (2-5种)":
    st.markdown("### 📊 多食材对比分析")
    st.caption("选择2-5种食材，分析它们的风味交集与互补性")
    
    # 对比篮子
    if 'comparison_basket' not in st.session_state:
        st.session_state.comparison_basket = []
    
    col_search, col_basket = st.columns([2, 1])
    
    with col_search:
        search = st.text_input("添加食材到对比篮子", placeholder="输入食材名称...")
        if search:
            results = lab.search_ingredients(search, limit=5)
            if results:
                options = [f"{r['cn_name']} ({r['name']})" for r in results]
                selected = st.selectbox("选择食材:", options, key="basket_select")
                if st.button("➕ 添加到篮子"):
                    name = selected.split("(")[1].rstrip(")")
                    if name not in st.session_state.comparison_basket:
                        if len(st.session_state.comparison_basket) < 5:
                            st.session_state.comparison_basket.append(name)
                            st.rerun()
                        else:
                            st.warning("对比篮子已满（最多5种食材）")
    
    with col_basket:
        st.markdown("**对比篮子**")
        for i, name in enumerate(st.session_state.comparison_basket):
            ing = lab.get_ingredient_by_name(name)
            if ing:
                col_name, col_del = st.columns([3, 1])
                with col_name:
                    st.markdown(f"{i+1}. {ing['cn_name']}")
                with col_del:
                    if st.button("❌", key=f"del_{i}"):
                        st.session_state.comparison_basket.pop(i)
                        st.rerun()
        
        if st.button("🗑️ 清空篮子"):
            st.session_state.comparison_basket = []
            st.rerun()
    
    # 执行对比分析
    if len(st.session_state.comparison_basket) >= 2:
        st.markdown("---")
        
        with st.spinner("分析中..."):
            comparison = lab.compare_multiple_ingredients(st.session_state.comparison_basket)
        
        if comparison:
            # 总览卡片
            overview_col, intersection_col, union_col = st.columns(3)
            
            with overview_col:
                score = comparison['avg_score']
                st.metric("平均契合度", f"{score:.1f}/100")
            
            with intersection_col:
                st.metric("共有风味分子", f"{comparison['intersection_count']} 个")
            
            with union_col:
                st.metric("风味覆盖范围", f"{comparison['union_count']} 种")
            
            # 配对详情表格
            st.markdown("**配对详情:**")
            pair_data = []
            for p in comparison['pair_scores']:
                pair_data.append({
                    '配对': f"{p['ing1']['cn_name']} × {p['ing2']['cn_name']}",
                    '契合度': f"{p['score']:.1f}",
                    '共有分子': p['common_count']
                })
            
            st.dataframe(pair_data, use_container_width=True, hide_index=True)
            
            # 共有风味
            if comparison['intersection']:
                st.markdown("**🎯 风味共鸣点（共有分子）:**")
                mol_html = ""
                for mol in list(comparison['intersection'])[:20]:
                    cn_name = lab.translate_flavor(mol)
                    mol_html += f'<span class="flavor-tag flavor-tag-common">{cn_name}</span>'
                st.markdown(mol_html, unsafe_allow_html=True)

# ============== 最佳组合推荐模式 ==============
elif mode == "🎯 最佳组合推荐":
    st.markdown("### 🎯 最佳组合推荐")
    st.caption("选择一种基础食材，发现最佳搭配组合")
    
    search = st.text_input("基础食材", placeholder="输入食材名称（如：西红柿、豆腐）")
    
    base_ing = None
    if search:
        results = lab.search_ingredients(search, limit=5)
        if results:
            options = [f"{r['cn_name']} ({r['name']})" for r in results]
            selected = st.selectbox("选择基础食材:", options)
            name = selected.split("(")[1].rstrip(")")
            base_ing = lab.get_ingredient_by_name(name)
    
    if base_ing:
        st.markdown("---")
        
        # 计算最佳配对
        all_scores = []
        for item in lab.parsed_data:
            if item['id'] != base_ing['id']:
                score, common_count, _ = lab.calculate_weighted_score(base_ing, item)
                all_scores.append({
                    'ingredient': item,
                    'score': score,
                    'common_count': common_count
                })
        
        all_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # 显示Top 10
        st.markdown(f"### 与 **{base_ing['cn_name']}** 的最佳搭配")
        
        for i, item in enumerate(all_scores[:10], 1):
            score = item['score']
            level, level_text, color = lab.get_score_level(score)
            
            with st.expander(f"#{i} {item['ingredient']['cn_name']} - 契合度 {score:.1f} ({level_text})"):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.progress(min(score / 100, 1.0))
                    st.markdown(f"共有分子: **{item['common_count']}** 个")
                
                with col2:
                    st.markdown(f"类别: {item['ingredient']['cn_category']}")

# ============== 页脚 ==============
st.markdown("---")
st.markdown("🧪 分子风味配对实验室 V4.0 | 专业版 | Powered by FlavorDB")
