import requests
import json

BASE_URL = "http://localhost:8000/api"

# Primeiro login
print("1. Fazendo login com admin...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin@clinicflow.com", "password": "senha123"}
)

if login_response.status_code != 200:
    print(f"   ✗ ERRO ao fazer login: {login_response.status_code}")
    print(f"   {login_response.text}")
    exit(1)

token_data = login_response.json()
token = token_data.get("access_token")
print(f"   ✓ Token obtido com sucesso")

# Testar a requisição exata que o frontend faz
print("\n2. Testando GET /api/consultas/?skip=0&limit=10 (filtro padrão)...")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Teste sem filtros
response = requests.get(
    f"{BASE_URL}/consultas/?skip=0&limit=10",
    headers=headers
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   ✓ Total de consultas: {data.get('total', 0)}")
    print(f"   ✓ Items retornados: {len(data.get('items', []))}")
else:
    print(f"   ✗ ERRO: {response.text}")
    exit(1)

# Teste com filtro de data (como aparecia na screenshot)
print("\n3. Testando GET /api/consultas/ com filtro data=2026-09-28...")
response = requests.get(
    f"{BASE_URL}/consultas/?skip=0&limit=10&data=2026-09-28",
    headers=headers
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   ✓ Total de consultas nesta data: {data.get('total', 0)}")
    print(f"   ✓ Items retornados: {len(data.get('items', []))}")
    
    if len(data.get('items', [])) == 0:
        print("\n   [INFO] Nenhuma consulta para essa data. Testando sem filtro...")
        response2 = requests.get(
            f"{BASE_URL}/consultas/?skip=0&limit=10",
            headers=headers
        )
        data2 = response2.json()
        print(f"   Total geral de consultas: {data2.get('total', 0)}")
else:
    print(f"   ✗ ERRO: {response.text}")

print("\n✅ Teste concluído!")
