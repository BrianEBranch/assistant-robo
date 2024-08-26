import openai
from openai import OpenAI
import gpt_run
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

client = OpenAI()
thread = client.beta.threads.create()

stanley = client.beta.assistants.create(
    instructions="You are Stanley, a helpful assistant tasked with helping the user in any safe way possible. RESPOND "
                 "AS CONCISE AS POSSIBLE.",
    name="Stanley",
    description="Stanley is a jarvis like AI-Assistant meant to help the user with day to day task.",
    model="gpt-4o-mini",
)

def get_gpt3_response(text):
    event_handler = gpt_run.EventHandler()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )
    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=stanley.id,
            instructions="You are Stanley, a helpful assistant tasked with helping the user in any safe way possible. RESPOND AS CONCISE AS POSSIBLE.",
            event_handler=event_handler,
    ) as stream:
        stream.until_done()
        return event_handler.generated_text
