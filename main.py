from app.interfaces import Interface

# Inicialização da interface para fins de teste
if __name__ == "__main__":

     #Teste de retorno
    def mock_on_submit(data):
        print("Debug:", data)
    
    # Passa mock_on_submit como o callback para on_submit
    app = Interface(on_submit=mock_on_submit)
    app.StartInterface()
