import json
import ollama
from typing import List


class TextModel:
    def generate_content(self, topic: str="an historical inspiring fact that changed today's computer science world") -> str:
        past_titles_path = os.path.expanduser("~/output.past_titles.txt")
        if not os.path.exists(past_titles_path):
            with open(past_titles_path, "w") as f:
                json.dump([], f)

        with open(past_titles_path, "r") as f:
            past_titles = json.load(f)

        system_message = """
        You are a YouTube Shorts Assistant. Your job is to generate exciting, short, 40-second engaging video scripts.

        Do not explain anything. Do not use formatting, symbols, or quotation marks. Only use plain English words. 

        Use casual, fun language. Include commas, exclamations, and questions where appropriate. 

        End the script with: 'Like, share, and subscribe for more!'

        You will be given a list of previous video titles. Do not repeat or copy any of them.
        """

        user_message = f"""
        Create content on this topic: {topic}

        Do not use ideas similar to these past video titles: {', '.join(past_titles)}.

        Start with: "Did you know..."
        """

        response = ollama.chat(
            model="gemma3:27b-it-qat",
            messages=[
                {"role": "system", "content": system_message>
                {"role": "user", "content": user_message.str>
            ],
        )

        content = response["message"]["content"]
        _content = content.replace('```', '').strip()
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

        if content.startswith('```json'):
            content = content[7:] 
        if content.endswith('```'):
            content = content[:-3]
       # content = re.sub(r'</?[^>]+>', '', content)   

        print(repr(content))
        final_response = json.loads(content)

        return list(final_response)


    def generate_video_description(self, content: str) -> str:
        system_message = """
        You are a YouTube Shorts Assistant help me to generate video description. 
        No explanation, No additional text, No additional decorations, only content as plain paragraph but include commas, exclamations, question marks accordingly. 
        Use simple english, No roman representations.
        Use the content which is the script of the video as a base to generate the description. Use whatever knowledge you have on what needs to be in a YouTube Shorts des>
        """

        user_message = f"""
        Create YouTube Short desciption from this sctipt, {content}.
        """

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_message.strip()},
                {"role": "user", "content": user_message.strip()},
            ],
        )

        content = response["message"]["content"]
        final_response = f"{content}"

        return final_response


    def generate_video_title(self, content: str) -> str:
        system_message = """
        You are a YouTube Shorts Assistant help me to generate video title. 
        No explanation, No additional text, No additional decorations, only content as plain paragraph but include commas, exclamations, question marks accordingly. 
        Use simple english, No roman representations. Must be under 100 characters.
        Use the content which is the script of the video as a base to generate the title. Use whatever knowledge you have on what needs to be in a YouTube Shorts title for>
        Generate only one good YouTube Title.
        """

        user_message = f"""
        Create YouTube Short title from this sctipt, {content}.
        """

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_message.strip()},
                {"role": "user", "content": user_message.strip()},
            ],
        )

        title = response["message"]["content"].strip()

        # Save the title to past_titles file
        titles_path = os.path.expanduser("~/output.past_titles.txt")

        # Make sure the file exists and load current titles
        if not os.path.exists(titles_path):
            with open(titles_path, "w") as f:
                json.dump([], f)
        with open(titles_path, "r") as f:
            past_titles = json.load(f)

        # Append only if new
        if title not in past_titles:
            past_titles.append(title)
            with open(titles_path, "w") as f:
                json.dump(past_titles, f, indent=2)

        return title
