import streamlit as st
import pandas as pd
from data_manager import DataManager

# 初始化数据管理器
@st.cache_resource
def get_data_manager():
    return DataManager()

def main():
    st.set_page_config(
        page_title="选手评分排名系统",
        page_icon="🏆",
        layout="wide"
    )
    
    # 初始化session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'
    
    data_manager = get_data_manager()
    
    # 主界面
    if st.session_state.current_page == 'main':
        show_main_menu()
    elif st.session_state.current_page == 'contestant_input':
        show_contestant_input(data_manager)
    elif st.session_state.current_page == 'score_input':
        show_score_input(data_manager)
    elif st.session_state.current_page == 'contestant_scores':
        show_contestant_scores(data_manager)
    elif st.session_state.current_page == 'rankings':
        show_rankings(data_manager)

def show_main_menu():
    """显示主菜单"""
    st.title("🏆 选手评分排名系统")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 请选择功能模块")
        st.markdown("")
        
        if st.button("1️⃣ 选手信息录入", use_container_width=True, key="btn_1"):
            st.session_state.current_page = 'contestant_input'
            st.rerun()
            
        if st.button("2️⃣ 评委分数录入", use_container_width=True, key="btn_2"):
            st.session_state.current_page = 'score_input'
            st.rerun()
            
        if st.button("3️⃣ 选手得分", use_container_width=True, key="btn_3"):
            st.session_state.current_page = 'contestant_scores'
            st.rerun()
            
        if st.button("4️⃣ 选手排名", use_container_width=True, key="btn_4"):
            st.session_state.current_page = 'rankings'
            st.rerun()
            
        st.markdown("")
        if st.button("5️⃣ 结束程序", use_container_width=True, key="btn_5", type="secondary"):
            st.success("感谢使用选手评分排名系统！")
            st.balloons()

