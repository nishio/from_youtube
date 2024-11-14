"""
YouTube動画のトランスクリプト（字幕）もPythonで取得できます。YouTube Data APIには字幕取得の直接的なエンドポイントがありませんが、youtube-transcript-apiライブラリを利用すると簡単に字幕データを取得できます。

以下が字幕を取得するための手順です。

パッケージのインストール
youtube-transcript-apiをインストールします。
"""

from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id, language="ja"):
    try:
        # 指定された言語（デフォルトは日本語）のトランスクリプトを取得
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except Exception as e:
        print("エラー:", e)
        return None


if __name__ == "__main__":
    # 使用例
    video_id = "C_f8pa9XhqM"
    transcript = get_transcript(video_id)
    if transcript:
        for entry in transcript:
            print(f"{entry['start']:.2f}s: {entry['text']}")
