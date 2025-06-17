# -*- coding: utf-8 -*-
"""
자바 프로그래밍 성적 조회 Streamlit 웹앱
"""

import streamlit as st
import pandas as pd
from grades import grades, calc_score, get_all_scores, get_student_rank, get_student_data_dict

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
</style>
""", unsafe_allow_html=True)

def main():
    """메인 앱 함수"""
    
    # 앱 제목
    st.markdown('<h1 class="main-header">📊 자바 프로그래밍 성적 조회</h1>', 
                unsafe_allow_html=True)
    
    # 모든 학생의 총점과 등수를 미리 계산
    all_scores = get_all_scores()
    total_students = len(all_scores)
    
    # 입력 섹션
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("### 🔐 학번을 입력하세요")
        sid = st.text_input(
            "학번", 
            type="password",
            placeholder="예: 9243",
            help="4자리 학번을 입력하고 조회 버튼을 클릭하세요"
        )
        
        # 조회 버튼
        if st.button("🔍 성적 조회", type="primary", use_container_width=True):
            if sid and sid in grades:
                # 성적 데이터 가져오기
                student_scores = grades[sid]
                student_data = get_student_data_dict(student_scores)
                total_score = calc_score(student_scores)
                student_rank = get_student_rank(sid)
                
                # 성공 메시지
                st.success(f"**총점: {total_score}점** | **등수: {student_rank}/{total_students}등**", 
                          icon="✅")
                
                # 상세 성적 표시
                st.write("### 📋 상세 성적표")
                
                # 상세 점수 데이터프레임 생성
                detail_data = {
                    "항목": [
                        "중간고사",
                        "중간 EXTRA", 
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
                        "3/11 (27.3%)",
                        "3/11 (27.3%)",
                        "4/10 (40%)", 
                        "-",
                        "-",
                        "-", 
                        "-",
                        "-",
                        "2/5 (40%)",
                        "100%"
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
                st.write("### 📊 전체 성적 현황")
                
                # 전체 성적 요약 표
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
                    label="📥 전체 성적 CSV 다운로드",
                    data=csv,
                    file_name="java_programming_scores.csv",
                    mime="text/csv"
                )
                
            elif sid:
                # 실패 메시지
                st.error("❌ 존재하지 않는 학번입니다. 학번을 다시 확인해주세요.", icon="🚫")
                
                # 등록된 학번 예시 표시 (디버깅용 - 실제 배포시 제거 가능)
                with st.expander("📝 참고: 등록된 학번 예시"):
                    sample_ids = list(grades.keys())[:10]  # 처음 10개만 표시
                    st.write("등록된 학번 예시:", ", ".join(sample_ids), "...")
                    st.write(f"총 {len(grades)}명의 학생이 등록되어 있습니다.")
            else:
                st.warning("⚠️ 학번을 입력해주세요.", icon="⚠️")
    
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
        grades = {
            "0000": [56, 10, 52, 10, 10, 0, 10, 10],
            "9243": [58, 10, 47, 10, 10, 10, 10, 10],
            # 추가 학생 데이터...
        }
        ```
        
        **데이터 형식**: [중간고사, 중간EXTRA, 기말고사, 연습과제1, 연습과제2, 연습과제3, 연습과제4, 연습과제5]
        """)
    
    # 푸터 정보
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #7F8C8D;'>
            <small>🔒 개인정보는 로컬에서만 처리되며 저장되지 않습니다</small><br>
            <small>📱 모바일에서도 이용 가능합니다</small><br>
            <small>💡 학번을 기억하여 언제든 성적을 확인하세요</small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 