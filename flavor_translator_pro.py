"""
专业风味翻译引擎 - Professional Flavor Translator
基于调香师、品酒师和食品科学的专业术语体系
"""

class FlavorTranslatorPro:
    """专业风味翻译器 - 支持多层次翻译和风味家族分类"""
    
    def __init__(self):
        # 核心风味描述词典 - 按风味家族组织
        self.flavor_map = {
            # 甜味家族 Sweet Family
            "sweet": "甜", "sugary": "糖甜", "honey": "蜂蜜", "caramel": "焦糖",
            "butterscotch": "奶油糖", "toffee": "太妃糖", "molasses": "糖蜜",
            "maple": "枫糖", "burnt sugar": "焦糖", "caramellic": "焦糖味",
            
            # 花香家族 Floral Family
            "floral": "花香", "rose": "玫瑰", "jasmine": "茉莉", "violet": "紫罗兰",
            "lavender": "薰衣草", "lily": "百合", "orange flower": "橙花",
            "rose flower": "玫瑰花", "rose water": "玫瑰水", "geranium": "天竺葵",
            "carnation": "康乃馨", "hyacinth": "风信子", "honeysuckle": "金银花",
            "magnolia": "玉兰", "gardenia": "栀子", "lilac": "丁香花",
            "mimosa": "含羞草", "blossom": "花朵", "orris": "鸢尾根",
            "ylang": "依兰", "cananga": "卡南加", "narcissus": "水仙",
            "muguet": "铃兰", "peony": "牡丹", "iris": "鸢尾",
            
            # 果香家族 Fruity Family
            "fruity": "果香", "apple": "苹果", "pear": "梨", "peach": "桃",
            "apricot": "杏", "cherry": "樱桃", "plum": "李子", "prune": "西梅",
            "banana": "香蕉", "strawberry": "草莓", "raspberry": "覆盆子",
            "blackcurrant": "黑醋栗", "blueberry": "蓝莓", "cranberry": "蔓越莓",
            "grape": "葡萄", "melon": "瓜", "citrus": "柑橘", "lemon": "柠檬",
            "lime": "青柠", "orange": "橙", "grapefruit": "葡萄柚", "mandarin": "橘",
            "pineapple": "菠萝", "mango": "芒果", "papaya": "木瓜", "kiwi": "猕猴桃",
            "coconut": "椰子", "berry": "浆果", "jammy": "果酱", "overripe fruit": "过熟水果",
            "unripe fruit": "生果", "tropical": "热带水果", "rhubarb": "大黄",
            "apple skin": "苹果皮", "grape skin": "葡萄皮", "orange peel": "橙皮",
            "lemon peel": "柠檬皮", "peely": "果皮", "pulpy": "果肉",
            
            # 柑橘家族 Citrus Family  
            "citral": "柠檬醛", "bergamot": "佛手柑", "neroli": "橙花醇",
            "lemongrass": "柠檬草",
            
            # 草本香料家族 Herbal & Spicy Family
            "herbal": "草本", "herb": "香草", "green": "青草", "grassy": "草味",
            "leafy": "叶香", "leaf": "叶", "cut grass": "割草", "hay": "干草",
            "new mown hay": "新割草", "weedy": "杂草", "mossy": "苔藓",
            "moss": "苔", "earthy": "泥土", "earth": "土", "peat": "泥炭",
            
            # 香料家族 Spice Family
            "spicy": "辛辣", "spice": "香料", "pepper": "胡椒", "peppery": "胡椒味",
            "cinnamon": "肉桂", "clove": "丁香", "anise": "八角", "fennel": "茴香",
            "mint": "薄荷", "menthol": "薄荷醇", "minty": "薄荷味", "peppermint": "胡椒薄荷",
            "spearmint": "留兰香", "thyme": "百里香", "rosemary": "迷迭香",
            "tarragon": "龙蒿", "basil": "罗勒", "oregano": "牛至", "cumin": "孜然",
            "coriander": "香菜", "cardamom": "豆蔻", "ginger": "姜", "garlic": "蒜",
            "onion": "洋葱", "mustard": "芥末", "wasabi": "山葵", "horseradish": "辣根",
            "celery": "芹菜", "leek": "韭葱", "allspice": "多香果", "curry": "咖喱",
            "fenugreek": "葫芦巴", "licorice": "甘草", "camphor": "樟脑",
            "camphoraceous": "樟脑味", "mentholic": "薄荷醇", "cool": "清凉",
            "cooling": "冷凉", "hot": "热辣", "pungent": "刺激", "sharp": "尖锐",
            "wintergreen": "冬青", "eucalyptus": "桤叶", "medicinal": "药草",
            "balsamic": "香脂", "balsam": "香膏",
            
            # 木质家族 Woody Family
            "woody": "木质", "wood": "木", "cedar": "雪松", "cedarwood": "雪松木",
            "sandalwood": "檀香", "pine": "松", "resin": "树脂", "turpentine": "松节油",
            "oakmoss": "橡苔", "vetiver": "岩兰草", "patchouli": "广藿香",
            "labdanum": "岩玫瑰", "galbanum": "白松香", "storax": "苏合香",
            "benzoin": "安息香", "myrrh": "没药", "incense": "熏香",
            "bark": "树皮", "sawdust": "木屑", "pencil": "铅笔", "box tree": "黄杨",
            
            # 坚果家族 Nutty Family
            "nutty": "坚果", "nut": "坚果", "almond": "杏仁", "hazelnut": "榛子",
            "walnut": "核桃", "peanut": "花生", "peanut butter": "花生酱",
            "pistachio": "开心果", "chestnut": "栗子", "roasted nut": "烤坚果",
            "roasted nuts": "烤坚果", "nut skin": "果仁皮", "almond shell": "杏仁壳",
            
            # 烘焙家族 Roasted & Toasted Family
            "roasted": "烘烤", "roast": "烤", "toasted": "焦", "burnt": "焦糊",
            "smoky": "烟熏", "smoke": "烟", "smoked": "熏制", "tobacco": "烟草",
            "coffee": "咖啡", "cocoa": "可可", "chocolate": "巧克力",
            "malt": "麦芽", "malted": "麦芽", "malty": "麦芽味", "grain": "谷物",
            "cereal": "麦片", "bread": "面包", "bready": "面包味", "baked": "烘焙",
            "bread crust": "面包皮", "toast": "吐司", "popcorn": "爆米花",
            "corn": "玉米", "sweet corn": "甜玉米", "roast beef": "烤牛肉",
            "gravy": "肉汁", "barbecue": "烧烤",
            
            # 奶油乳制品家族 Creamy & Dairy Family
            "creamy": "奶油", "cream": "乳脂", "butter": "黄油", "buttery": "黄油味",
            "dairy": "乳制品", "milk": "牛奶", "milky": "奶香", "cheese": "奶酪",
            "cheesy": "芝士味", "yogurt": "酸奶", "cultured dairy": "发酵乳",
            "lactonic": "内酯", "fatty": "油脂", "fat": "脂肪", "oily": "油",
            "waxy": "蜡质", "tallow": "牛脂", "lard": "猪油",
            
            # 鲜味与蛋白家族 Umami & Savory Family
            "savory": "鲜味", "umami": "鲜", "meaty": "肉香", "meat": "肉",
            "beef": "牛肉", "chicken": "鸡肉", "pork": "猪肉", "bacon": "培根",
            "sausage": "香肠", "broth": "高汤", "meat broth": "肉汤", "bouillon": "清汤",
            "soup": "汤", "stock": "高汤", "mushroom": "蘑菇", "fungal": "真菌",
            "yeast": "酵母", "yeasty": "酵母味", "beany": "豆", "bean": "豆",
            "soy": "酱油", "soybean": "大豆", "miso": "味噌",
            "fish": "鱼", "fishy": "鱼腥", "shellfish": "贝类", "shrimp": "虾",
            "seafood": "海鲜", "seaweed": "海藻", "iodine": "碘",
            
            # 蔬菜家族 Vegetable Family
            "vegetable": "蔬菜", "tomato": "番茄", "cucumber": "黄瓜", "cabbage": "卷心菜",
            "cauliflower": "花菜", "broccoli": "西兰花", "lettuce": "生菜",
            "watercress": "西洋菜", "radish": "萝卜", "potato": "土豆",
            "cooked potato": "熟土豆", "bell": "甜椒", "green pepper": "青椒",
            "pea": "豌豆", "green bean": "四季豆", "asparagus": "芦笋",
            
            # 发酵与酒精家族 Fermented & Alcoholic Family
            "fermented": "发酵", "wine": "葡萄酒", "wine_like": "酒香", "winey": "酒味",
            "vinegar": "醋", "acetic": "醋酸", "acid": "酸", "acidic": "酸味",
            "sour": "酸", "tart": "酸涩", "sharp": "尖酸",
            "alcoholic": "酒精", "alcohol": "酒", "rum": "朗姆", "whiskey": "威士忌",
            "brandy": "白兰地", "cognac": "干邑", "wine-lee": "酒糟",
            "estery": "酯", "ester": "酯类", "solvent": "溶剂", "ethereal": "醚",
            "ether": "醚类", "fusel": "杂醇", "rummy": "朗姆味",
            
            # 氧化与陈化家族 Oxidative & Aged Family
            "oxidized": "氧化", "rancid": "哈败", "stale": "陈腐", "musty": "霉",
            "mouldy": "发霉", "moldy": "霉变", "mildew": "霉味",
            
            # 硫化物家族 Sulfurous Family
            "sulfur": "硫", "sulfury": "硫味", "sulfurous": "硫化", "garlic": "大蒜",
            "onion": "洋葱", "leek": "韭葱", "scallion": "葱", "alliaceous": "葱蒜",
            "cabbage": "卷心菜", "cruciferous": "十字花",
            
            # 动物与麝香家族 Animal & Musk Family
            "animal": "动物", "musk": "麝香", "civet": "灵猫香", "castoreum": "海狸香",
            "leather": "皮革", "sweat": "汗", "sweaty": "汗味",
            "fecal": "粪", "indole": "吲哚", "skatole": "粪臭素",
            "urine": "尿", "cat": "猫", "cat-urine": "猫尿",
            
            # 化学与工业家族 Chemical & Industrial Family
            "chemical": "化学", "solvent": "溶剂", "paint": "油漆", "varnish": "清漆",
            "plastic": "塑料", "rubber": "橡胶", "petroleum": "石油",
            "gasoline": "汽油", "kerosene": "煤油", "tar": "焦油",
            "asphalt": "沥青", "phenolic": "酚", "phenol": "苯酚",
            "medicinal": "医药", "medicine": "药", "medical": "药用",
            "disinfectant": "消毒剂", "hospital": "医院",
            "metallic": "金属", "metal": "金属", "iron": "铁", "copper": "铜",
            "tin": "锡", "blood": "血",
            
            # 香脂与树脂家族 Balsamic & Resinous Family
            "vanilla": "香草", "vanillin": "香兰素", "coumarin": "香豆素",
            "tonka": "零陵香豆", "heliotrope": "天芥菜", "almond": "苦杏仁",
            
            # 其他描述性术语 Descriptive Terms
            "sweet": "甜", "bitter": "苦", "salty": "咸", "umami": "鲜",
            "astringent": "涩", "dry": "干", "wet": "湿", "watery": "水",
            "juicy": "多汁", "fresh": "新鲜", "ripe": "成熟", "unripe": "未熟",
            "raw": "生", "cooked": "熟", "fried": "炸", "steamed": "蒸",
            "warm": "温暖", "hot": "热", "cold": "冷", "cooling": "冷却",
            "light": "轻", "heavy": "重", "strong": "强", "mild": "温和",
            "weak": "弱", "powerful": "强烈", "intense": "浓烈", "delicate": "精致",
            "subtle": "微妙", "complex": "复杂", "simple": "简单",
            "clean": "清洁", "dirty": "脏", "pure": "纯净", "natural": "自然",
            "artificial": "人工", "synthetic": "合成",
            "pleasant": "宜人", "unpleasant": "不快", "offensive": "难闻",
            "fragrant": "芳香", "aromatic": "芳香的", "perfumed": "香水",
            "odorless": "无味", "bland": "平淡", "neutral": "中性",
            "faint": "微弱", "very mild": "极淡", "soft": "柔和",
            
            # 质地相关 Texture-related
            "powdery": "粉状", "crystalline": "结晶", "oily": "油腻",
            "greasy": "油腻", "sticky": "粘", "smooth": "顺滑", "rough": "粗糙",
            "silky": "丝滑", "velvety": "天鹅绒", "chalky": "白垩",
            
            # 温度与触感 Temperature & Feel
            "warm": "温暖", "hot": "热", "burning": "灼热", "fiery": "火热",
            "cool": "凉爽", "cold": "冷", "icy": "冰", "freezing": "冰冻",
            "numbing": "麻", "tingling": "刺痛",
            
            # 其他常见 Other Common
            "berry": "浆果", "seed": "种子", "seedy": "籽", "nutty": "坚果",
            "ozone": "臭氧", "marine": "海洋", "aquatic": "水生",
            "green": "青", "verdant": "翠绿", "chlorophyll": "叶绿素",
            
            # 特殊术语 Special Terms
            "damascone": "大马酮", "ionone": "紫罗兰酮", "rose oxide": "氧化玫瑰",
            "linalool": "芳樟醇", "geraniol": "香叶醇", "citronellol": "香茅醇",
            "terpene": "萜烯", "pinene": "蒎烯", "limonene": "柠檬烯",
            "myrcene": "月桂烯", "caryophyllene": "石竹烯",
            "acetophenone": "苯乙酮", "cinnamyl": "肉桂醇", "benzyl": "苄基",
            "phenyl": "苯基", "methyl": "甲基", "ethyl": "乙基",
            "formyl": "甲酰", "acetyl": "乙酰",
            
            # 复杂描述 Complex Descriptors
            "roasted meat": "烤肉", "burnt almonds": "焦杏仁", "burnt sugar": "焦糖",
            "caramelized": "焦糖化", "roasted coffee": "烤咖啡",
            "fresh bread": "新鲜面包", "baked bread": "烤面包",
            "ripe fruit": "成熟水果", "dried fruit": "干果",
            "candied": "蜜饯", "preserved": "腌制", "pickled": "酸菜",
            "smoked meat": "熏肉", "grilled": "烧烤",
            "tea": "茶", "black tea": "红茶", "green tea": "绿茶",
            "herbal tea": "草本茶", "mate": "马黛茶",
            
            # 负面描述 Negative Descriptors
            "rotten": "腐烂", "putrid": "腐臭", "spoiled": "变质", "decayed": "腐败",
            "decomposed": "分解", "fermented": "发酵", "sour": "酸败",
            "off": "变质", "stale": "陈旧", "flat": "走味",
            "cardboard": "纸板", "paper": "纸", "dusty": "灰尘",
            "musty": "霉", "dank": "阴湿", "basement": "地下室",
            "soapy": "肥皂", "soap": "皂", "detergent": "洗涤剂",
            "ammonia": "氨", "ammoniacal": "氨味", "amine": "胺",
            "feet": "脚", "body odor": "体臭", "armpit": "腋下",
            "barn": "畜棚", "stable": "马厩", "manure": "粪肥",
        }
        
        # 风味家族分类
        self.flavor_families = {
            "sweet": ["sweet", "honey", "caramel", "butterscotch", "maple", "burnt sugar", "caramellic"],
            "floral": ["floral", "rose", "jasmine", "violet", "lavender", "lily", "orange flower"],
            "fruity": ["fruity", "apple", "pear", "peach", "cherry", "berry", "citrus", "tropical"],
            "herbal": ["herbal", "herb", "green", "grassy", "leafy", "mint", "thyme", "rosemary"],
            "spicy": ["spicy", "pepper", "cinnamon", "clove", "ginger", "mustard", "pungent"],
            "woody": ["woody", "wood", "cedar", "pine", "resin", "oakmoss", "sandalwood"],
            "nutty": ["nutty", "nut", "almond", "hazelnut", "walnut", "peanut"],
            "roasted": ["roasted", "toasted", "burnt", "smoky", "coffee", "cocoa", "malt"],
            "creamy": ["creamy", "cream", "butter", "dairy", "milk", "cheese", "fatty"],
            "savory": ["savory", "meaty", "meat", "umami", "mushroom", "yeast", "soy"],
            "earthy": ["earthy", "earth", "moss", "mushroom", "peat", "soil"],
            "animal": ["animal", "musk", "leather", "civet", "sweat", "indole"],
            "chemical": ["chemical", "solvent", "plastic", "rubber", "medicinal", "metallic"],
        }
        
    def translate(self, flavor_text):
        """
        翻译单个风味描述
        Args:
            flavor_text: 英文风味描述
        Returns:
            中文翻译,如果找不到则返回原文
        """
        if not flavor_text:
            return ""
        
        # 转小写并去除空格
        flavor_text = flavor_text.strip().lower()
        
        # 直接查找
        if flavor_text in self.flavor_map:
            return self.flavor_map[flavor_text]
        
        # 尝试部分匹配(针对复合词)
        for eng, chn in self.flavor_map.items():
            if eng in flavor_text or flavor_text in eng:
                return chn
        
        # 找不到就返回原文,但首字母大写
        return flavor_text.capitalize()
    
    def translate_list(self, flavor_string, separator=","):
        """
        翻译风味列表字符串
        Args:
            flavor_string: 逗号分隔的风味描述字符串
            separator: 分隔符,默认逗号
        Returns:
            翻译后的中文字符串
        """
        if not flavor_string:
            return ""
        
        # 分割、翻译、去重、重组
        flavors = [f.strip() for f in flavor_string.split(separator) if f.strip()]
        translated = [self.translate(f) for f in flavors]
        
        # 去重但保持顺序
        seen = set()
        unique_translated = []
        for t in translated:
            if t not in seen:
                seen.add(t)
                unique_translated.append(t)
        
        return ", ".join(unique_translated)
    
    def get_flavor_family(self, flavor_text):
        """
        判断风味所属的家族
        Args:
            flavor_text: 风味描述(英文)
        Returns:
            风味家族名称,如果找不到返回'other'
        """
        flavor_text = flavor_text.strip().lower()
        
        for family, keywords in self.flavor_families.items():
            if any(keyword in flavor_text for keyword in keywords):
                return family
        
        return "other"
    
    def analyze_flavor_profile(self, flavor_string):
        """
        分析风味配置文件,返回风味家族统计
        Args:
            flavor_string: 逗号分隔的风味描述字符串
        Returns:
            dict: {家族名: 出现次数}
        """
        if not flavor_string:
            return {}
        
        flavors = [f.strip() for f in flavor_string.split(",") if f.strip()]
        family_count = {}
        
        for flavor in flavors:
            family = self.get_flavor_family(flavor)
            family_count[family] = family_count.get(family, 0) + 1
        
        return family_count
    
    def get_family_name_cn(self, family_key):
        """获取风味家族的中文名称"""
        family_names_cn = {
            "sweet": "甜味系",
            "floral": "花香系",
            "fruity": "果香系",
            "herbal": "草本系",
            "spicy": "辛香系",
            "woody": "木质系",
            "nutty": "坚果系",
            "roasted": "烘焙系",
            "creamy": "乳脂系",
            "savory": "鲜味系",
            "earthy": "土壤系",
            "animal": "动物系",
            "chemical": "化工系",
            "other": "其他"
        }
        return family_names_cn.get(family_key, family_key)


# 测试代码
if __name__ == "__main__":
    translator = FlavorTranslatorPro()
    
    # 测试单词翻译
    test_flavors = ["sweet", "roasted", "floral", "fruity", "chemical", "unknown_flavor"]
    print("=== 单词翻译测试 ===")
    for flavor in test_flavors:
        print(f"{flavor} -> {translator.translate(flavor)}")
    
    # 测试列表翻译
    print("\n=== 列表翻译测试 ===")
    test_string = "sweet, roasted, floral, nutty, chemical, woody"
    print(f"原文: {test_string}")
    print(f"译文: {translator.translate_list(test_string)}")
    
    # 测试风味家族分析
    print("\n=== 风味家族分析测试 ===")
    complex_string = "sweet, honey, rose, jasmine, apple, peach, roasted, coffee, woody, chemical"
    profile = translator.analyze_flavor_profile(complex_string)
    print(f"原文: {complex_string}")
    print("风味家族分布:")
    for family, count in sorted(profile.items(), key=lambda x: x[1], reverse=True):
        print(f"  {translator.get_family_name_cn(family)}: {count}个")