def show_contestant_input(data_manager):
    """选手信息录入界面"""
    st.title("1️⃣ 选手信息录入")
    
    # 返回按钮
    if st.button("← 返回主菜单", key="back_1"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.markdown("---")
    
    # 加载现有选手数据
    contestants = data_manager.load_contestants()
    
    # 显示现有选手
    if contestants:
        st.subheader("📋 现有选手信息")
        df = pd.DataFrame(contestants)
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
    
    # 添加新选手
    st.subheader("➕ 添加新选手")
    
    with st.form("add_contestant"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("选手姓名", placeholder="请输入选手姓名")
        
        with col2:
            phone = st.text_input("联系电话", placeholder="请输入联系电话")
        
        submitted = st.form_submit_button("添加选手", use_container_width=True)
        
        if submitted:
            if name and phone:
                # 生成新的ID
                new_id = len(contestants) + 1 if contestants else 1
                
                # 检查是否已存在相同姓名或电话
                existing_names = [c['name'] for c in contestants]
                existing_phones = [c['phone'] for c in contestants]
                
                if name in existing_names:
                    st.error("该选手姓名已存在！")
                elif phone in existing_phones:
                    st.error("该联系电话已存在！")
                else:
                    new_contestant = {
                        'id': new_id,
                        'name': name,
                        'phone': phone
                    }
                    contestants.append(new_contestant)
                    
                    if data_manager.save_contestants(contestants):
                        st.success(f"选手 {name} 添加成功！")
                        st.rerun()
                    else:
                        st.error("保存失败，请重试！")
            else:
                st.error("请填写完整的选手信息！")

def show_score_input(data_manager):
    """评委分数录入界面"""
    st.title("2️⃣ 评委分数录入")
    
    # 返回按钮
    if st.button("← 返回主菜单", key="back_2"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.markdown("---")
    
    contestants = data_manager.load_contestants()
    scores_data = data_manager.load_scores()
    
    if not contestants:
        st.warning("请先录入选手信息！")
        return
    
    # 选择选手
    st.subheader("👤 选择选手")
    contestant_options = {f"{c['name']} (ID: {c['id']})": c['id'] for c in contestants}
    selected_contestant = st.selectbox("请选择要录入分数的选手", options=list(contestant_options.keys()))
    
    if selected_contestant:
        contestant_id = contestant_options[selected_contestant]
        contestant_name = selected_contestant.split(' (ID:')[0]
        
        st.markdown("---")
        st.subheader(f"🎯 为选手 {contestant_name} 录入评委分数")
        
        # 显示当前分数（如果有）
        current_scores = scores_data.get(str(contestant_id), [])
        
        with st.form(f"score_input_{contestant_id}"):
            st.markdown("请输入10位评委的分数（0-100分）：")
            
            cols = st.columns(5)
            scores = []
            
            for i in range(10):
                with cols[i % 5]:
                    default_value = current_scores[i] if i < len(current_scores) else 0.0
                    score = st.number_input(
                        f"评委{i+1}", 
                        min_value=0.0, 
                        max_value=100.0, 
                        value=float(default_value),
                        step=0.1,
                        key=f"score_{contestant_id}_{i}"
                    )
                    scores.append(score)
            
            submitted = st.form_submit_button("保存分数", use_container_width=True)
            
            if submitted:
                scores_data[str(contestant_id)] = scores
                if data_manager.save_scores(scores_data):
                    st.success(f"选手 {contestant_name} 的分数保存成功！")
                    
                    # 显示分数统计
                    st.markdown("### 📊 分数统计")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("最高分", f"{max(scores):.1f}")
                    with col2:
                        st.metric("最低分", f"{min(scores):.1f}")
                    with col3:
                        st.metric("平均分", f"{sum(scores)/len(scores):.1f}")
                    with col4:
                        final_score = data_manager.calculate_final_score(scores)
                        st.metric("最终得分", f"{final_score:.1f}")
                else:
                    st.error("保存失败，请重试！")

def show_contestant_scores(data_manager):
    """选手得分界面"""
    st.title("3️⃣ 选手得分")
    
    # 返回按钮
    if st.button("← 返回主菜单", key="back_3"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.markdown("---")
    
    contestants = data_manager.load_contestants()
    scores_data = data_manager.load_scores()
    
    if not contestants:
        st.warning("请先录入选手信息！")
        return
    
    if not scores_data:
        st.warning("请先录入评委分数！")
        return
    
    st.subheader("🎯 选手得分详情")
    st.markdown("*计算方法：去掉最高分和最低分后的平均分*")
    
    for contestant in contestants:
        contestant_id = str(contestant['id'])
        if contestant_id in scores_data:
            scores = scores_data[contestant_id]
            
            with st.expander(f"🏃‍♂️ {contestant['name']} (ID: {contestant['id']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**各评委分数：**")
                    score_cols = st.columns(5)
                    for i, score in enumerate(scores):
                        with score_cols[i % 5]:
                            st.metric(f"评委{i+1}", f"{score:.1f}")
                
                with col2:
                    st.markdown("**统计信息：**")
                    st.metric("最高分", f"{max(scores):.1f}")
                    st.metric("最低分", f"{min(scores):.1f}")
                    final_score = data_manager.calculate_final_score(scores)
                    st.metric("**最终得分**", f"{final_score:.1f}")
        else:
            with st.expander(f"🏃‍♂️ {contestant['name']} (ID: {contestant['id']})"):
                st.warning("该选手尚未录入分数")

def show_rankings(data_manager):
    """选手排名界面"""
    st.title("4️⃣ 选手排名")
    
    # 返回按钮
    if st.button("← 返回主菜单", key="back_4"):
        st.session_state.current_page = 'main'
        st.rerun()
    
    st.markdown("---")
    
    rankings = data_manager.get_rankings()
    
    if not rankings:
        st.warning("暂无排名数据，请先录入选手信息和评委分数！")
        return
    
    st.subheader("🏆 选手排名榜")
    st.markdown("*按最终得分从高到低排序*")
    
    # 创建排名表格
    ranking_data = []
    for i, contestant in enumerate(rankings):
        if contestant['scores']:  # 只显示有分数的选手
            ranking_data.append({
                '排名': i + 1,
                '选手姓名': contestant['name'],
                '选手ID': contestant['id'],
                '联系电话': contestant['phone'],
                '最终得分': f"{contestant['final_score']:.1f}",
                '最高分': f"{max(contestant['scores']):.1f}",
                '最低分': f"{min(contestant['scores']):.1f}"
            })
    
    if ranking_data:
        df = pd.DataFrame(ranking_data)
        
        # 使用颜色突出前三名
        def highlight_top3(row):
            if row['排名'] == 1:
                return ['background-color: #FFD700'] * len(row)  # 金色
            elif row['排名'] == 2:
                return ['background-color: #C0C0C0'] * len(row)  # 银色
            elif row['排名'] == 3:
                return ['background-color: #CD7F32'] * len(row)  # 铜色
            else:
                return [''] * len(row)
        
        styled_df = df.style.apply(highlight_top3, axis=1)
        st.dataframe(styled_df, use_container_width=True)
        
        # 显示获奖选手
        if len(ranking_data) >= 1:
            st.markdown("---")
            st.subheader("🎉 获奖选手")
            
            cols = st.columns(3)
            
            if len(ranking_data) >= 1:
                with cols[0]:
                    st.markdown("### 🥇 冠军")
                    st.success(f"**{ranking_data[0]['选手姓名']}**")
                    st.write(f"得分: {ranking_data[0]['最终得分']}")
            
            if len(ranking_data) >= 2:
                with cols[1]:
                    st.markdown("### 🥈 亚军")
                    st.info(f"**{ranking_data[1]['选手姓名']}**")
                    st.write(f"得分: {ranking_data[1]['最终得分']}")
            
            if len(ranking_data) >= 3:
                with cols[2]:
                    st.markdown("### 🥉 季军")
                    st.warning(f"**{ranking_data[2]['选手姓名']}**")
                    st.write(f"得分: {ranking_data[2]['最终得分']}")
    else:
        st.warning("所有选手都尚未录入分数！")

if __name__ == "__main__":
    main() 