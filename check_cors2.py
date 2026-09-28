import requests
import json

BASE_URL = "http://localhost:8000/api"

# Login para obter token
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@clinicflow.com", "password": "admin123"}
)

if login_response.status_code != 200:
    print(f"✗ Login falhou: {login_response.status_code}")
    exit(1)

token = login_response.json().get("access_token")
print(f"✓ Token obtido")

# Agora testa com auth
headers = {"Authorization": f"Bearer {token}"}

print("\n1. Teste com autenticação:")
response = requests.get(f"{BASE_URL}/consultas/", headers=headers)
print(f"   Status: {response.status_code}")
print(f"   Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'NÃO ENCONTRADO')}")
print(f"   Content-Type: {response.headers.get('content-type', 'NÃO ENCONTRADO')}")

if response.status_code == 200:
    data = response.json()
    print(f"   ✓ Total consultas: {data.get('total')}")
else:
    print(f"   ✗ Resposta: {response.text[:100]}")

# OPTIONS request
print("\n2. Teste OPTIONS (CORS preflight):")
response = requests.options(f"{BASE_URL}/consultas/", headers=headers)
print(f"   Status: {response.status_code}")
for h in ['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-headers']:
    val = response.headers.get(h)
    if val:
        print(f"   {h}: {val}")
