import requests
import json

BASE_URL = "http://localhost:8000/api"

# Login para obter o token (admin)
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@clinicflow.com", "password": "senha123"}
)

if login_response.status_code != 200:
    print("Erro ao fazer login:")
    print(login_response.text)
    exit(1)

token_data = login_response.json()
token = token_data.get("access_token")
print(f"✓ Token obtido: {token[:50]}...")

# Agora usar o token para fazer requisição de consultas
headers = {"Authorization": f"Bearer {token}"}

consultas_response = requests.get(
    f"{BASE_URL}/consultas/",
    headers=headers
)

print(f"\n✓ Status code: {consultas_response.status_code}")

if consultas_response.status_code == 200:
    data = consultas_response.json()
    print(f"✓ Total de consultas: {data.get('total', 0)}")
    print(f"✓ Items retornados: {len(data.get('items', []))}")
    if len(data.get('items', [])) > 0:
        print(f"\nPrimeira consulta:")
        print(json.dumps(data['items'][0], indent=2, default=str))
else:
    print(f"Erro: {consultas_response.text}")
