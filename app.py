# app.py
import streamlit as st

# ------------------------------------
# 1️⃣ 페이지 설정
# ------------------------------------
st.set_page_config(
    page_title="AI dazy document sorter",
    page_icon="🗂️",
    layout="wide",
)

st.title("🗂️ AI Dazy Document Sorter")
st.caption("문서를 업로드하면 의미 기반으로 자동 분류합니다.")

# ------------------------------------
# 2️⃣ 파일 업로드
# ------------------------------------
uploaded_files = st.file_uploader(
    "📤 문서를 업로드하세요 (.md, .pdf, .txt)",
    type=["md", "pdf", "txt"],
    accept_multiple_files=True,
)

if not uploaded_files:
    st.info("파일을 업로드하면 분석 준비를 시작합니다.")
    st.stop()

# ------------------------------------
# 3️⃣ UI 준비 단계 (lazy import)
# ------------------------------------
with st.spinner("파일 분석 준비 중..."):
    from ui.sidebar import sidebar_controls
    from ui.components import progress_ui, status_ui, log_ui

options = sidebar_controls()
st.success(f"✅ {len(uploaded_files)}개 파일 업로드 완료")

# ------------------------------------
# 4️⃣ 실행 트리거
# ------------------------------------
if not st.button("🚀 정리 시작", type="primary"):
    st.stop()

# ------------------------------------
# 5️⃣ 상태 UI 초기화
# ------------------------------------
progress = progress_ui()
status, update_status = status_ui("📊 문서 정리 진행 상황")
log = log_ui()

progress.progress(0)
update_status("파일 검증 중...", "running")

# ------------------------------------
# 6️⃣ 실행 단계
# ------------------------------------
try:
    update_status("처리 엔진 로딩 중...", "running")
    from core.pipeline import run_pipeline
    update_status("처리 엔진 로딩 완료", "complete")
    progress.progress(10)

    update_status("문서 분석 및 정리 중...", "running")
    zip_path = run_pipeline(
        files=uploaded_files,
        use_expand=options.get("use_expand", True),
        make_zip=options.get("make_zip", True),
        log_cb=log,
        progress_cb=lambda p: progress.progress(10 + int(p * 0.8)),
    )
    update_status("문서 분석 및 정리 완료", "complete")
    progress.progress(95)

    if options.get("make_zip", True):
        update_status("ZIP 파일 생성 완료", "complete")

    progress.progress(100)
    update_status("전체 작업 완료 🎉", "complete")

except Exception as e:
    update_status(f"오류 발생: {e}", "error")
    st.error("문서 처리 중 오류가 발생했습니다.")
    st.stop()

# ------------------------------------
# 7️⃣ 결과 출력
# ------------------------------------
st.success("🎉 문서 정리가 완료되었습니다.")

if options.get("make_zip", True) and zip_path:
    with open(zip_path, "rb") as f:
        st.download_button(
            "📥 정리된 ZIP 파일 다운로드",
            f,
            file_name="result_documents.zip",
            mime="application/zip",
        )
