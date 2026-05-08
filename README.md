# 食管癌知识库 (Esophageal Cancer Knowledge Base)

基于CSCO指南和临床研究的食管癌结构化知识库，采用知识三元组格式存储，支持RAG/LLM应用集成。

## 📊 知识库统计

- **知识三元组总数**: 48条
- **知识域数量**: 4个
- **知识领域**: 流行病学、分子标志物、CSCO指南、治疗方案

## 📁 目录结构

```
esophageal-cancer-kb/
├── data/
│   ├── knowledge-graph/     # 原始知识图谱文件
│   │   ├── epidemiology.json
│   │   ├── biomarkers.json
│   │   ├── csco_2024.json
│   │   └── treatment.json
│   ├── kb.json              # 构建后的知识库
│   └── kb_meta.json         # 知识库元数据
├── scripts/
│   ├── build_kb.py          # 构建脚本
│   ├── sync_to_github.py    # GitHub同步脚本
│   └── tests/
│       └── test_kb_format.py # 格式验证测试
├── schemas/
│   └── triplet_schema.json   # 知识三元组Schema
├── docs/
│   └── domain_guide.md      # 领域指南
├── README.md
├── UPDATE_POLICY.md
├── CHANGELOG.md
└── DEPLOY.md
```

## 🔬 知识域

### 1. epidemiology（流行病学）
- 2022年中国新发病例22.40万
- 死亡人数约18万
- 病死比约80%
- 病理类型：鳞癌（90%）、腺癌（少见）
- 高发地区：华北/华中地区

### 2. biomarkers（分子标志物）
- HER2阳性率：约10-30%（腺癌）
- PD-L1表达与CPS评分
- MSI状态与TMB
- 关键基因突变：TP53、NOTCH1等

### 3. csco_2024（CSCO 2024指南推荐）
- 可切除：新辅助放化疗+手术（CROSS方案）
- 中国特色：白蛋白紫杉醇+顺铂
- 不可切除：同步放化疗
- 晚期：化疗+免疫治疗（PD-1抑制剂）

### 4. treatment（治疗方案）
- 手术入路：McKeown/Ivor-Lewis/Orringer
- 颈部食管癌：喉咽全切除+游离空肠移植
- 吻合口瘘预防
- 围手术期营养支持

## 🚀 快速开始

### 构建知识库
```bash
python3 scripts/build_kb.py
```

### 验证格式
```bash
python3 scripts/tests/test_kb_format.py
```

### 同步到GitHub
```bash
python3 scripts/sync_to_github.py
```

## 📖 知识三元组格式

```json
{
  "head": "食管癌",
  "relation": "2022年中国新发病例数",
  "tail": "22.40万",
  "source": "国家癌症中心",
  "evidence": "2022年中国恶性肿瘤流行情况分析",
  "domain": "epidemiology",
  "confidence": 0.95,
  "pmid": "36942248"
}
```

## 📚 参考文献

- GLOBOCAN 2022
- 国家癌症中心恶性肿瘤登记数据
- CSCO食管癌诊疗指南2024
- NCCN Guidelines Esophageal Cancer
- CROSS研究 (NEJM 2010)
- KEYNOTE-590研究

## 👤 作者

- **lockwang127** - GitHub: [@lockwang127](https://github.com/lockwang127)

## 📄 许可证

本知识库仅供学术研究和AI应用开发使用。

## 🔄 更新政策

详见 [UPDATE_POLICY.md](UPDATE_POLICY.md)
