
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_wechat(title, content):
    """
    Send a message to WeChat using PushPlus.
    
    Args:
        title (str): The title of the message.
        content (str): The content of the message (Markdown supported).
        
    Returns:
        bool: True if successful, False otherwise.
    """
    token = os.getenv("PUSHPLUS_TOKEN")
    if not token:
        print("⚠️ PUSHPLUS_TOKEN not found in environment variables. Skipping WeChat push.")
        return False

    url = "http://www.pushplus.plus/send"
    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown"  # Use markdown template for better formatting
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 200:
            print(f"✅ WeChat notification sent successfully: {title}")
            return True
        else:
            print(f"❌ Failed to send WeChat notification: {result.get('msg')}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending WeChat notification: {str(e)}")
        return False


