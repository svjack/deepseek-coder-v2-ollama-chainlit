from openai import OpenAI, AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)

settings = {
    "model": "deepseek-coder-v2",
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


@cl.on_chat_start
async def start_chat():
    elements = [
    cl.Image(name="image1", display="inline", path="deepseek-coder-v2.png", size = "large")
    ]
    await cl.Message(content="Hello there, I am deepseek-coder-v2. How can I help you ?", elements=elements).send()

    cl.user_session.set(
        "message_history",
        [
          {"role": "system", 
           "content": "You are an expert in guiding coding issues. Please carefully answer users’ questions about code writing."}
        ],
    )

@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
