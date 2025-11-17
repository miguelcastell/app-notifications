import csv
from datetime import datetime

class MessageService():
    @staticmethod
    def extract_contacts(search_path):
        contacts = []
        try:
            with open(search_path, mode='r', encoding='utf-8-sig') as file:
                read_cvs = csv.DictReader(file, delimiter=';')
               
                for line_num, row in enumerate(read_cvs, start=2):
                    nome = row.get("nome")
                    telefone = row.get("telefone")

                    if nome and nome.strip() and telefone and telefone.strip():
                        contact ={
                            "user_name": nome.strip().split()[0].capitalize(),
                            "to":telefone.strip()
                        }
                        contacts.append(contact)
                    else:
                        print(f"Aviso: Linha {line_num} do CSV ignorada por conter dados vazios.")
                return contacts
        except FileNotFoundError:
            print("Falha ao localizar arquivo")
            return []
        except Exception as e:
            print(f"Não deu para ler o arquivo:{e}")
            return []
        
    @staticmethod
    def _greeting():
        now = datetime.now().hour

        if now <= now <= 12:
            return "Bom dia"
        elif 12 <= now < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
        
    @staticmethod
    def data_format(contacts:list, template:str, img_url:str):
        greeting = MessageService._greeting()
        data_formatted = []
        
        for contact in contacts:
            data = {
                    "to": contact["to"],
                    "template_name": template, 
                    "img_url": img_url,
                    "greeting": greeting, 
                    "user_name": contact["user_name"]
                    }
            data_formatted.append(data) 
        return data_formatted

