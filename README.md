# 📊 자바 프로그래밍 성적 조회 시스템

Streamlit으로 제작된 학생 성적 조회 웹앱입니다.

## 🚀 빠른 시작

### 로컬 실행
```bash
# 1. 저장소 클론
git clone <your-repo-url>
cd score-app

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run app.py
```

## 📁 프로젝트 구조
```
score-app/
├── app.py              # 메인 Streamlit 앱
├── grades.py          # 성적 데이터 및 계산 함수
├── requirements.txt   # Python 패키지 의존성
└── README.md         # 이 파일
```

## 🌐 Streamlit Cloud 배포 가이드

### 1. GitHub 저장소 생성
1. GitHub에서 새 저장소 생성
2. 로컬에서 코드를 push:
```bash
git init
git add .
git commit -m "Initial commit: Java programming grade checker"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Streamlit Community Cloud 배포
1. **[Streamlit Community Cloud](https://share.streamlit.io/)** 방문
2. **"New app"** 클릭
3. GitHub 저장소 연결:
   - Repository: `your-username/your-repo-name`
   - Branch: `main`
   - Main file path: `app.py`
4. **"Deploy!"** 클릭

### 3. 배포 완료
- 약 2-3분 후 앱이 배포됩니다
- URL 예시: `https://your-app-name.streamlit.app`
- 이 URL을 학생들에게 공유하세요!

## 📊 기능

### ✨ 주요 기능
- 🔐 학번을 통한 개별 성적 조회
- 📋 상세 성적표 (중간·중간EXTRA·기말·연습과제별)
- 🏆 전체 학생 대비 등수 표시
- 📥 전체 성적 CSV 다운로드
- 📱 모바일 친화적 반응형 디자인

### 📈 성적 계산 공식
```
총점 = (중간고사 * 3/11) + (중간EXTRA * 3/11) + (기말고사 * 4/10) + (연습과제합계 * 2/5)
```

## 🔧 성적 데이터 업데이트

### 방법 1: GitHub에서 직접 수정
1. GitHub 저장소의 `grades.py` 파일 열기
2. `grades` 딕셔너리 수정:
```python
grades = {
    "20240001": {
        "mid": 85,        # 중간고사
        "mid_extra": 90,  # 중간 EXTRA
        "final": 88,      # 기말고사
        "exercises": [95, 87, 92, 85, 90]  # 연습과제 5개
    },
    # 추가 학생 데이터...
}
```
3. Commit & Push
4. Streamlit Cloud에서 자동 재배포 (1-2분 소요)

### 방법 2: 로컬에서 수정 후 Push
```bash
# grades.py 파일 수정 후
git add grades.py
git commit -m "Update student grades"
git push origin main
```

## 🛠️ 사용 팁

### 무료 플랜 슬립 방지
- Streamlit Community Cloud 무료 플랜은 비활성시 슬립 모드 진입
- 해결책: [UptimeRobot](https://uptimerobot.com/) 같은 서비스로 주기적 ping

### 데이터 보안
- 학번만으로 조회 (비밀번호 역할)
- 개인정보는 로컬에서만 처리
- 서버에 데이터 저장 안함

### 모바일 최적화
- 반응형 디자인으로 모든 기기에서 사용 가능
- 터치 친화적 인터페이스

## 🎯 확장 가능한 기능

- [ ] 학기별 성적 관리
- [ ] 성적 통계 대시보드  
- [ ] 이메일 알림 기능
- [ ] 엑셀 파일 업로드 지원
- [ ] 관리자 패널

## 📞 문의사항

성적 조회에 문제가 있거나 학번이 없다면 담당 교수님께 문의하세요.

---
💡 **Tip**: 즐겨찾기에 추가하여 언제든 성적을 확인하세요! 