import requests
import pandas as pd
import time

# 1. 建立一个基础的中英文对照表（你可以根据需要在这里添加）
ZH_MAP = {
    "sweet": "甜味", "bitter": "苦味", "floral": "花香", "fruity": "果香",
    "woody": "木质香", "spicy": "辛辣", "nutty": "坚果味", "sour": "酸味",
    "roasted": "烘烤香", "earthy": "泥土味", "creamy": "奶油味", "herbal": "草本",
    "citrus": "柑橘", "bready": "面香味", "meaty": "肉香味"
}

def translate_flavors(flavor_str):
    if not flavor_str: return ""
    # 将英文描述拆开，查表翻译，再拼回去
    items = [i.strip().lower() for i in flavor_str.split(',')]
    translated = [ZH_MAP.get(item, item) for item in items] # 没查到的保留英文
    return ", ".join(translated)

def start_spider(start_id, end_id):
    results = []
    print(f"--- 任务开始：准备抓取 ID {start_id} 到 {end_id} ---")

    for i in range(start_id, end_id + 1):
        try:
            # FlavorDB2 的官方数据接口
            url = f"https://cosylab.iiitd.edu.in/flavordb2/api/entity/{i}"
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # 提取我们要的关键信息
                name_en = data.get('entity_alias_readable', 'Unknown')
                category = data.get('category_readable', 'Unknown')
                
                # 提取该食物里所有的风味分子描述
                all_molecules = data.get('molecules', [])
                flavor_list = []
                for m in all_molecules:
                    if m.get('flavor_profile'):
                        flavor_list.append(m.get('flavor_profile'))
                
                # 合并并去重风味描述
                combined_flavors = ", ".join(list(set(", ".join(flavor_list).split(", "))))
                
                # 生成中英文对照
                results.append({
                    "ID": i,
                    "名称(En)": name_en,
                    "分类": category,
                    "英文风味描述": combined_flavors,
                    "中文风味对照": translate_flavors(combined_flavors),
                    "分子数量": len(all_molecules)
                })
                print(f"成功抓取: {name_en}")
            else:
                print(f"ID {i} 无数据，跳过")
                
            # 休息 1 秒，别把人家服务器爬崩了
            time.sleep(1)
            
        except Exception as e:
            print(f"抓取 ID {i} 失败: {e}")

    # 保存结果
    df = pd.DataFrame(results)
    df.to_csv("flavordb2_new_data.csv", index=False, encoding="utf-8-sig")
    print("--- 任务完成！已生成文件：flavordb2_new_data.csv ---")

# 这里设置你想抓取的范围。FlavorDB2 大约有 2500 条数据。
# 建议先试一下 1 到 10
if __name__ == "__main__":
    start_spider(1, 10)
