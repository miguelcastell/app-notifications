from dotenv import load_dotenv
import  os, requests, json

load_dotenv()

api_url = os.getenv('API_URL')
bearer_token = os.getenv('BEARER_TOKEN')
content_type = os.getenv('CONTENT_TYPE')
user_agent = os.getenv('USER_AGENT')

if not all([api_url, bearer_token, content_type]):
    raise ValueError("Uma ou mais variáveis de ambiente não foram importadas corretamente.")

class SendService():

    @staticmethod
    def send_to_api(data:str):

        try:
            send_data = json.loads(data)
        except json.JSONDecodeError as e:
            print('Json invalido')
            return None
        
        headers = {
            'Authorization':f'Bearer {bearer_token}',
            'Content-Type':content_type,
            'User-Agent':user_agent
        }

        try:
            response = requests.post(api_url, headers=headers, json=send_data)
            if response.status_code != 200:
                return {"response": response.json(),}  # Retorna status e corpo da resposta

            print("Debug: Enviado realizado com sucesso")
            return {"status_code": response.status_code, "response": response.json()}  # Retorna status e corpo da resposta
    
        except requests.exceptions.RequestException as e:
            print(f"Debug: Ocorreu um erro ao enviar os dados: {e}")
            return None