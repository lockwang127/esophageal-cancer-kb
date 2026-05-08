#!/usr/bin/env python3
"""
知识库格式验证脚本
验证kb.json是否符合Schema定义
"""

import json
import sys
from pathlib import Path

# 路径配置
KB_FILE = Path(__file__).parent.parent.parent / "data" / "kb.json"
SCHEMA_FILE = Path(__file__).parent.parent.parent / "schemas" / "triplet_schema.json"

def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_triplet(triplet, index):
    """验证单个三元组"""
    required_fields = ['head', 'relation', 'tail', 'source', 'evidence', 'domain', 'confidence']
    errors = []
    
    for field in required_fields:
        if field not in triplet:
            errors.append(f"  索引{index}: 缺少必需字段 '{field}'")
    
    if 'confidence' in triplet:
        if not isinstance(triplet['confidence'], (int, float)):
            errors.append(f"  索引{index}: confidence必须是数字")
        elif not 0 <= triplet['confidence'] <= 1:
            errors.append(f"  索引{index}: confidence必须在0-1之间")
    
    if 'domain' in triplet:
        valid_domains = ['epidemiology', 'biomarkers', 'csco_2024', 'treatment']
        if triplet['domain'] not in valid_domains:
            errors.append(f"  索引{index}: domain必须是 {valid_domains} 之一")
    
    return errors

def validate_kb_format():
    """验证知识库格式"""
    print("=" * 50)
    print("食管癌知识库格式验证")
    print("=" * 50)
    
    errors = []
    warnings = []
    
    # 检查文件存在性
    if not KB_FILE.exists():
        errors.append(f"知识库文件不存在: {KB_FILE}")
        print(f"\n错误: {errors[-1]}")
        return False, errors, warnings
    
    if not SCHEMA_FILE.exists():
        errors.append(f"Schema文件不存在: {SCHEMA_FILE}")
        print(f"\n错误: {errors[-1]}")
        return False, errors, warnings
    
    print(f"\n检查文件:")
    print(f"  知识库: {KB_FILE}")
    print(f"  Schema: {SCHEMA_FILE}")
    
    # 加载数据
    try:
        kb_data = load_json(KB_FILE)
        print(f"\n知识库加载成功")
    except json.JSONDecodeError as e:
        errors.append(f"JSON解析错误: {e}")
        print(f"\n错误: {errors[-1]}")
        return False, errors, warnings
    
    # 检查顶层结构
    required_top_fields = ['schema_version', 'kb_name', 'triplets']
    for field in required_top_fields:
        if field not in kb_data:
            errors.append(f"缺少顶层字段: '{field}'")
    
    # 检查三元组
    if 'triplets' in kb_data:
        triplets = kb_data['triplets']
        print(f"\n知识三元组数量: {len(triplets)}")
        
        if len(triplets) == 0:
            warnings.append("知识三元组列表为空")
        
        for i, triplet in enumerate(triplets):
            triplet_errors = validate_triplet(triplet, i)
            errors.extend(triplet_errors)
        
        # 统计各域
        domains = {}
        for t in triplets:
            d = t.get('domain', 'unknown')
            domains[d] = domains.get(d, 0) + 1
        
        print(f"\n各域分布:")
        for domain, count in sorted(domains.items()):
            print(f"  {domain}: {count} 条")
    
    # 打印结果
    print("\n" + "=" * 50)
    print("验证结果")
    print("=" * 50)
    
    if warnings:
        print(f"\n警告 ({len(warnings)}项):")
        for w in warnings:
            print(f"  ⚠ {w}")
    
    if errors:
        print(f"\n错误 ({len(errors)}项):")
        for e in errors:
            print(f"  ✗ {e}")
        return False, errors, warnings
    else:
        print("\n✓ 所有验证通过！")
        return True, errors, warnings

if __name__ == "__main__":
    success, errors, warnings = validate_kb_format()
    sys.exit(0 if success else 1)
