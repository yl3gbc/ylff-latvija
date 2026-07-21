FROM debian:bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

RUN apt update && apt install -y \
    build-essential \
    git \
    curl \
    wget \
    ca-certificates \
    pkg-config \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev \
    uuid-dev \
    && rm -rf /var/lib/apt/lists/*

# =========================
# PYTHON 3.14 STABLE
# =========================

WORKDIR /tmp

RUN git clone --depth 1 \
    --branch v3.14.6 \
    https://github.com/python/cpython.git

WORKDIR /tmp/cpython

RUN ./configure \
    --enable-optimizations \
    --with-lto \
    --enable-shared \
    && make -j$(nproc) \
    && make altinstall

ENV LD_LIBRARY_PATH=/usr/local/lib

# =========================
# UV
# =========================

COPY --from=ghcr.io/astral-sh/uv:0.11.30 \
    /uv \
    /usr/local/bin/uv

# =========================
# APP
# =========================

WORKDIR /app

COPY pyproject.toml .

# =========================
# PROJECT DEPENDENCIES
# =========================

WORKDIR /app

RUN uv sync \
    --python /usr/local/bin/python3.14

COPY . .

EXPOSE 8003

CMD ["uv", "run", "--python", "/usr/local/bin/python3.14", "python", "app.py"]