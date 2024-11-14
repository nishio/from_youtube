"""
YouTubeのコメントをPythonでダウンロードするには、google-authやgoogle-auth-oauthlib、そしてgoogle-auth-httplib2などのライブラリを用いてYouTube Data API v3を利用するのが一般的です。以下がその手順の概要です。

APIキーを取得
	Google Cloud Consoleで新規プロジェクトを作成し、YouTube Data API v3を有効化した後、APIキーを取得します。

Pythonパッケージのインストール
	以下のようにパッケージをインストールします。
	$pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

from googleapiclient.discovery import build
import dotenv
import os

dotenv.load_dotenv()

# APIキーを設定
api_key = os.getenv("YOUTUBE_API_KEY")

# YouTube APIクライアントの設定
youtube = build("youtube", "v3", developerKey=api_key)


def get_comments(video_id):
    comments = []
    next_page_token = None

    while True:
        response = (
            youtube.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                maxResults=100,
            )
            .execute()
        )

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return comments


if __name__ == "__main__":
    # 使用例
    video_id = "C_f8pa9XhqM"
    comments = get_comments(video_id)
    for comment in comments:
        print(comment)
