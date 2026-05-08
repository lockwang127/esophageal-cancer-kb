# 食管癌知识库更新日志

All notable changes to this knowledge base will be documented in this file.

## [1.0.0] - 2026-05-08

### Added
- 初始版本发布
- 4个知识域完整结构

#### 流行病学 (epidemiology.json)
- 12条知识三元组
- 覆盖发病率、死亡率、病理类型、地理分布、危险因素

#### 分子标志物 (biomarkers.json)
- 12条知识三元组
- 覆盖HER2、PD-L1、MSI、TMB及关键基因突变

#### CSCO 2024指南 (csco_2024.json)
- 12条知识三元组
- 覆盖新辅助治疗、手术指征、晚期治疗、MDT模式

#### 治疗方案 (treatment.json)
- 12条知识三元组
- 覆盖手术入路、围手术期管理、并发症预防

### Scripts
- `build_kb.py` - 知识库构建脚本
- `sync_to_github.py` - GitHub同步脚本
- `test_kb_format.py` - 格式验证测试

### Documentation
- `README.md` - 项目说明
- `UPDATE_POLICY.md` - 更新政策
- `DEPLOY.md` - 部署指南
- `domain_guide.md` - 领域指南

### Metadata
- `schemas/triplet_schema.json` - 三元组Schema定义

---

## 计划更新

### v1.1.0 (待定)
- [ ] 补充食管癌分子分型最新进展
- [ ] 增加基因检测相关内容
- [ ] 补充免疫相关不良反应处理

### v1.2.0 (待定)
- [ ] 跟踪CSCO 2025指南更新
- [ ] 增加真实世界研究数据
- [ ] 完善围手术期管理细节

### v2.0.0 (长期)
- [ ] 多语言支持（中英双语）
- [ ] 知识图谱可视化
- [ ] API接口开发
