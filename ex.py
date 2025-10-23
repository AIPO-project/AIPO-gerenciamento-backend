import requests

USERNAME = "20221174010009"
PASSWORD = "Orna.123"

URL_TOKEN = "https://suap.ifrn.edu.br/api/token/pair"
URL_DADOS = "https://suap.ifrn.edu.br/api/rh/meus-dados"


def gerar_tokens(username, password):
    dados = {
        "username": username,
        "password": password
    }
    response = requests.post(URL_TOKEN, json=dados)

    if response.status_code == 200:
        tokens = response.json()
        print("✅ Token gerado com sucesso!")
        print("Access Token:", tokens["access"])
        print("Refresh Token:", tokens["refresh"])
        return tokens
    else:
        print("❌ Erro ao gerar token:", response.status_code)
        print(response.text)
        return None


def consultar_dados(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(URL_DADOS, headers=headers)

    if response.status_code == 200:
        dados = response.json()
        print("✅ Dados do usuário obtidos com sucesso!")
        print(dados)
        return dados
    else:
        print("❌ Erro ao obter dados:", response.status_code)
        print(response.text)
        return None


tokens = gerar_tokens(USERNAME, PASSWORD)

if tokens:
    consultar_dados(tokens["access"])