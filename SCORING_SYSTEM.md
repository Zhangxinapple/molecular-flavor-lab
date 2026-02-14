# 📊 分子风味配对实验室 - 评分系统说明

## 概述

本系统使用**双重评分机制**，分别对应两种不同的配对哲学：

1. **Consonance (同味型叠加)** - 寻找和谐搭配
2. **Contrast (对比味型)** - 寻找互补搭配

---

## 一、Consonance 评分系统

### 核心思想
> 共享的风味分子越多，两种食材越和谐

### 计算公式

```
总评分 = Jaccard相似度 × 100 + 共同风味数 × 0.5

其中:
- Jaccard相似度 = |A ∩ B| / |A ∪ B|
- 共同风味数 = |A ∩ B|
```

### 公式解析

| 组成部分 | 权重 | 说明 |
|----------|------|------|
| Jaccard × 100 | 主要 | 衡量风味集合的重叠比例（0-100分） |
| 共同数 × 0.5 | 辅助 | 奖励高重叠数量（每多1个+0.5分） |

### 示例计算

**案例：Strawberry vs Apple**

```
Strawberry 风味数: 280
Apple 风味数: 295
共同风味数: 224
并集风味数: 351

Jaccard = 224 / 351 = 0.638
评分 = 0.638 × 100 + 224 × 0.5
     = 63.8 + 112
     = 175.8
```

### 评分等级

| 分数范围 | 等级 | 说明 |
|----------|------|------|
| 150+ | ⭐⭐⭐⭐⭐ 极佳 | 风味高度重合，经典搭配 |
| 100-150 | ⭐⭐⭐⭐ 优秀 | 风味协调，推荐尝试 |
| 60-100 | ⭐⭐⭐ 良好 | 有一定共同风味 |
| 30-60 | ⭐⭐ 一般 | 少量共同风味 |
| <30 | ⭐ 较弱 | 风味差异较大 |

### 为什么用 Jaccard？

**优点：**
- 归一化到 0-1 范围，便于比较
- 惩罚风味差异大的食材
- 科学文献中常用的相似度指标

**对比其他指标：**

| 指标 | 公式 | 缺点 |
|------|------|------|
| 仅共同数 | \|A ∩ B\| | 大食材占便宜（如"食物"包含所有风味） |
| 余弦相似度 | A·B / (\|A\|×\|B\|) | 对集合大小不敏感 |
| **Jaccard** | \|A ∩ B\| / \|A ∪ B\| | ✅ 平衡且科学 |

---

## 二、Contrast 评分系统

### 核心思想
> 互补的风味特征能创造更丰富的味觉层次

### 计算公式

```
总评分 = 对比分 + 类别加分 + 交集加分

其中:
- 对比分 = Σ(互补风味匹配数 × 2)
- 类别加分 = 跨类别(10) + 优先类别(15)
- 交集加分 = 适度交集(3-15个) ? 8 : 0
```

### 对比风味映射表

```python
CONTRAST_MAPPING = {
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
```

### 公式解析

| 组成部分 | 权重 | 说明 |
|----------|------|------|
| 对比分 | 主要 | 互补风味匹配，每对+2分 |
| 类别加分 | 次要 | 跨类别+10，优先类别额外+15 |
| 交集加分 | 调节 | 避免完全无关或过于相似 |

### 示例计算

**案例：Strawberry vs Gruyere Cheese**

```
Strawberry 主要特征: sweet, fruity, fresh, floral
Gruyere Cheese 主要特征: fatty, creamy, salty, nutty

对比匹配:
- sweet → fatty ✓ (+2)
- sweet → salty ✓ (+2)
- fruity → nutty ✓ (+2)
- fresh → creamy ✓ (+2)
对比分 = 8

类别加分:
- 跨类别 (Fruit → Dairy) = +10
- 优先类别 (Dairy) = +15
类别分 = 25

交集加分:
- 共同风味数 = 8 (在3-15范围内)
交集分 = 8

总评分 = 8 + 25 + 8 = 41
```

### 评分等级

| 分数范围 | 等级 | 说明 |
|----------|------|------|
| 40+ | ⭐⭐⭐⭐⭐ 极佳 | 高度互补，创意搭配 |
| 30-40 | ⭐⭐⭐⭐ 优秀 | 良好互补，值得尝试 |
| 20-30 | ⭐⭐⭐ 良好 | 有一定互补性 |
| 10-20 | ⭐⭐ 一般 | 轻微互补 |
| <10 | ⭐ 较弱 | 互补性不强 |

