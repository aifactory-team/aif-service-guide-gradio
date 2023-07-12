import gradio as gr
import requests
import json

api_request_env = "https://api.aifactory.space/task/checkServiceRequest"

def sendRequestForService(key):
  res = requests.post(api_request_env, json= {'service': 'gui', 'key': key})
  return res

block = gr.Blocks()

def predict(text, url_params):
  error = ""
  try:      
    key = url_params['key']   
    # print(key)     
    res = sendRequestForService(key)      
    json_data = json.loads(res.text)      
    if(json_data['ct'] == 1) : # 오류 발생 
      return  ["",  json_data['message'], url_params]
    
    # execute predict function 

  except Exception as e:
    print("error")
    print(str(e))
  return [text, error, url_params] # 결과 정상인 경우 
    
get_window_url_params = """
    function(text_input, url_params) {
        console.log(text_input, url_params);
        const params = new URLSearchParams(window.location.search);
        url_params = Object.fromEntries(params);
        return [text_input, url_params];
        }
    """

with block:
  url_params = gr.JSON({}, visible=True, label="URL Params")
  text_input = gr.Text(label="Input")
  text_output = gr.Text(label="Output")
  error = gr.Label(label="error")    

  btn = gr.Button("Run")
  btn.click(fn=predict, inputs=[text_input, url_params],
            outputs=[text_output, error, url_params], _js=get_window_url_params)

block.launch(debug=True)
# block.launch(server_name="0.0.0.0", debug=True)