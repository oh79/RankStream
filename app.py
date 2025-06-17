# -*- coding: utf-8 -*-
"""
자바 프로그래밍 성적 조회 Streamlit 웹앱
"""

import streamlit as st
import pandas as pd
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
        with st.expander(f"📝 {selected_class} 등록된 학번 목록 보기"):
            st.write(f"**{selected_class} 전체 학번 목록 ({len(grades_data)}명)**")
            
            # 학번을 4개씩 한 줄에 표시
            student_ids = list(grades_data.keys())
            cols = st.columns(4)
            
            for i, student_id in enumerate(student_ids):
                col_idx = i % 4
                with cols[col_idx]:
                    st.write(f"`{student_id}`")
        
        # 선택된 학번이 있으면 기본값으로 설정
        default_sid = st.session_state.get(f'selected_student_id', '')
        
        sid = st.text_input(
            "학번", 
            value=default_sid,
            placeholder="예: 9243 (1분반) 또는 0066 (2분반)",
            help="4자리 학번을 입력하고 조회 버튼을 클릭하세요"
        )
        
        # 조회 버튼
        if st.button("🔍 성적 조회", type="primary", use_container_width=True):
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
    
    # 분반별 통계 정보
    st.markdown("---")
    st.write("### 📈 분반별 현황")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 1분반")
        class1_data = get_grades_by_class("1분반")
        class1_scores = get_all_scores("1분반")
        if class1_scores:
            avg_score = sum(class1_scores.values()) / len(class1_scores)
            max_score = max(class1_scores.values())
            min_score = min(class1_scores.values())
            
            st.metric("학생 수", len(class1_data))
            st.metric("평균 점수", f"{avg_score:.2f}점")
            st.metric("최고 점수", f"{max_score:.2f}점")
            st.metric("최저 점수", f"{min_score:.2f}점")
    
    with col2:
        st.write("#### 2분반")
        class2_data = get_grades_by_class("2분반")
        class2_scores = get_all_scores("2분반")
        if class2_scores:
            avg_score = sum(class2_scores.values()) / len(class2_scores)
            max_score = max(class2_scores.values())
            min_score = min(class2_scores.values())
            
            st.metric("학생 수", len(class2_data))
            st.metric("평균 점수", f"{avg_score:.2f}점")
            st.metric("최고 점수", f"{max_score:.2f}점")
            st.metric("최저 점수", f"{min_score:.2f}점")
    
    # 구분선 및 업데이트 안내
    st.markdown("---")
    
    # 업데이트 안내 섹션
    with st.expander("📋 성적 업데이트 방법"):
        st.markdown("""
        ### 성적 데이터 업데이트 방법
        
        1. **GitHub Repository**에서 `grades.py` 파일을 수정합니다
        2. 변경사항을 **commit & push** 합니다
        3. Streamlit Cloud에서 **자동으로 재배포**됩니다
        4. 약 1-2분 후 새로운 성적이 반영됩니다
        
        #### grades.py 수정 예시:
        ```python
        # 1분반 데이터
        grades_class1 = {
            "0066": [78, 10, 44, 10, 9, 10, 9, 7],
            "0201": [72, 10, 43, 10, 10, 10, 9, 10],
            # 추가 학생 데이터...
        }
        
        # 2분반 데이터
        grades_class2 = {
            "0000": [56, 10, 52, 10, 10, 0, 10, 10],
            "0103": [93, 10, 84, 10, 10, 10, 10, 10],
            # 추가 학생 데이터...
        }
        ```
        
        **데이터 형식**: [중간고사, 중간EXTRA, 기말고사, 연습1, 연습2, 연습3, 연습4, 연습5]
        """)
    
    # 푸터 정보
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #7F8C8D;'>
            <small>🔒 개인정보는 로컬에서만 처리되며 저장되지 않습니다</small><br>
            <small>📱 모바일에서도 이용 가능합니다</small><br>
            <small>💡 분반과 학번을 정확히 선택하여 성적을 확인하세요</small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 