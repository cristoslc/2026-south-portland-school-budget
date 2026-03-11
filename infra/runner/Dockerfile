FROM ubuntu:24.04

ARG RUNNER_VERSION=2.332.0
ARG RUNNER_ARCH=x64

ENV DEBIAN_FRONTEND=noninteractive
ENV RUNNER_ALLOW_RUNASROOT=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    git-lfs \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Python pipeline dependencies
RUN pip3 install --no-cache-dir --break-system-packages \
    pyyaml \
    pdfplumber \
    beautifulsoup4 \
    markdownify \
    openpyxl \
    yt-dlp

# GitHub Actions runner
RUN mkdir -p /runner && cd /runner \
    && curl -fsSL "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz" \
       | tar xz \
    && ./bin/installdependencies.sh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /runner

COPY start.sh /runner/start.sh
RUN chmod +x /runner/start.sh

ENTRYPOINT ["/runner/start.sh"]
