import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from googletrans import Translator

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
API_KEY = "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"

headers = {"Authorization": f"Bearer {API_KEY}"}

translator = Translator()

def translate_to_portuguese(text):
    try:
        translated = translator.translate(text, dest="pt")
        return translated.text
    except Exception as e:
        return "Erro na tradução: " + str(e)

def generate_response():
    user_input = input_text.get("1.0", "end-1c").strip() 
    if not user_input:
        messagebox.showwarning("Entrada Vazia", "Por favor, insira uma mensagem.")
        return

    chat_output.config(state=tk.NORMAL)
    chat_output.insert(tk.END, f"Você: {user_input}\n")
    chat_output.config(state=tk.DISABLED)
    input_text.delete("1.0", tk.END)

    payload = {"inputs": user_input}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()

            if isinstance(result, list):
                bot_response = result[0].get("generated_text", "Desculpe, não consegui entender.")
            elif isinstance(result, dict):
                bot_response = result.get("generated_text", "Desculpe, não consegui entender.")
            else:
                bot_response = "Resposta inesperada da IA."

            translated_response = translate_to_portuguese(bot_response)

            chat_output.config(state=tk.NORMAL)
            chat_output.insert(tk.END, f"IA (Traduzido): {translated_response}\n")
            chat_output.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Erro na API", f"Erro: {response.status_code} - {response.json()}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

app = tk.Tk()
app.title("IA Generativa - Chat")
app.geometry("500x600")

chat_output = scrolledtext.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD, height=25, width=60)
chat_output.pack(pady=10)

input_text = tk.Text(app, height=4, width=60)
input_text.pack(pady=10)

send_button = tk.Button(app, text="Enviar", command=generate_response, bg="blue", fg="white")
send_button.pack(pady=10)

app.mainloop()