### 为什么需要交集加分？

**问题：** 完全不相关的食材也可能得高分

**解决方案：**
- 完全无交集 → 可能不搭（排除）
- 交集太多 → 变成 Consonance（排除）
- 适度交集(3-15) → 既有联系又有差异 ✅

---

## 三、两种模式的对比

| 维度 | Consonance | Contrast |
|------|------------|----------|
| **哲学** | 和谐统一 | 对比平衡 |
| **核心指标** | 共同风味数 | 互补风味数 |
| **经典案例** | 番茄+罗勒 | 蜂蜜+柠檬 |
| **适用场景** | 安全稳健搭配 | 创意冒险搭配 |
| **分数范围** | 0-200+ | 0-50+ |
| **推荐用途** | 日常烹饪 | 创新实验 |

---

## 四、算法优化技巧

### 1. 倒排索引加速

```python
# 构建风味 → 食材索引
flavor_index = {
    'sweet': [apple, banana, ...],
    'sour': [lemon, lime, ...],
    ...
}

# 查询时只检查相关食材
candidates = set()
for flavor in target_flavors:
    candidates.update(flavor_index[flavor])
```

**效果：** 从 O(n) 降到 O(k)，k 为相关食材数

### 2. 提前过滤

```python
# 排除黑名单
if ingredient.name in blacklist:
    continue

# 排除同类别（Contrast模式）
if mode == 'contrast' and ing.category == target.category:
    category_bonus = 0  # 不加分
```

### 3. 缓存机制

```python
@functools.lru_cache(maxsize=1000)
def get_pairing_score(ingredient_a, ingredient_b, mode):
    # 缓存常用配对结果
    ...
```

---

## 五、评分调参指南

### 调整 Consonance 权重

```python
# 更看重 Jaccard 相似度
score = jaccard * 120 + common * 0.3

# 更看重共同数量
score = jaccard * 80 + common * 0.8
```

### 调整 Contrast 权重

```python
# 更看重互补性
score = contrast * 3 + category + intersection

# 更看重跨类别
score = contrast * 2 + category * 2 + intersection
```

### 添加自定义规则

```python
# 某些类别天然互补
if target.category == 'Fruit' and candidate.category == 'Dairy':
    bonus += 5

# 某些搭配经典加分
if (target.name, candidate.name) in CLASSIC_PAIRS:
    bonus += 10
```

---

## 六、常见问题

### Q1: 为什么两个模式的分数范围不同？

**A:** 两种算法的量纲不同：
- Consonance 基于 Jaccard (0-1) + 计数，自然分数较高
- Contrast 基于离散匹配，分数相对较低

建议**不要跨模式比较分数**，只在同模式内排序。

### Q2: 为什么有些奇怪的搭配分数很高？

**A:** 可能原因：
1. 数据质量问题（某些食材风味标签过多）
2. 缺乏上下文（如烹饪方式、文化偏好）
3. 需要人工审核和调参

### Q3: 如何验证评分效果？

**A:** 建议方法：
1. **专家评审** - 让厨师/美食家打分
2. **A/B 测试** - 用户选择偏好
3. **经典验证** - 已知搭配是否排在前面

---

## 七、扩展思路

### 1. 机器学习优化

```python
# 用用户反馈训练模型
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(features, user_ratings)
score = model.predict(new_pair_features)
```

### 2. 多维度评分

```python
scores = {
    'flavor': calculate_flavor_score(a, b),
    'texture': calculate_texture_score(a, b),
    'nutrition': calculate_nutrition_score(a, b),
    'culture': calculate_culture_score(a, b),
}
total = weighted_sum(scores)
```

### 3. 个性化推荐

```python
# 基于用户历史偏好
user_profile = get_user_favorite_flavors(user_id)
score = calculate_match(pair, user_profile)
```

---

## 八、总结

| 要点 | 说明 |
|------|------|
| **Consonance** | Jaccard + 共同数，找和谐搭配 |
| **Contrast** | 互补分 + 类别分 + 交集分，找创意搭配 |
| **核心优化** | 倒排索引 + 提前过滤 + 缓存 |
| **调参方向** | 根据实际效果调整权重 |
| **验证方法** | 专家 + A/B测试 + 经典验证 |

---

<p align="center">
🧪 分子风味配对实验室 | Molecular Flavor Lab<br>
<sub>科学评分，有据可依</sub>
</p>
