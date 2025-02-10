import whisper
import sys

def transcribe_audio(filename):
    print("文字起こしを開始します...")
    # 必要に応じて'medium'や'large'に変更
    model = whisper.load_model("medium")
    result = model.transcribe(filename)
    print("\nTranscription:\n")
    print(result["text"])
    # 結果をテキストファイルとして保存
    output_file = filename.replace('.wav', '.txt')
    with open(output_file, 'w') as f:
        f.write(result["text"])
    print(f"文字起こし結果を保存しました: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("音声ファイルを指定してください。")
        sys.exit(1)

    filename = sys.argv[1]
    transcribe_audio(filename)