"""
分子风味配对实验室 (Molecular Flavor Lab) - V3.0 深度汉化版
基于FlavorDB数据的食材配对灵感引擎
新增功能：完整中文搜索/显示 + 多食材组合匹配 + 评分可视化
"""

import streamlit as st
import pandas as pd
from collections import Counter
import os
from itertools import combinations

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
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e0e0e0;
    }
    .main-title {
        font-size: 2.5rem !important;
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
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .ingredient-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .flavor-tag {
        display: inline-block;
        background: rgba(0,212,255,0.15);
        color: #00d4ff;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        margin: 0.15rem;
        border: 1px solid rgba(0,212,255,0.3);
    }
    .flavor-tag-common {
        background: rgba(123,44,191,0.2);
        color: #c77dff;
        border-color: rgba(123,44,191,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============== 食材中英文映射表 ==============
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
    'fennel': '茴香', 'garlic': '大蒜', 'ginger': '姜', 'lettuce': '生菜',
    'mushroom': '蘑菇', 'onion': '洋葱', 'pea': '豌豆', 'pepper': '辣椒',
    'potato': '土豆', 'pumpkin': '南瓜', 'radish': '萝卜', 'spinach': '菠菜',
    'squash': '南瓜', 'tomato': '西红柿', 'zucchini': '西葫芦',
    'basil': '罗勒', 'bay leaf': '月桂叶', 'cinnamon': '肉桂', 'clove': '丁香',
    'coriander': '香菜籽', 'cumin': '孜然', 'dill': '莳萝', 'mint': '薄荷',
    'nutmeg': '肉豆蔻', 'oregano': '牛至', 'parsley': '欧芹', 'peppermint': '薄荷',
    'rosemary': '迷迭香', 'saffron': '藏红花', 'sage': '鼠尾草', 'thyme': '百里香',
    'turmeric': '姜黄', 'vanilla': '香草',
    'beef': '牛肉', 'chicken': '鸡肉', 'duck': '鸭肉', 'lamb': '羊肉',
    'pork': '猪肉', 'turkey': '火鸡肉', 'veal': '小牛肉', 'venison': '鹿肉',
    'bacon': '培根', 'ham': '火腿', 'sausage': '香肠',
    'anchovy': '凤尾鱼', 'clam': '蛤蜊', 'cod': '鳕鱼', 'crab': '蟹',
    'lobster': '龙虾', 'mackerel': '鲭鱼', 'mussel': '青口', 'octopus': '章鱼',
    'oyster': '生蚝', 'salmon': '三文鱼', 'sardine': '沙丁鱼', 'scallop': '扇贝',
    'shrimp': '虾', 'squid': '鱿鱼', 'tuna': '金枪鱼',
    'blue cheese': '蓝纹奶酪', 'butter': '黄油', 'cheese': '奶酪', 'cream': '奶油',
    'feta': '菲达奶酪', 'milk': '牛奶', 'mozzarella': '马苏里拉奶酪',
    'parmesan': '帕尔马干酪', 'yogurt': '酸奶',
    'bread': '面包', 'croissant': '牛角包',
    'almond': '杏仁', 'cashew': '腰果', 'chestnut': '栗子', 'coconut': '椰子',
    'hazelnut': '榛子', 'peanut': '花生', 'pistachio': '开心果', 'walnut': '核桃',
    'bean': '豆类', 'chickpea': '鹰嘴豆', 'lentil': '小扁豆', 'soybean': '大豆',
    'tofu': '豆腐',
    'beer': '啤酒', 'brandy': '白兰地', 'coffee': '咖啡', 'gin': '金酒',
    'green tea': '绿茶', 'red wine': '红酒', 'rum': '朗姆酒', 'sake': '清酒',
    'vodka': '伏特加', 'whiskey': '威士忌', 'white wine': '白葡萄酒', 'wine': '葡萄酒',
    'egg': '鸡蛋', 'honey': '蜂蜜', 'sugar': '糖', 'vinegar': '醋',
}

INGREDIENT_TRANSLATIONS_REVERSE = {v: k for k, v in INGREDIENT_TRANSLATIONS.items()}

CATEGORY_TRANSLATIONS = {
    'Fruit': '水果', 'Berry': '浆果', 'Vegetable': '蔬菜',
    'Herb': '香草', 'Spice': '香料', 'Meat': '肉类', 'Fish': '鱼类',
    'Seafood': '海鲜', 'Dairy': '乳制品', 'Bakery': '烘焙', 'Cereal': '谷物',
    'Nut': '坚果', 'Legume': '豆类', 'Beverage': '饮品',
    'Beverage Alcoholic': '酒精饮品', 'Beverage Caffeinated': '咖啡因饮品',
    'Essential Oil': '精油',
}

# ============== 核心配对类 ==============
class MolecularFlavorLab:
    def __init__(self, csv_path='flavordb_data.csv'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, csv_path)
        self.df = pd.read_csv(full_path)
        self.parsed_data = self._parse_data()
        self.name_index = self._build_name_index()
        
    def _parse_data(self):
        parsed = []
        for idx, row in self.df.iterrows():
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
    
    def calculate_pairing_score(self, ing1, ing2):
        set1 = ing1['molecule_set']
        set2 = ing2['molecule_set']
        common = set1 & set2
        common_count = len(common)
        total_count = len(set1) + len(set2)
        
        if total_count == 0:
            return 0, 0, []
        
        score = (common_count * 2) / total_count * 100
        return score, common_count, list(common)
    
    def pair_two_ingredients(self, name1, name2):
        ing1 = self.get_ingredient_by_name(name1)
        ing2 = self.get_ingredient_by_name(name2)
        
        if not ing1 or not ing2:
            return None
        
        score, common_count, common_molecules = self.calculate_pairing_score(ing1, ing2)
        
        return {
            'ingredient1': ing1,
            'ingredient2': ing2,
            'score': score,
            'common_count': common_count,
            'common_molecules': common_molecules,
        }
    
    def find_best_combinations(self, base_ingredient_name, combo_size=3, top_n=10):
        base = self.get_ingredient_by_name(base_ingredient_name)
        if not base:
            return []
        
        candidates = [item for item in self.parsed_data if item['id'] != base['id']]
        results = []
        
        for combo in combinations(candidates, combo_size - 1):
            combo_list = [base] + list(combo)
            total_score = 0
            pair_count = 0
            all_pairs = []
            
            for i in range(len(combo_list)):
                for j in range(i + 1, len(combo_list)):
                    score, common_count, _ = self.calculate_pairing_score(combo_list[i], combo_list[j])
                    total_score += score
                    pair_count += 1
                    all_pairs.append({
                        'ing1': combo_list[i],
                        'ing2': combo_list[j],
                        'score': score,
                        'common_count': common_count
                    })
            
            if pair_count > 0:
                avg_score = total_score / pair_count
                results.append({
                    'ingredients': combo_list,
                    'avg_score': avg_score,
                    'pairs': all_pairs,
                })
        
        results.sort(key=lambda x: x['avg_score'], reverse=True)
        return results[:top_n]
    
    def get_score_level(self, score):
        if score >= 70:
            return 'excellent', '绝佳'
        elif score >= 50:
            return 'good', '优秀'
        elif score >= 30:
            return 'average', '良好'
        else:
            return 'poor', '一般'

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
    
    st.markdown("---")
    st.markdown("### 🔍 配对模式")
    
    mode = st.radio(
        "选择配对模式:",
        ["双食材配对", "多食材组合 (3种)", "多食材组合 (4种)", "多食材组合 (5种)"]
    )
    
    st.markdown("---")
    st.markdown("### 📖 评分公式")
    st.markdown("`Score = (共有分子数 × 2) / (总分子数) × 100`")

# ============== 主页面 ==============
st.markdown('<h1 class="main-title">🧪 分子风味配对实验室</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">深度汉化版 | 支持中文搜索与多食材组合匹配</p>', unsafe_allow_html=True)

if not data_loaded:
    st.stop()

# ============== 双食材配对模式 ==============
if mode == "双食材配对":
    st.markdown("### 🔍 选择两种食材进行配对")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search1 = st.text_input("食材 A", placeholder="输入食材名称（如：西红柿、牛肉）")
    
    with col2:
        search2 = st.text_input("食材 B", placeholder="输入食材名称（如：鸡蛋、土豆）")
    
    ing1 = None
    if search1:
        results1 = lab.search_ingredients(search1, limit=5)
        if results1:
            options1 = [f"{r['cn_name']} ({r['name']})" for r in results1]
            selected1 = st.selectbox("选择食材 A:", options1, key="sel1")
            name1 = selected1.split("(")[1].rstrip(")")
            ing1 = lab.get_ingredient_by_name(name1)
    
    ing2 = None
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
            level, level_text = lab.get_score_level(score)
            
            score_col, info_col = st.columns([1, 2])
            
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
            
            with info_col:
                st.markdown(f"**配对详情**")
                st.markdown(f"**{ing1['cn_name']}** × **{ing2['cn_name']}**")
                st.markdown(f"共有风味分子: **{result['common_count']}** 个")
                st.markdown(f"食材A分子数: {ing1['molecule_count']} | 食材B分子数: {ing2['molecule_count']}")
            
            if result['common_molecules']:
                st.markdown("**共有风味分子:**")
                mol_html = ""
                for mol in result['common_molecules'][:20]:
                    mol_html += f'<span class="flavor-tag flavor-tag-common">{mol}</span>'
                st.markdown(mol_html, unsafe_allow_html=True)

# ============== 多食材组合模式 ==============
else:
    combo_size = int(mode.split("(")[1].split("种")[0])
    
    st.markdown(f"### 🔍 选择基础食材，寻找最佳{combo_size}食材组合")
    
    search = st.text_input("基础食材", placeholder="输入食材名称（如：西红柿、牛肉）")
    
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
        st.info(f"正在计算与 **{base_ing['cn_name']}** 的最佳{combo_size}食材组合，请稍候...")
        
        with st.spinner("计算中..."):
            combinations_result = lab.find_best_combinations(base_ing['name'], combo_size, top_n=5)
        
        if combinations_result:
            st.markdown(f"### 🎯 推荐组合（Top 5）")
            
            for i, combo in enumerate(combinations_result, 1):
                score = combo['avg_score']
                level, level_text = lab.get_score_level(score)
                
                with st.expander(f"#{i} 组合 - 平均契合度: {score:.1f} ({level_text})"):
                    ing_names = [f"{ing['cn_name']}" for ing in combo['ingredients']]
                    st.markdown(f"**食材组合:** {' + '.join(ing_names)}")
                    
                    st.markdown("**配对详情:**")
                    for pair in combo['pairs']:
                        st.markdown(f"- {pair['ing1']['cn_name']} × {pair['ing2']['cn_name']}: {pair['score']:.1f} 分 ({pair['common_count']} 个共有分子)")
                    
                    st.progress(min(score / 100, 1.0))
        else:
            st.warning("未找到合适的组合，请尝试其他食材。")

# ============== 页脚 ==============
st.markdown("---")
st.markdown("🧪 分子风味配对实验室 V3.0 | 深度汉化版")
