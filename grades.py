# -*- coding: utf-8 -*-
"""
자바 프로그래밍 성적 데이터 및 계산 함수
"""

# 성적 데이터 딕셔너리 (학번: [중간고사, 중간EXTRA, 기말고사, 연습과제1, 연습과제2, 연습과제3, 연습과제4, 연습과제5])
grades = {
    "0000": [56, 10, 52, 10, 10, 0, 10, 10],
    "0103": [93, 10, 84, 10, 10, 10, 10, 10],
    "0303": [20, 10, 14, 10, 10, 10, 10, 10],
    "0305": [32, 10, 13, 0, 9, 9, 9, 10],
    "0314": [35, 10, 34, 10, 9, 10, 10, 10],
    "0412": [14, 10, 9, 10, 10, 9, 9, 9],
    "0429": [10, 10, 6, 0, 0, 10, 9, 10],
    "0507": [3, 10, 8, 10, 10, 10, 9, 9],
    "0552": [16, 10, 36, 10, 10, 9, 10, 10],
    "0613": [25, 10, 23, 10, 10, 0, 0, 0],
    "0709": [58, 10, 39, 10, 10, 10, 9, 9],
    "0817": [43, 10, 40, 10, 10, 8, 0, 0],
    "1024": [77, 10, 51, 10, 10, 10, 6, 10],
    "1109": [67, 10, 42, 10, 10, 10, 10, 10],
    "1234": [45, 10, 43, 10, 10, 10, 9, 10],
    "1315": [60, 10, 33, 10, 10, 10, 9, 10],
    "1414": [20, 10, 21, 10, 10, 9, 10, 10],
    "1835": [52, 10, 49, 10, 10, 10, 10, 10],
    "2136": [22, 10, 23, 10, 10, 9, 9, 9],
    "2267": [21, 10, 35, 10, 10, 10, 10, 10],
    "2464": [14, 10, 18, 10, 10, 10, 9, 9],
    "2580": [50, 10, 27, 10, 0, 10, 8, 9],
    "2603": [57, 10, 73, 10, 10, 10, 10, 10],
    "3056": [64, 10, 54, 10, 10, 10, 9, 10],
    "3138": [15, 0, 18, 0, 10, 9, 0, 9],
    "3165": [50, 10, 33, 9, 10, 10, 10, 10],
    "3581": [23, 10, 37, 10, 9, 7, 10, 10],
    "3923": [11, 0, 7, 10, 8, 0, 0, 0],
    "4060": [14, 10, 3, 10, 10, 10, 10, 10],
    "5093": [37, 10, 10, 10, 10, 10, 9, 10],
    "5631": [56, 10, 50, 10, 10, 10, 10, 10],
    "6127": [15, 10, 48, 10, 10, 10, 9, 10],
    "6758": [25, 10, 42, 10, 10, 10, 8, 10],
    "8096": [9, 10, 6, 10, 10, 10, 9, 10],
    "8273": [34, 10, 46, 10, 10, 10, 10, 10],
    "9243": [58, 10, 47, 10, 10, 10, 10, 10],
}

def calc_score(student_scores):
    """
    학생의 총점을 계산하는 함수
    
    Args:
        student_scores (list): [중간고사, 중간EXTRA, 기말고사, 연습과제1, 연습과제2, 연습과제3, 연습과제4, 연습과제5]
    
    Returns:
        float: 총점 (소수점 2자리)
    
    계산 공식:
    total = mid*3/11 + extra*3/11 + final*4/10 + sum(exercises)*2/5
    """
    try:
        if len(student_scores) != 8:
            print(f"잘못된 데이터 형식: {len(student_scores)}개 요소 (8개 필요)")
            return 0.0
            
        mid = student_scores[0]           # 중간고사
        mid_extra = student_scores[1]     # 중간 EXTRA
        final = student_scores[2]         # 기말고사
        exercises = student_scores[3:8]   # 연습과제 5개
        
        # 총점 계산 (가중치 적용)
        total = (
            mid * 3/11 +              # 중간고사 (3/11)
            mid_extra * 3/11 +        # 중간 EXTRA (3/11)  
            final * 4/10 +            # 기말고사 (4/10)
            sum(exercises) * 2/5      # 연습과제 합계 (2/5)
        )
        
        return round(total, 2)
        
    except (IndexError, TypeError) as e:
        print(f"데이터 처리 중 오류 발생: {e}")
        return 0.0
    except Exception as e:
        print(f"점수 계산 중 오류 발생: {e}")
        return 0.0

def get_student_data_dict(student_scores):
    """
    리스트 형태의 성적을 딕셔너리로 변환 (UI 표시용)
    
    Args:
        student_scores (list): [중간고사, 중간EXTRA, 기말고사, 연습과제1, 연습과제2, 연습과제3, 연습과제4, 연습과제5]
    
    Returns:
        dict: 딕셔너리 형태의 성적 데이터
    """
    return {
        "mid": student_scores[0],
        "mid_extra": student_scores[1],
        "final": student_scores[2],
        "exercises": student_scores[3:8]
    }

def get_all_scores():
    """
    모든 학생의 총점을 계산하여 반환
    
    Returns:
        dict: {학번: 총점} 형태의 딕셔너리
    """
    scores = {}
    for student_id, scores_list in grades.items():
        scores[student_id] = calc_score(scores_list)
    return scores

def get_student_rank(student_id):
    """
    특정 학생의 등수를 계산
    
    Args:
        student_id (str): 학번
    
    Returns:
        int: 등수 (1부터 시작)
    """
    all_scores = get_all_scores()
    if student_id not in all_scores:
        return -1
    
    student_score = all_scores[student_id]
    # 자신보다 높은 점수의 개수 + 1이 등수
    rank = sum(1 for score in all_scores.values() if score > student_score) + 1
    return rank 