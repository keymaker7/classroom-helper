import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import io
from pydub import AudioSegment

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

    st.info("💡 **브라우저에서 마이크 권한을 허용해주세요!**")

    # JavaScript를 사용한 웹 오디오 API 기반 소음 측정기
    noise_meter_html = """
    <div id="noise-meter-container">
        <div style="text-align: center; margin: 20px 0;">
            <button id="startBtn" onclick="startMonitoring()" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-size: 1.2rem;
                padding: 1rem 2rem;
                border-radius: 10px;
                border: none;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
            ">🎙️ 측정 시작</button>

            <button id="stopBtn" onclick="stopMonitoring()" style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                font-size: 1.2rem;
                padding: 1rem 2rem;
                border-radius: 10px;
                border: none;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
                display: none;
            ">⏸️ 측정 중지</button>
        </div>

        <div id="noise-display" style="
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        ">
            🟢 0 dB<br><small style="font-size: 1.5rem;">😊 조용함</small>
        </div>

        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; color: #666;">현재 소음</div>
                <div id="current-db" style="font-size: 2rem; font-weight: bold;">0 dB</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; color: #666;">최대 소음</div>
                <div id="max-db" style="font-size: 2rem; font-weight: bold;">0 dB</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; color: #666;">평균 소음</div>
                <div id="avg-db" style="font-size: 2rem; font-weight: bold;">0 dB</div>
            </div>
        </div>

        <canvas id="waveform" width="800" height="100" style="width: 100%; background: #f0f0f0; border-radius: 10px; margin: 20px 0;"></canvas>
    </div>

    <script>
        let audioContext;
        let analyser;
        let microphone;
        let dataArray;
        let animationId;
        let isMonitoring = false;
        let maxDb = 0;
        let dbHistory = [];

        async function startMonitoring() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioContext.createAnalyser();
                microphone = audioContext.createMediaStreamSource(stream);

                analyser.fftSize = 256;
                const bufferLength = analyser.frequencyBinCount;
                dataArray = new Uint8Array(bufferLength);

                microphone.connect(analyser);

                document.getElementById('startBtn').style.display = 'none';
                document.getElementById('stopBtn').style.display = 'inline-block';

                isMonitoring = true;
                maxDb = 0;
                dbHistory = [];

                updateNoiseMeter();
            } catch (err) {
                alert('마이크 접근 권한이 필요합니다: ' + err.message);
            }
        }

        function stopMonitoring() {
            isMonitoring = false;

            if (animationId) {
                cancelAnimationFrame(animationId);
            }

            if (microphone) {
                microphone.disconnect();
            }

            if (audioContext) {
                audioContext.close();
            }

            document.getElementById('startBtn').style.display = 'inline-block';
            document.getElementById('stopBtn').style.display = 'none';
        }

        function updateNoiseMeter() {
            if (!isMonitoring) return;

            analyser.getByteFrequencyData(dataArray);

            // 평균 볼륨 계산
            let sum = 0;
            for (let i = 0; i < dataArray.length; i++) {
                sum += dataArray[i];
            }
            const average = sum / dataArray.length;

            // 데시벨로 변환 (0-100 범위를 0-100 dB로 매핑)
            const db = Math.round(average);

            // 최대값 업데이트
            if (db > maxDb) {
                maxDb = db;
            }

            // 히스토리 저장
            dbHistory.push(db);
            if (dbHistory.length > 50) {
                dbHistory.shift();
            }

            // 평균 계산
            const avgDb = Math.round(dbHistory.reduce((a, b) => a + b, 0) / dbHistory.length);

            // UI 업데이트
            updateDisplay(db, maxDb, avgDb);

            // 파형 그리기
            drawWaveform();

            animationId = requestAnimationFrame(updateNoiseMeter);
        }

        function updateDisplay(current, max, avg) {
            let color, emoji, status;

            if (current < 30) {
                color = 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)';
                emoji = '🟢';
                status = '😊 조용함';
            } else if (current < 60) {
                color = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
                emoji = '🟡';
                status = '😐 보통';
            } else {
                color = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
                emoji = '🔴';
                status = '😱 시끄러움!';
            }

            const display = document.getElementById('noise-display');
            display.style.background = color;
            display.innerHTML = `${emoji} ${current} dB<br><small style="font-size: 1.5rem;">${status}</small>`;

            document.getElementById('current-db').textContent = current + ' dB';
            document.getElementById('max-db').textContent = max + ' dB';
            document.getElementById('avg-db').textContent = avg + ' dB';
        }

        function drawWaveform() {
            const canvas = document.getElementById('waveform');
            const canvasCtx = canvas.getContext('2d');
            const WIDTH = canvas.width;
            const HEIGHT = canvas.height;

            analyser.getByteTimeDomainData(dataArray);

            canvasCtx.fillStyle = '#f0f0f0';
            canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

            canvasCtx.lineWidth = 2;
            canvasCtx.strokeStyle = '#667eea';
            canvasCtx.beginPath();

            const sliceWidth = WIDTH / dataArray.length;
            let x = 0;

            for (let i = 0; i < dataArray.length; i++) {
                const v = dataArray[i] / 128.0;
                const y = v * HEIGHT / 2;

                if (i === 0) {
                    canvasCtx.moveTo(x, y);
                } else {
                    canvasCtx.lineTo(x, y);
                }

                x += sliceWidth;
            }

            canvasCtx.lineTo(WIDTH, HEIGHT / 2);
            canvasCtx.stroke();
        }
    </script>
    """

    components.html(noise_meter_html, height=600)

    st.markdown("---")
    st.markdown("### 📖 소음 기준 안내")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🟢 **0-30 dB**\n\n조용한 상태\n\n(도서관, 조용한 교실)")

    with col2:
        st.warning("🟡 **30-60 dB**\n\n보통 상태\n\n(일반 대화, 활동 시간)")

    with col3:
        st.error("🔴 **60+ dB**\n\n시끄러운 상태\n\n(큰 소리, 소란)")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p style='font-size: 0.9rem;'>🎓 교실 도우미 v1.1 | Made with ❤️ for Teachers</p>
    <p style='font-size: 0.8rem;'>💡 TIP: 소음 측정은 브라우저의 마이크 권한이 필요합니다</p>
</div>
""", unsafe_allow_html=True)
