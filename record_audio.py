import pyaudio
import wave
import argparse
import numpy as np

# 録音設定
FORMAT = pyaudio.paInt16
RATE = 16000  # サンプリングレート
CHUNK = 1024  # フレームサイズ
CHANNELS = 2  # ステレオチャンネル (左: マイク, 右: スピーカー)

def list_audio_devices():
    """ 利用可能なオーディオデバイス一覧を表示 """
    audio = pyaudio.PyAudio()
    print("\n利用可能なオーディオデバイス一覧:")
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        print(f"ID: {info['index']}, 名前: {info['name']}, チャンネル数: {info['maxInputChannels']}")
    audio.terminate()

def get_device_info(target_name):
    """ 指定した名前を持つオーディオデバイスの情報を取得 """
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if target_name.lower() in info['name'].lower():
            return info
    audio.terminate()
    return None

def get_device_index_by_name(target_name):
    """ 指定した名前を持つオーディオデバイスのインデックスを取得 """
    info = get_device_info(target_name)
    return info['index'] if info else None

def record_mixed_audio(output_file, mic_device, speaker_device):
    """ マイクとスピーカーを同時録音し、1つのファイルに保存 """
    audio = pyaudio.PyAudio()

    # デバイス情報取得
    mic_info = get_device_info(mic_device)
    speaker_info = get_device_info(speaker_device)

    # デバイス確認
    if mic_info is None or speaker_info is None:
        print(f"エラー: '{mic_device}' または '{speaker_device}' が見つかりませんでした。")
        list_audio_devices()
        return

    # デバイスインデックスとチャンネル数を取得
    mic_index = mic_info['index']
    speaker_index = speaker_info['index']

    # ストリームを開く
    mic_stream = audio.open(format=FORMAT, channels=1,  # モノラル入力
                            rate=RATE, input=True,
                            input_device_index=mic_index,
                            frames_per_buffer=CHUNK)

    speaker_stream = audio.open(format=FORMAT, channels=1,  # モノラル入力
                                rate=RATE, input=True,
                                input_device_index=speaker_index,
                                frames_per_buffer=CHUNK)

    print(f"録音開始 (マイク: {mic_device}, スピーカー: {speaker_device}) ... Ctrl+Cで終了します。")

    frames = []

    try:
        while True:  # 無限ループで録音を続ける
            # データを取得
            mic_data = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
            speaker_data = np.frombuffer(speaker_stream.read(CHUNK), dtype=np.int16)

            # データサイズの不一致を補正
            if len(mic_data) > len(speaker_data):
                speaker_data = np.pad(speaker_data, (0, len(mic_data) - len(speaker_data)), mode='constant')
            elif len(mic_data) < len(speaker_data):
                mic_data = np.pad(mic_data, (0, len(speaker_data) - len(mic_data)), mode='constant')

            # ステレオデータ (左: マイク, 右: スピーカー) を作成
            stereo_data = np.column_stack((mic_data, speaker_data)).flatten()
            frames.append(stereo_data.tobytes())

    except KeyboardInterrupt:  # Ctrl+C で終了
        print("\n録音終了")

    # ストリームを閉じる
    mic_stream.stop_stream()
    mic_stream.close()
    speaker_stream.stop_stream()
    speaker_stream.close()
    audio.terminate()

    # 音声ファイルを保存
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"録音が完了しました: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="マイクとスピーカーを同時録音し、1つのファイルに保存します。")
    parser.add_argument("output_file", help="保存するファイル名 (例: output.wav)")
    parser.add_argument("--mic_device", type=str, default="MacBook Air Microphone", help="マイクデバイス名")
    parser.add_argument("--speaker_device", type=str, default="BlackHole 2ch", help="スピーカーデバイス名")
    args = parser.parse_args()

    # 録音開始
    record_mixed_audio(args.output_file, args.mic_device, args.speaker_device)