import json
import ollama
from typing import List


class TextModel:
    def generate_content(self, topic: str="an historical inspiring fact that changed today's computer science world") -> str:

        system_message = """
        You are a YouTube Shorts Assistant help me to generate content. 
        No explanation, No additional text, No additional decorations, No screenplay, only content as plain paragraph but include commas, exclamations, question marks accordingly. 
        Use simple english, No roman representations.
        Ask for like, share and subscribe at the end of content.
        """

        user_message = f"""
        Create a 40-second content about {topic},

        Did you know...
        """

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_message.strip()},
                {"role": "user", "content": user_message.strip()},
            ],
        )

        content = response["message"]["content"]
        final_response = f"Welcome to the channel, {content}"

        return final_response

    def generate_image_prompts(self, content: str) -> List[str]:
        system_message = """
        You are an artist and a prompt engineer who could describe image in words clearly by a content sequentially. 
        No explanation, No additional text, No additional decorations, only list of strings as array as response. 

        Response has to be strictly json list of strings. No string prefix or suffix around json output.
        """

        user_message = f"""
        Give list of 5 descriptive, clear image prompts for below content sequentially

        {content}
        """

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_message.strip()},
                {"role": "user", "content": user_message.strip()},
            ],
        )

        content = response["message"]["content"]
        final_response = json.loads(content)

        return list(final_response)
