import flask,os
from flask import Flask,jsonify,request,send_file
from matplotlib.pyplot import switch_backend
from flask_cors import CORS
from demo import makeup_transfer
from mix import makeup_transfer2

from setup import setup_config, setup_argparser
from psgan import Inference,PostProcess
app = Flask(__name__)
CORS(app)

# 载入模型
def load_model():
    parser = setup_argparser()
    parser.add_argument(
        "--speed",
        action="store_true",
        help="test speed")
    parser.add_argument(
        "--device",
        default="cuda",
        help="device used for inference")
    parser.add_argument(
        "--model_path",
        default="assets/models/G.pth",
        help="model for loading")

    args = parser.parse_args()
    config = setup_config(args)

    # Using the second cpu
    inference = Inference(config, args.device, args.model_path)
    postprocess = PostProcess(config)

    return (args,inference,postprocess)



@app.route("/")
def index():
    return "hello flask"

@app.route("/predict",methods=["GET","POST"])
def transfer():
    sourceImg = request.files["source"]
    referImg = request.files["refer"]
    
    source_path="source."+sourceImg.filename.split('.')[-1]
    refer_path="refer."+referImg.filename.split('.')[-1]

    sourceImg.save(source_path)
    referImg.save(refer_path)
    return "hello flask"

@app.route("/predict2",methods=["POST"])
def transfer2():
    data = {
        "success": False,
        "transfered":""
    }
    if flask.request.method == 'POST':
        if flask.request.files.get("source") and flask.request.files.get("refer"):
            sourceImg = request.files["source"]
            referImg = request.files["refer"]
            print(sourceImg.filename)
            
            source_path="static/source."+sourceImg.filename.split('.')[-1]
            refer_path="static/refer."+referImg.filename.split('.')[-1]

            sourceImg.save(source_path)
            referImg.save(refer_path)
            save_paths=['static/transfered.png','static/transfered.jpg','static/transfered.jpeg']
            makeup_transfer2(args,inference,postprocess,source_path,refer_path,save_paths)
            data["transfered"] = "http://localhost:5000/"+save_paths[0]
        else:
            print("not receive")
        data["success"] = True
 
    return flask.jsonify(data)

@app.route("/download",methods=["GET"])
def download():
    type = request.args.get("type")
    if not type:
        return send_file('static/transfered.png', as_attachment=True)
    file_path = "static/transfered."+type
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({
            'msg': '文件不存在',
        })

if __name__ == '__main__':
    args,inference,postprocess = load_model()
    app.run(host="0.0.0.0",port=5000)