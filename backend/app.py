from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
import os
from google.cloud import storage
from io import BytesIO
import pandas as pd

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/chat',methods=['GET'])
def answer():
    text = request.args.get("text","")
    
    # for local
    df=pd.read_csv("all_edinetcodeinfo.csv",header=None)
    
    # for GCP
    #storage_client = storage.Client()
    #bucket = storage_client.get_bucket('edinetcodeinfo')
    #blob = bucket.get_blob('all_edinetcodeinfo')
    #df = pd.read_csv(BytesIO(blob.download_as_string()),header=None)
    
    dfc=df[df[5].str.contains(text)]
    if(len(dfc)==0):
        result={"output":[{"type":"text","value":"見つかりませんでした"}]}
        return make_response(jsonify(result))
    else:
        ft=str(len(dfc))+"件見つかりました"
        html=""
        for i in range(len(dfc)):
            code=dfc.iloc[i,0]
            company=dfc.iloc[i,2]
            value=str(code)+": "+"<a href=\"https://stocks.finance.yahoo.co.jp/stocks/chart/?code="+str(code)+"\" target=\"_blank\" >"+str(company)+"</a><br>"
            html+=value
        result={"output":[{"type":"text","value":ft,"delayMs": 300},{"type":"html","value":html}]}
        return make_response(jsonify(result))

@app.errorhandler(404)
def not_found (error):
    return make_response(jsonify({"error","Not found"}),404)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

