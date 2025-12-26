# Whisper Dual-Channel Recorder & Transcriber

Web会議やオンライン講義を、「自分の声」と「相手の声（PC音）」に分けて録音し、OpenAI Whisperで高精度に文字起こしするためのツールです。

## 特徴

* **2チャンネル同時録音**: マイク入力（左）とシステム音（右）を分離して1つのWAVファイルに保存。
* **高精度文字起こし**: OpenAI Whisper（Mediumモデル）を採用し、専門用語や日本語も高精度にテキスト化。
* **Docker対応**: 巨大な機械学習ライブラリやGPU環境構築の手間を省き、コンテナですぐに実行可能。
* **柔軟なデバイス選択**: デバイス名による指定が可能（JabraヘッドセットやBlackHoleなど）。

## システム構成

* **Backend**: Python 3.11
* **Machine Learning**: OpenAI Whisper (Medium model)
* **Audio Processing**: PyAudio, NumPy, FFmpeg
* **Infrastructure**: Docker

## 使い方

### 1. 録音の実行（ローカル環境）

まず使用可能なデバイスを確認します。

```bash
python record_audio.py --list_devices

```

次にマイクとスピーカー（仮想オーディオデバイス等）を指定して録音を開始します。

```bash
# Ctrl+C で録音停止・保存
python record_audio.py output.wav --mic_device "Jabra Evolve2 40" --speaker_device "BlackHole 2ch"

```

### 2. 文字起こしの実行（Docker推奨）

環境を汚さずに文字起こしを実行します。初回実行時はモデルのダウンロードが走ります。

```bash
docker build -t whisper-recorder .
docker run --rm \
  -v $(pwd):/app \
  -v ~/.cache/whisper:/root/.cache/whisper \
  -w /app \
  whisper-recorder python transcribe.py output.wav

```

---

## セットアップ詳細

### Docker を使用する場合

Whisperのキャッシュディレクトリの権限を適切に設定することで、2回目以降の実行を高速化できます。

```bash
sudo chown -R $USER ~/.cache/whisper
sudo chmod -R 755 ~/.cache/whisper

```

### ローカル仮想環境を使用する場合

```bash
# 1. 依存ライブラリのインストール (macOS)
brew install portaudio
export CPATH=$(brew --prefix portaudio)/include
export LIBRARY_PATH=$(brew --prefix portaudio)/lib

# 2. 仮想環境の構築
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
