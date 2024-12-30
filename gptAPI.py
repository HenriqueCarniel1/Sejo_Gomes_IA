import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from googletrans import Translator

URL_API = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
CHAVE_API = "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"

cabecalhos = {"Authorization": f"Bearer {CHAVE_API}"}

tradutor = Translator()

def traduzir_para_portugues(texto):
    try:
        traduzido = tradutor.translate(texto, dest="pt")
        return traduzido.text
    except Exception as e:
        return "Erro na tradução: " + str(e)

def gerar_resposta():
    entrada_usuario = entrada_texto.get("1.0", "end-1c").strip()
    if not entrada_usuario:
        messagebox.showwarning("Entrada Vazia", "Por favor, insira uma mensagem.")
        return

    saida_chat.config(state=tk.NORMAL)
    saida_chat.insert(tk.END, f"Você: {entrada_usuario}\n")
    saida_chat.config(state=tk.DISABLED)
    entrada_texto.delete("1.0", tk.END)

    dados = {"inputs": entrada_usuario}
    try:
        resposta = requests.post(URL_API, headers=cabecalhos, json=dados)
        if resposta.status_code == 200:
            resultado = resposta.json()

            if isinstance(resultado, list):
                resposta_ia = resultado[0].get("generated_text", "Desculpe, não consegui entender.")
            elif isinstance(resultado, dict):
                resposta_ia = resultado.get("generated_text", "Desculpe, não consegui entender.")
            else:
                resposta_ia = "Resposta inesperada da IA."

            resposta_traduzida = traduzir_para_portugues(resposta_ia)

            saida_chat.config(state=tk.NORMAL)
            saida_chat.insert(tk.END, f"IA (Traduzido): {resposta_traduzida}\n")
            saida_chat.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Erro na API", f"Erro: {resposta.status_code} - {resposta.json()}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

app = tk.Tk()
app.title("IA Generativa - Chat")
app.geometry("500x600")

saida_chat = scrolledtext.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD, height=25, width=60)
saida_chat.pack(pady=10)

entrada_texto = tk.Text(app, height=4, width=60)
entrada_texto.pack(pady=10)

botao_enviar = tk.Button(app, text="Enviar", command=gerar_resposta, bg="blue", fg="white")
botao_enviar.pack(pady=10)

app.mainloop()
