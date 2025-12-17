import streamlit as st
from core.pipeline import run_pipeline
from ui.components import progress_ui, log_ui

def main_panel(options):
    st.subheader("📤 파일 업로드")
    files = st.file_uploader(
        "문서를 업로드하세요 (.md, .pdf, .txt)",
        type=["md", "pdf", "txt"],
        accept_multiple_files=True,
    )
    if not files:
        return

    if not st.button("🚀 정리 시작"):
        return

    progress, _ = progress_ui()
    log = log_ui()

    zip_path = run_pipeline(
        files=files,
        use_expand=options["use_expand"],
        make_zip=options["make_zip"],
        log_cb=log,
        progress_cb=lambda p: progress.progress(p),
    )

    if options["make_zip"] and zip_path:
        with open(zip_path, "rb") as f:
            st.download_button(
                "📥 정리된 ZIP 다운로드",
                f,
                file_name="result_documents.zip",
                mime="application/zip",
            )
