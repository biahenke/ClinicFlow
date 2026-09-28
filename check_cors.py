import requests

url = "http://localhost:8000/api/consultas/"

# Tenta sem auth
print("1. Teste SEM autenticação:")
response = requests.head(url)
print(f"   Status: {response.status_code}")
print(f"   Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'NÃO ENCONTRADO')}")
print(f"   Content-Type: {response.headers.get('content-type', 'NÃO ENCONTRADO')}")

# Tenta com OPTIONS (CORS preflight)
print("\n2. Teste OPTIONS (CORS preflight):")
response = requests.options(url)
print(f"   Status: {response.status_code}")
for h in ['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-headers']:
    print(f"   {h}: {response.headers.get(h, 'NÃO ENCONTRADO')}")
