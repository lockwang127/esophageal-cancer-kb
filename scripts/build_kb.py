#!/usr/bin/env python3
"""
食管癌知识库构建脚本
将分散的JSON知识图谱文件合并为统一的kb.json和kb_meta.json
支持原文件和literature_batch_*.json批次文件
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 路径配置
SCRIPT_DIR = Path(__file__).parent.parent
DATA_DIR = SCRIPT_DIR / "data" / "knowledge-graph"
KB_FILE = SCRIPT_DIR / "data" / "kb.json"
KB_META_FILE = SCRIPT_DIR / "data" / "kb_meta.json"

# 知识域定义
DOMAINS = {
    "epidemiology": "流行病学数据",
    "biomarkers": "分子标志物",
    "csco_2024": "CSCO 2024指南推荐",
    "treatment": "治疗方案",
    "nccn_esmo_guideline": "NCCN/ESMO指南",
    "molecular_biology_biomarkers": "分子分型与生物标志物",
    "clinical_trials": "临床试验数据",
    "real_world_evidence_prognosis": "真实世界数据与预后",
    "new_targets_drug_development": "新靶点与新药研发"
}


def load_all_triplets():
    """加载knowledge-graph目录下所有JSON文件"""
    all_triplets = []
    file_stats = {}
    
    if not DATA_DIR.exists():
        print(f"Error: 数据目录不存在: {DATA_DIR}")
        sys.exit(1)
    
    # 获取所有JSON文件
    json_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.json')])
    
    if not json_files:
        print(f"Error: 未找到JSON文件 in {DATA_DIR}")
        sys.exit(1)
    
    for filename in json_files:
        filepath = DATA_DIR / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 支持两种格式：直接数组 或 {"triplets": [...]} 格式
            if isinstance(data, list):
                triplets = data
            elif isinstance(data, dict) and "triplets" in data:
                triplets = data["triplets"]
            else:
                print(f"Warning: {filename} 格式无法识别，跳过")
                continue
            
            # 为每个三元组添加来源文件标记
            for triplet in triplets:
                triplet['source_file'] = filename
            
            all_triplets.extend(triplets)
            
            # 确定domain
            if triplets and 'domain' in triplets[0]:
                domain = triplets[0]['domain']
            else:
                # 从文件名推断domain
                domain = filename.replace('literature_batch_', '').replace('.json', '')
            
            file_stats[filename] = len(triplets)
            print(f"  加载 {filename}: {len(triplets)} 条")
            
        except json.JSONDecodeError as e:
            print(f"Error: {filename} JSON解析失败: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: 加载 {filename} 失败: {e}")
            sys.exit(1)
    
    return all_triplets, file_stats


def build_knowledge_base():
    """构建知识库"""
    print("=" * 50)
    print("食管癌知识库构建")
    print("=" * 50)
    print(f"\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"数据目录: {DATA_DIR}\n")
    
    # 加载三元组
    print("加载知识图谱文件...")
    triplets, file_stats = load_all_triplets()
    
    # 统计信息
    total_triplets = len(triplets)
    unique_domains = len(set(t['domain'] for t in triplets))
    unique_relations = len(set(t['relation'] for t in triplets))
    unique_entities = len(set([t['head'] for t in triplets] + [t['tail'] for t in triplets]))
    
    # 置信度统计
    confidences = [t['confidence'] for t in triplets]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    high_confidence = len([c for c in confidences if c >= 0.9])
    
    # 构建kb.json
    kb_data = {
        "schema_version": "1.0",
        "kb_name": "食管癌知识库",
        "kb_name_en": "Esophageal Cancer Knowledge Base",
        "description": "基于CSCO指南和临床研究的食管癌结构化知识库",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "triplets": triplets
    }
    
    # 构建kb_meta.json
    kb_meta = {
        "schema_version": "1.0",
        "kb_name": "食管癌知识库",
        "build_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "statistics": {
            "total_triplets": total_triplets,
            "domain_count": unique_domains,
            "unique_relations": unique_relations,
            "unique_entities": unique_entities,
            "avg_confidence": round(avg_confidence, 3),
            "high_confidence_count": high_confidence
        },
        "domains": {
            domain: {
                "name": DOMAINS.get(domain, domain),
                "triplet_count": len([t for t in triplets if t['domain'] == domain]),
                "description": ""
            }
            for domain in set(t['domain'] for t in triplets)
        },
        "sources": list(set(t['source'] for t in triplets)),
        "pmids": [t['pmid'] for t in triplets if t.get('pmid')]
    }
    
    # 保存文件
    with open(KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, ensure_ascii=False, indent=2)
    print(f"\n已保存: {KB_FILE}")
    
    with open(KB_META_FILE, 'w', encoding='utf-8') as f:
        json.dump(kb_meta, f, ensure_ascii=False, indent=2)
    print(f"已保存: {KB_META_FILE}")
    
    # 打印统计摘要
    print("\n" + "=" * 50)
    print("构建完成 - 统计摘要")
    print("=" * 50)
    print(f"  知识三元组总数: {total_triplets}")
    print(f"  知识域数量: {unique_domains}")
    print(f"  唯一关系数: {unique_relations}")
    print(f"  唯一实体数: {unique_entities}")
    print(f"  平均置信度: {avg_confidence:.3f}")
    print(f"  高置信度(≥0.9)条目: {high_confidence}")
    print(f"  参考文献数: {len(kb_meta['pmids'])}")
    print("=" * 50)
    
    return kb_data, kb_meta


if __name__ == "__main__":
    build_knowledge_base()
