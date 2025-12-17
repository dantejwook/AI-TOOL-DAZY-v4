# app.py
import streamlit as st

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
# 상단: 2컬럼 레이아웃 (고정)
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
    zip_placeholder = st.empty()  # 실행 후 여기에 버튼 표시

# -------------------------------------------------
# 실행 버튼 (컬럼 아래, 위치 고정)
# -------------------------------------------------
run_clicked = st.button(
    "🚀 정리 시작",
    type="primary",
    disabled=not bool(uploaded_files),
)

# -------------------------------------------------
# 하단 고정 영역: STATUS + LOG
# -------------------------------------------------
st.divider()

status_container = st.empty()   # STATUS BAR 고정
log_container = st.empty()      # LOG 고정

# 상태/로그 초기화 (session_state로 1회만)
if "logs" not in st.session_state:
    st.session_state.logs = []

def update_status(text):
    status_container.markdown(
        f"""
        <div style="
            background:#2e2e2e;
            padding:8px;
            border-radius:6px;
            font-size:0.9em;
        ">
        {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def log(msg):
    st.session_state.logs.append(msg)
    log_container.markdown(
        "<br>".join(st.session_state.logs[-10:]),
        unsafe_allow_html=True,
    )

# 초기 상태 표시
update_status("대기 중")

# -------------------------------------------------
# 실행 로직
# -------------------------------------------------
if run_clicked:
    try:
        update_status("🔄 처리 엔진 로딩 중... [0%]")
        log("엔진 로딩 시작")

        from core.pipeline import run_pipeline

        def progress_cb(pct):
            update_status(f"🔄 processing [{pct}%]")

        zip_path = run_pipeline(
            files=uploaded_files,
            log_cb=log,
            progress_cb=progress_cb,
        )

        update_status("✅ 완료 [100%]")
        log("모든 문서 정리 완료")

        # ZIP 다운로드 버튼을 오른쪽 컬럼에 표시
        with right_col:
            with open(zip_path, "rb") as f:
                zip_placeholder.download_button(
                    "📥 정리된 ZIP 다운로드",
                    f,
                    file_name="result_documents.zip",
                    mime="application/zip",
                )

    except Exception as e:
        update_status("❌ 오류 발생")
        log(f"ERROR: {e}")
        st.error("처리 중 오류가 발생했습니다.")
