import tkinter as tk
import itertools
import threading
from tkinter import filedialog
from app.models import MessageJson
from app.services import MessageService, SendService

class Interface:
    def __init__(self, on_submit):
        ## Implementação de interfaces
        self.root = tk.Tk()
        self.root.title("Saga Notícias v1.0")
        self.root.geometry("425x175")

        # Rótulo e botão para carregar o CSV
        self.label_csv = tk.Label(self.root, text="Carregar contatos (.csv)")
        self.label_csv.grid(row=0, column=0, pady=5, padx=5, sticky='w')

        self.load_button = tk.Button(self.root, text="Carregar CSV", command=self.button_load_csv)
        self.load_button.grid(row=0, column=1, pady=5, padx=5)

        # Label para mostrar o status do carregamento, alinhado à direita
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12), anchor='w')
        self.status_label.grid(row=1, column=1, padx=5, sticky='w')

        # Rótulo e campo para inserir o link da imagem
        self.label_img = tk.Label(self.root, text="Imagem ID:")
        self.label_img.grid(row=2, column=0, pady=5, padx=5, sticky='w')

        self.entry_img = tk.Entry(self.root, width=40)
        self.entry_img.grid(row=2, column=1, pady=5, padx=5)

        # Rótulo e campo para template
        self.label_template = tk.Label(self.root, text="WhatsApp Template:")
        self.label_template.grid(row=3, column=0, pady=5, padx=5, sticky='w')

        self.entry_template = tk.Entry(self.root, width=40)
        self.entry_template.grid(row=3, column=1, pady=5, padx=5)

        # Botão para enviar a mensagem
        self.send_button = tk.Button(self.root, text="Enviar", command=self.button_send_message, state=tk.DISABLED)
        self.send_button.grid(row=4, column=1, pady=5, padx=5, sticky='we')

        # Callback e lista de contatos
        self.on_submit = on_submit
        self.contacts = []
        self.send_text = itertools.cycle(["Enviando", "Enviando.", "Enviando..", "Enviando..."])
        self.sending = False

    # Método para carregar CSV
    def button_load_csv(self):
        search_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Importar contatos"
        )
        if search_path:
            self.contacts = MessageService.extract_contacts(search_path)
            if not self.contacts:
                self.send_button.config(state=tk.DISABLED)
                self.status_label.config(text="Erro: Nenhum contato encontrado", fg="red")
            else:
                self.send_button.config(state=tk.NORMAL)
                self.status_label.config(text="Contatos carregados com sucesso!", fg="green")

    # Método para enviar mensagem
    def button_send_message(self):
        template = self.entry_template.get()
        img_id = self.entry_img.get()
        img_url = img_id

        if template and img_url and self.contacts:
            formatted_datas = MessageService.data_format(self.contacts, template, img_url)
            
            # Inicia a animação de status
            self.sending = True
            threading.Thread(target=self._start_send_animation, args=(self.status_label,), daemon=True).start()

            # Inicia o envio de mensagem em uma nova thread para permitir a atualização da interface
            threading.Thread(target=self.send_messages, args=(formatted_datas,), daemon=True).start()

    def _start_send_animation(self, status_label):
        # Executa a animação de envio enquanto a mensagem está sendo enviada
        status_label.config(fg="blue")
        while self.sending:
            status_label.config(text=next(self.send_text))
            status_label.update_idletasks()
            self.root.after(500)  # Intervalo de 500ms para troca de texto

        # Quando terminar, exibe a mensagem final
        if not self.sending:
            status_label.config(text="Envio realizado com sucesso", fg="green")

    def send_messages(self, formatted_datas):
        index = 0
        try:
            for formatted_data in formatted_datas:
                print(f"Enviando mensagem {index + 1}/{len(formatted_datas)}: {formatted_data}")
                data = MessageJson(formatted_data)
                json_data_dict = data.to_json()

                if self.on_submit:
                    result = self.on_submit(SendService.send_to_api(json_data_dict))
                    if result and result.get('status_code') == 200:
                        continue  # Continua para o próximo envio se foi bem-sucedido
                    else:
                        self.sending = False
                        self.status_label.config(text="Erro no envio", fg="red")

            # Finaliza o envio com sucesso
            self.sending = False

        except Exception as e:
            self.sending = False
            self.status_label.config(text=f"Erro: {str(e)}", fg="red")

    def StartInterface(self):
        self.root.mainloop()
