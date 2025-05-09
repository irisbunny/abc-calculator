import streamlit as st
import random
import math
from datetime import datetime

# 设置页面
st.set_page_config(page_title="Calculator", layout="centered")

# 自定义样式
st.markdown("""
<style>
    .stNumberInput input {border-radius: 8px;}
    .stButton>button {background-color: #4a6bdf; color: white;}
    .result-box {background: white; border-radius: 10px; padding: 15px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

# 优化后的计算函数（核心改进）
def find_abc_combinations(d, max_results=5, max_attempts=10000000):
    results = []
    attempt = 0
    
    while len(results) < max_results and attempt < max_attempts:
        b = round(random.uniform(2000, 5000), 1)
        a = round(random.uniform(1, 5), 1)
        c = round(random.uniform(0.1, 5), 1)
        
        d_candidate = a * b * c
        
        if math.floor(d_candidate * 10) / 10 == d:
            results.append({
                'a': a,
                'b': b,
                'c': c,
                'd_val': d_candidate,
                'floor': math.floor(d_candidate * 10) / 10
            })
        attempt += 1
    
    return results, attempt

# 侧边栏设置
with st.sidebar:
    st.header("⚙️ 计算设置")
    max_results = st.slider("需要的结果数量", 1, 20, 5, key='max_results')
    max_attempts = st.number_input("最大尝试次数", 1000, 10000000, 50000, step=1000)

# 主界面
st.title("🧮 Calculator")
d_value = st.number_input("目标d值", min_value=0.1, value=None, step=0.1, format="%.1f")

if st.button("🚀 开始计算"):
    if d_value is None:
        st.warning("请输入目标d值")
    else:
        with st.spinner(f'正在搜索 {max_results} 组解...'):
            start_time = datetime.now()
            results, total_attempts = find_abc_combinations(d_value, max_results, max_attempts)
            compute_time = (datetime.now() - start_time).total_seconds()
            
            if not results:
                st.error(f"未找到解 (尝试了 {total_attempts} 次)")
            else:
                st.success(f"找到 {len(results)} 组解 | 耗时 {compute_time:.2f}s)")
                
                for i, sol in enumerate(results, 1):
                    with st.expander(f"组合 {i}", expanded=True):
                        st.markdown(f"""
                        <div class="result-box">
                            <p>🔢 <b>参数</b>: a={sol['a']:.1f}, b={sol['b']:.1f}, c={sol['c']:.1f}</p>
                            <p>🧮 <b>计算值</b>: {sol['d_val']:.4f}</p>
                            <p>⌛ <b>向下取整</b>: {sol['floor']}</p>
                        </div>
                        """, unsafe_allow_html=True)
