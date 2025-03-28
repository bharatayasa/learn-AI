import ollama

def chat_with_model():
    while True:
        user_input = input("\nAnda: ")
        if user_input.lower() in ["exit", "keluar"]:
            break
        
        response = ollama.chat(
            model="deepseek-r1:14b",
            messages=[{"role": "user", "content": user_input}]
        )
        print("\nAI:", response["message"]["content"])

if __name__ == "__main__":
    chat_with_model()