from opensciencegrid/tensorflow-gpu:2.2-cuda-10.1

RUN apt-get update && apt-get install --yes \
    python3-numpy \
    python3-matplotlib \
    python3-seaborn \
    python3-pillow \
    python3-pip \
    vim \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

RUN pip3 install tqdm==4.48.2 opencv-python==4.3.0.36