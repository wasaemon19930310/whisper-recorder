# Docker
## 1. Dockerイメージをビルド
```
docker build -t whisper-recorder .
docker build --no-cache -t whisper-transcriber .
```
## 2. Dockerコンテナを実行
<!-- docker run --rm --device /dev/snd -v $(pwd):/app whisper-recorder -->
## 3. Whisperのキャッシュを有効化
```
ls -ld ~/.cache/whisper
sudo chown -R $USER ~/.cache/whisper
sudo chmod -R 755 ~/.cache/whisper
```
# 仮想環境
## 1. PortAudioをインストール（初回のみ？）
```
brew install portaudio
```
```
export CPATH=$(brew --prefix portaudio)/include
export LIBRARY_PATH=$(brew --prefix portaudio)/lib
```
## 2. 仮想環境を作成（ローカル、初回のみ？）
```
python3.12 -m venv myenv
```
## 3. 仮想環境を有効化
```
source myenv/bin/activate
```
## 4. pipのアップグレード（初回のみ？）
```
python3.12 -m pip install --upgrade pip
```
## 5. パッケージのインストール（初回のみ？）
```
pip install pyaudio
pip install numpy
```
## 6. 仮想環境を終了
```
deactivate
```
# 録音実行コマンド
```
python record_audio.py output.wav
python record_audio.py output.wav --mic_device "Jabra Evolve2 40" --speaker_device "BlackHole 2ch"
```
# 文字起こし実行コマンド
```
docker run --rm -v $(pwd):/app -v ~/.cache/whisper:/root/.cache/whisper -w /app whisper-transcriber python transcribe.py output.wav
docker run --rm -v $(pwd):/app -v ~/.cache/whisper:/root/.cache/whisper -w /app whisper-recorder python transcribe.py output.wav
```