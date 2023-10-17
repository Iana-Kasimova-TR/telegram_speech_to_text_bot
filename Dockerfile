# STAGE 1 - Download the pytorch model

# Use Python slim-buster as base image
FROM python:3.11 as builder

# Set working directory
WORKDIR /app

# Install pytorch and other dependencies
RUN pip install torch torchvision
RUN pip install pyctcdecode
RUN pip install transformers
RUN pip install https://github.com/kpu/kenlm/archive/master.zip

# Copy download model script
COPY ./bot_voice_msg/downloader.py /app

# Download your model when image is built
RUN python downloader.py 'https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml'

# STAGE 2 - Transfer the downloaded model to the final image

# Use Python slim-buster as base image
FROM python:3.11

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
    POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"
# Copy the python libraries including downloaded models from builder image 
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Copy the downloaded models from builder image
COPY --from=builder /app/downloaded_model /app/downloaded_model
COPY --from=builder /root/.cache/torch /root/.cache/torch

WORKDIR /app

COPY . /app

RUN poetry config virtualenvs.create false \
    && poetry lock --no-update \ 
    && poetry install

CMD ["python", "app/bot_voice_msg/main.py"]


