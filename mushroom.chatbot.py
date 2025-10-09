import os
import io
import base64
import json
import re
import gradio as gr
from PIL import Image
from typing import List, Optional, Tuple
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in your environment variables")

MODEL_NAME = "gemini-1.5-flash"
GEN_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

SYSTEM_PROMPT = """You are an expert mycologist (mushroom specialist).
Only answer mushroom-related questions. Redirect off-topic chats back to mushrooms.
Always emphasize safety when discussing edibility.
"""

IMAGE_ANALYSIS_PROMPT = """When analyzing a mushroom image, provide TWO responses:

[JSON] → JSON object with fields:
{
  "common_name": "string or null",
  "genus": "string or null",
  "confidence": 0.0–1.0,
  "visible": ["cap","hymenium","stipe"],
  "color": "color",
  "edible": true/false/null
}

[RESPONSE] → Natural language summary for the user.
"""

class MushroomChatbot:
    def __init__(self):
        self.last_image_analysis = None

    def encode_image(self, image_path: Optional[str]) -> Optional[dict]:
        if not image_path:
            return None
        try:
            img = Image.open(image_path).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=90)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            return {"inlineData": {"mimeType": "image/jpeg", "data": b64}}
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def call_gemini(self, contents: list) -> str:
        headers = {"Content-Type": "application/json"}
        url = f"{GEN_ENDPOINT}?key={API_KEY}"

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024},
        }

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=120)

            if r.status_code != 200:
                return f"API error: {r.status_code} - {r.text}"

            obj = r.json()
            cands = obj.get("candidates", [])
            if not cands:
                return "No response from Gemini"

            parts = cands[0].get("content", {}).get("parts", [])
            response_text = "".join(p.get("text", "") for p in parts)
            return response_text

        except Exception as e:
            return f"API error: {e}"

    def _clean_json_block(self, json_str: str) -> str:
        json_str = re.sub(r"```(?:json)?", "", json_str, flags=re.IGNORECASE).strip()
        json_str = json_str.strip("` \n\r\t")
        return json_str

    def process_image_response(self, response_text: str):
        try:
            if "[JSON]" in response_text and "[RESPONSE]" in response_text:
                json_block = response_text.split("[JSON]", 1)[1].split("[RESPONSE]", 1)[0].strip()
                user_response = response_text.split("[RESPONSE]", 1)[1].strip()
            else:
                match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if match:
                    json_block = match.group(0)
                    user_response = response_text.replace(json_block, "").strip()
                else:
                    return None, response_text

            json_block = self._clean_json_block(json_block)
            json_data = json.loads(json_block)

            print(json.dumps(json_data, indent=2))
            print(user_response)

            return json_data, user_response

        except Exception as e:
            return None, response_text

    def stream_response(self, message: str, history: List[Tuple[str, str]], image_path: Optional[str] = None) -> str:
        prompt = SYSTEM_PROMPT
        if history:
            prompt += "\nRecent conversation:\n"
            for m in history[-3:]:
                user_msg, bot_msg = m
                prompt += f"User: {user_msg}\nAssistant: {bot_msg}\n"

        latest_message = message

        if image_path:
            prompt += f"\n{IMAGE_ANALYSIS_PROMPT}\nUser's message: {latest_message}"
            img_part = self.encode_image(image_path)
            if img_part:
                contents = [{"role": "user", "parts": [{"text": prompt}, img_part]}]
            else:
                contents = [{"role": "user", "parts": [{"text": prompt}]}]
        else:
            prompt += f"\nUser's message: {latest_message}"
            contents = [{"role": "user", "parts": [{"text": prompt}]}]

        response_text = self.call_gemini(contents)

        if image_path:
            json_data, user_text = self.process_image_response(response_text)
            if json_data:
                self.last_image_analysis = json_data
            return user_text
        else:
            return response_text

def main():
    chatbot = MushroomChatbot()

    with gr.Blocks(fill_height=True, theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Your Personal Mushroom Expert")

        gr.ChatInterface(
            fn=chatbot.stream_response,
            additional_inputs=[gr.Image(label="Upload Mushroom Image (Optional)", type="filepath")],
            title="Mushroom Expert Chatbot",
            description="Ask mushroom questions in text, or upload mushroom images for analysis.",
            type="tuples"
        )

    return demo

if __name__ == "__main__":
    demo = main()
    demo.queue(max_size=10).launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)
