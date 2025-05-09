import streamlit as st
import random
import math
from datetime import datetime

# 设置页面标题和图标
st.set_page_config(
    page_title="组合计算器",
    page_icon="🧮",
    layout="centered"
)

# 自定义CSS美化界面
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stNumberInput, .stButton>button {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    .stButton>button {
        background-color: #4a6bdf;
        color: white;
        font-weight: bold;
    }
    .result-box {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 计算函数（直接使用你的原有代码）
def find_abc_combinations(d, max_attempts=1000000):
    attempts = 0
    results = []
    
    while attempts < max_attempts and len(results) < 10:
        b = round(random.uniform(2000, 5000), 1)
        a = round(random.uniform(1, 5), 1)
        c = round(random.uniform(0.1, 5), 1)
        
        d_candidate = a * b * c
        
        if math.floor(d_candidate * 10) / 10 == d:
            results.append({
                'a': f"{a:.1f}",
                'b': f"{b:.1f}",
                'c': f"{c:.1f}",
                'd_val': f"{d_candidate:.4f}",
                'floor': f"{math.floor(d_candidate * 10) / 10}"
            })
        attempts += 1
    return results

# 网页界面
st.title("🧮 组合计算器")
st.markdown("""
查找满足 **a × b × c ≈ d** 的组合，其中：
- b ∈ [2000.0, 5000.0]（一位小数）
- a, c ∈ [0.1, 5.0]（一位小数）
- 计算结果向下取整到一位小数等于目标d值
""")

# 侧边栏（可选）
with st.sidebar:
    st.header("设置")
    max_results = st.slider("最大显示结果数", 1, 20, 5)
    show_raw_data = st.checkbox("显示原始数据")

# 主界面
d_value = st.number_input(
    "请输入目标d值", 
    min_value=0.1, 
    value=23400.0, 
    step=0.1,
    format="%.1f"
)

if st.button("开始计算", help="点击查找符合条件的组合"):
    if d_value <= 0:
        st.error("d值必须大于0！")
    else:
        with st.spinner(f'正在搜索d={d_value}的组合...'):
            start_time = datetime.now()
            results = find_abc_combinations(d_value)
            compute_time = (datetime.now() - start_time).total_seconds()
            
            if not results:
                st.warning(f"未找到满足d={d_value}的组合")
            else:
                st.success(f"找到 {len(results)} 个组合 (耗时: {compute_time:.2f}s)")
                
                for i, sol in enumerate(results[:max_results], 1):
                    with st.expander(f"组合 {i}: a={sol['a']}, b={sol['b']}, c={sol['c']}"):
                        st.markdown(f"""
                        <div class="result-box">
                            <p>🔢 <b>计算式</b>: {sol['a']} × {sol['b']} × {sol['c']}</p>
                            <p>📊 <b>精确值</b>: {sol['d_val']}</p>
                            <p>⌛ <b>向下取整</b>: {sol['floor']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if show_raw_data:
                            st.json(sol)
