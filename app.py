"""
分子风味配对实验室 (Molecular Flavor Lab) - V2.0
基于FlavorDB数据的食材配对灵感引擎
新增功能：中英文双语系统 + 算法可视化评分
"""

import streamlit as st
import pandas as pd
from collections import Counter
import os

# ============== 页面配置 ==============
st.set_page_config(
    page_title="分子风味配对实验室",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== 自定义CSS（支持动态颜色进度条）=============
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e0e0e0;
    }
    
    /* 标题样式 */
    .main-title {
        font-size: 3rem !important;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .ingredient-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .ingredient-card:hover {
        background: rgba(255,255,255,0.08);
        border-color: #00d4ff;
        transform: translateY(-2px);
    }
    
    /* 分数徽章 */
    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00d4ff, #7b2cbf);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* 风味标签 */
    .flavor-tag {
        display: inline-block;
        background: rgba(0,212,255,0.15);
        color: #00d4ff;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid rgba(0,212,255,0.3);
    }
    
    .flavor-tag-common {
        background: rgba(123,44,191,0.2);
        color: #c77dff;
        border-color: rgba(123,44,191,0.4);
    }
    
    /* 类别标签 */
    .category-tag {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        color: #aaa;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.75rem;
        margin-right: 0.5rem;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff, #7b2cbf);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(0,212,255,0.4);
    }
    
    /* 信息框 */
    .info-box {
        background: rgba(0,212,255,0.1);
        border-left: 4px solid #00d4ff;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* 配对类型标签 */
    .pairing-type {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    
    .pairing-consonance {
        background: rgba(0,212,255,0.2);
        color: #00d4ff;
        border: 1px solid #00d4ff;
    }
    
    .pairing-contrast {
        background: rgba(231,111,81,0.2);
        color: #e76f51;
        border: 1px solid #e76f51;
    }
    
    /* 评分卡片 */
    .score-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 分隔线 */
    hr {
        border-color: rgba(255,255,255,0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============== 多语言文本配置 ==============
I18N = {
    'zh': {
        'title': '🧪 分子风味配对实验室',
        'subtitle': '基于分子指纹的食材配对灵感引擎 | Powered by FlavorDB',
        'search_placeholder': '输入食材名称（如: 草莓、牛肉、咖啡...）',
        'search_label': '🔍 搜索食材',
        'category_filter': '📂 类别筛选',
        'all_categories': '全部',
        'search_results': '📋 搜索结果',
        'select_ingredient': '选择食材:',
        'flavor_tags': '风味标签数',
        'unique_flavors': '唯一风味数',
        'main_flavors': '主要风味特征:',
        'pairing_mode': '🔍 配对模式',
        'consonance_label': '同味型叠加 (Consonance)',
        'contrast_label': '对比味型 (Contrast)',
        'consonance_help': '寻找风味相似的食材',
        'contrast_help': '寻找风味互补的食材',
        'settings': '⚙️ 设置',
        'result_count': '显示结果数量',
        'blacklist': '🚫 黑名单',
        'blacklist_placeholder': '例如:\n大蒜\n洋葱',
        'blacklist_help': '这些食材将不会出现在配对结果中',
        'about': '📖 关于',
        'about_text': '基于 **FlavorDB** 分子风味数据库，使用集合运算计算食材间的风味重合度，为您提供科学的食材配对建议。',
        'data_overview': '📊 数据概览',
        'ingredient_count': '食材总数',
        'flavor_count': '风味标签',
        'category_count': '食材类别',
        'popular_ingredients': '🔥 热门食材推荐',
        'pairing_score': '配对得分',
        'jaccard_score': 'Jaccard 相似度',
        'common_flavors': '共有风味分子',
        'contrast_features': '互补性特征',
        'category_bonus': '跨类别加分',
        'recommendations': '🎯 推荐搭配',
        'view_principle': '🔬 查看配对原理',
        'generate_recipe': '🍳 生成菜谱建议',
        'no_results': '未找到合适的配对结果，请尝试其他食材或调整设置。',
        'no_match': '未找到匹配的食材，请尝试其他关键词。',
        'usage_guide': '📖 使用指南',
        'science_principle': '🧪 科学原理',
        'consonance_desc': '基于共享风味分子的搭配原理。当两种食材含有大量共同的风味化合物时，它们会产生和谐、协调的味觉体验。',
        'contrast_desc': '基于风味互补的搭配原理。不同风味特征的食材通过对比和平衡，创造出更丰富、更有层次的味觉体验。',
        'footer': '🧪 分子风味配对实验室 | Molecular Flavor Lab',
        'footer_sub': 'Powered by FlavorDB | Data-driven Ingredient Pairing',
        'score_excellent': '极佳',
        'score_good': '优秀',
        'score_average': '良好',
        'score_poor': '一般',
        'excellent_threshold': 150,
        'good_threshold': 100,
        'average_threshold': 60,
    },
    'en': {
        'title': '🧪 Molecular Flavor Lab',
        'subtitle': 'Ingredient Pairing Engine Powered by Molecular Fingerprints | FlavorDB',
        'search_placeholder': 'Search ingredients (e.g., Strawberry, Beef, Coffee...)',
        'search_label': '🔍 Search Ingredient',
        'category_filter': '📂 Category Filter',
        'all_categories': 'All',
        'search_results': '📋 Search Results',
        'select_ingredient': 'Select Ingredient:',
        'flavor_tags': 'Flavor Tags',
        'unique_flavors': 'Unique Flavors',
        'main_flavors': 'Main Flavor Profile:',
        'pairing_mode': '🔍 Pairing Mode',
        'consonance_label': 'Consonance (Harmony)',
        'contrast_label': 'Contrast (Complement)',
        'consonance_help': 'Find ingredients with similar flavors',
        'contrast_help': 'Find ingredients with complementary flavors',
        'settings': '⚙️ Settings',
        'result_count': 'Number of Results',
        'blacklist': '🚫 Blacklist',
        'blacklist_placeholder': 'e.g.:\nGarlic\nOnion',
        'blacklist_help': 'These ingredients will be excluded from results',
        'about': '📖 About',
        'about_text': 'Powered by **FlavorDB**, using set operations to calculate flavor overlap between ingredients for scientifically-backed pairing suggestions.',
        'data_overview': '📊 Data Overview',
        'ingredient_count': 'Total Ingredients',
        'flavor_count': 'Flavor Tags',
        'category_count': 'Categories',
        'popular_ingredients': '🔥 Popular Ingredients',
        'pairing_score': 'Pairing Score',
        'jaccard_score': 'Jaccard Similarity',
        'common_flavors': 'Shared Flavor Molecules',
        'contrast_features': 'Complementary Features',
        'category_bonus': 'Cross-Category Bonus',
        'recommendations': '🎯 Recommended Pairings',
        'view_principle': '🔬 View Pairing Principle',
        'generate_recipe': '🍳 Generate Recipe Idea',
        'no_results': 'No suitable pairings found. Try a different ingredient or adjust settings.',
        'no_match': 'No matching ingredients found. Try different keywords.',
        'usage_guide': '📖 User Guide',
        'science_principle': '🧪 Scientific Principle',
        'consonance_desc': 'Based on shared flavor molecules. When two ingredients share many flavor compounds, they create harmonious, coordinated taste experiences.',
        'contrast_desc': 'Based on flavor complementarity. Different flavor characteristics create richer, more layered taste experiences through contrast and balance.',
        'footer': '🧪 Molecular Flavor Lab',
        'footer_sub': 'Powered by FlavorDB | Data-driven Ingredient Pairing',
        'score_excellent': 'Excellent',
        'score_good': 'Good',
        'score_average': 'Average',
        'score_poor': 'Fair',
        'excellent_threshold': 150,
        'good_threshold': 100,
        'average_threshold': 60,
    }
}

# ============== 食材中英文映射表（常用食材）=============
INGREDIENT_TRANSLATIONS = {
    # 水果类
    'tomato': '西红柿', 'strawberry': '草莓', 'apple': '苹果', 'banana': '香蕉',
    'orange': '橙子', 'lemon': '柠檬', 'lime': '青柠', 'grape': '葡萄',
    'peach': '桃子', 'pear': '梨', 'cherry': '樱桃', 'mango': '芒果',
    'pineapple': '菠萝', 'watermelon': '西瓜', 'melon': '甜瓜', 'blueberry': '蓝莓',
    'raspberry': '覆盆子', 'blackberry': '黑莓', 'apricot': '杏', 'plum': '李子',
    'grapefruit': '葡萄柚', 'coconut': '椰子', 'kiwi': '猕猴桃', 'papaya': '木瓜',
    'pomegranate': '石榴', 'fig': '无花果', 'date': '枣', 'olive': '橄榄',
    'avocado': '牛油果', 'lychee': '荔枝', 'durian': '榴莲', 'mangosteen': '山竹',
    
    # 蔬菜类
    'potato': '土豆', 'onion': '洋葱', 'garlic': '大蒜', 'carrot': '胡萝卜',
    'cucumber': '黄瓜', 'lettuce': '生菜', 'cabbage': '卷心菜', 'broccoli': '西兰花',
    'cauliflower': '花椰菜', 'spinach': '菠菜', 'celery': '芹菜', 'asparagus': '芦笋',
    'eggplant': '茄子', 'pepper': '辣椒', 'chili': '辣椒', 'bell pepper': '甜椒',
    'corn': '玉米', 'pea': '豌豆', 'bean': '豆类', 'mushroom': '蘑菇',
    'ginger': '姜', 'radish': '萝卜', 'beetroot': '甜菜', 'pumpkin': '南瓜',
    'squash': '南瓜', 'zucchini': '西葫芦', 'leek': '韭菜', 'shallot': '青葱',
    
    # 香草香料
    'basil': '罗勒', 'mint': '薄荷', 'rosemary': '迷迭香', 'thyme': '百里香',
    'oregano': '牛至', 'sage': '鼠尾草', 'cilantro': '香菜', 'parsley': '欧芹',
    'dill': '莳萝', 'chives': '细香葱', 'tarragon': '龙蒿', 'bay leaf': '月桂叶',
    'cinnamon': '肉桂', 'vanilla': '香草', 'clove': '丁香', 'nutmeg': '肉豆蔻',
    'cardamom': '豆蔻', 'saffron': '藏红花', 'turmeric': '姜黄', 'cumin': '孜然',
    'coriander': '香菜籽', 'fennel': '茴香', 'anise': '八角', 'star anise': '八角',
    'pepper': '胡椒', 'black pepper': '黑胡椒', 'white pepper': '白胡椒',
    'chili pepper': '辣椒', 'paprika': '红椒粉', 'cayenne': '卡宴辣椒',
    
    # 肉类
    'beef': '牛肉', 'pork': '猪肉', 'chicken': '鸡肉', 'lamb': '羊肉',
    'duck': '鸭肉', 'turkey': '火鸡肉', 'veal': '小牛肉', 'venison': '鹿肉',
    'bacon': '培根', 'ham': '火腿', 'sausage': '香肠', 'salami': '萨拉米',
    
    # 海鲜
    'salmon': '三文鱼', 'tuna': '金枪鱼', 'cod': '鳕鱼', 'shrimp': '虾',
    'prawn': '大虾', 'crab': '蟹', 'lobster': '龙虾', 'oyster': '生蚝',
    'scallop': '扇贝', 'mussel': '青口', 'clam': '蛤蜊', 'squid': '鱿鱼',
    'octopus': '章鱼', 'anchovy': '凤尾鱼', 'sardine': '沙丁鱼', 'herring': '鲱鱼',
    
    # 乳制品
    'milk': '牛奶', 'cheese': '奶酪', 'butter': '黄油', 'cream': '奶油',
    'yogurt': '酸奶', 'cheddar': '切达奶酪', 'mozzarella': '马苏里拉奶酪',
    'parmesan': '帕尔马干酪', 'brie': '布里奶酪', 'camembert': '卡门贝尔奶酪',
    'feta': '菲达奶酪', 'goat cheese': '山羊奶酪', 'blue cheese': '蓝纹奶酪',
    'ricotta': '里科塔奶酪', 'mascarpone': '马斯卡彭奶酪',
    
    # 谷物坚果
    'rice': '大米', 'wheat': '小麦', 'bread': '面包', 'pasta': '意大利面',
    'noodle': '面条', 'oat': '燕麦', 'barley': '大麦', 'quinoa': '藜麦',
    'almond': '杏仁', 'walnut': '核桃', 'peanut': '花生', 'cashew': '腰果',
    'pistachio': '开心果', 'hazelnut': '榛子', 'pecan': '山核桃', 'macadamia': '夏威夷果',
    'sesame': '芝麻', 'sunflower seed': '葵花籽', 'pumpkin seed': '南瓜籽',
    
    # 饮品
    'coffee': '咖啡', 'tea': '茶', 'green tea': '绿茶', 'black tea': '红茶',
    'wine': '葡萄酒', 'red wine': '红酒', 'white wine': '白酒', 'beer': '啤酒',
    'whiskey': '威士忌', 'vodka': '伏特加', 'rum': '朗姆酒', 'brandy': '白兰地',
    'champagne': '香槟', 'cider': '苹果酒', 'sake': '清酒', 'juice': '果汁',
    'honey': '蜂蜜', 'chocolate': '巧克力', 'cocoa': '可可',
    
    # 其他
    'sugar': '糖', 'salt': '盐', 'vinegar': '醋', 'oil': '油',
    'olive oil': '橄榄油', 'soy sauce': '酱油', 'fish sauce': '鱼露',
    'oyster sauce': '蚝油', 'ketchup': '番茄酱', 'mustard': '芥末',
    'mayonnaise': '蛋黄酱', 'truffle': '松露', 'caviar': '鱼子酱',
    'egg': '鸡蛋', 'egg yolk': '蛋黄', 'egg white': '蛋白',
}

# 创建反向映射（中文 -> 英文）
INGREDIENT_TRANSLATIONS_REVERSE = {v: k for k, v in INGREDIENT_TRANSLATIONS.items()}

# ============== 风味标签翻译词典 ==============
FLAVOR_TRANSLATIONS = {
    'sweet': '甜', 'bitter': '苦', 'sour': '酸', 'salty': '咸', 'umami': '鲜',
    'fruity': '果香', 'citrus': '柑橘', 'apple': '苹果', 'pear': '梨', 'peach': '桃子',
    'apricot': '杏', 'plum': '李子', 'cherry': '樱桃', 'strawberry': '草莓',
    'raspberry': '覆盆子', 'blueberry': '蓝莓', 'pineapple': '菠萝', 'banana': '香蕉',
    'grape': '葡萄', 'grapefruit': '葡萄柚', 'lemon': '柠檬', 'lime': '青柠',
    'orange': '橙子', 'melon': '甜瓜', 'tropical': '热带水果', 'berry': '浆果',
    'floral': '花香', 'rose': '玫瑰', 'jasmine': '茉莉', 'lily': '百合',
    'lavender': '薰衣草', 'honeysuckle': '金银花', 'muguet': '铃兰', 'violet': '紫罗兰',
    'peony': '牡丹', 'carnation': '康乃馨', 'herbal': '草本', 'mint': '薄荷',
    'peppermint': '薄荷', 'menthol': '薄荷醇', 'thyme': '百里香', 'cinnamon': '肉桂',
    'clove': '丁香', 'vanilla': '香草', 'anise': '茴香', 'camphor': '樟脑',
    'camphoraceous': '樟脑味', 'eucalyptus': '桉树', 'green': '青草', 'grassy': '草香',
    'leafy': '叶香', 'hay': '干草', 'nutty': '坚果', 'almond': '杏仁',
    'hazelnut': '榛子', 'walnut': '核桃', 'peanut': '花生', 'coconut': '椰子',
    'popcorn': '爆米花', 'malt': '麦芽', 'bread': '面包', 'bready': '面包香',
    'cereal': '谷物', 'roasted': '烘焙', 'caramel': '焦糖', 'caramellic': '焦糖味',
    'butterscotch': '奶油糖', 'butter': '黄油', 'buttery': '黄油味', 'creamy': '奶油',
    'milky': '奶香', 'cheese': '奶酪', 'cheesy': '奶酪味', 'chocolate': '巧克力',
    'cocoa': '可可', 'coffee': '咖啡', 'burnt': '焦香', 'smoky': '烟熏',
    'smoke': '烟味', 'baked': '烘烤', 'toasted': '烘烤', 'woody': '木质',
    'wood': '木香', 'earthy': '泥土', 'mushroom': '蘑菇', 'musty': '霉味',
    'moss': '苔藓', 'balsam': '香脂', 'balsamic': '香醋', 'resin': '树脂',
    'resinous': '树脂味', 'pine': '松木', 'cedar': '雪松', 'fresh': '清新',
    'waxy': '蜡质', 'fatty': '油脂', 'oily': '油润', 'pungent': '辛辣',
    'spicy': '香料', 'spice': '辛香', 'peppery': '胡椒', 'warm': '温暖',
    'cool': '清凉', 'medicinal': '药草', 'medical': '药香', 'phenolic': '酚类',
    'sulfur': '硫磺', 'sulfurous': '硫磺味', 'sweat': '汗味', 'sweaty': '汗味',
    'rancid': '酸败', 'fishy': '鱼腥味', 'meaty': '肉香', 'beef': '牛肉',
    'chicken': '鸡肉', 'wine': '酒香', 'alcoholic': '酒精', 'alcohol': '酒味',
    'fermented': '发酵', 'vinegar': '醋', 'acid': '酸性', 'acidic': '酸味',
    'sharp': '尖锐', 'strong': '浓烈', 'mild': '温和', 'faint': '微弱',
    'odorless': '无味', 'fragrant': '芳香', 'aromatic': '香气', 'perfume': '香水',
    'powdery': '粉质', 'soapy': '皂香', 'plastic': '塑料', 'rubber': '橡胶',
    'chemical': '化学', 'gasoline': '汽油', 'ether': '乙醚', 'ethereal': '飘渺',
    'solvent': '溶剂', 'metallic': '金属', 'leather': '皮革', 'raw': '生青',
    'green bean': '青豆', 'tomato': '番茄', 'potato': '土豆', 'onion': '洋葱',
    'garlic': '大蒜', 'cabbage': '卷心菜', 'pea': '豌豆', 'cucumber': '黄瓜',
    'seaweed': '海藻', 'truffle': '松露', 'egg': '蛋', 'honey': '蜂蜜',
    'maple': '枫糖', 'sugar': '糖', 'jam': '果酱', 'candy': '糖果',
    'cotton candy': '棉花糖', 'tutti frutti': '什锦水果', 'sandalwood': '檀香',
}

# ============== 核心配对类 ==============
class MolecularFlavorLab:
    """分子风味配对实验室核心类"""
    
    def __init__(self, csv_path='flavordb_data.csv'):
        """初始化，加载数据"""
        # 使用相对路径，确保云端部署兼容性
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, csv_path)
        
        self.df = pd.read_csv(full_path)
        self.flavor_translations = FLAVOR_TRANSLATIONS
        self.ingredient_translations = INGREDIENT_TRANSLATIONS
        
        # 解析flavors字段
        self.parsed_data = self._parse_flavors()
        
        # 构建风味倒排索引
        self.flavor_index = self._build_flavor_index()
        
        # 构建名称搜索索引（支持中英文）
        self.name_index = self._build_name_index()
        
    def _parse_flavors(self):
        """解析flavors字段"""
        def parse_flavor_str(flavor_str):
            if pd.isna(flavor_str):
                return []
            groups = str(flavor_str).split(',')
            all_flavors = []
            for group in groups:
                flavors = group.strip().split('@')
                all_flavors.extend([f.strip().lower() for f in flavors if f.strip()])
            return all_flavors
        
        parsed = []
        for idx, row in self.df.iterrows():
            if pd.notna(row['flavors']):
                flavors = parse_flavor_str(row['flavors'])
                parsed.append({
                    'id': row['id'],
                    'name': row['name'],
                    'category': row['category'],
                    'flavors': flavors,
                    'flavor_set': set(flavors)
                })
        return parsed
    
    def _build_flavor_index(self):
        """构建风味倒排索引"""
        index = {}
        for item in self.parsed_data:
            for flavor in item['flavor_set']:
                if flavor not in index:
                    index[flavor] = []
                index[flavor].append(item)
        return index
    
    def _build_name_index(self):
        """构建名称搜索索引（支持中英文）"""
        index = {}
        for item in self.parsed_data:
            # 英文名索引
            en_name = item['name'].lower()
            index[en_name] = item
            
            # 中文名索引（如果有翻译）
            cn_name = self.ingredient_translations.get(en_name, '')
            if cn_name:
                index[cn_name] = item
        return index
    
    def translate_flavor(self, flavor_en):
        """翻译风味标签为中文"""
        return self.flavor_translations.get(flavor_en, flavor_en)
    
    def translate_ingredient_to_cn(self, name_en):
        """将食材英文名翻译为中文"""
        return self.ingredient_translations.get(name_en.lower(), name_en)
    
    def translate_ingredient_to_en(self, name_cn):
        """将食材中文名翻译为英文"""
        return INGREDIENT_TRANSLATIONS_REVERSE.get(name_cn, name_cn)
    
    def get_ingredient_display_name(self, item, lang='zh'):
        """获取食材的显示名称（根据语言）"""
        en_name = item['name']
        cn_name = self.translate_ingredient_to_cn(en_name)
        
        if lang == 'zh':
            return f"{cn_name}" if cn_name != en_name else en_name
        else:
            return en_name
    
    def get_ingredient_by_name(self, name):
        """根据名称查找食材（支持中英文）"""
        name_lower = name.lower().strip()
        
        # 先尝试直接查找
        if name_lower in self.name_index:
            return self.name_index[name_lower]
        
        # 尝试中文转英文后查找
        en_name = self.translate_ingredient_to_en(name_lower)
        if en_name.lower() in self.name_index:
            return self.name_index[en_name.lower()]
        
        # 模糊匹配
        for item in self.parsed_data:
            if name_lower in item['name'].lower():
                return item
        
        return None
    
    def search_ingredients(self, query, limit=20):
        """搜索食材（支持中英文）"""
        if not query:
            return []
        
        query_lower = query.lower().strip()
        results = []
        matched_ids = set()
        
        # 1. 精确匹配中文名
        if query_lower in INGREDIENT_TRANSLATIONS_REVERSE:
            en_name = INGREDIENT_TRANSLATIONS_REVERSE[query_lower]
            for item in self.parsed_data:
                if item['name'].lower() == en_name.lower() and item['id'] not in matched_ids:
                    results.append(item)
                    matched_ids.add(item['id'])
        
        # 2. 精确匹配英文名
        for item in self.parsed_data:
            if item['name'].lower() == query_lower and item['id'] not in matched_ids:
                results.append(item)
                matched_ids.add(item['id'])
        
        # 3. 模糊匹配英文名
        for item in self.parsed_data:
            if query_lower in item['name'].lower() and item['id'] not in matched_ids:
                results.append(item)
                matched_ids.add(item['id'])
            if len(results) >= limit:
                break
        
        # 4. 模糊匹配中文翻译
        for cn_name, en_name in INGREDIENT_TRANSLATIONS_REVERSE.items():
            if query_lower in cn_name and len(results) < limit:
                for item in self.parsed_data:
                    if item['name'].lower() == en_name.lower() and item['id'] not in matched_ids:
                        results.append(item)
                        matched_ids.add(item['id'])
        
        return results[:limit]
    
    def get_categories(self):
        """获取所有类别"""
        return sorted(set(item['category'] for item in self.parsed_data))
    
    def get_ingredients_by_category(self, category):
        """根据类别获取食材"""
        return [item for item in self.parsed_data if item['category'] == category]
    
    # ==================== Consonance 评分算法 ====================
    def consonance_pairing(self, ingredient_name, top_n=10, exclude_categories=None, blacklist=None):
        """
        同味型叠加配对（Consonance）
        评分公式: score = jaccard * 100 + common_count * 0.5
        """
        target = self.get_ingredient_by_name(ingredient_name)
        if not target:
            return []
        
        exclude_categories = exclude_categories or []
        blacklist = [b.lower() for b in (blacklist or [])]
        target_flavors = target['flavor_set']
        
        results = []
        for item in self.parsed_data:
            # 排除自己
            if item['id'] == target['id']:
                continue
            # 排除指定类别
            if item['category'] in exclude_categories:
                continue
            # 排除黑名单
            if item['name'].lower() in blacklist:
                continue
            
            # 计算交集和并集
            common_flavors = target_flavors & item['flavor_set']
            if len(common_flavors) > 0:
                union_flavors = target_flavors | item['flavor_set']
                jaccard = len(common_flavors) / len(union_flavors)
                
                # Consonance 评分公式
                score = jaccard * 100 + len(common_flavors) * 0.5
                
                # 归一化到 0-100 范围用于进度条显示
                score_normalized = min(score / 2, 100)
                
                results.append({
                    'ingredient': item,
                    'common_flavors': common_flavors,
                    'common_count': len(common_flavors),
                    'jaccard': jaccard,
                    'score': score,
                    'score_normalized': score_normalized,
                    'pairing_type': 'consonance'
                })
        
        # 按分数降序排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]
    
    # ==================== Contrast 评分算法 ====================
    def contrast_pairing(self, ingredient_name, top_n=10, prefer_categories=None, blacklist=None):
        """
        对比味型配对（Contrast）
        评分公式: score = contrast_score + category_bonus + intersection_bonus
        """
        target = self.get_ingredient_by_name(ingredient_name)
        if not target:
            return []
        
        prefer_categories = prefer_categories or []
        blacklist = [b.lower() for b in (blacklist or [])]
        target_flavors = target['flavor_set']
        target_category = target['category']
        
        # 对比风味映射表
        contrast_mapping = {
            'sweet': ['sour', 'bitter', 'salty', 'acidic'],
            'sour': ['sweet', 'fatty', 'umami', 'creamy'],
            'bitter': ['sweet', 'salty', 'sour', 'honey'],
            'fatty': ['sour', 'bitter', 'acidic', 'fresh'],
            'creamy': ['sour', 'acidic', 'fresh', 'citrus'],
            'fresh': ['warm', 'spicy', 'roasted', 'smoky'],
            'light': ['strong', 'rich', 'heavy', 'pungent'],
            'fruity': ['earthy', 'woody', 'nutty', 'meaty'],
            'floral': ['earthy', 'woody', 'spicy', 'herbal'],
        }
        
        results = []
        for item in self.parsed_data:
            # 排除自己
            if item['id'] == target['id']:
                continue
            # 排除黑名单
            if item['name'].lower() in blacklist:
                continue
            
            item_flavors = item['flavor_set']
            
            # 计算对比分数
            contrast_score = 0
            matched_contrast_pairs = []
            for target_flavor in target_flavors:
                if target_flavor in contrast_mapping:
                    for contrast_flavor in contrast_mapping[target_flavor]:
                        if contrast_flavor in item_flavors:
                            contrast_score += 2
                            matched_contrast_pairs.append(
                                (target_flavor, contrast_flavor)
                            )
            
            # 类别加分
            category_bonus = 0
            if item['category'] != target_category:
                category_bonus = 10  # 跨类别加分
            if item['category'] in prefer_categories:
                category_bonus += 15  # 优先类别额外加分
            
            # 交集加分（适度交集表示有一定联系但不过度相似）
            common = target_flavors & item_flavors
            intersection_bonus = 0
            if 3 <= len(common) <= 15:
                intersection_bonus = 8
            
            # Contrast 总分
            total_score = contrast_score + category_bonus + intersection_bonus
            
            if total_score > 0:
                # 归一化到 0-100 范围
                score_normalized = min(total_score * 2, 100)
                
                results.append({
                    'ingredient': item,
                    'contrast_score': contrast_score,
                    'category_bonus': category_bonus,
                    'intersection_bonus': intersection_bonus,
                    'common_flavors': common,
                    'common_count': len(common),
                    'matched_pairs': matched_contrast_pairs,
                    'score': total_score,
                    'score_normalized': score_normalized,
                    'pairing_type': 'contrast'
                })
        
        # 按分数降序排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]
    
    def get_score_level(self, score, pairing_type='consonance'):
        """根据分数返回等级和颜色"""
        if pairing_type == 'consonance':
            if score >= 150:
                return 'excellent', '#00c853'  # 绿色
            elif score >= 100:
                return 'good', '#64dd17'  # 浅绿
            elif score >= 60:
                return 'average', '#ffd600'  # 黄色
            else:
                return 'poor', '#ff9100'  # 橙色
        else:  # contrast
            if score >= 40:
                return 'excellent', '#00c853'
            elif score >= 30:
                return 'good', '#64dd17'
            elif score >= 20:
                return 'average', '#ffd600'
            else:
                return 'poor', '#ff9100'

# ============== 初始化（使用缓存）=============
@st.cache_resource
def get_lab():
    """缓存数据加载，提高性能"""
    return MolecularFlavorLab('flavordb_data.csv')

try:
    lab = get_lab()
    data_loaded = True
except Exception as e:
    st.error(f"数据加载失败: {e}")
    data_loaded = False

# ============== 侧边栏配置 ==============
with st.sidebar:
    # 语言切换
    st.markdown("## 🌐 Language / 语言")
    lang = st.selectbox(
        "Select Language / 选择语言",
        options=['zh', 'en'],
        format_func=lambda x: '中文' if x == 'zh' else 'English',
        index=0
    )
    
    # 获取当前语言的文本
    t = I18N[lang]
    
    st.markdown(f"## {t['title']}")
    st.markdown("---")
    
    if data_loaded:
        st.markdown(f"**{t['data_overview']}**")
        st.markdown(f"- {t['ingredient_count']}: `{len(lab.parsed_data)}`")
        st.markdown(f"- {t['flavor_count']}: `{len(lab.flavor_index)}`")
        st.markdown(f"- {t['category_count']}: `{len(lab.get_categories())}`")
    
    st.markdown("---")
    st.markdown(f"### {t['pairing_mode']}")
    
    pairing_mode = st.radio(
        t['pairing_mode'],
        [t['consonance_label'], t['contrast_label']],
        help=f"{t['consonance_help']} | {t['contrast_help']}"
    )
    
    st.markdown("---")
    st.markdown(f"### {t['settings']}")
    
    top_n = st.slider(t['result_count'], 5, 20, 10)
    
    # 黑名单功能
    st.markdown(f"### {t['blacklist']}")
    blacklist_input = st.text_area(
        t['blacklist'],
        placeholder=t['blacklist_placeholder'],
        help=t['blacklist_help']
    )
    blacklist = [name.strip() for name in blacklist_input.split('\n') if name.strip()]
    
    st.markdown("---")
    st.markdown(f"### {t['about']}")
    st.markdown(t['about_text'])

# ============== 主页面 ==============
st.markdown(f'<h1 class="main-title">{t["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)

if not data_loaded:
    st.stop()

# 搜索区域
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        t['search_label'],
        placeholder=t['search_placeholder'],
        help=t['search_placeholder']
    )

with col2:
    category_filter = st.selectbox(
        t['category_filter'],
        [t['all_categories']] + lab.get_categories()
    )

# 搜索建议与结果显示
if search_query:
    search_results = lab.search_ingredients(search_query, limit=10)
    
    if category_filter != t['all_categories']:
        search_results = [r for r in search_results if r['category'] == category_filter]
    
    if search_results:
        st.markdown(f"### {t['search_results']}")
        
        # 构建显示选项（中英文）
        ingredient_options = []
        for item in search_results:
            display_name = lab.get_ingredient_display_name(item, lang)
            en_name = item['name']
            cn_name = lab.translate_ingredient_to_cn(en_name)
            
            if lang == 'zh' and cn_name != en_name:
                option_label = f"{display_name} ({en_name}) - {item['category']}"
            else:
                option_label = f"{display_name} - {item['category']}"
            
            ingredient_options.append((option_label, item['name']))
        
        selected_label = st.radio(
            t['select_ingredient'],
            [opt[0] for opt in ingredient_options],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # 获取选中的英文名
        selected_name = dict(ingredient_options)[selected_label]
        selected_ingredient = lab.get_ingredient_by_name(selected_name)
        
        if selected_ingredient:
            st.markdown("---")
            
            # 显示选中食材信息
            col_info1, col_info2 = st.columns([2, 3])
            
            display_name = lab.get_ingredient_display_name(selected_ingredient, lang)
            
            with col_info1:
                st.markdown(f"""
                <div class="ingredient-card">
                    <h3>🍃 {display_name}</h3>
                    <span class="category-tag">{selected_ingredient['category']}</span>
                    <p style="margin-top: 1rem;">
                        <strong>{t['flavor_tags']}:</strong> {len(selected_ingredient['flavors'])}<br>
                        <strong>{t['unique_flavors']}:</strong> {len(selected_ingredient['flavor_set'])}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_info2:
                # 显示主要风味标签
                flavor_counts = Counter(selected_ingredient['flavors'])
                top_flavors = flavor_counts.most_common(15)
                
                st.markdown(f"**{t['main_flavors']}**")
                flavor_html = ""
                for flavor, count in top_flavors:
                    flavor_cn = lab.translate_flavor(flavor)
                    flavor_html += f'<span class="flavor-tag">{flavor_cn}</span>'
                st.markdown(flavor_html, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 执行配对
            is_consonance = "Consonance" in pairing_mode or "同味型" in pairing_mode
            
            if is_consonance:
                results = lab.consonance_pairing(
                    selected_name, 
                    top_n=top_n,
                    blacklist=blacklist
                )
                st.markdown(f'<span class="pairing-type pairing-consonance">🔄 {t["consonance_label"]}</span>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="info-box">
                    {t['consonance_desc']}
                </div>
                """, unsafe_allow_html=True)
            else:
                results = lab.contrast_pairing(
                    selected_name,
                    top_n=top_n,
                    blacklist=blacklist
                )
                st.markdown(f'<span class="pairing-type pairing-contrast">⚡ {t["contrast_label"]}</span>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="info-box" style="border-color: #e76f51; background: rgba(231,111,81,0.1);">
                    {t['contrast_desc']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"### {t['recommendations']}")
            
            if results:
                for i, result in enumerate(results, 1):
                    ing = result['ingredient']
                    common_list = list(result['common_flavors'])
                    common_cn = [lab.translate_flavor(f) for f in common_list[:8]]
                    
                    # 获取分数等级和颜色
                    level, color = lab.get_score_level(result['score'], result['pairing_type'])
                    
                    # 显示名称
                    partner_display_name = lab.get_ingredient_display_name(ing, lang)
                    
                    with st.container():
                        # 分数显示区域
                        score_col, info_col = st.columns([1, 3])
                        
                        with score_col:
                            # 使用 st.metric 显示分数
                            st.metric(
                                label=t['pairing_score'],
                                value=f"{result['score']:.1f}",
                                delta=None
                            )
                            
                            # 进度条显示归一化分数
                            progress_value = result['score_normalized'] / 100
                            st.progress(progress_value)
                            
                            # 显示分数等级
                            if level == 'excellent':
                                st.success(f"⭐⭐⭐⭐⭐ {t['score_excellent']}")
                            elif level == 'good':
                                st.info(f"⭐⭐⭐⭐ {t['score_good']}")
                            elif level == 'average':
                                st.warning(f"⭐⭐⭐ {t['score_average']}")
                            else:
                                st.error(f"⭐⭐ {t['score_poor']}")
                        
                        with info_col:
                            st.markdown(f"""
                            <div class="ingredient-card">
                                <h4>#{i} {partner_display_name} <span class="category-tag">{ing['category']}</span></h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 根据配对类型显示不同信息
                            if is_consonance:
                                st.markdown(f"**{t['jaccard_score']}:** {result['jaccard']:.3f}")
                                st.markdown(f"**{t['common_flavors']}:** {result['common_count']} {t['flavor_count']}")
                            else:
                                st.markdown(f"**{t['contrast_features']}:** +{result['contrast_score']} {t['pairing_score']}")
                                st.markdown(f"**{t['category_bonus']}:** +{result['category_bonus']} {t['pairing_score']}")
                                st.markdown(f"**{t['common_flavors']}:** {result['common_count']} {t['flavor_count']}")
                            
                            # 显示共同风味标签
                            if common_cn:
                                st.markdown("**" + t['common_flavors'] + ":**")
                                common_html = ""
                                for flavor_cn in common_cn:
                                    common_html += f'<span class="flavor-tag flavor-tag-common">{flavor_cn}</span>'
                                st.markdown(common_html, unsafe_allow_html=True)
                            
                            # 展开查看配对原理解释
                            with st.expander(t['view_principle']):
                                if is_consonance:
                                    st.markdown(f"""
                                    **{t['consonance_label']}**
                                    
                                    - **Jaccard 相似度:** {result['jaccard']:.3f}
                                    - **共有风味分子:** {result['common_count']} 个
                                    - **原始分数:** {result['score']:.1f}
                                    
                                    这种搭配基于**风味共鸣**原理——当两种食材拥有大量共同的风味化合物时，
                                    它们能够产生和谐、协调的味觉体验。
                                    """)
                                else:
                                    st.markdown(f"""
                                    **{t['contrast_label']}**
                                    
                                    - **对比分数:** +{result['contrast_score']}
                                    - **类别加分:** +{result['category_bonus']}
                                    - **交集加分:** +{result['intersection_bonus']}
                                    - **总分数:** {result['score']}
                                    
                                    这种搭配基于**风味互补**原理——不同风味特征的食材通过对比和平衡，
                                    创造出更丰富、更有层次的味觉体验。
                                    """)
                                
                                # 生成菜谱建议按钮
                                if st.button(t['generate_recipe'], key=f"recipe_{i}"):
                                    st.info(f"""
                                    **{display_name} × {partner_display_name}**
                                    
                                    💡 **建议烹饪方式:**
                                    - 考虑两种食材的风味特征，选择能突出共同风味的烹饪方法
                                    - 建议先小批量试做，调整比例找到最佳搭配
                                    
                                    📝 **搭配要点:**
                                    - 共同风味: {', '.join(common_cn[:5]) if common_cn else '无'}
                                    - 注意平衡两种食材的用量比例
                                    
                                    *（完整AI菜谱功能开发中...）*
                                    """)
                        
                        st.markdown("---")
            else:
                st.warning(t['no_results'])
    else:
        st.info(t['no_match'])

else:
    # 默认页面 - 展示热门食材
    st.markdown(f"### {t['popular_ingredients']}")
    
    popular_ingredients = [
        ("Strawberry", "🍓"), ("Beef", "🥩"), ("Coffee", "☕"),
        ("Chocolate", "🍫"), ("Vanilla", "🌿"), ("Tomato", "🍅"),
        ("Garlic", "🧄"), ("Lemon", "🍋"), ("Honey", "🍯"),
        ("Mint", "🌱"), ("Ginger", "🫚"), ("Cinnamon", "🪵")
    ]
    
    cols = st.columns(4)
    for i, (name, emoji) in enumerate(popular_ingredients):
        with cols[i % 4]:
            display_name = lab.get_ingredient_display_name({'name': name}, lang)
            if st.button(f"{emoji} {display_name}", key=f"pop_{name}"):
                st.session_state['search_query'] = name
                st.rerun()
    
    st.markdown("---")
    
    # 展示数据概览
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"""
        <div class="ingredient-card" style="text-align: center;">
            <h2>🥗</h2>
            <h3>{len(lab.parsed_data)}</h3>
            <p>{t['ingredient_count']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="ingredient-card" style="text-align: center;">
            <h2>🏷️</h2>
            <h3>{len(lab.flavor_index)}</h3>
            <p>{t['flavor_count']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div class="ingredient-card" style="text-align: center;">
            <h2>📂</h2>
            <h3>{len(lab.get_categories())}</h3>
            <p>{t['category_count']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 使用说明
    st.markdown(f"""
    ### {t['usage_guide']}
    
    1. **🔍 {t['search_label']}** - {t['search_placeholder']}
    2. **📂 {t['category_filter']}** - {t['category_filter']}
    3. **🔄 {t['pairing_mode']}** - {t['consonance_label']} / {t['contrast_label']}
    4. **🎯 {t['recommendations']}** - {t['pairing_score']}
    5. **🔬 {t['view_principle']}** - {t['science_principle']}
    6. **🍳 {t['generate_recipe']}** - AI
    
    ### {t['science_principle']}
    
    **{t['consonance_label']}**  
    {t['consonance_desc']}
    
    **{t['contrast_label']}**  
    {t['contrast_desc']}
    """)

# ============== 页脚 ==============
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>{t['footer']}</p>
    <p style="font-size: 0.8rem;">{t['footer_sub']}</p>
</div>
""", unsafe_allow_html=True)
