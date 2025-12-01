import streamlit as st
import pyttsx3
import sounddevice as sd
import numpy as np
import threading
import time
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
import base64

# 페이지 설정
st.set_page_config(
    page_title="교실 도우미",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .noise-level {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    .warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    .danger {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        padding: 1rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'noise_monitoring' not in st.session_state:
    st.session_state.noise_monitoring = False
if 'current_db' not in st.session_state:
    st.session_state.current_db = 0
if 'max_db' not in st.session_state:
    st.session_state.max_db = 0
if 'noise_history' not in st.session_state:
    st.session_state.noise_history = []

# 헤더
st.markdown('<h1 class="main-header">🎓 교실 도우미</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">텍스트 읽기 & 우리반 소음 측정기</p>', unsafe_allow_html=True)

# 탭 생성
tab1, tab2 = st.tabs(["📢 텍스트 읽어주기", "📊 우리반 소음 측정기"])

# ========== 탭 1: TTS 기능 ==========
with tab1:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 📝 텍스트를 입력하면 음성으로 읽어드립니다")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        text_input = st.text_area(
            "읽을 텍스트를 입력하세요",
            height=200,
            placeholder="예: 안녕하세요, 여러분! 오늘도 즐거운 하루 되세요!",
            key="tts_input"
        )

    with col2:
        st.markdown("### ⚙️ 설정")

        language = st.selectbox(
            "언어 선택",
            ["한국어", "영어", "일본어", "중국어", "스페인어", "프랑스어"],
            key="language"
        )

        lang_code = {
            "한국어": "ko",
            "영어": "en",
            "일본어": "ja",
            "중국어": "zh-CN",
            "스페인어": "es",
            "프랑스어": "fr"
        }

        speed = st.slider(
            "읽기 속도",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            key="speed"
        )

        pitch_adjustment = st.slider(
            "음높이 (피치)",
            min_value=-10,
            max_value=10,
            value=0,
            step=1,
            key="pitch",
            help="양수: 높은 목소리, 음수: 낮은 목소리"
        )

    st.markdown("---")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("🔊 읽기 시작", key="tts_start", use_container_width=True):
            if text_input.strip():
                with st.spinner("음성을 생성하는 중..."):
                    try:
                        # gTTS로 음성 생성
                        tts = gTTS(text=text_input, lang=lang_code[language], slow=(speed < 0.8))

                        # 메모리에 저장
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)

                        # 오디오 플레이어로 재생
                        audio_bytes = fp.read()

                        # 속도 조절을 위한 처리
                        if speed != 1.0:
                            audio = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
                            # 속도 조절
                            audio = audio._spawn(audio.raw_data, overrides={
                                "frame_rate": int(audio.frame_rate * speed)
                            })
                            audio = audio.set_frame_rate(audio.frame_rate)

                            # 다시 바이트로 변환
                            fp_out = io.BytesIO()
                            audio.export(fp_out, format="mp3")
                            audio_bytes = fp_out.getvalue()

                        st.audio(audio_bytes, format='audio/mp3')
                        st.success("✅ 재생이 완료되었습니다!")

                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
            else:
                st.warning("⚠️ 텍스트를 입력해주세요!")

    with col_btn2:
        if st.button("📥 음성 파일 다운로드", key="tts_download", use_container_width=True):
            if text_input.strip():
                try:
                    tts = gTTS(text=text_input, lang=lang_code[language], slow=(speed < 0.8))
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)

                    st.download_button(
                        label="💾 MP3 파일 저장",
                        data=fp,
                        file_name="음성파일.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")
            else:
                st.warning("⚠️ 텍스트를 입력해주세요!")

    with col_btn3:
        if st.button("🗑️ 초기화", key="tts_clear", use_container_width=True):
            st.rerun()

    # 예시 문장
    st.markdown("---")
    st.markdown("### 💡 예시 문장")
    examples = [
        "안녕하세요, 여러분! 오늘도 즐거운 하루 되세요!",
        "조용히 해주세요. 수업 시작하겠습니다.",
        "점심시간입니다. 맛있게 드세요!",
        "오늘 숙제는 수학 문제집 10페이지입니다."
    ]

    cols = st.columns(2)
    for idx, example in enumerate(examples):
        with cols[idx % 2]:
            if st.button(f"📌 {example[:20]}...", key=f"example_{idx}", use_container_width=True):
                st.session_state.tts_input = example
                st.rerun()

