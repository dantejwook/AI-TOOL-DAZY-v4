# app.py
import streamlit as st
from pathlib import Path
from datetime import datetime

# -------------------------------------------------
# 페이지 설정
# -------------------------------------------------
st.set_page_config(
    page_title="AI dazy document sorter",
    page_icon="🗂️",
    layout="wide",
)

st.title("🗂️ AI Dazy Document Sorter")

# -------------------------------------------------
# CSS: STATUS BAR 하단 고정
# -------------------------------------------------
st.markdown(
    """
    <style>
    #status-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #1f2937;
        color: white;
        padding: 8px 16px;
        font-size: 14px;
        z-index: 9999;
        border-top: 1px solid #374151;
    }
    .content-padding {
        padding-bottom: 60px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="content-padding">', unsafe_allow_html=True)

# -------------------------------------------------
# 상단: 좌 / 우 고정 레이아웃
# -------------------------------------------------
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("📤 파일 업로드")
    uploaded_files = st.file_uploader(
        "문서를 업로드하세요 (.md, .pdf, .txt)",
        type=["md", "pdf", "txt"],
        accept_multiple_files=True,
    )

with right_col:
    st.subheader("📦 ZIP 다운로드")
    zip_placeholder = st.empty()

# -------------------------------------------------
# 실행 버튼
# -------------------------------------------------
run_clicked = st.button(
    "🚀 정리 시작",
    type="primary",
    disabled=not bool(uploaded_files),
)

# -------------------------------------------------
# 로그 파일 준비
# -------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

if "log_file" not in st.session_state:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.log_file = LOG_DIR / f"run_{ts}.log"
    st.session_state.logs = []

def log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"

    # UI 로그
    st.session_state.logs.append(line)

    # 파일 로그
    with open(st.session_state.log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# -------------------------------------------------
# STATUS BAR 상태 관리
# -------------------------------------------------
status_placeholder = st.empty()

def update_status(done: int, total: int, message: str = ""):
    pct = int((done / total) * 100) if total else 0
    status_placeholder.markdown(
        f"""
        <div id="status-bar">
            🔄 {message}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>{pct}%</b> processing
            &nbsp;&nbsp;
            ({done} / {total} complete)
        </div>
        """,
        unsafe_allow_html=True,
    )

# 초기 상태
update_status(0, max(len(uploaded_files), 1), "대기 중")

# -------------------------------------------------
# LOG UI (하단, status 위)
# -------------------------------------------------
st.subheader("🧵 Log")
log_container = st.empty()

def render_logs():
    log_container.markdown(
        "<br>".join(st.session_state.logs[-15:]),
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# 실행 로직
# -------------------------------------------------
if run_clicked:
    try:
        total_steps = 4
        done = 0

        log("처리 시작")
        update_status(done, total_steps, "엔진 로딩 중")

        from core.pipeline import run_pipeline

        done += 1
        update_status(done, total_steps, "문서 분석 중")
        log("문서 분석 시작")

        def progress_cb(pct):
            # pct: 0~100 → 전체 step 기준 환산
            sub_done = done + pct / 100
            update_status(int(sub_done), total_steps, "문서 정리 중")

        zip_path = run_pipeline(
            files=uploaded_files,
            log_cb=log,
            progress_cb=lambda p: progress_cb(p),
        )

        done += 2
        update_status(done, total_steps, "ZIP 생성 중")
        log("ZIP 생성 완료")

        done = total_steps
        update_status(done, total_steps, "완료")
        log("모든 작업 완료")

        with right_col:
            with open(zip_path, "rb") as f:
                zip_placeholder.download_button(
                    "📥 정리된 ZIP 다운로드",
                    f,
                    file_name="result_documents.zip",
                    mime="application/zip",
                )

    except Exception as e:
        log(f"ERROR: {e}")
        update_status(0, 1, "오류 발생")
        st.error("처리 중 오류가 발생했습니다.")

# -------------------------------------------------
# 하단 padding 종료
# -------------------------------------------------
st.markdown("</div>", unsafe_allow_html=True)
