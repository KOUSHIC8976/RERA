FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install --no-cache-dir pandas matplotlib seaborn pyyaml tqdm gymnasium plotly

COPY ./ /app/RERA
ENV PYTHONPATH="/app"

CMD ["python3", "/app/RERA/main.py", "--config", "/app/RERA/configs/default.yaml"]
