"""
分子风味配对实验室 (Molecular Flavor Lab) - V5.0 科学版
烹饪科学思维导图 | 雷达图谱分析 | 风险预警 | 延展思考
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
    page_title="分子风味配对实验室 | 科学版",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== 自定义CSS ==============
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #faf8f5 0%, #f5f0e8 100%); color: #2c3e50; }
    .main-title {
        font-size: 2.5rem !important; font-weight: 700;
        background: linear-gradient(90deg, #2D5A27, #4a7c43);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.5rem;
    }
    .subtitle { text-align: center; color: #666; font-size: 1rem; margin-bottom: 1.5rem; }
    .ingredient-card {
        background: white; border-radius: 12px; padding: 1rem;
        margin: 0.5rem 0; border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .flavor-tag {
        display: inline-block; background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        color: #2e7d32; padding: 0.25rem 0.6rem;
        border-radius: 15px; font-size: 0.75rem;
        margin: 0.15rem; border: 1px solid #a5d6a7;
    }
    .flavor-tag-common {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        color: #e65100; border-color: #ffcc80; font-weight: 600;
    }
    .risk-warning {
        background: linear-gradient(135deg, #fff8e1, #ffecb3);
        border-left: 4px solid #ffc107;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
    .risk-danger {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border-left: 4px solid #f44336;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border-left: 4px solid #2196f3;
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
    }
    .dimension-green { color: #4caf50; font-weight: 600; }
    .dimension-brown { color: #795548; font-weight: 600; }
    .dimension-pink { color: #e91e63; font-weight: 600; }
    .dimension-amber { color: #ff9800; font-weight: 600; }
    .dimension-purple { color: #9c27b0; font-weight: 600; }
    .dimension-red { color: #f44336; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ============== 风味维度分类（6大科学维度）=============
FLAVOR_DIMENSIONS = {
    "green_herbal": {
        "name": "草本/清新",
        "color": "#4caf50",
        "keywords": [
            "green", "grassy", "leafy", "herbal", "fresh", "mint", "peppermint", "menthol",
            "basil", "parsley", "cilantro", "dill", "chives", "watercress", "spinach",
            "cucumber", "celery", "lettuce", "cabbage", "eucalyptus", "camphor", "thyme",
            "oregano", "sage", "rosemary", "lavender", "jasmine", "lily", "floral"
        ]
    },
    "roasted_nutty": {
        "name": "烘焙/坚果",
        "color": "#795548",
        "keywords": [
            "roasted", "toasted", "baked", "burnt", "caramel", "caramellic", "butterscotch",
            "nutty", "almond", "hazelnut", "walnut", "peanut", "chestnut", "coconut",
            "popcorn", "malt", "bread", "bready", "cereal", "coffee", "cocoa", "chocolate",
            "vanilla", "maple", "honey", "brown", "smoky", "smoke"
        ]
    },
    "floral_fruity": {
        "name": "花果/甜润",
        "color": "#e91e63",
        "keywords": [
            "fruity", "sweet", "citrus", "apple", "pear", "peach", "apricot", "plum",
            "cherry", "strawberry", "raspberry", "blueberry", "blackberry", "pineapple",
            "banana", "grape", "grapefruit", "lemon", "lime", "orange", "melon",
            "tropical", "berry", "rose", "jasmine", "lily", "lavender", "honeysuckle",
            "violet", "peony", "carnation", "floral", "perfume", "fragrant"
        ]
    },
    "earthy_woody": {
        "name": "泥土/菌菇",
        "color": "#ff9800",
        "keywords": [
            "earthy", "woody", "wood", "mushroom", "truffle", "moss", "musty", "damp",
            "forest", "balsam", "balsamic", "resin", "resinous", "pine", "cedar",
            "sandalwood", "root", "beetroot", "potato", "carrot", "turnip", "radish",
            "ginger", "turmeric", "galangal"
        ]
    },
    "animalic_fatty": {
        "name": "动物/油脂",
        "color": "#9c27b0",
        "keywords": [
            "meaty", "beef", "chicken", "pork", "lamb", "fatty", "oily", "waxy",
            "butter", "buttery", "creamy", "milky", "cheese", "cheesy", "egg",
            "fishy", "seafood", "oyster", "clam", "mussel", "liver", "blood"
        ]
    },
    "spicy_pungent": {
        "name": "辛辣/药香",
        "color": "#f44336",
        "keywords": [
            "spicy", "spice", "pungent", "peppery", "hot", "sharp", "strong",
            "garlic", "onion", "chive", "leek", "scallion", "shallot", "hing", "asafoetida",
            "clove", "cinnamon", "nutmeg", "cardamom", "pepper", "chili", "wasabi",
            "horseradish", "mustard", "ginger", "medicinal", "medical", "phenolic",
            "sulfur", "sulfurous", "ammonia", "urine", "fecal"
        ]
    }
}

# ============== 风险词汇配置 ==============
RISK_KEYWORDS = {
    "sulfur": {
        "level": "warning",
        "message": "⚠️ 硫化物警示：两种食材共有强烈的硫化物（葱蒜类辛香），比例不当可能产生过重的气味。建议通过高温煎炸（美拉德反应）来中和。"
    },
    "sulfurous": {
        "level": "warning", 
        "message": "⚠️ 硫化物警示：检测到高浓度硫化物风味，建议控制用量，避免风味过于刺激。"
    },
    "fecal": {
        "level": "danger",
        "message": "🚨 动物异香警示：检测到粪便/动物异香类分子，这通常是某些奶酪或发酵食品的特征。建议谨慎搭配，或用于特定风味主题。"
    },
    "ammonia": {
        "level": "warning",
        "message": "⚠️ 氨味警示：检测到氨类风味分子，可能来自某些海鲜或陈年奶酪。建议搭配酸性食材平衡。"
    },
    "rancid": {
        "level": "warning",
        "message": "⚠️ 酸败警示：检测到酸败/油脂氧化类风味。确保食材新鲜，或用于特定发酵主题。"
    },
    "fishy": {
        "level": "warning",
        "message": "⚠️ 鱼腥警示：检测到鱼腥类分子。建议搭配姜、葱、柠檬等去腥食材。"
    }
}

# ============== Vegan 配置 ==============
NON_VEGAN_CATEGORIES = ['Meat', 'Seafood', 'Fish', 'Poultry', 'Dairy', 'Egg']
WUXIN_KEYWORDS = ['onion', 'garlic', 'chive', 'leek', 'scallion', 'shallot', 'asafoetida', 'hing']

# ============== 汉化字典 ==============
FLAVOR_CHEF_TRANSLATIONS = {
    'sweet': '甜味', 'bitter': '苦味', 'sour': '酸味', 'salty': '咸味', 'umami': '鲜味',
    'fruity': '果香', 'citrus': '柑橘香', 'apple': '苹果香', 'pear': '梨香', 'peach': '桃香',
    'apricot': '杏香', 'plum': '李子香', 'cherry': '樱桃香', 'strawberry': '草莓香',
    'raspberry': '覆盆子香', 'blueberry': '蓝莓香', 'pineapple': '菠萝香', 'banana': '香蕉香',
    'grape': '葡萄香', 'grapefruit': '葡萄柚香', 'lemon': '柠檬香', 'lime': '青柠香',
    'orange': '橙香', 'melon': '甜瓜香', 'tropical': '热带果香', 'berry': '浆果香',
    'floral': '花香', 'rose': '玫瑰香', 'jasmine': '茉莉香', 'lily': '百合香',
    'lavender': '薰衣草香', 'honeysuckle': '金银花香', 'violet': '紫罗兰香',
    'peony': '牡丹香', 'carnation': '康乃馨香',
    'herbal': '草本香', 'mint': '薄荷香', 'peppermint': '薄荷醇香', 'menthol': '清凉薄荷',
    'thyme': '百里香', 'cinnamon': '肉桂香', 'clove': '丁香', 'vanilla': '香草甜',
    'anise': '茴香', 'camphor': '樟脑', 'eucalyptus': '桉树香', 'green': '青草香',
    'grassy': '草香', 'leafy': '叶香', 'hay': '干草香',
    'nutty': '坚果香', 'almond': '杏仁香', 'hazelnut': '榛子香', 'walnut': '核桃香',
    'peanut': '花生香', 'coconut': '椰香', 'popcorn': '爆米花香', 'malt': '麦芽香',
    'bread': '面包香', 'bready': '烘焙香', 'cereal': '谷物香',
    'roasted': '烘焙香', 'caramel': '焦糖香', 'caramellic': '焦糖甜', 'butterscotch': '奶油糖',
    'butter': '黄油香', 'buttery': '黄油感', 'creamy': '奶油感', 'milky': '奶香',
    'cheese': '奶酪香', 'cheesy': '奶酪味', 'chocolate': '巧克力香', 'cocoa': '可可香',
    'coffee': '咖啡香', 'burnt': '焦香', 'smoky': '烟熏香', 'smoke': '烟味',
    'baked': '烘烤香', 'toasted': '烘烤香',
    'woody': '木香', 'wood': '木质', 'earthy': '泥土香', 'mushroom': '蘑菇香',
    'musty': '霉味', 'moss': '苔藓香', 'balsam': '香脂', 'balsamic': '香醋',
    'resin': '树脂', 'resinous': '树脂味', 'pine': '松木香', 'cedar': '雪松香',
    'sandalwood': '檀香', 'truffle': '松露香',
    'fresh': '清新', 'waxy': '蜡质', 'fatty': '油脂感', 'oily': '油润',
    'pungent': '辛辣', 'spicy': '香料', 'spice': '辛香', 'peppery': '胡椒',
    'warm': '温暖', 'cool': '清凉', 'medicinal': '药草', 'medical': '药香',
    'phenolic': '酚类', 'sulfur': '硫磺', 'sulfurous': '葱蒜辛香',
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
    'pea': '豌豆', 'cucumber': '黄瓜', 'seaweed': '海藻', 'egg': '蛋香',
    'honey': '蜂蜜甜', 'maple': '枫糖', 'sugar': '糖甜', 'jam': '果酱',
    'candy': '糖果', 'cotton candy': '棉花糖', 'tutti frutti': '什锦果',
    'saffron': '藏红花', 'caviar': '鱼子酱', 'matsutake': '松茸',
    'morel': '羊肚菌', 'chanterelle': '鸡油菌', 'porcini': '牛肝菌',
    'fecal': '动物异香', 'ammonia': '氨味', 'urine': '尿味'
}

# ============== 稀有风味权重 ==============
RARE_FLAVORS = {
    'truffle': 3.0, 'saffron': 3.0, 'caviar': 3.0, 'matsutake': 3.0,
    'morel': 2.5, 'chanterelle': 2.5, 'porcini': 2.5,
    'vanilla': 2.0, 'sandalwood': 2.0, 'rose': 2.0, 'jasmine': 2.0,
    'popcorn': 1.8, 'caramel': 1.5, 'chocolate': 1.5, 'coffee': 1.5,
    'coconut': 1.3, 'almond': 1.3, 'hazelnut': 1.3,
}

# ============== 食材翻译 ==============
INGREDIENT_TRANSLATIONS = {
    'apple': '苹果', 'apricot': '杏', 'avocado': '牛油果', 'banana': '香蕉',
    'cherry': '樱桃', 'grape': '葡萄', 'grapefruit': '葡萄柚', 'kiwi': '猕猴桃',
    'lemon': '柠檬', 'lime': '青柠', 'lychee': '荔枝', 'mango': '芒果',
    'melon': '甜瓜', 'orange': '橙子', 'papaya': '木瓜', 'peach': '桃子',
    'pear': '梨', 'pineapple': '菠萝', 'plum': '李子', 'pomegranate': '石榴',
    'pomelo': '柚子', 'raspberry': '覆盆子', 'strawberry': '草莓', 'watermelon': '西瓜',
    'blackberry': '黑莓', 'blueberry': '蓝莓', 'mulberry': '桑葚',
    'artichoke': '洋蓟', 'asparagus': '芦笋', 'broccoli': '西兰花',
    'cabbage': '卷心菜', 'carrot': '胡萝卜', 'cauliflower': '花椰菜',
    'celery': '芹菜', 'corn': '玉米', 'cucumber': '黄瓜', 'eggplant': '茄子',
    'fennel': '茴香', 'lettuce': '生菜', 'mushroom': '蘑菇',
    'pea': '豌豆', 'pepper': '辣椒', 'potato': '土豆', 'pumpkin': '南瓜',
    'radish': '萝卜', 'spinach': '菠菜', 'squash': '南瓜', 'tomato': '西红柿',
    'zucchini': '西葫芦', 'bamboo shoots': '竹笋', 'lotus root': '莲藕',
    'water chestnut': '荸荠', 'okra': '秋葵',
    'basil': '罗勒', 'bay leaf': '月桂叶', 'cinnamon': '肉桂', 'clove': '丁香',
    'coriander': '香菜籽', 'cumin': '孜然', 'dill': '莳萝', 'mint': '薄荷',
    'nutmeg': '肉豆蔻', 'oregano': '牛至', 'parsley': '欧芹', 'peppermint': '薄荷',
    'rosemary': '迷迭香', 'saffron': '藏红花', 'sage': '鼠尾草', 'thyme': '百里香',
    'turmeric': '姜黄', 'vanilla': '香草', 'cardamom': '豆蔻', 'star anise': '八角',
    'ginger': '姜', 'wasabi': '芥末', 'horseradish': '辣根',
    'beef': '牛肉', 'chicken': '鸡肉', 'duck': '鸭肉', 'lamb': '羊肉',
    'pork': '猪肉', 'turkey': '火鸡肉', 'veal': '小牛肉', 'venison': '鹿肉',
    'bacon': '培根', 'ham': '火腿', 'sausage': '香肠',
    'anchovy': '凤尾鱼', 'clam': '蛤蜊', 'cod': '鳕鱼', 'crab': '蟹',
    'lobster': '龙虾', 'mackerel': '鲭鱼', 'mussel': '青口', 'octopus': '章鱼',
    'oyster': '生蚝', 'salmon': '三文鱼', 'sardine': '沙丁鱼', 'scallop': '扇贝',
    'shrimp': '虾', 'squid': '鱿鱼', 'tuna': '金枪鱼',
    'blue cheese': '蓝纹奶酪', 'butter': '黄油', 'cheese': '奶酪', 'cream': '奶油',
    'feta': '菲达奶酪', 'milk': '牛奶', 'mozzarella': '马苏里拉奶酪',
    'parmesan': '帕尔马干酪', 'yogurt': '酸奶', 'ice cream': '冰淇淋',
    'bread': '面包', 'croissant': '牛角包', 'bagel': '百吉饼', 'baguette': '法棍',
    'muffin': '马芬', 'pita': '皮塔饼', 'pretzel': '椒盐卷饼',
    'almond': '杏仁', 'cashew': '腰果', 'chestnut': '栗子', 'coconut': '椰子',
    'hazelnut': '榛子', 'peanut': '花生', 'pistachio': '开心果', 'walnut': '核桃',
    'macadamia': '夏威夷果', 'pine nut': '松子', 'pecan': '山核桃',
    'bean': '豆类', 'chickpea': '鹰嘴豆', 'lentil': '小扁豆', 'soybean': '大豆',
    'tofu': '豆腐', 'edamame': '毛豆', 'mung bean': '绿豆',
    'beer': '啤酒', 'brandy': '白兰地', 'coffee': '咖啡', 'gin': '金酒',
    'green tea': '绿茶', 'black tea': '红茶', 'red wine': '红酒', 'rum': '朗姆酒',
    'sake': '清酒', 'vodka': '伏特加', 'whiskey': '威士忌', 'white wine': '白葡萄酒',
    'wine': '葡萄酒', 'champagne': '香槟', 'cider': '苹果酒',
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

# ============== 核心类 ==============
class MolecularFlavorLab:
    def __init__(self, csv_path='flavordb_data.csv', vegan_mode=True):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, csv_path)
        self.df = pd.read_csv(full_path)
        self.vegan_mode = vegan_mode
        self.parsed_data = self._parse_and_filter_data()
        self.name_index = self._build_name_index()
        
    def _parse_and_filter_data(self):
        parsed = []
        for idx, row in self.df.iterrows():
            if self.vegan_mode:
                if row['category'] in NON_VEGAN_CATEGORIES:
                    continue
                name_lower = row['name'].lower()
                if any(w in name_lower for w in WUXIN_KEYWORDS):
                    continue
            
            molecules = self._extract_molecules(row)
            if molecules:
                # 计算风味维度分布
                dimensions = self._calculate_dimensions(molecules)
                
                parsed.append({
                    'id': row['id'],
                    'name': row['name'],
                    'cn_name': INGREDIENT_TRANSLATIONS.get(row['name'].lower(), row['name']),
                    'category': row['category'],
                    'cn_category': CATEGORY_TRANSLATIONS.get(row['category'], row['category']),
                    'molecules': molecules,
                    'molecule_set': set(molecules),
                    'molecule_count': len(molecules),
                    'dimensions': dimensions
                })
        return parsed
    
    def _extract_molecules(self, row):
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
    
    def _calculate_dimensions(self, molecules):
        """计算食材的6大风味维度分布"""
        dimensions = {key: 0 for key in FLAVOR_DIMENSIONS.keys()}
        
        for mol in molecules:
            mol_lower = mol.lower()
            for dim_key, dim_data in FLAVOR_DIMENSIONS.items():
                if any(kw in mol_lower for kw in dim_data['keywords']):
                    dimensions[dim_key] += 1
        
        return dimensions
    
    def _build_name_index(self):
        index = {}
        for item in self.parsed_data:
            en_name = item['name'].lower()
            index[en_name] = item
            cn_name = item['cn_name']
            if cn_name and cn_name != item['name']:
                index[cn_name.lower()] = item
        return index
    
    def search_ingredients(self, query, limit=20):
        if not query:
            return []
        query_lower = query.lower().strip()
        results = []
        matched_ids = set()
        
        if query_lower in INGREDIENT_TRANSLATIONS_REVERSE:
            en_name = INGREDIENT_TRANSLATIONS_REVERSE[query_lower]
            for item in self.parsed_data:
                if item['name'].lower() == en_name.lower() and item['id'] not in matched_ids:
                    results.append(item)
                    matched_ids.add(item['id'])
        
        for item in self.parsed_data:
            if item['name'].lower() == query_lower and item['id'] not in matched_ids:
                results.append(item)
                matched_ids.add(item['id'])
        
        for item in self.parsed_data:
            if query_lower in item['name'].lower() and item['id'] not in matched_ids:
                results.append(item)
                matched_ids.add(item['id'])
            if len(results) >= limit:
                break
        
        for cn_name, en_name in INGREDIENT_TRANSLATIONS_REVERSE.items():
            if query_lower in cn_name.lower() and len(results) < limit:
                for item in self.parsed_data:
                    if item['name'].lower() == en_name.lower() and item['id'] not in matched_ids:
                        results.append(item)
                        matched_ids.add(item['id'])
        
        return results[:limit]
    
    def get_ingredient_by_name(self, name):
        name_lower = name.lower().strip()
        if name_lower in self.name_index:
            return self.name_index[name_lower]
        if name_lower in INGREDIENT_TRANSLATIONS_REVERSE:
            en_name = INGREDIENT_TRANSLATIONS_REVERSE[name_lower]
            if en_name.lower() in self.name_index:
                return self.name_index[en_name.lower()]
        return None
    
    def translate_flavor(self, flavor):
        return FLAVOR_CHEF_TRANSLATIONS.get(flavor.lower(), flavor.title())
    
    def calculate_weighted_score(self, ing1, ing2):
        set1 = ing1['molecule_set']
        set2 = ing2['molecule_set']
        common = set1 & set2
        
        if not common:
            return 0, 0, []
        
        weighted_common = 0
        for mol in common:
            weight = RARE_FLAVORS.get(mol.lower(), 1.0)
            weighted_common += weight
        
        common_count = len(common)
        total_count = len(set1) + len(set2)
        base_score = (common_count * 2) / total_count * 100
        weighted_score = base_score * (1 + weighted_common / common_count * 0.3)
        
        return min(weighted_score, 100), common_count, list(common)
    
    def detect_risks(self, common_molecules):
        """检测风险风味"""
        risks = []
        for mol in common_molecules:
            mol_lower = mol.lower()
            for risk_key, risk_data in RISK_KEYWORDS.items():
                if risk_key in mol_lower:
                    risks.append(risk_data)
        return risks
    
    def analyze_pairing_type(self, ing1, ing2, common_molecules):
        """分析配对类型：Consonance（共鸣）vs Contrast（对比）"""
        # 计算维度相似度
        dims1 = ing1['dimensions']
        dims2 = ing2['dimensions']
        
        # 找出主导维度
        dom1 = max(dims1, key=dims1.get)
        dom2 = max(dims2, key=dims2.get)
        
        # 判断配对类型
        if dom1 == dom2:
            pairing_type = "consonance"
            explanation = f"这是**深度共鸣**组合。{ing1['cn_name']}与{ing2['cn_name']}都以**{FLAVOR_DIMENSIONS[dom1]['name']}**为主导风味，能创造出极具统一性的味觉体验。"
            suggestion = "建议：可加入少量酸味剂（如柠檬、醋）来防止风味过于沉闷，或加入少量对比元素增加层次。"
        else:
            pairing_type = "contrast"
            dim1_name = FLAVOR_DIMENSIONS[dom1]['name']
            dim2_name = FLAVOR_DIMENSIONS[dom2]['name']
            explanation = f"这是**跨界对比**组合。{ing1['cn_name']}的**{dim1_name}**与{ing2['cn_name']}的**{dim2_name}**形成对冲，能创造惊喜和平衡。"
            suggestion = "建议：加入油脂（如橄榄油、黄油）作为媒介来融合这种对冲，让两种风味更好地交织。"
        
        return pairing_type, explanation, suggestion
    
    def generate_chef_insight(self, score, common_molecules, ing1, ing2):
        """生成厨师延展思考"""
        insights = []
        
        # 基于分数的建议
        if score >= 70:
            insights.append("💡 **高契合度提示**：这组配对风味高度统一，适合作为主菜的核心搭配。")
        elif score >= 50:
            insights.append("💡 **良好契合度提示**：这组配对有一定共鸣，适合作为配菜或调味组合。")
        elif score >= 30:
            insights.append("💡 **中等契合度提示**：这组配对风味关联较弱，可能需要额外调味来连接。")
        else:
            insights.append("💡 **低契合度提示**：这组配对风味差异较大，属于冒险尝试，建议小量测试。")
        
        # 基于分子活性的温度建议
        volatile_count = sum(1 for m in common_molecules if any(k in m.lower() for k in ['fresh', 'citrus', 'mint', 'green', 'floral']))
        heavy_count = sum(1 for m in common_molecules if any(k in m.lower() for k in ['roasted', 'caramel', 'mushroom', 'earthy', 'meaty']))
        
        if volatile_count > heavy_count:
            insights.append("🌡️ **温度建议**：这组配对含有较多高挥发组分，建议**低温烹饪**或**最后加入**，保留其灵动的香气。")
        elif heavy_count > volatile_count:
            insights.append("🌡️ **温度建议**：这组配对含有较多重分子组分，建议**炖煮**或**发酵**，释放其深层的底蕴。")
        
        # 比例建议
        ratio = ing1['molecule_count'] / max(ing2['molecule_count'], 1)
        if ratio > 3:
            insights.append(f"⚖️ **比例建议**：{ing1['cn_name']}的风味强度约为{ing2['cn_name']}的{ratio:.1f}倍，建议用量比例为 1:{ratio:.0f}。")
        elif ratio < 0.33:
            insights.append(f"⚖️ **比例建议**：{ing2['cn_name']}的风味强度约为{ing1['cn_name']}的{1/ratio:.1f}倍，建议用量比例为 {1/ratio:.0f}:1。")
        
        return "\n\n".join(insights)
    
    def create_radar_chart(self, ing1, ing2=None):
        """创建风味雷达图"""
        categories = [FLAVOR_DIMENSIONS[k]['name'] for k in FLAVOR_DIMENSIONS.keys()]
        
        fig = go.Figure()
        
        # 食材1
        values1 = list(ing1['dimensions'].values())
        fig.add_trace(go.Scatterpolar(
            r=values1 + [values1[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=ing1['cn_name'],
            line_color='#4caf50',
            fillcolor='rgba(76, 175, 80, 0.3)'
        ))
        
        # 食材2（如果有）
        if ing2:
            values2 = list(ing2['dimensions'].values())
            fig.add_trace(go.Scatterpolar(
                r=values2 + [values2[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=ing2['cn_name'],
                line_color='#ff9800',
                fillcolor='rgba(255, 152, 0, 0.3)'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(max(values1), max(values2) if ing2 else [0]) * 1.2])
            ),
            showlegend=True,
            height=400,
            margin=dict(l=80, r=80, t=40, b=40)
        )
        
        return fig
    
    def pair_two_ingredients(self, name1, name2):
        ing1 = self.get_ingredient_by_name(name1)
        ing2 = self.get_ingredient_by_name(name2)
        
        if not ing1 or not ing2:
            return None
        
        score, common_count, common_molecules = self.calculate_weighted_score(ing1, ing2)
        risks = self.detect_risks(common_molecules)
        pairing_type, explanation, suggestion = self.analyze_pairing_type(ing1, ing2, common_molecules)
        chef_insight = self.generate_chef_insight(score, common_molecules, ing1, ing2)
        
        return {
            'ingredient1': ing1,
            'ingredient2': ing2,
            'score': score,
            'common_count': common_count,
            'common_molecules': common_molecules,
            'risks': risks,
            'pairing_type': pairing_type,
            'explanation': explanation,
            'suggestion': suggestion,
            'chef_insight': chef_insight
        }

# ============== 初始化 ==============
@st.cache_resource
def get_lab(vegan_mode=True):
    return MolecularFlavorLab('flavordb_data.csv', vegan_mode=vegan_mode)

# ============== 侧边栏 ==============
with st.sidebar:
    st.markdown("## 🧪 分子风味配对实验室")
    st.markdown("---")
    
    vegan_mode = st.toggle("🌱 Vegan 纯素模式", value=True)
    
    if vegan_mode:
        st.markdown("<span style='background: linear-gradient(135deg, #2D5A27, #4a7c43); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;'>✓ 已过滤肉类、蛋奶、五辛</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    try:
        lab = get_lab(vegan_mode=vegan_mode)
        data_loaded = True
        st.markdown(f"**📊 数据概览**")
        st.markdown(f"- 可用食材: `{len(lab.parsed_data)}` 种")
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        data_loaded = False

# ============== 主页面 ==============
st.markdown('<h1 class="main-title">🧪 分子风味配对实验室</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">烹饪科学思维导图 | 雷达图谱分析 | 风险预警 | 延展思考</p>', unsafe_allow_html=True)

if not data_loaded:
    st.stop()

# ============== 双食材配对模式 ==============
st.markdown("### 🔍 选择两种食材进行科学配对分析")

col1, col2 = st.columns(2)

with col1:
    search1 = st.text_input("食材 A", placeholder="如：西红柿、罗勒、竹笋", key="search1")

with col2:
    search2 = st.text_input("食材 B", placeholder="如：土豆、迷迭香、柠檬", key="search2")

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

# ============== 结果显示 ==============
if ing1 and ing2:
    st.markdown("---")
    result = lab.pair_two_ingredients(ing1['name'], ing2['name'])
    
    if result:
        score = result['score']
        
        # 分数与雷达图
        score_col, radar_col = st.columns([1, 2])
        
        with score_col:
            st.metric(label="风味契合度", value=f"{score:.1f}/100")
            st.progress(min(score / 100, 1.0))
            
            if score >= 70:
                st.success("⭐⭐⭐⭐⭐ 绝佳")
            elif score >= 50:
                st.info("⭐⭐⭐⭐ 优秀")
            elif score >= 30:
                st.warning("⭐⭐⭐ 良好")
            else:
                st.error("⭐⭐ 一般")
            
            st.markdown(f"**共有分子: {result['common_count']} 个**")
        
        with radar_col:
            radar_chart = lab.create_radar_chart(ing1, ing2)
            st.plotly_chart(radar_chart, use_container_width=True)
        
        # 风险预警
        if result['risks']:
            st.markdown("### ⚠️ 风险预警")
            for risk in result['risks']:
                if risk['level'] == 'danger':
                    st.markdown(f"<div class='risk-danger'>{risk['message']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='risk-warning'>{risk['message']}</div>", unsafe_allow_html=True)
        
        # 味型逻辑解读
        st.markdown("### 🧠 味型逻辑解读")
        
        if result['pairing_type'] == 'consonance':
            st.markdown(f"<div class='insight-box'><strong>🔄 味型相同 (Consonance - 共鸣)</strong><br><br>{result['explanation']}<br><br>{result['suggestion']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='insight-box'><strong>⚡ 味型对比 (Contrast - 对比)</strong><br><br>{result['explanation']}<br><br>{result['suggestion']}</div>", unsafe_allow_html=True)
        
        # 厨师延展思考
        st.markdown("### 👨‍🍳 厨师延展思考")
        st.markdown(f"<div class='insight-box'>{result['chef_insight']}</div>", unsafe_allow_html=True)
        
        # 共有风味标签云
        if result['common_molecules']:
            st.markdown("### 🏷️ 共有风味分子")
            
            # 按维度分类显示
            dim_molecules = {key: [] for key in FLAVOR_DIMENSIONS.keys()}
            for mol in result['common_molecules']:
                mol_lower = mol.lower()
                for dim_key, dim_data in FLAVOR_DIMENSIONS.items():
                    if any(kw in mol_lower for kw in dim_data['keywords']):
                        dim_molecules[dim_key].append(mol)
            
            for dim_key, mols in dim_molecules.items():
                if mols:
                    dim_data = FLAVOR_DIMENSIONS[dim_key]
                    st.markdown(f"**<span style='color: {dim_data['color']}'>{dim_data['name']}</span>**")
                    mol_html = ""
                    for mol in mols[:10]:
                        cn_name = lab.translate_flavor(mol)
                        mol_html += f'<span class="flavor-tag flavor-tag-common">{cn_name}</span>'
                    st.markdown(mol_html, unsafe_allow_html=True)

# ============== 页脚 ==============
st.markdown("---")
st.markdown("🧪 分子风味配对实验室 V5.0 | 科学版 | 烹饪科学思维导图")
