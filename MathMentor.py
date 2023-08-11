import gradio as gr
import openai
import os
openai.api_key = os.getenv('OPENAI_API_KEY')

message_history = [{"role": "user","content":"You are a math trivia bot and you are to give math equations that elementary and middle school children should be able to do. I will specify the grade level and you will give fun math equations based on that. You will only reply with whether or not the answer is correct and why it is correct or incorrect. Also the user will be able to input strings or integers or may put spaces in the answer choice. Please make sure if the user put a string instead of an integer that it counts correct. If you understand say OK"},
                   {"role": "assistant", "content": "OK"}]

def predict(input):
    global message_history
    message_history.append({"role": "user", "content":input})
    complete = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = message_history
    )
    reply_content = complete.choices[0].message.content
    print(reply_content)
    message_history.append({"role": "assistant", "content": reply_content})
    response = [(message_history[i]["content"],message_history[i+1]["content"]) for i in range(2, len(message_history)-1,2)]
    return response
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        txt = gr.Textbox(show_lable = False, placeholder = "Type you grade level here").style(container = False)
        txt.submit(predict,txt,chatbot)
        txt.submit(lambda: "",None,txt)
        txt.submit(None,None,txt,_js = "() => {''}")
demo.launch()