# ========== 탭 2: 소음 측정기 ==========
with tab2:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("### 🎤 우리 반 소음을 실시간으로 측정합니다")
    st.markdown('</div>', unsafe_allow_html=True)

    # 소음 측정 함수
    def calculate_db(audio_data):
        """오디오 데이터에서 데시벨 계산"""
        if len(audio_data) == 0:
            return 0

        # RMS (Root Mean Square) 계산
        rms = np.sqrt(np.mean(audio_data**2))

        # 데시벨 변환 (참조값 기반)
        if rms > 0:
            db = 20 * np.log10(rms) + 94  # 94는 보정값
            return max(0, min(120, db))  # 0-120 dB 범위로 제한
        return 0

    def monitor_noise():
        """소음을 지속적으로 모니터링"""
        duration = 0.5  # 0.5초마다 측정
        sample_rate = 44100

        while st.session_state.noise_monitoring:
            try:
                # 마이크로 녹음
                audio = sd.rec(int(duration * sample_rate),
                             samplerate=sample_rate,
                             channels=1,
                             dtype='float32')
                sd.wait()

                # 데시벨 계산
                db = calculate_db(audio.flatten())

                # 세션 상태 업데이트
                st.session_state.current_db = round(db, 1)
                st.session_state.max_db = max(st.session_state.max_db, st.session_state.current_db)

                # 히스토리 저장 (최근 50개)
                st.session_state.noise_history.append(st.session_state.current_db)
                if len(st.session_state.noise_history) > 50:
                    st.session_state.noise_history.pop(0)

                time.sleep(0.1)

            except Exception as e:
                st.session_state.noise_monitoring = False
                break

    # 컨트롤 버튼
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎙️ 측정 시작", key="start_monitoring", disabled=st.session_state.noise_monitoring, use_container_width=True):
            st.session_state.noise_monitoring = True
            st.session_state.max_db = 0
            st.session_state.noise_history = []

            # 백그라운드 스레드에서 모니터링 시작
            thread = threading.Thread(target=monitor_noise, daemon=True)
            thread.start()
            st.rerun()

    with col2:
        if st.button("⏸️ 측정 중지", key="stop_monitoring", disabled=not st.session_state.noise_monitoring, use_container_width=True):
            st.session_state.noise_monitoring = False
            st.rerun()

    with col3:
        if st.button("🔄 초기화", key="reset_monitoring", use_container_width=True):
            st.session_state.noise_monitoring = False
            st.session_state.current_db = 0
            st.session_state.max_db = 0
            st.session_state.noise_history = []
            st.rerun()

    st.markdown("---")

    # 현재 소음 레벨 표시
    current_db = st.session_state.current_db

    # 소음 레벨에 따른 클래스 결정
    if current_db < 50:
        level_class = "safe"
        status = "😊 조용함"
        emoji = "🟢"
    elif current_db < 70:
        level_class = "warning"
        status = "😐 보통"
        emoji = "🟡"
    else:
        level_class = "danger"
        status = "😱 시끄러움!"
        emoji = "🔴"

    st.markdown(f'<div class="noise-level {level_class}">{emoji} {current_db} dB<br><small>{status}</small></div>', unsafe_allow_html=True)

    # 통계 정보
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("현재 소음", f"{current_db} dB", delta=None)

    with col2:
        st.metric("최대 소음", f"{st.session_state.max_db} dB", delta=None)

    with col3:
        avg_db = round(np.mean(st.session_state.noise_history), 1) if st.session_state.noise_history else 0
        st.metric("평균 소음", f"{avg_db} dB", delta=None)

    # 실시간 그래프
    if st.session_state.noise_history:
        st.markdown("### 📈 실시간 소음 그래프")
        st.line_chart(st.session_state.noise_history, use_container_width=True)

    # 소음 기준 안내
    st.markdown("---")
    st.markdown("### 📖 소음 기준 안내")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🟢 **0-50 dB**\n\n조용한 상태\n\n(도서관, 조용한 교실)")

    with col2:
        st.warning("🟡 **50-70 dB**\n\n보통 상태\n\n(일반 대화, 활동 시간)")

    with col3:
        st.error("🔴 **70+ dB**\n\n시끄러운 상태\n\n(큰 소리, 소란)")

    # 자동 새로고침 (측정 중일 때만)
    if st.session_state.noise_monitoring:
        time.sleep(0.5)
        st.rerun()

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p style='font-size: 0.9rem;'>🎓 교실 도우미 v1.0 | Made with ❤️ for Teachers</p>
    <p style='font-size: 0.8rem;'>💡 TIP: 소음 측정은 마이크 권한이 필요합니다</p>
</div>
""", unsafe_allow_html=True)
