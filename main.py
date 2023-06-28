from flask import Flask, render_template, request, jsonify
import json
import requests
import os
# from gramformer import Gramformer
import re

# def set_seed(seed):
#   torch.manual_seed(seed)
#   if torch.cuda.is_available():
#     torch.cuda.manual_seed_all(seed)

# set_seed(1212)

# gf = Gramformer(models = 1, use_gpu=False)

API_URL = "https://api-inference.huggingface.co/models/MikeVey42/ToddTalk_Titled_Model-2000"
headers = {"Authorization": "Bearer " + os.environ['TITLED_API_KEY']}


def query(payload):
  data = json.dumps(payload)
  response = requests.request("POST", API_URL, headers=headers, data=data)
  return json.loads(response.content.decode("utf-8"))


# output = query({
#   "inputs": "Can you please let us know more details about your ",
#   "parameters": {
#     "top_k": 50,
#     "top_p": 0.95,
#     "temperature": 0.5,
#     "repitition_penalty": 15.0,
#     "max_new_tokens": 250.0,
#     "max_time": 120.0
#   },
#   "options": {
#     "wait_for_model": True
#   }
# })

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
  input = request.get_json()
  formatted_input = 'In the TEDTalk titled "' + input["inputs"] + '" the speaker says:'
  payload = {
    "inputs": formatted_input,
    "parameters": {
      "do_sample": False,
      "max_new_tokens": 200,
      "repetition_penalty": 2.02,
      "return_full_text": False
    },
    "options": {
      "wait_for_model": True
    }
  }
  output = query(payload)
  print(output)
  final_data = re.sub(r'[^a-zA-Z.,\?\'": ]', "", output[0]['generated_text'])
  final_data = re.sub(r'\s{2,}'," ",final_data)
  return jsonify({"data": final_data})


app.run(host='0.0.0.0', port=81)
