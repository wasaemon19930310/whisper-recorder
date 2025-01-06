FROM python:3.11-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    python3-dev \
    gcc \
    ffmpeg \
    curl \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Zscaler証明書をシステムに追加
COPY ./zscaler.ca.crt /usr/local/share/ca-certificates/zscaler.ca.crt
RUN chmod 644 /usr/local/share/ca-certificates/zscaler.ca.crt && update-ca-certificates

# 証明書パスを指定
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# pipのアップグレードと依存関係のインストール（タイムアウト対策込み）
RUN pip install --timeout=120 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pip --upgrade

RUN pip install --timeout=120 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org \
    numpy pydub torch torchaudio openai-whisper

# キャッシュディレクトリを作成
RUN mkdir -p /root/.cache/whisper

# スクリプトと必要ファイルをコピー
COPY transcribe.py /app/

# 作業ディレクトリ設定
WORKDIR /app

# コマンドを実行
CMD ["python", "transcribe.py", "audio.wav"]