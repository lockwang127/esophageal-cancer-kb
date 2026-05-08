# 食管癌知识库部署指南

## 本地部署

### 前置要求
- Python 3.8+
- Git

### 克隆仓库
```bash
git clone https://github.com/lockwang127/esophageal-cancer-kb.git
cd esophageal-cancer-kb
```

### 构建知识库
```bash
python3 scripts/build_kb.py
```

### 验证格式
```bash
python3 scripts/tests/test_kb_format.py
```

## GitHub远程仓库创建

由于GitHub API限制，需要手动创建远程仓库：

### 步骤1：创建GitHub仓库

1. 访问 [https://github.com/new](https://github.com/new)
2. 填写仓库信息：
   - **Repository name**: `esophageal-cancer-kb`
   - **Description**: 基于CSCO指南的食管癌结构化知识库
   - **Visibility**: Public（公开）
   - **不要勾选** "Add a README file"（已有）
   - **不要勾选** "Add .gitignore"（已有）

3. 点击 "Create repository"

### 步骤2：配置本地仓库

在克隆后的目录中执行：

```bash
# 如果是首次克隆，执行：
git remote add origin git@github.com:lockwang127/esophageal-cancer-kb.git

# 或者已有origin但URL错误，执行：
git remote set-url origin git@github.com:lockwang127/esophageal-cancer-kb.git
```

### 步骤3：推送代码

```bash
# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 食管癌知识库 v1.0"

# 推送到远程
git push -u origin main
```

### 步骤4：验证

访问 `https://github.com/lockwang127/esophageal-cancer-kb` 查看仓库。

## 使用同步脚本

或者使用项目自带的同步脚本：

```bash
python3 scripts/sync_to_github.py
```

脚本会自动：
1. 初始化Git仓库（如需要）
2. 创建初始提交（如需要）
3. 提示用户创建GitHub仓库
4. 引导配置远程仓库

## 知识库文件说明

### kb.json
构建生成的主知识库文件，包含所有知识三元组。

### kb_meta.json
知识库元数据，包含统计信息和来源列表。

### 重新构建

当更新知识图谱文件后，需要重新构建：

```bash
python3 scripts/build_kb.py
git add .
git commit -m "Update: 知识库内容更新"
git push
```

## 常见问题

### Q: 推送被拒绝？
检查是否有未提交的更改，或者远程仓库已有更新的提交。

```bash
git pull origin main --rebase
git push origin main
```

### Q: 如何更新知识库？
编辑 `data/knowledge-graph/` 下的JSON文件，然后运行 `build_kb.py` 重新构建。

### Q: 如何添加新的知识域？
1. 在 `data/knowledge-graph/` 创建新JSON文件
2. 在 `scripts/build_kb.py` 中注册新域
3. 更新 `schemas/triplet_schema.json` 的domain枚举
4. 重新构建

## 联系方式

如有问题，请提交 GitHub Issue:
https://github.com/lockwang127/esophageal-cancer-kb/issues
