"""
输入区域组件
"""

import streamlit as st


def render_input_area():
    """渲染主区域输入行，返回关键词和按钮点击状态

    Returns:
        tuple[str, bool]: (keyword, button_clicked)
    """
    st.write('## 小红书爆款文案生成器')

    col1, col2 = st.columns([4, 1])
    with col1:
        keyword = st.text_input('请输入文案关键词：', key='input_keyword')
    with col2:
        button = st.button('✨ 生成', type='primary', key='input_generate_btn')

    return keyword, button
