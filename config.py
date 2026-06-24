"""
配置管理模块
定义 API 端点、模型列表、生成参数选项及默认值
"""

# ── API 服务商配置 ──────────────────────────────────

OPENAI_BASE_URL = 'https://twapi.openai-hk.com/v1'
OPENAI_MODELS = ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4o', 'gpt-4.1', 'gpt-4.1-nano', 'gpt-5.1']

DEEPSEEK_BASE_URL = 'https://api.deepseek.com'
DEEPSEEK_MODELS = ['deepseek-chat', 'deep-reasoner']

# ── 生成参数选项 ────────────────────────────────────

STYLE_OPTIONS = ['幽默', '严肃', '温馨', '轻松', '真诚', '热情', '鼓励']

WORD_COUNT_OPTIONS = {
    '短': 200,
    '中': 500,
    '长': 800,
}

EMOJI_LEVEL_OPTIONS = ['少', '适中', '多']

# ── 默认值 ──────────────────────────────────────────

DEFAULT_STYLE = '轻松'
DEFAULT_WORD_COUNT = '中'
DEFAULT_EMOJI_LEVEL = '适中'
