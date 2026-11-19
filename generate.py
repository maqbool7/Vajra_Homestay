import os
import sys
from google import genai

# Initialize the Gemini client
client = genai.Client()

HOTEL_CONTEXT = """
You are an expert web developer for 'Vajara Homestay'.
Generate ONLY clean, complete, valid HTML/CSS code for index.html based on user requests.
Do not include conversational filler—return ONLY the HTML code.
"""

def update_index_page(user_prompt):
    print(f"\n⏳ Sending prompt to Gemini: '{user_prompt}'...")
    
    try:
        full_prompt = f"{HOTEL_CONTEXT}\nUser Request: {user_prompt}\nProvide the complete HTML code for index.html:"
        
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=full_prompt
        )
        
        html_code = response.text
        
        # Clean up markdown code blocks if present
        if "```html" in html_code:
            html_code = html_code.split("```html")[1].split("```")[0].strip()
        elif "```" in html_code:
            html_code = html_code.split("```")[1].split("```")[0].strip()

        # Overwrite templates/index.html directly
        file_path = os.path.join("templates", "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_code)

        print("✅ Success! 'templates/index.html' has been updated directly in VS Code.")
        print("👉 Refresh your browser (http://127.0.0.1:5000) to view the changes!\n")

    except Exception as e:
        print(f"❌ Error updating file: {str(e)}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Prompt passed directly via command line args: python generate.py "Change hero image"
        prompt = " ".join(sys.argv[1:])
        update_index_page(prompt)
    else:
        # Interactive loop in terminal
        print("="*60)
        print("🤖 Vajara Homestay - Terminal Code Generator")
        print("Type your change prompt below, or type 'exit' to quit.")
        print("="*60)
        
        while True:
            try:
                prompt = input("\nEnter prompt > ").strip()
                if not prompt:
                    continue
                if prompt.lower() in ["exit", "quit", "q"]:
                    print("Exiting generator. Goodbye!")
                    break
                update_index_page(prompt)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting generator.")
                break