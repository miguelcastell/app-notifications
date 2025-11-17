import json

class MessageJson():
    def __init__(self, formatted_data: dict):
        self.data = {
            "messaging_product": "whatsapp",
            "to": formatted_data["to"],
            "type": 'template',
            "template": {
                "name": formatted_data["template_name"],
                "language": {
                    "code": "pt_BR"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "id": formatted_data["img_url"]
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": formatted_data.get("greeting", "Olá")},
                            {"type": "text", "text": formatted_data.get("user_name", "MEI")}
                        ]
                    }
                ]
            }
        }
    

    def to_json(self):
        return json.dumps(self.data, indent=4)