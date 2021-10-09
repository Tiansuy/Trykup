from flask import Flask,jsonify,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 载入模型
def load_model():
    """Load the pre-trained model, you can use your model just as easily.
    """
    global model
    model = resnet50(pretrained=True)
    model.eval()
    if use_gpu:
        model.cuda()

@app.route("/")
def index():
    return "hello flask"


if __name__ == '__main__':
    load_model()
    app.run(host="0.0.0.0",port=5000)