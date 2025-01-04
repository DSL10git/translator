import gradio.interface
import openai
import gradio
import json

with open("keys.json") as f:
  keys = json.load(f)

openai.api_key = keys["openai_key"]


def login(username, password, users_state):
    users = users_state['users']
    logged_users = users_state['logged_users']

    if username in users:
        if password == users[username]:
            logged_users.add(username)
            message = "user logged in successfully"
        else:
            message ="password doesn't match"
    else:
        message ="user isn't in the system"

    return message, users_state


def CustomChatGPT(sentence, language, users_state):
    users = users_state['users']
    logged_users = users_state['logged_users']

    if len(logged_users) == 0:
        return "No users, please log in first!", users_state

    messages = [{"role": "system", "content": "you are chatgpt"}]
    messages.append(
        {
            "role": "user",
            "content":
f"""
Can you translate the following to {language}?
{sentence}

Please answer with the translation only.
""",
        }
    )
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, users_state

language = gradio.Dropdown(
    ["Spanish", "Arabic", "German", "English", "Chinese", "French", "Italian", "Japanese", "Dutch", "Korean", "Russian", "Vietnamese"],
    label="Language"
)
with gradio.Blocks() as demo:
    users_state = gradio.State({
        "users": keys["users"],
        "logged_users": set()
    })
    password = gradio.Textbox(type="password")
    login_interface = gradio.Interface(
        fn=login,
        inputs=["text", password, users_state],
        outputs=["text", users_state],
        title="Login"
    )
    demo_interface = gradio.Interface(
        fn=CustomChatGPT,
        inputs = ["text", language, users_state],
        outputs = ["text", users_state],
        title = "Translator",

    )

demo.launch(share=False, server_name="0.0.0.0")