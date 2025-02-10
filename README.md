# Docker
## 1. Dockerイメージをビルド
```
docker build -t whisper-recorder .
```
## 2. Dockerコンテナを実行
```
docker run --rm -v $(pwd):/app -v ~/.cache/whisper:/root/.cache/whisper -w /app whisper-recorder python transcribe.py output.wav
```
--rm オプションは、コンテナ終了後に自動的に削除するオプション。
## 3. Whisperのキャッシュを有効化
```
ls -ld ~/.cache/whisper
sudo chown -R $USER ~/.cache/whisper
sudo chmod -R 755 ~/.cache/whisper
```
# 仮想環境
## 1. PortAudioをインストール
```
brew install portaudio
```
```
export CPATH=$(brew --prefix portaudio)/include
export LIBRARY_PATH=$(brew --prefix portaudio)/lib
```
## 2. 仮想環境を作成
```
python3.12 -m venv myenv
```
## 3. 仮想環境を有効化
```
source myenv/bin/activate
```
仮想環境は、使用する際に毎回有効化する必要がある。
## 4. pipのアップグレード
```
python3.12 -m pip install --upgrade pip
```
pip は、Python パッケージを管理するツールであり、定期的にアップデートすることを推奨する。しかし、必須ではない。
## 5. パッケージのインストール
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
docker run --rm -v $(pwd):/app -v ~/.cache/whisper:/root/.cache/whisper -w /app whisper-recorder python transcribe.py output.wav
```