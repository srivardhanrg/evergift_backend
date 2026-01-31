# Agent Context: MagicTales Backend

> **Traceability**: This document describes the *actual* implementation of the `magictales_backend` codebase as of Jan 2026. It is the Source of Truth for agents.

## 1. System Architecture

**Type**: FastAPI (Python 3.10+)
**Role**: AI Orchestration & Business Logic
**Database**: Supabase (PostgreSQL)
**Storage**: Cloudflare R2 (S3-compatible)
**Infrastructure**: Render / Railway (Dockerized)

### Communication Pattern: Direct API (CORS)
The backend serves requests directly from the frontend.
- **CORS**: Enabled in `main.py` to allow requests from the frontend domain.
- **Authentication**:
    - **Guest**: `session_id` (UUID) tracks guest limits (max 3 stories).
    - **Shopify User**: `X-Shopify-Customer-Id` / `X-Shopify-Customer-Email` headers (trusted from frontend context).
- **Rate Limiting**: `slowapi` (In-Memory). Limits applied per IP.

## 2. Critical Workflows (Deep Trace)

### A. Story Generation (The "Preview" Job)
**Trigger**: `POST /api/preview/preview`
**Entry Point**: `app.api.endpoints.preview.create_preview`

1.  **Validation**:
    *   Checks `X-Shopify-Customer-Id` or `session_id`.
    *   **Guest Config**: Max 3 stories per session (checked against DB).
    *   **Idempotency**: Block duplicate requests for 30s (`photo_url` + `session_id`).
2.  **Database**:
    *   Creates `previews` row (Status: `pending`).
    *   Creates `generation_jobs` row (Status: `queued`).
3.  **Async Execution**:
    *   Calls `background_tasks.add_task(generate_full_preview, ...)`.
    *   **File**: `app.background.tasks.generate_full_preview`.
    *   **Technique**: **Progressive Generation** (5 pages initial).
4.  **Pipeline Execution** (`PhotorealisticPipeline`):
    *   **Face Analysis**: Calls `fal-ai/llava-next` (VLM) to describe child's face.
    *   **Storage**: Analyzed features saved to DB `previews.analyzed_features` for consistency.
    *   **Image Gen**: Iterate 5 pages -> `generate_with_face_analysis`.
        *   **Model**: `fal-ai/nano-banana/edit`.
        *   **Prompting**: Strict "Subject + Action + Style" layering.
    *   **Watermarking**: `app.background.tasks.create_watermarked_preview`.
5.  **Completion**:
    *   Updates `previews` -> `preview_images` (JSONB).
    *   Updates `generation_jobs` -> `completed`.

### B. PDF Generation (The "Paid" Job)
**Trigger**: Webhook or Test Endpoint
**Entry Point**: `app.background.tasks.generate_remaining_pages_and_pdf`

1.  **Restoration**: Loads `analyzed_features` from DB (locks character identity).
2.  **Completion**: Generates pages 6-10 using the *same* seed/features.
3.  **PDF Composition**:
    *   **Service**: `StoryGiftPDFGeneratorService` (`app/services/storygift_pdf_generator.py`).
    *   **Library**: `ReportLab`.
    *   **Assets**: Downloads high-res images from R2 -> Composites with text -> Uploads PDF to R2.
4.  **Delivery**:
    *   Updates `orders.pdf_url`.
    *   Triggers Email (`app.services.email_service`).

## 3. Data Model (Supabase)

### Core Tables
*   **`previews`**: The central entity.
    *   `status`: `pending` -> `generating` -> `active` -> `purchased`.
    *   `generation_phase`: `preview` (5 pages) -> `generating_full` -> `complete` (10 pages).
*   **`orders`**: Links payment to preview.
    *   `preview_id`: FK to `previews`.
    *   `hq_images`: Stores the final, unwatermarked URLs.
*   **`generation_jobs`**: Async task tracking.
    *   `reference_id`: Links to `preview_id`.
    *   `progress`: 0-100 integer for frontend polling.

## 4. Critical Files Map

| File Path | Responsibility | Key Notes |
| :--- | :--- | :--- |
| `app/main.py` | App Entry | Configures CORS, Middleware, Static Mounts. |
| `app/config.py` | Config | **Single Source of Truth**. Loads `.env` via Pydantic. |
| `app/api/endpoints/preview.py` | API Logic | Handles Idempotency, Guest Limits, Job Creation. |
| `app/background/tasks.py` | Orchestration | The "Brain" of the async worker. Manages job lifecycle. |
| `app/ai/pipelines/photorealistic_pipeline.py` | AI Logic | **Core IP**. LLaVA for analysis + NanoBanana for Gen. |
| `app/services/storage.py` | IO | Hides Boto3/S3 complexity. Handles R2 Upload/Download. |
| `app/services/face_validation.py` | Vetting | MediaPipe logic. Enforces "One Face, Front Facing". |

## 5. Implementation Patterns & Gotchas

### Async & Database
*   **Sync DB in Async**: The codebase uses `supabase-py` (REST client), which is synchronous in some versions but wrapped in async functions here.
*   **Background Tasks**: We use FastAPI `BackgroundTasks`.
    *   *Risk*: If the server restarts, queuing tasks are lost.
    *   *Mitigation*: Stateless jobs. If failed, user validates via "Retry" button (creates new job).

### AI Pipeline Stability
*   **Fal.ai**: Used for all inference.
*   **Sequential Generation**: We generate pages *sequentially* in `generate_all_pages` to avoid hitting API rate limits or timeout issues.
*   **Consistency**: `analyzed_features` is the "Identity DNA". It MUST be saved after the first 5 pages and reused for pages 6-10.

### Configuration (`.env`)
Required vars for operation:
*   `SUPABASE_URL`, `SUPABASE_KEY`
*   `FAL_KEY` (AI)
*   `R2_ENDPOINT`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`
*   `RESEND_API_KEY` (Email)
