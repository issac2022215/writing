# 小红书爆款文案生成器

基于 Streamlit 的小红书爆款文案自动生成工具，接入 OpenAI 和 DeepSeek 大语言模型，输入关键词即可一键生成符合小红书风格的标题和正文。

🌐 **在线体验**：[[writingagent.streamlit.app](https://writingagent.streamlit.app/)]

## 功能特点

- 🎯 **双 API 支持** — 可在 OpenAI 和 DeepSeek 之间自由切换
- 🧠 **多模型可选** — 支持 GPT-4o、GPT-5.1、DeepSeek-Chat 等多种模型
- ⚡ **流式输出** — 文案实时逐字生成，体验流畅
- 🎛️ **参数可调** — 支持调节文案风格、字数范围、Emoji 浓度
- 📋 **历史管理** — 自动保存生成记录，支持搜索、回看和删除
- ⭐ **收藏功能** — 满意的文案可收藏置顶
- 📥 **一键下载** — 支持导出为 Markdown 文件
- 🔥 **爆款风格** — 内置小红书爆款文案创作规则，自动生成吸睛标题和正文

## API Key 获取

| 服务商 | 获取地址 | 说明 |
|--------|---------|------|
| OpenAI | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | 需注册 OpenAI 账号并充值 |
| DeepSeek | [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) | 需注册 DeepSeek 账号 |

> ⚠️ **注意**：本文默认使用的 OpenAI 接口地址为第三方代理 `https://twapi.openai-hk.com/v1`，如需使用官方地址请将 `main.py` 中的 `base_url` 修改为 `https://api.openai.com/v1`。

## 项目结构

```
XiaoHongShu/
├── main.py             # Streamlit 应用入口，UI 编排
├── config.py           # 配置管理（模型列表、参数选项）
├── prompts.py          # 提示词模板（根据参数动态组装）
├── generator.py        # LLM 流式调用封装
├── storage.py          # SQLite 本地历史存储
├── ui/
│   ├── sidebar.py      # 侧边栏组件（API配置 + 生成参数 + 历史）
│   ├── input_area.py   # 输入区域组件
│   └── result_area.py  # 结果展示 + 操作按钮
├── requirements.txt    # Python 依赖
├── history.db          # 历史记录数据库（自动生成，已 gitignore）
└── README.md           # 本文件
```

## 技术栈

- [Streamlit](https://streamlit.io/) — Web 界面框架
- [OpenAI Python SDK](https://github.com/openai/openai-python) — 大模型 API 调用
- SQLite — 本地历史数据存储（Python 标准库，无需额外安装）

## 注意事项

- API Key 仅在当前会话中使用，不会被存储或上传
- 生成效果受所选模型影响，推荐使用 GPT-4o 或 DeepSeek-Chat 获得较好结果
- 如遇到「暂时无法调用大模型」错误，请检查 API Key 和网络连接是否正常
