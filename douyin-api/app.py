from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/get_video_info", methods=["GET"])
def get_video_info():
    url = request.args.get("url")
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)',
    }
    try:
        resp = requests.get(url, headers=headers, allow_redirects=True)
        real_url = resp.url
        item_id = real_url.split("video/")[1].split("?")[0]
        api_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}'
        data = requests.get(api_url, headers=headers).json()
        item = data['item_list'][0]

        result = {
            "title": item.get('desc', ''),
            "author": item.get('author', {}).get('nickname', ''),
            "cover_url": item.get('video', {}).get('cover', {}).get('url_list', [''])[0],
            "digg_count": item.get('statistics', {}).get('digg_count', 0),
            "comment_count": item.get('statistics', {}).get('comment_count', 0),
            "share_count": item.get('statistics', {}).get('share_count', 0),
            "play_count": item.get('statistics', {}).get('play_count', 0),
            "create_time": item.get('create_time', 0)
        }

        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)})

@app.route("/get_top10_videos", methods=["GET"])
def get_top10_videos():
    return jsonify({"status": "mocked", "message": "这个功能需要进一步实现，当前为演示占位符。"})

@app.route("/get_hot_comments", methods=["GET"])
def get_hot_comments():
    return jsonify({"status": "mocked", "message": "这个功能需要进一步实现，当前为演示占位符。"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)