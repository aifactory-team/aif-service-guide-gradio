import gradio as gr
import os
os.environ["OPENAI_API_KEY"] = "open api key 입력"
from langchain import OpenAI, ConversationChain
import requests
import json

llm = OpenAI(temperature=0.95)
conversation = ConversationChain(llm=llm, verbose=False)


get_window_url_params = """
    function(text_input, url_params) {
        console.log(text_input, url_params);
        const params = new URLSearchParams(window.location.search);
        url_params = Object.fromEntries(params);
        return [text_input, url_params];
        }
    """

api_request_env = "https://api.aifactory.space/task/checkServiceRequest"

def sendRequestForService(key):
  res = requests.post(api_request_env, json= {'service': 'gui', 'key': key})
  return res

def parse_URL_params(text, url_params):
    return [text, url_params]


def chat(message, history):  
    error = ""
    try:      
        key = url_params['key']   
        print(key)     
        res = sendRequestForService(key)      
        json_data = json.loads(res.text)      
        if(json_data['ct'] == 1) : # 오류 발생시
            return  ["",  json_data['message'], url_params]
        
        # execute predict function 

    except Exception as e:
        print("error")
        print(str(e))

    history = history or []
    response = conversation.predict(input=message)
    history.append((message, response))

    return history, history # 결과 정상인 경우 


url_params = gr.JSON({}, visible=True, label="URL Params")
with gr.Blocks() as demo:

    state = gr.State([])
    gen_btn = gr.Button(value = '초기화')
    ga = gr.Textbox(visible=False)
    gen_btn.click(fn=parse_URL_params, inputs=[ga, url_params], outputs=[ga, url_params], _js=get_window_url_params)

    # url_params.render() # 실제 오는지 확인용

    chatbot = gr.Chatbot()
    with gr.Row():
        with gr.Column():
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter"
            )
            
        with gr.Column():
            submit_btn = gr.Button(value="Send", variant="secondary")

    
    submit_btn.click(chat, 
            inputs=[txt, state], 
            outputs=[chatbot, state])
    txt.submit(chat, [txt, state], [chatbot, state])


if __name__=='__main__':
    demo.launch()