# app.py
import streamlit as st

# --------------------------------------------------
# 1️⃣ 페이지 설정 (가벼움: UI만)
# --------------------------------------------------
st.set_page_config(
    page_title="AI dazy document sorter",
    page_icon="🗂️",
    layout="wide",
)

st.title("🗂️ AI Dazy Document Sorter")
st.caption("문서를 업로드하면 의미 기반으로 자동 분류합니다.")

# --------------------------------------------------
# 2️⃣ 파일 업로드 (아직 core 로딩 ❌)
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "📤 문서를 업로드하세요 (.md, .pdf, .txt)",
    type=["md", "pdf", "txt"],
    accept_multiple_files=True,
)

# --------------------------------------------------
# 3️⃣ 파일 업로드 전 상태
# --------------------------------------------------
if not uploaded_files:
    st.info("파일을 업로드하면 분석 준비를 시작합니다.")
    st.stop()

# --------------------------------------------------
# 4️⃣ 파일 업로드 후: UI 준비 단계
#    (여기서부터 필요한 UI 모듈만 lazy import)
# --------------------------------------------------
with st.spinner("파일 분석 준비 중..."):
    from ui.sidebar import sidebar_controls
    from ui.components import progress_ui, log_ui

options = sidebar_controls()

st.success(f"✅ {len(uploaded_files)}개 파일 업로드 완료")
st.caption("설정을 확인한 후 정리 시작 버튼을 누르세요.")

# --------------------------------------------------
# 5️⃣ 실행 트리거
# --------------------------------------------------
run_clicked = st.button("🚀 정리 시작", type="primary")

if not run_clicked:
    st.stop()

# --------------------------------------------------
# 6️⃣ 실행 단계 (여기서부터 core 로딩)
# --------------------------------------------------
progress, progress_text = progress_ui()
log = log_ui()

with st.spinner("문서 정리 중..."):
    # ⚠️ 무거운 로직은 여기서만 import
    from core.pipeline import run_pipeline

    zip_path = run_pipeline(
        files=uploaded_files,
        use_expand=options.get("use_expand", True),
        make_zip=options.get("make_zip", True),
        log_cb=log,
        progress_cb=lambda p: progress.progress(p),
    )

# --------------------------------------------------
# 7️⃣ 결과 출력
# --------------------------------------------------
st.success("🎉 문서 정리가 완료되었습니다.")

if options.get("make_zip", True) and zip_path:
    with open(zip_path, "rb") as f:
        st.download_button(
            "📥 정리된 ZIP 파일 다운로드",
            f,
            file_name="result_documents.zip",
            mime="application/zip",
        )
