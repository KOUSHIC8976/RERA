# Use NVIDIA's official CUDA 12.1 image
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies & SUMO Traffic Simulator
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    git \
    wget \
    sumo \
    sumo-tools \
    sumo-doc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

ENV SUMO_HOME=/usr/share/sumo
WORKDIR /app

# 2. Install PyTorch with CUDA 12.1
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. Copy SMARTS specifically and install with SUMO bindings
COPY ./SMARTS /app/SMARTS
RUN pip3 install --no-cache-dir -e "/app/SMARTS[camera-obs,sumo]"

# 4. Install all RRAE Enterprise Pipeline Dependencies (Plotly goes here!)
RUN pip3 install --no-cache-dir pandas matplotlib seaborn pyyaml tqdm gymnasium plotly

# 5. Copy the rest of the RERA engine
COPY ./ /app/RERA_ENGINE

# 6. Set Python paths
ENV PYTHONPATH="/app:/app/RERA_ENGINE"

# 7. Run the full enterprise pipeline
CMD ["python3", "/app/RERA_ENGINE/main.py", "--config", "/app/RERA_ENGINE/configs/default.yaml"]