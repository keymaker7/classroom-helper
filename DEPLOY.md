# 🚀 배포 가이드 (Deploy Guide)

## 무료로 인터넷에 배포하는 3가지 방법

---

## 방법 1: Streamlit Community Cloud (가장 추천!) ⭐⭐⭐⭐⭐

**장점:**
- 완전 무료
- 클릭 몇 번으로 배포 완료
- 자동 업데이트
- SSL 인증서 자동 제공 (https://)
- 무제한 사용자

**단계별 가이드:**

### 1단계: GitHub에 코드 올리기

1. **GitHub 계정 만들기**
   - https://github.com 접속
   - "Sign up" 클릭
   - 이메일, 비밀번호 입력
   - 이메일 인증 완료

2. **새 저장소(Repository) 만들기**
   - 로그인 후 오른쪽 상단 "+" → "New repository"
   - Repository name: `classroom-helper` 입력
   - Description: "교실 도우미 - 텍스트 읽기 & 소음 측정기"
   - **Public** 선택 (중요!)
   - "Create repository" 클릭

3. **파일 업로드**
   - "uploading an existing file" 클릭
   - 아래 파일들을 드래그 앤 드롭:
     * `app.py`
     * `requirements.txt`
     * `README.md`
   - "Commit changes" 버튼 클릭

### 2단계: Streamlit Cloud에 배포

1. **Streamlit Cloud 가입**
   - https://streamlit.io/cloud 접속
   - "Sign up" 클릭
   - "Continue with GitHub" 선택
   - GitHub 계정으로 로그인

2. **앱 배포하기**
   - 로그인 후 "New app" 버튼 클릭
   - Repository 선택: `classroom-helper`
   - Branch: `main`
   - Main file path: `app.py`
   - **"Deploy!" 버튼 클릭**

3. **기다리기**
   - 5-10분 정도 소요
   - 자동으로 앱이 빌드되고 배포됩니다

4. **완료!**
   - URL이 생성됩니다: `https://classroom-helper-[랜덤문자].streamlit.app`
   - 이 주소를 북마크하거나 공유하세요!

### 3단계: 커스텀 도메인 설정 (선택사항)

무료 도메인을 사용하거나, 자신의 도메인을 연결할 수 있습니다.

---

## 방법 2: Render (추천도: ⭐⭐⭐⭐)

**장점:**
- 무료 플랜 제공
- GitHub 연동 자동 배포
- 간단한 설정

**단점:**
- 비활성 시 앱이 슬립 모드로 전환 (첫 접속 시 로딩 시간 증가)

### 배포 단계:

1. **Render 가입**
   - https://render.com 접속
   - "Get Started" 클릭
   - GitHub 계정으로 가입

2. **새 Web Service 만들기**
   - "New" → "Web Service" 클릭
   - GitHub 저장소 선택: `classroom-helper`

3. **설정**
   ```
   Name: classroom-helper
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

4. **"Create Web Service"** 클릭

5. **완료!**
   - URL이 생성됩니다: `https://classroom-helper.onrender.com`

---

## 방법 3: Hugging Face Spaces (추천도: ⭐⭐⭐)

**장점:**
- ML/AI 커뮤니티에서 인기
- 무료 호스팅
- GPU 사용 가능 (유료)

### 배포 단계:

1. **Hugging Face 가입**
   - https://huggingface.co 접속
   - "Sign up" 클릭

2. **새 Space 만들기**
   - 프로필 → "Spaces" → "Create new Space"
   - Space name: `classroom-helper`
   - License: MIT
   - SDK: Streamlit 선택
   - "Create Space" 클릭

3. **파일 업로드**
   - "Files" 탭 → "Add file" → "Upload files"
   - `app.py`, `requirements.txt` 업로드

4. **완료!**
   - URL: `https://huggingface.co/spaces/[사용자명]/classroom-helper`

---

## 로컬에서 실행하기 (배포 안 함)

**인터넷 없이 자신의 컴퓨터에서만 사용하고 싶다면:**

### Mac/Linux:
```bash
cd /Users/jkey/Downloads/app
pip3 install -r requirements.txt
streamlit run app.py
```

### Windows:
```bash
cd C:\Users\[사용자명]\Downloads\app
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 열기

---

## 업데이트 방법

### Streamlit Cloud / Render:
1. GitHub 저장소에서 파일 수정
2. "Commit changes" 클릭
3. 자동으로 재배포됨!

### Hugging Face Spaces:
1. Space 페이지에서 직접 파일 수정
2. 저장하면 자동 재배포

---

## 문제 해결

### "앱이 로드되지 않습니다"
- 5-10분 기다려주세요 (처음 배포 시)
- 브라우저 캐시 삭제 후 새로고침

### "마이크가 작동하지 않습니다"
- HTTPS 필요 (Streamlit Cloud는 자동 제공)
- 브라우저 마이크 권한 확인

### "requirements.txt 오류"
`requirements.txt`에 버전 명시:
```
streamlit==1.39.0
pyttsx3==2.98
gTTS==2.5.4
sounddevice==0.5.1
numpy==1.26.4
pydub==0.25.1
```

### "포트 오류"
Streamlit Cloud는 자동으로 포트를 관리하므로 걱정 안 해도 됩니다.

---

## 보안 설정 (선택사항)

### 비밀번호 보호 추가:

`app.py` 상단에 추가:
```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "교실도우미2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("비밀번호", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("비밀번호", type="password", on_change=password_entered, key="password")
        st.error("비밀번호가 틀렸습니다")
        return False
    else:
        return True

if not check_password():
    st.stop()

# 여기부터 기존 코드
```

---

## 비용 안내

### 완전 무료:
- Streamlit Community Cloud (무제한 사용자)
- Hugging Face Spaces (제한적)
- Render (슬립 모드 있음)

### 유료 옵션 (더 나은 성능):
- Streamlit Cloud Pro: $20/월
- Render Plus: $7/월
- AWS/GCP/Azure: 사용량에 따라

---

## 도메인 연결 (선택사항)

### 1. 무료 도메인 얻기:
- Freenom (무료)
- Netlify (서브도메인 무료)

### 2. Streamlit Cloud에 연결:
- Settings → Custom Domain
- 도메인 입력
- DNS 설정 (안내에 따라)

---

## 추천 배포 방법 요약

| 서비스 | 난이도 | 속도 | 비용 | 추천도 |
|--------|--------|------|------|--------|
| **Streamlit Cloud** | ⭐ 쉬움 | ⚡ 빠름 | 💰 무료 | ⭐⭐⭐⭐⭐ |
| Render | ⭐⭐ 보통 | ⚡⚡ 보통 | 💰 무료 | ⭐⭐⭐⭐ |
| Hugging Face | ⭐⭐ 보통 | ⚡ 빠름 | 💰 무료 | ⭐⭐⭐ |
| 로컬 실행 | ⭐ 쉬움 | ⚡⚡⚡ 가장 빠름 | 💰 무료 | ⭐⭐⭐ |

---

## 단계별 체크리스트

### 배포 전:
- [ ] GitHub 계정 만들기
- [ ] 코드 파일 준비 (`app.py`, `requirements.txt`)
- [ ] README.md 작성

### 배포 중:
- [ ] GitHub에 저장소 생성
- [ ] 파일 업로드
- [ ] Streamlit Cloud 연결
- [ ] 배포 클릭

### 배포 후:
- [ ] URL 작동 확인
- [ ] 모든 기능 테스트
- [ ] URL 공유 및 북마크
- [ ] (선택) 커스텀 도메인 연결

---

## 🎉 완료!

이제 전 세계 어디서나 접속 가능한 웹앱이 완성되었습니다!

**다음 단계:**
1. URL을 선생님들과 공유하세요
2. 피드백을 받아 개선하세요
3. GitHub에서 버전 관리하세요

**질문이 있으시면 README.md를 참고하세요!**
