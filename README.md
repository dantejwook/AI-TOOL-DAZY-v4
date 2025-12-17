# 🗂️ AI Dazy Document Sorter

AI 기반 문서 자동 분류 및 폴더 정리 도구입니다.  
문서 파일을 업로드하면 **의미 기반 분석 → 클러스터링 → 폴더 구조 생성 → README 자동 생성 → ZIP 다운로드**까지 한 번에 처리합니다.

본 프로젝트는 **UI / Core / 설정을 명확히 분리**하여  
Streamlit, FastAPI, CLI 등 다양한 인터페이스로 확장 가능하도록 설계되었습니다.

---

## ✨ 주요 기능

- 📄 문서 자동 의미 분석 (GPT 기반 0차 전처리)
- 🧠 의미 기반 클러스터링 (HDBSCAN)
- 🗂️ 자동 폴더 구조 생성
- 📝 폴더별 README.md 자동 생성
- 📦 ZIP 파일로 결과 다운로드
- 📄 PDF / TXT / MD 텍스트 추출 플러그인 구조
- 🔄 UI / 로직 분리로 쉬운 유지보수 & 롤백

---

## 🧠 사용 모델 요약
| 단계 | 모델 / 알고리즘 | 역할 |
|------|------------------|------|
| 1 | text-embedding-3-large | 문서 의미 임베딩 |
| 2 | HDBSCAN | 의미 기반 문서 분류 |
| 3 | cosine similarity + gpt-5-nano | 태그 기반 주제 보정 |
| 4 | gpt-4o-mini | README.md 자동 생성 |

---



## 🧠 전체 파이프라인 개요

```text
[사용자]
   ↓
[Streamlit UI]
   ↓
[core.pipeline.run_pipeline]
   ↓
┌─────────────────────────────┐
│ 0차 GPT 의미 확장 (선택)     │  ← expand.py
│   - 제목/키워드/요약 생성    │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 임베딩 생성                  │  ← embedding.py
│ (text-embedding-3-large)    │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 클러스터링                   │  ← clustering.py
│ (HDBSCAN)                   │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ 폴더 생성 & 파일 저장        │
│ README 생성                  │
└──────────────┬──────────────┘
               ↓
[ZIP 파일 생성 → 다운로드]
```

---

## 📁 프로젝트 구조

```text
repo/
│
├── app.py                  # Streamlit entry point (얇게 유지)
├── config.py               # 설정 / 모델 / 파라미터 (롤백 포인트)
├── requirements.txt
│
├── ui/                     # UI 레이어 (Streamlit 전용)
│   ├── layout.py
│   ├── sidebar.py
│   ├── main_panel.py
│   └── components.py
│
├── core/                   # 핵심 로직 (UI/API/CLI 공용)
│   ├── pipeline.py         # 전체 처리 흐름
│   ├── expand.py           # 0차 GPT 의미 확장
│   ├── embedding.py        # 임베딩 + 캐시
│   ├── clustering.py       # HDBSCAN
│   ├── naming.py           # 폴더명 / README 생성
│   ├── cache.py            # 캐시 유틸
│   │
│   └── extractors/         # 텍스트 추출 플러그인
│       ├── base.py
│       ├── pdf.py
│       ├── text.py
│       └── registry.py
│
└── output_docs/            # 결과물 생성 디렉토리
```

---

## 🧩 설계 원칙

### 1️⃣ UI / Core 완전 분리
- `app.py` 및 `ui/*`는 화면과 사용자 입력만 담당
- `core/*`는 순수 처리 로직만 담당
- UI 수정 시 core 수정 불필요

### 2️⃣ 수시 업데이트 & 롤백 친화
- 모델/파라미터 변경 → `config.py`
- 기능 실험 → 파일 단위 브랜치
- git diff가 명확히 보이는 구조

### 3️⃣ 확장 전제 설계
- Streamlit → FastAPI / CLI 즉시 전환 가능
- 파일 포맷 추가 → extractor 플러그인만 추가

---

## 📄 PDF 텍스트 추출 (플러그인 방식)

파일 형식별로 Extractor를 분리하여 처리합니다.

```text
core/extractors/
├── base.py        # 공통 인터페이스
├── pdf.py         # PDFExtractor
├── text.py        # TXT / MD
└── registry.py    # 자동 선택
```

새 포맷(DOCX 등) 추가 시:
1. extractor 파일 추가
2. `supports()` / `extract()` 구현
3. `registry.py`에 등록

UI / pipeline 수정 ❌

---

## 🚀 실행 방법 (로컬)

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Streamlit Cloud 배포

1. GitHub에 레포 업로드
2. Streamlit Cloud → New App
3. Main file path: `app.py`
4. Secrets 설정

```toml
OPENAI_API_KEY = "sk-..."
```

---

## 🔌 FastAPI / CLI 확장

본 프로젝트의 `core`는 UI에 의존하지 않으므로  
FastAPI / CLI에서 그대로 재사용 가능합니다.

- `run_pipeline()` 직접 호출
- 파일 어댑터 패턴 적용 시 완전 통합 가능

---

## 📌 한 줄 요약

> **이 프로젝트는 일회성 도구가 아니라  
> 장기 운영과 확장을 전제로 설계된 문서 분류 파이프라인입니다.**
