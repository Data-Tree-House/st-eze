# ==================== // STAGE 1 // =====================
# ======= // Base builder: shared dependencies // ========

# Both apps inherit from this stage, so the shared layer is only downloaded once.
FROM python:3.14-slim AS base-builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache "."

# =============== // STAGE 2(A) // ===============
# ========= // STREAMLIT DEPS BUILDER // =========
FROM base-builder AS streamlit-builder

RUN . /opt/venv/bin/activate && \
    uv pip install --no-cache ".[streamlit]"

# =============== // STAGE 2(B) // ===============
# ========= // FASTAPI DEPS BUILDER // =========
FROM base-builder AS api-builder

RUN . /opt/venv/bin/activate && \
    uv pip install --no-cache ".[api]"

# =============== // STAGE 2(C) // ===============
# =========== // CLI DEPS BUILDER // =============
FROM base-builder AS cli-builder

RUN . /opt/venv/bin/activate && \
    uv pip install --no-cache ".[cli]"

# =============== // STAGE 3(A) // ===============
# =========== // STREAMLIT RUNTIME // ============
FROM python:3.14-slim AS streamlit

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY --from=streamlit-builder /opt/venv /opt/venv

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

WORKDIR /app/src

ENTRYPOINT ["streamlit", "run", "main-app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =============== // STAGE 3(B) // ===============
# =========== // FAST API RUNTIME // ============

FROM python:3.14-slim AS api

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY --from=api-builder /opt/venv /opt/venv

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8000/ping || exit 1

WORKDIR /app/src

ENTRYPOINT ["fastapi", "run", "main-api.py", "--port", "8000", "--host", "0.0.0.0"]

# =============== // STAGE 3(C) // ===============
# ============ // CLI (CRON) RUNTIME // ==========
FROM python:3.14-slim AS cli

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY --from=cli-builder /opt/venv /opt/venv

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

RUN crontab config/crontab

ENTRYPOINT ["cron", "-f"]
