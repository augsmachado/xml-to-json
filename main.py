import requests
import random
import json
import time
import jwt
from faker import Faker
from google.auth import jwt as google_jwt
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np  # Para cálculos de percentis

# Configurações do Google Cloud
SERVICE_ACCOUNT_FILE = "path-to-service-account.json"
PROJECT_ID = "project_id"
API_URL = "url.com"
AUTH_TOKEN = "jwt token"

# Constantes do teste
DURACAO_TESTE = 600
MAX_NUM_REQUISICOES = 250
MAX_WORKERS = 20


def gerar_jwt_token():
    """
    Função para gerar o JWT token
    """

    service_account_info = json.load(open(SERVICE_ACCOUNT_FILE))
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['email']
    )

    # credentials = service_account.Credentials.from_service_account_file(
    #     SERVICE_ACCOUNT_FILE,
    #     audience='https://us-central1-data-lake-raw-development.cloudfunctions.net',
    # )
    # Gera o token JWT
    token = credentials.refresh(Request()).token
    return print(token)
    # return token


def gerar_emails():
    """
    Função para gerar e-mails aleatórios
    """

    quantidade = random.randint(1, 15)
    fake = Faker()
    return [fake.email() for _ in range(quantidade)]


def testar_status(access_token):
    """
    Função para testar o endpoint GET /status
    """

    url = f'{API_URL}/status'
    # token = gerar_jwt_token()
    headers = {'Authorization': f'Bearer {AUTH_TOKEN}'}
    
    start_time = time.time()  # Marca o tempo de início
    response = requests.get(url, headers=headers)
    duration = time.time() - start_time  # Calcula o tempo de resposta

    return response.status_code, duration


def testar_validate():
    """
    Função para testar o endpoint POST /validate
    """

    url = f'{API_URL}/validate'
    # token = gerar_jwt_token()
    payload = {'email_list': gerar_emails()}
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }

    start_time = time.time()  # Marca o tempo de início
    response = requests.post(url, headers=headers, json=payload)
    duration = time.time() - start_time  # Calcula o tempo de resposta

    return response.status_code, duration, len(payload["email_list"])


def realizar_teste_carga(duracao_teste=DURACAO_TESTE, quantidade_requisicoes=MAX_NUM_REQUISICOES):
    """
    Função principal para executar os testes de carga
    """

    start_time = time.time()
    tempos_resposta = []  # Lista para armazenar os tempos de resposta
    sucessos = 0  # Contador de sucessos
    erros = 0  # Contador de erros
    numero_emails_avaliados = 0  # Acumulador do número de emails avaliados
    numero_requisicoes = 0

    # Calculando o intervalo entre requisições para garantir uma taxa de requisições
    intervalo = duracao_teste / quantidade_requisicoes

    # Utilizando threads para as requisições paralelas
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while time.time() - start_time < duracao_teste:  # Executa por um tempo determinado
            list_size = 0
            # Alternando entre os testes de GET e POST
            # if random.choice([True, False]):
            status_code, duration = testar_status(access_token)
            # else:
            # status_code, duration, list_size = testar_validate()

            # Armazena o número de requisicoes
            numero_requisicoes += 1

            # Armazenando o tempo de resposta
            tempos_resposta.append(duration)

            # Atualizando contadores de sucesso e erro
            if status_code == 200:
                sucessos += 1
            else:
                erros += 1

            # Soma número de emails avaliados
            numero_emails_avaliados += list_size

            # Espera o intervalo para a próxima requisição
            time.sleep(intervalo)

    # Calculando percentis 50 e 99
    percentil_50 = np.percentile(tempos_resposta, 50)
    percentil_99 = np.percentile(tempos_resposta, 99)

    # Calculando taxas de sucesso e erro
    taxa_sucesso = (sucessos / (sucessos + erros)) * \
        100 if (sucessos + erros) > 0 else 0
    taxa_erro = (erros / (sucessos + erros)) * \
        100 if (sucessos + erros) > 0 else 0

    # Exibindo as métricas
    print(f'Número de emails avaliados: {numero_emails_avaliados:.0f}')
    print(f'Número de requisições: {numero_requisicoes:.0f}')
    print(f'Tempo total de execução: {time.time() - start_time:.2f} segundos')
    print(f'Tempo de resposta no percentil 50: {percentil_50:.4f} segundos')
    print(f'Tempo de resposta no percentil 99: {percentil_99:.4f} segundos')
    print(f'Taxa de sucesso: {taxa_sucesso:.2f}%')
    print(f'Taxa de erro: {taxa_erro:.2f}%')


# Executando o teste de carga
if __name__ == '__main__':
    realizar_teste_carga(
        duracao_teste=DURACAO_TESTE,
        quantidade_requisicoes=MAX_NUM_REQUISICOES
    )
