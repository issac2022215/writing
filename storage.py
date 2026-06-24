"""
本地历史存储模块
使用 SQLite 保存和检索生成的文案记录，数据库文件在项目根目录
"""

import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.db')


def _get_conn():
    """获取数据库连接，首次调用自动建表"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            titles TEXT NOT NULL,
            content TEXT NOT NULL,
            style TEXT DEFAULT '',
            word_count TEXT DEFAULT '',
            emoji_level TEXT DEFAULT '',
            model_name TEXT DEFAULT '',
            is_favorite INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_keyword ON history(keyword)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON history(created_at)')
    conn.commit()
    return conn


def save(keyword, titles, content, style='', word_count='', emoji_level='', model_name=''):
    """保存一条文案记录

    Args:
        keyword: 输入的关键词
        titles: 标题列表，如 ['标题1', '标题2', '标题3']
        content: 正文内容（markdown 格式）
        style: 生成时的风格参数
        word_count: 生成时的字数参数
        emoji_level: 生成时的 emoji 浓度参数
        model_name: 使用的模型名称

    Returns:
        int: 新记录的 id
    """
    conn = _get_conn()
    cursor = conn.execute(
        'INSERT INTO history (keyword, titles, content, style, word_count, emoji_level, model_name) '
        'VALUES (?, ?, ?, ?, ?, ?, ?)',
        (keyword, json.dumps(titles, ensure_ascii=False), content,
         style, word_count, emoji_level, model_name)
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def search(keyword='', limit=50):
    """搜索历史记录

    Args:
        keyword: 搜索关键词（模糊匹配），为空时返回全部
        limit: 最大返回条数

    Returns:
        list[dict]: 记录列表，按收藏优先+时间倒序排列
    """
    conn = _get_conn()
    if keyword.strip():
        rows = conn.execute(
            'SELECT * FROM history WHERE keyword LIKE ? '
            'ORDER BY is_favorite DESC, created_at DESC LIMIT ?',
            (f'%{keyword.strip()}%', limit)
        ).fetchall()
    else:
        rows = conn.execute(
            'SELECT * FROM history ORDER BY is_favorite DESC, created_at DESC LIMIT ?',
            (limit,)
        ).fetchall()
    conn.close()
    result = [dict(row) for row in rows]
    for item in result:
        item['titles'] = json.loads(item['titles'])
    return result


def get_by_id(row_id):
    """按 ID 获取单条记录

    Args:
        row_id: 记录 ID

    Returns:
        dict | None: 找到返回字典，不存在返回 None
    """
    conn = _get_conn()
    row = conn.execute('SELECT * FROM history WHERE id = ?', (row_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    result = dict(row)
    result['titles'] = json.loads(result['titles'])
    return result


def delete(row_id):
    """删除一条记录

    Args:
        row_id: 记录 ID
    """
    conn = _get_conn()
    conn.execute('DELETE FROM history WHERE id = ?', (row_id,))
    conn.commit()
    conn.close()


def toggle_favorite(row_id):
    """切换收藏状态（收藏↔取消收藏）

    Args:
        row_id: 记录 ID
    """
    conn = _get_conn()
    conn.execute(
        'UPDATE history SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END '
        'WHERE id = ?', (row_id,)
    )
    conn.commit()
    conn.close()
