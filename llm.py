from groq import Groq
from config.config import GROQ_API_KEY

def get_response(prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",   # ✅ NEW WORKING MODEL
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"