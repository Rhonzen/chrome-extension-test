from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/analyse", methods=["POST"])
def receive_data():
    data = request.json
    tweetText = data.get("tweet_text", "")
    result = {"message": "Received tweet text successfully", "tweet_text": tweetText}
    print(tweetText)
    # return jsonify(result)
    return processText(tweetText)

def processText(tweetText):
    claims = [
        {
        'accuracy': 'high',
        'claim': 'a',
        'analysis': 'This is true',
        },
        {
        'accuracy': 'medium',
        'claim': 'b',
        'analysis': 'This might be true',
        },
        {
        'accuracy': 'low',
        'claim': 'c',
        'analysis': 'This is false',
        }
    ]
    return jsonify(claims)

if __name__ == "__main__":
    app.run(host="localhost", port=1000)
