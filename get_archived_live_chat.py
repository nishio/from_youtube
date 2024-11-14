"""
ライブ配信の終了後、アーカイブされたライブチャットのメッセージは直接YouTube Data APIから取得する方法がありません。しかし、YouTubeのアーカイブ動画に含まれているチャットリプレイデータをPythonで解析するために、以下の方法を試すことができます。

pip install yt-dlp
"""

import yt_dlp
import json


def download_chat(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "skip_download": True,  # 動画自体はダウンロードせず、チャットのみ取得
        "writesubtitles": True,
        "subtitleslangs": ["live_chat"],
        "outtmpl": f"livechat_{video_id}",  # 保存ファイル名
        "writeautomaticsub": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def read_chat_jsonl(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                chat_data = json.loads(line)

                # 必要なデータを抽出
                actions = chat_data.get("replayChatItemAction", {}).get("actions", [])
                for action in actions:
                    message_data = action.get("addChatItemAction", {}).get("item", {})
                    text_message = message_data.get("liveChatTextMessageRenderer", {})

                    if text_message:
                        try:
                            message = text_message["message"]["runs"][0]["text"]
                            author = text_message["authorName"]["simpleText"]
                            timestamp = text_message["timestampText"]["simpleText"]
                            print(f"{timestamp} - {author}: {message}")
                        except:
                            pass
            except json.JSONDecodeError:
                print("JSON形式のエラーが発生しました")


if __name__ == "__main__":
    # 動画IDを指定
    video_id = "C_f8pa9XhqM"
    download_chat(video_id)

    """
    チャットデータの確認 このコードを実行すると、f"livechat_{video_id}.live_chat.json"としてチャットメッセージが保存されます。
    """

    filename = f"livechat_{video_id}.live_chat.json"
    read_chat_jsonl(filename)
