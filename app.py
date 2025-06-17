# -*- coding: utf-8 -*-
"""
자바 프로그래밍 성적 조회 Streamlit 웹앱
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from grades import (
    get_grades_by_class, 
    calc_score, 
    get_all_scores, 
    get_student_rank, 
    get_student_data_dict,
    get_available_classes
)

# 페이지 설정 (다크모드 지원)
st.set_page_config(
    page_title="자바 프로그래밍 성적 조회",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링 
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86C1;
        margin-bottom: 30px;
    }
    .score-container {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .success-text {
        font-size: 18px;
        font-weight: bold;
    }
    .class-info {
        background-color: #E8F4FD;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #2E86C1;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """메인 앱 함수"""
    
    # 앱 제목
    st.markdown('<h1 class="main-header">📊 자바 프로그래밍 성적 조회</h1>', 
                unsafe_allow_html=True)
    
    # 분반 선택 섹션
    available_classes = get_available_classes()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("### 🏫 분반을 선택하세요")
        selected_class = st.selectbox(
            "분반 선택",
            available_classes,
            index=0,
            help="소속 분반을 선택하세요"
        )
        
        # 선택된 분반 정보 표시
        grades_data = get_grades_by_class(selected_class)
        total_students = len(grades_data)
        
        st.markdown(f"""
        <div class="class-info">
            <strong>📚 {selected_class}</strong><br>
            <small>총 {total_students}명의 학생이 등록되어 있습니다</small>
        </div>
        """, unsafe_allow_html=True)
    
    # 입력 섹션
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("### 🔐 학번을 입력하세요")
        
        # 등록된 학번 리스트 보기 버튼
        # Expander 상태 관리
        is_expanded = st.session_state.get('expander_open', False)
        
        # Expander 토글 감지를 위한 버튼
        col_exp1, col_exp2 = st.columns([3, 1])
        with col_exp1:
            if st.button(f"📝 {selected_class} 등록된 학번 목록 {'닫기' if is_expanded else '보기'}", key=f"toggle_expander_{selected_class}"):
                st.session_state['expander_open'] = not is_expanded
                st.rerun()
        
        if is_expanded:
            with st.container():
                st.write(f"**{selected_class} 전체 학번 목록 ({len(grades_data)}명)**")
                
                # 학번 검색 기능
                search_term = st.text_input("🔍 학번 검색", placeholder="검색할 학번 입력 (예: 00)", key=f"search_{selected_class}")
                
                student_ids = list(grades_data.keys())
                
                # 검색어가 있으면 필터링
                if search_term:
                    filtered_ids = [sid for sid in student_ids if search_term in sid]
                    if filtered_ids:
                        st.write(f"**검색 결과: {len(filtered_ids)}개**")
                        student_ids = filtered_ids
                    else:
                        st.write("⚠️ 검색 결과가 없습니다.")
                        student_ids = []
                
                # 학번을 4개씩 한 줄에 표시
                if student_ids:
                    cols = st.columns(4)
                    
                    for i, student_id in enumerate(student_ids):
                        col_idx = i % 4
                        with cols[col_idx]:
                            # 클릭 가능한 버튼으로 표시
                            if st.button(f"`{student_id}`", key=f"btn_{selected_class}_{student_id}", help="클릭하면 자동으로 성적을 조회합니다"):
                                st.session_state[f'selected_student_id'] = student_id
                                st.session_state['auto_search'] = True
                                st.session_state['expander_open'] = False  # expander 닫기
                                st.rerun()
        
        # 선택된 학번이 있으면 기본값으로 설정
        default_sid = st.session_state.get(f'selected_student_id', '')
        
        sid = st.text_input(
            "학번", 
            value=default_sid,
            placeholder="예: 9243 (1분반) 또는 0066 (2분반)",
            help="4자리 학번을 입력하고 조회 버튼을 클릭하세요"
        )
        
        # 자동 검색 또는 수동 검색
        search_triggered = st.session_state.get('auto_search', False) or st.button("🔍 성적 조회", type="primary", use_container_width=True)
        
        # 자동 검색 플래그 초기화
        if st.session_state.get('auto_search', False):
            st.session_state['auto_search'] = False
        
        # 조회 로직
        if search_triggered:
            if sid and sid in grades_data:
                # 성적 데이터 가져오기
                student_scores = grades_data[sid]
                student_data = get_student_data_dict(student_scores)
                total_score = calc_score(student_scores)
                student_rank = get_student_rank(sid, selected_class)
                
                # 성공 메시지
                st.success(f"**{selected_class} | 총점: {total_score}점** | **등수: {student_rank}/{total_students}등**", 
                          icon="✅")
                
                # 상세 성적 표시
                st.write("### 📋 상세 성적표")
                
                # 상세 점수 데이터프레임 생성
                detail_data = {
                    "항목": [
                        "중간고사",
                        "중간 EXTRA", 
                        "중간고사 합계 (중간+EXTRA)",
                        "기말고사",
                        "연습과제 1",
                        "연습과제 2", 
                        "연습과제 3",
                        "연습과제 4",
                        "연습과제 5",
                        "연습과제 합계",
                        "총점"
                    ],
                    "점수": [
                        f"{student_data['mid']}점",
                        f"{student_data['mid_extra']}점",
                        f"{student_data['mid'] + student_data['mid_extra']}점",
                        f"{student_data['final']}점",
                        f"{student_data['exercises'][0]}점",
                        f"{student_data['exercises'][1]}점", 
                        f"{student_data['exercises'][2]}점",
                        f"{student_data['exercises'][3]}점",
                        f"{student_data['exercises'][4]}점",
                        f"{sum(student_data['exercises'])}점",
                        f"{total_score}점"
                    ],
                    "가중치": [
                        "-",
                        "-",
                        "33.33% (중간 전체)",
                        "44.44% (기말고사)", 
                        "-",
                        "-",
                        "-", 
                        "-",
                        "-",
                        "22.22% (연습과제 전체)",
                        "100% (출석 10% 제외)"
                    ]
                }
                
                df = pd.DataFrame(detail_data)
                
                # 스타일링된 데이터프레임 표시
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "항목": st.column_config.TextColumn("항목", width="medium"),
                        "점수": st.column_config.TextColumn("점수", width="small"), 
                        "가중치": st.column_config.TextColumn("가중치", width="medium")
                    }
                )
                
                # 전체 성적 다운로드 기능 (선택 옵션)
                st.write(f"### 📊 {selected_class} 전체 성적 현황")
                
                # 전체 성적 요약 표
                all_scores = get_all_scores(selected_class)
                all_scores_list = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
                summary_data = {
                    "등수": list(range(1, len(all_scores_list) + 1)),
                    "학번": [item[0] for item in all_scores_list],
                    "총점": [f"{item[1]}점" for item in all_scores_list]
                }
                
                summary_df = pd.DataFrame(summary_data)
                
                # 현재 학생 행 하이라이트
                def highlight_current_student(row):
                    if row['학번'] == sid:
                        return ['background-color: #FFE5B4'] * len(row)
                    return [''] * len(row)
                
                styled_df = summary_df.style.apply(highlight_current_student, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # 다운로드 버튼
                csv = summary_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label=f"📥 {selected_class} 전체 성적 CSV 다운로드",
                    data=csv,
                    file_name=f"java_programming_scores_{selected_class}.csv",
                    mime="text/csv"
                )
                
            elif sid:
                # 실패 메시지
                st.error(f"❌ {selected_class}에 존재하지 않는 학번입니다. 학번을 다시 확인해주세요.", icon="🚫")
                st.info("💡 위의 '등록된 학번 목록 보기'에서 정확한 학번을 확인하세요!", icon="ℹ️")
            else:
                st.warning("⚠️ 학번을 입력해주세요.", icon="⚠️")
    
    # 분반별 통계 정보
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("### 📈 분반별 현황")
        
        # 분반별 데이터 수집
        class1_data = get_grades_by_class("1분반")
        class1_scores = get_all_scores("1분반")
        class2_data = get_grades_by_class("2분반")
        class2_scores = get_all_scores("2분반")
        
        if class1_scores and class2_scores:
            # 1분반 통계
            class1_avg = sum(class1_scores.values()) / len(class1_scores)
            class1_max = max(class1_scores.values())
            class1_min = min(class1_scores.values())
            
            # 2분반 통계
            class2_avg = sum(class2_scores.values()) / len(class2_scores)
            class2_max = max(class2_scores.values())
            class2_min = min(class2_scores.values())
            
            # 차트 데이터 준비
            chart_data = pd.DataFrame({
                "1분반": [class1_avg, class1_max, class1_min],
                "2분반": [class2_avg, class2_max, class2_min]
            }, index=["평균 점수", "최고 점수", "최저 점수"])
            
            # Plotly를 사용한 꺾은선 차트
            fig = go.Figure()
            
            # 1분반 선 (빨간색)
            fig.add_trace(go.Scatter(
                x=chart_data.index,
                y=chart_data["1분반"],
                mode='lines+markers+text',
                name='1분반',
                line=dict(color='red', width=3),
                marker=dict(size=8),
                text=[f'{val:.1f}' for val in chart_data["1분반"]],
                textposition="bottom center",
                textfont=dict(size=12, color='red')
            ))
            
            # 2분반 선 (파란색)
            fig.add_trace(go.Scatter(
                x=chart_data.index,
                y=chart_data["2분반"],
                mode='lines+markers+text',
                name='2분반',
                line=dict(color='blue', width=3),
                marker=dict(size=8),
                text=[f'{val:.1f}' for val in chart_data["2분반"]],
                textposition="top center",
                textfont=dict(size=12, color='blue')
            ))
            
            # 차트 레이아웃 설정
            fig.update_layout(
                title="분반별 점수 비교",
                xaxis_title="항목",
                yaxis_title="점수",
                yaxis=dict(range=[-5, 105]),
                height=450,
                showlegend=True,
                margin=dict(t=80, b=80, l=60, r=60)
            )
            
            # 차트 표시
            st.plotly_chart(fig, use_container_width=True)
            
            # 차트 설명
            st.markdown("""
            <div style='text-align: center; color: #7F8C8D; margin-top: 15px;'>
                <small>📊 분반별 점수 분포 비교 차트 | 높이는 점수를 나타냅니다</small>
            </div>
            """, unsafe_allow_html=True)
    
    # 구분선
    st.markdown("---")
    
    # 푸터 정보
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #7F8C8D;'>
            <small>🔒 개인정보는 사용자의 로컬에서만 처리되며 저장되지 않습니다</small><br>
            <small>📱 모바일에서도 이용 가능합니다</small><br>
            <small>💡 분반과 학번을 정확히 선택하여 성적을 확인하세요</small>
        </div>
        """, unsafe_allow_html=True)
    
    # 저작권 및 개발자 정보
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #95A5A6; font-size: 12px;'>
        <p><strong>© 2025 오승민 (SeungMin Oh)</strong></p>
        <p>
            📧 <a href="mailto:32202688@dankook.ac.kr" style="color: #3498DB;">32202688@dankook.ac.kr</a> | 
            🐙 <a href="https://github.com/oh79" target="_blank" style="color: #3498DB;">github.com/oh79</a> | 
            🌐 <a href="https://ip-dr.vercel.app" target="_blank" style="color: #3498DB;">ip-dr.vercel.app</a>
        </p>
        <p><small>자바 프로그래밍 성적 조회 시스템 | Developed with Streamlit</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 