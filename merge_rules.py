import requests
import os
import re
from datetime import datetime

# ====== 规则源列表（从你的清单中整理） ======
RULES_SOURCES = [
    # 国际基础规则
    "https://easylist-downloads.adblockplus.org/easylist.txt",
    "https://easylist-downloads.adblockplus.org/easyprivacy.txt",
    "https://www.i-dont-care-about-cookies.eu/abp/",
    # 中文区规则
    "https://easylist-downloads.adblockplus.org/easylistchina.txt",
    "https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt",
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt",
    "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt",
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    "https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt",
]

OUTPUT_FILE = "final-adblock-rules.txt"

def fetch_rule(url):
    """下载单个规则文件内容，如果失败返回None"""
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"⚠️ 下载失败: {url} - {e}")
    return None

def merge_and_deduplicate():
    all_lines = []
    print(f"🚀 开始获取规则源，共 {len(RULES_SOURCES)} 个...")
    
    for url in RULES_SOURCES:
        print(f"📥 正在拉取: {url}")
        content = fetch_rule(url)
        if content:
            # 按行拆分，过滤掉空行和注释行（以!或[开头，以及纯空行）
            lines = content.splitlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('!') and not line.startswith('['):
                    all_lines.append(line)
    
    # ====== 去重 ======
    print(f"🧹 原始规则总数: {len(all_lines)}")
    unique_lines = list(dict.fromkeys(all_lines))  # 保留顺序去重
    print(f"✅ 去重后规则总数: {len(unique_lines)}")
    
    # ====== 写入最终文件 ======
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"! 合并去重后的广告拦截规则\n")
        f.write(f"! 更新时间: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
        f.write(f"! 规则总数: {len(unique_lines)}\n")
        f.write(f"! 上游源数量: {len(RULES_SOURCES)}\n\n")
        for line in unique_lines:
            f.write(line + "\n")
    
    print(f"🎉 已生成最终规则文件: {OUTPUT_FILE}")
    print(f"📊 最终规则数: {len(unique_lines)}")

if __name__ == "__main__":
    merge_and_deduplicate()
