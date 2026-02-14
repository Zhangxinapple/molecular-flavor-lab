"""
分子风味配对实验室 (Molecular Flavor Lab)
基于FlavorDB数据的食材配对灵感引擎
"""

import streamlit as st
import pandas as pd
from collections import Counter
import json

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
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: rgba(0,0,0,0.2);
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
    
    /* 分隔线 */
    hr {
        border-color: rgba(255,255,255,0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
    'licorice': '甘草', 'sarsaparilla': '菝葜', 'fenugreek': '葫芦巴',
    'coriander': '香菜', 'turmeric': '姜黄', 'ginger': '姜', 'wasabi': '芥末',
    'horseradish': '辣根', 'mustard': '芥末', 'paprika': '红椒', 'nutmeg': '肉豆蔻',
    'allspice': '多香果', 'cardamom': '豆蔻', 'saffron': '藏红花', 'tarragon': '龙蒿',
    'sage': '鼠尾草', 'rosemary': '迷迭香', 'basil': '罗勒', 'oregano': '牛至',
    'dill': '莳萝', 'fennel': '茴香', 'caraway': '葛缕子', 'cumin': '孜然',
    'bay': '月桂', 'laurel': '月桂', 'tea': '茶', 'black tea': '红茶',
    'green tea': '绿茶', 'jasmin': '茉莉', 'mimosa': '含羞草', 'neroli': '橙花',
    'orange flower': '橙花', 'ylang': '依兰', 'cananga': '依兰', 'tuberose': '晚香玉',
    'gardenia': '栀子花', 'magnolia': '木兰', 'hawthorn': '山楂', 'hawthorne': '山楂',
    'linden': '菩提', 'acacia': '金合欢', 'locust': '洋槐', 'rose water': '玫瑰水',
    'rose flower': '玫瑰花', 'rose dried': '干玫瑰', 'red rose': '红玫瑰',
    'iris': '鸢尾', 'orris': '鸢尾', 'violet leaf': '紫罗兰叶', 'hyacinth': '风信子',
    'narcissus': '水仙', 'lilac': '丁香花', 'lily of the valley': '铃兰',
    'citrus peel': '柑橘皮', 'orange peel': '橙皮', 'lemon peel': '柠檬皮',
    'lime peel': '青柠皮', 'grapefruit peel': '葡萄柚皮', 'mandarin': '橘子',
    'tangerine': '橘子', 'clementine': '小柑橘', 'kumquat': '金桔', 'pomelo': '柚子',
    'bergamot': '佛手柑', 'citron': '香橼', 'yuzu': '柚子', 'sudachi': '酢橘',
    'calamansi': '金桔', 'finger lime': '指橙', 'blood orange': '血橙',
    'cara cara': '卡拉卡拉橙', 'navel': '脐橙', 'valencia': '瓦伦西亚橙',
    'seville': '塞维利亚橙', 'bergamot orange': '佛手柑橙', 'bitter orange': '苦橙',
    'sweet orange': '甜橙', 'meyer lemon': '迈耶柠檬', 'persian lime': '波斯青柠',
    'key lime': '墨西哥青柠', 'kaffir lime': '箭叶橙', 'combava': '箭叶橙',
    'citronella': '香茅', 'lemongrass': '柠檬草', 'verbena': '马鞭草',
    'lemon balm': '柠檬香蜂草', 'lemon verbena': '柠檬马鞭草', 'melissa': '香蜂草',
    'citral': '柠檬醛', 'citronellal': '香茅醛', 'geraniol': '香叶醇',
    'linalool': '芳樟醇', 'limonene': '柠檬烯', 'pinene': '蒎烯', 'myrcene': '月桂烯',
    'caryophyllene': '石竹烯', 'humulene': '蛇麻烯', 'bisabolene': '红没药烯',
    'farnesene': '法尼烯', 'nerolidol': '橙花叔醇', 'phytol': '植醇',
    'menthone': '薄荷酮', 'menthol': '薄荷醇', 'carvone': '香芹酮',
    'anethole': '茴香脑', 'estragole': '草蒿脑', 'eugenol': '丁香酚',
    'chavicol': '胡椒酚', 'safrole': '黄樟素', 'myristicin': '肉豆蔻醚',
    'apiol': '芹菜脑', 'elemicin': '榄香素', 'asarone': '细辛脑',
    'cinnamaldehyde': '肉桂醛', 'cinnamic': '肉桂', 'cinnamyl': '肉桂基',
    'benzaldehyde': '苯甲醛', 'benzyl': '苄基', 'phenyl': '苯基',
    'anisaldehyde': '茴香醛', 'cuminaldehyde': '枯茗醛', 'vanillin': '香兰素',
    'ethyl vanillin': '乙基香兰素', 'maltol': '麦芽酚', 'ethyl maltol': '乙基麦芽酚',
    'furaneol': '呋喃酮', 'sotolone': '葫芦巴内酯', 'maple furanone': '枫糖内酯',
    'cotton furanone': '棉糖内酯', 'strawberry furanone': '草莓呋喃酮',
    'pineapple ketone': '菠萝酮', 'raspberry ketone': '覆盆子酮',
    'ionone': '紫罗兰酮', 'damascone': '大马士酮', 'damascenone': '大马士烯酮',
    'beta-ionone': 'β-紫罗兰酮', 'alpha-ionone': 'α-紫罗兰酮',
    'beta-damascone': 'β-大马士酮', 'alpha-damascone': 'α-大马士酮',
    'theaspirane': '茶螺烷', 'thearubigin': '茶红素', 'theaflavin': '茶黄素',
    'catechin': '儿茶素', 'epicatechin': '表儿茶素', 'epigallocatechin': '表没食子儿茶素',
    'egcg': '表没食子儿茶素没食子酸酯', 'theanine': '茶氨酸', 'caffeine': '咖啡因',
    'theobromine': '可可碱', 'theophylline': '茶碱', 'trigonelline': '葫芦巴碱',
    'chlorogenic acid': '绿原酸', 'quinic acid': '奎宁酸', 'citric acid': '柠檬酸',
    'malic acid': '苹果酸', 'tartaric acid': '酒石酸', 'succinic acid': '琥珀酸',
    'lactic acid': '乳酸', 'acetic acid': '乙酸', 'formic acid': '甲酸',
    'butyric acid': '丁酸', 'caproic acid': '己酸', 'caprylic acid': '辛酸',
    'capric acid': '癸酸', 'lauric acid': '月桂酸', 'myristic acid': '肉豆蔻酸',
    'palmitic acid': '棕榈酸', 'stearic acid': '硬脂酸', 'oleic acid': '油酸',
    'linoleic acid': '亚油酸', 'linolenic acid': '亚麻酸', 'arachidic acid': '花生酸',
    'behenic acid': '山嵛酸', 'erucic acid': '芥酸', 'nervonic acid': '神经酸',
}

# ============== 核心配对类 ==============
class MolecularFlavorLab:
    """分子风味配对实验室核心类"""
    
    def __init__(self, csv_path='flavordb_data.csv'):
        """初始化，加载数据"""
        self.df = pd.read_csv(csv_path)
        self.flavor_translations = FLAVOR_TRANSLATIONS
        
        # 解析flavors字段
        self.parsed_data = self._parse_flavors()
        
        # 构建风味倒排索引
        self.flavor_index = self._build_flavor_index()
        
        # 构建名称搜索索引
        self.name_index = {item['name'].lower(): item for item in self.parsed_data}
        
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
    
    def translate_flavor(self, flavor_en):
        """翻译风味标签为中文"""
        return self.flavor_translations.get(flavor_en, flavor_en)
    
    def get_ingredient_by_name(self, name):
        """根据名称查找食材"""
        name_lower = name.lower()
        for item in self.parsed_data:
            if name_lower in item['name'].lower():
                return item
        return None
    
    def search_ingredients(self, query, limit=20):
        """搜索食材"""
        if not query:
            return []
        query_lower = query.lower()
        results = []
        for item in self.parsed_data:
            if query_lower in item['name'].lower():
                results.append(item)
            if len(results) >= limit:
                break
        return results
    
    def get_categories(self):
        """获取所有类别"""
        return sorted(set(item['category'] for item in self.parsed_data))
    
    def get_ingredients_by_category(self, category):
        """根据类别获取食材"""
        return [item for item in self.parsed_data if item['category'] == category]
    
    def consonance_pairing(self, ingredient_name, top_n=10, exclude_categories=None, blacklist=None):
        """同味型叠加配对（Consonance）"""
        target = self.get_ingredient_by_name(ingredient_name)
        if not target:
            return []
        
        exclude_categories = exclude_categories or []
        blacklist = blacklist or []
        target_flavors = target['flavor_set']
        
        results = []
        for item in self.parsed_data:
            if item['id'] == target['id']:
                continue
            if item['category'] in exclude_categories:
                continue
            if item['name'] in blacklist:
                continue
            
            common_flavors = target_flavors & item['flavor_set']
            if len(common_flavors) > 0:
                union_flavors = target_flavors | item['flavor_set']
                jaccard = len(common_flavors) / len(union_flavors)
                score = jaccard * 100 + len(common_flavors) * 0.5
                
                results.append({
                    'ingredient': item,
                    'common_flavors': common_flavors,
                    'common_count': len(common_flavors),
                    'jaccard': jaccard,
                    'score': score
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]
    
    def contrast_pairing(self, ingredient_name, top_n=10, prefer_categories=None, blacklist=None):
        """对比味型配对（Contrast）"""
        target = self.get_ingredient_by_name(ingredient_name)
        if not target:
            return []
        
        prefer_categories = prefer_categories or []
        blacklist = blacklist or []
        target_flavors = target['flavor_set']
        target_category = target['category']
        
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
            if item['id'] == target['id']:
                continue
            if item['name'] in blacklist:
                continue
            
            item_flavors = item['flavor_set']
            
            contrast_score = 0
            for target_flavor in target_flavors:
                if target_flavor in contrast_mapping:
                    for contrast_flavor in contrast_mapping[target_flavor]:
                        if contrast_flavor in item_flavors:
                            contrast_score += 2
            
            category_bonus = 0
            if item['category'] != target_category:
                category_bonus = 10
            if item['category'] in prefer_categories:
                category_bonus += 15
            
            common = target_flavors & item_flavors
            intersection_bonus = 0
            if 3 <= len(common) <= 15:
                intersection_bonus = 8
            
            total_score = contrast_score + category_bonus + intersection_bonus
            
            if total_score > 0:
                results.append({
                    'ingredient': item,
                    'contrast_score': contrast_score,
                    'category_bonus': category_bonus,
                    'common_flavors': common,
                    'common_count': len(common),
                    'score': total_score
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]
    
    def explain_pairing(self, target_name, partner_name, pairing_type):
        """解释配对原理"""
        target = self.get_ingredient_by_name(target_name)
        partner = self.get_ingredient_by_name(partner_name)
        
        if not target or not partner:
            return "无法找到食材信息"
        
        common = target['flavor_set'] & partner['flavor_set']
        target_unique = target['flavor_set'] - partner['flavor_set']
        partner_unique = partner['flavor_set'] - target['flavor_set']
        
        if pairing_type == 'consonance':
            explanation = f"""
            **同味型叠加原理（Consonance）**
            
            {target['name']} 与 {partner['name']} 共享 **{len(common)}** 个风味分子标签：
            {', '.join([self.translate_flavor(f) for f in list(common)[:8]])}
            
            这种搭配基于**风味共鸣**原理——当两种食材拥有大量共同的风味化合物时，
            它们能够产生和谐、协调的味觉体验。这是经典搭配的科学基础。
            """
        else:
            explanation = f"""
            **对比味型原理（Contrast）**
            
            {target['name']} 与 {partner['name']} 形成**互补搭配**：
            
            - {target['name']} 的独特风味：{', '.join([self.translate_flavor(f) for f in list(target_unique)[:5]])}
            - {partner['name']} 的独特风味：{', '.join([self.translate_flavor(f) for f in list(partner_unique)[:5]])}
            
            这种搭配基于**风味互补**原理——不同风味特征的食材通过对比和平衡，
            创造出更丰富、更有层次的味觉体验。
            """
        
        return explanation

# ============== 初始化 ==============
@st.cache_resource
def get_lab():
    return MolecularFlavorLab('flavordb_data.csv')

try:
    lab = get_lab()
    data_loaded = True
except Exception as e:
    st.error(f"数据加载失败: {e}")
    data_loaded = False

# ============== 侧边栏 ==============
with st.sidebar:
    st.markdown("## 🧪 分子风味配对实验室")
    st.markdown("---")
    
    if data_loaded:
        st.markdown(f"**📊 数据概览**")
        st.markdown(f"- 食材总数: `{len(lab.parsed_data)}`")
        st.markdown(f"- 风味标签: `{len(lab.flavor_index)}`")
        st.markdown(f"- 食材类别: `{len(lab.get_categories())}`")
    
    st.markdown("---")
    st.markdown("### 🔍 配对模式")
    
    pairing_mode = st.radio(
        "选择配对类型:",
        ["同味型叠加 (Consonance)", "对比味型 (Contrast)"],
        help="Consonance: 寻找风味相似的食材 | Contrast: 寻找风味互补的食材"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ 设置")
    
    top_n = st.slider("显示结果数量", 5, 20, 10)
    
    # 黑名单功能
    st.markdown("### 🚫 黑名单")
    blacklist_input = st.text_area(
        "排除的食材（每行一个）:",
        placeholder="例如:\nGarlic\nOnion",
        help="这些食材将不会出现在配对结果中"
    )
    blacklist = [name.strip() for name in blacklist_input.split('\n') if name.strip()]
    
    st.markdown("---")
    st.markdown("### 📖 关于")
    st.markdown("""
    基于 **FlavorDB** 分子风味数据库，
    使用集合运算计算食材间的风味重合度，
    为您提供科学的食材配对建议。
    """)

# ============== 主页面 ==============
st.markdown('<h1 class="main-title">🧪 分子风味配对实验室</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">基于分子指纹的食材配对灵感引擎 | Powered by FlavorDB</p>', unsafe_allow_html=True)

if not data_loaded:
    st.stop()

# 搜索区域
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "🔍 搜索食材",
        placeholder="输入食材名称（如: Strawberry, Beef, Coffee...）",
        help="支持模糊搜索，输入部分名称即可"
    )

with col2:
    category_filter = st.selectbox(
        "📂 类别筛选",
        ["全部"] + lab.get_categories()
    )

# 搜索建议
if search_query:
    search_results = lab.search_ingredients(search_query, limit=10)
    
    if category_filter != "全部":
        search_results = [r for r in search_results if r['category'] == category_filter]
    
    if search_results:
        st.markdown("### 📋 搜索结果")
        
        # 使用radio选择食材
        ingredient_names = [f"{r['name']} ({r['category']})" for r in search_results]
        selected = st.radio(
            "选择食材:",
            ingredient_names,
            horizontal=True,
            label_visibility="collapsed"
        )
        
        selected_name = selected.split(' (')[0]
        selected_ingredient = lab.get_ingredient_by_name(selected_name)
        
        if selected_ingredient:
            st.markdown("---")
            
            # 显示选中食材信息
            col_info1, col_info2 = st.columns([2, 3])
            
            with col_info1:
                st.markdown(f"""
                <div class="ingredient-card">
                    <h3>🍃 {selected_ingredient['name']}</h3>
                    <span class="category-tag">{selected_ingredient['category']}</span>
                    <p style="margin-top: 1rem;">
                        <strong>风味标签数:</strong> {len(selected_ingredient['flavors'])}<br>
                        <strong>唯一风味数:</strong> {len(selected_ingredient['flavor_set'])}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_info2:
                # 显示主要风味标签
                flavor_counts = Counter(selected_ingredient['flavors'])
                top_flavors = flavor_counts.most_common(15)
                
                st.markdown("**主要风味特征:**")
                flavor_html = ""
                for flavor, count in top_flavors:
                    flavor_cn = lab.translate_flavor(flavor)
                    flavor_html += f'<span class="flavor-tag">{flavor_cn}</span>'
                st.markdown(flavor_html, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 执行配对
            is_consonance = "Consonance" in pairing_mode
            
            if is_consonance:
                results = lab.consonance_pairing(
                    selected_name, 
                    top_n=top_n,
                    blacklist=blacklist
                )
                st.markdown('<span class="pairing-type pairing-consonance">🔄 同味型叠加 Consonance</span>', unsafe_allow_html=True)
                st.markdown("""
                <div class="info-box">
                    寻找与目标食材<strong>共享最多风味分子</strong>的搭配方案。
                    这种搭配会产生和谐、协调的味觉体验。
                </div>
                """, unsafe_allow_html=True)
            else:
                results = lab.contrast_pairing(
                    selected_name,
                    top_n=top_n,
                    blacklist=blacklist
                )
                st.markdown('<span class="pairing-type pairing-contrast">⚡ 对比味型 Contrast</span>', unsafe_allow_html=True)
                st.markdown("""
                <div class="info-box" style="border-color: #e76f51; background: rgba(231,111,81,0.1);">
                    寻找与目标食材<strong>风味互补</strong>的创意搭配。
                    这种搭配通过对比和平衡创造丰富的味觉层次。
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 推荐搭配")
            
            if results:
                for i, result in enumerate(results, 1):
                    ing = result['ingredient']
                    common_list = list(result['common_flavors'])
                    common_cn = [lab.translate_flavor(f) for f in common_list[:8]]
                    
                    with st.container():
                        col_r1, col_r2 = st.columns([1, 4])
                        
                        with col_r1:
                            st.markdown(f'<span class="score-badge">#{i} 匹配度: {result["score"]:.0f}</span>', unsafe_allow_html=True)
                        
                        with col_r2:
                            st.markdown(f"""
                            <div class="ingredient-card">
                                <h4>{ing['name']} <span class="category-tag">{ing['category']}</span></h4>
                                <p><strong>共同风味 ({result['common_count']}个):</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 显示共同风味标签
                            common_html = ""
                            for flavor_cn in common_cn:
                                common_html += f'<span class="flavor-tag flavor-tag-common">{flavor_cn}</span>'
                            st.markdown(common_html, unsafe_allow_html=True)
                            
                            # 展开查看配对原理解释
                            with st.expander("🔬 查看配对原理"):
                                explanation = lab.explain_pairing(
                                    selected_name, 
                                    ing['name'],
                                    'consonance' if is_consonance else 'contrast'
                                )
                                st.markdown(explanation)
                                
                                # 生成菜谱建议按钮
                                if st.button(f"🍳 生成菜谱建议", key=f"recipe_{i}"):
                                    st.info(f"""
                                    **{selected_name} × {ing['name']} 创意菜谱**
                                    
                                    💡 **建议烹饪方式:**
                                    - 考虑两种食材的风味特征，选择能突出共同风味的烹饪方法
                                    - 建议先小批量试做，调整比例找到最佳搭配
                                    
                                    📝 **搭配要点:**
                                    - 共同风味: {', '.join(common_cn[:5])}
                                    - 注意平衡两种食材的用量比例
                                    
                                    *（完整AI菜谱功能开发中...）*
                                    """)
                        
                        st.markdown("---")
            else:
                st.warning("未找到合适的配对结果，请尝试其他食材或调整设置。")
    else:
        st.info("未找到匹配的食材，请尝试其他关键词。")

else:
    # 默认页面 - 展示热门食材
    st.markdown("### 🔥 热门食材推荐")
    
    popular_ingredients = [
        ("Strawberry", "🍓"), ("Beef", "🥩"), ("Coffee", "☕"),
        ("Chocolate", "🍫"), ("Vanilla", "🌿"), ("Tomato", "🍅"),
        ("Garlic", "🧄"), ("Lemon", "🍋"), ("Honey", "🍯"),
        ("Mint", "🌱"), ("Ginger", "🫚"), ("Cinnamon", "🪵")
    ]
    
    cols = st.columns(4)
    for i, (name, emoji) in enumerate(popular_ingredients):
        with cols[i % 4]:
            if st.button(f"{emoji} {name}", key=f"pop_{name}"):
                st.session_state['search_query'] = name
                st.rerun()
    
    st.markdown("---")
    
    # 展示数据概览
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown("""
        <div class="ingredient-card" style="text-align: center;">
            <h2>🥗</h2>
            <h3>{}</h3>
            <p>食材总数</p>
        </div>
        """.format(len(lab.parsed_data)), unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown("""
        <div class="ingredient-card" style="text-align: center;">
            <h2>🏷️</h2>
            <h3>{}</h3>
            <p>风味标签</p>
        </div>
        """.format(len(lab.flavor_index)), unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown("""
        <div class="ingredient-card" style="text-align: center;">
            <h2>📂</h2>
            <h3>{}</h3>
            <p>食材类别</p>
        </div>
        """.format(len(lab.get_categories())), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 使用说明
    st.markdown("""
    ### 📖 使用指南
    
    1. **🔍 搜索食材** - 在搜索框中输入食材名称（支持模糊搜索）
    2. **📂 筛选类别** - 使用类别筛选缩小搜索范围
    3. **🔄 选择配对模式** - 在侧边栏选择 Consonance（同味型）或 Contrast（对比味型）
    4. **🎯 查看结果** - 系统会推荐最佳搭配食材及匹配分数
    5. **🔬 查看原理** - 点击"查看配对原理"了解科学解释
    6. **🍳 生成菜谱** - 获取AI生成的创意菜谱建议
    
    ### 🧪 科学原理
    
    **同味型叠加 (Consonance)**  
    基于共享风味分子的搭配原理。当两种食材含有大量共同的风味化合物时，
    它们会产生和谐、协调的味觉体验。这是经典搭配（如番茄+罗勒）的科学基础。
    
    **对比味型 (Contrast)**  
    基于风味互补的搭配原理。不同风味特征的食材通过对比和平衡，
    创造出更丰富、更有层次的味觉体验。例如甜味与酸味的平衡。
    """)

# ============== 页脚 ==============
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧪 分子风味配对实验室 | Molecular Flavor Lab</p>
    <p style="font-size: 0.8rem;">Powered by FlavorDB | Data-driven Ingredient Pairing</p>
</div>
""", unsafe_allow_html=True)
