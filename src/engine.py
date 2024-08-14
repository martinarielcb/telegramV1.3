import requests
import json
import re

# Configura las credenciales y URL de la API
url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v3.0/response/suspiciousObjects'
url_path_isolate = '/v3.0/response/endpoints/isolate'
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJjaWQiOiJjZGFkZDQxYy04ZGFjLTRjZDAtYjNkYS1lOTY0MzA5YzVjYTIiLCJjcGlkIjoic3ZwIiwicHBpZCI6ImN1cyIsIml0IjoxNzIzNjQzMTY1LCJldCI6MTc1NTE3OTE2NCwiaWQiOiI3ZDc2OGQ0My04YmI2LTQzMjktYjM2OS02YjEwM2Y3OTVlNGMiLCJ0b2tlblVzZSI6ImN1c3RvbWVyIn0.BHiYiVzvkrNJ0KDhKT-QW9iupdP6b25IjyCLvhDbOPMu4JtgfYkw47UI8NCQM0H3O5dHDZebO4nRrNqjKuGSVvs2ZOKvB1Os0Bclvd9NJjFjxOpKLtIOjpE3jS3cOlfJsjdSwXpBvpiUmXBdyTdhdtrMP64iNx3hpHR_KPFvoUBSlkM4CVfdwquym7oS4Qtp5GmRp8GiXb1jXXr8eMEszEIFbgCVSaVFGCvJz2THgIdtx5sYOWqx7T8R8TsGrpjF7jO8vOj1mwdNVYx3uOyD-98Rzs1EwkRRnBA-HX2w86g2s_EtYBB3n0ypqpXLU6AY74BUOB6TOY2VHzigR4-89DemUGgjn662UJfqoVPZF9ADpAZOJK-muWKxo9rAZI2U0mE4YwVCXGTT22HREl5kdXMjM45VWTkVKNOPbzFOFkSkJBEC9H9Q50DbDk239SZOPM8eYqB0IwftP2maLZ9YkNk59RpRz91HvT00fLhhPFgisq2KhVYV1bI633Ywey6HaTyzcz4FcqgojVJ7E2F9adKdPFA8LchtNmd6KfE16wbHdSKfVi9pVnQ7t0e_AKHjMBTU2EzO-wGYSdaLJXGxdLR1kdADUncd1E4N4V61EXUpQaShsZ-HlXsyTaOgJgAbxFMPXHDhhacK-RFJH_g_B_lw6vnl5LmE1Lz9oU-wU8M'  # Sustituye con tu token real

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json;charset=utf-8'
}

def get_chiste():
    joke = requests.get('https://api.chucknorris.io/jokes/random')
    data = joke.json()
    return data["value"]

def get_ips(content):
    # Función simplificada para extraer IPs
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(ip_pattern, content)

def get_hashes(content):
    # Función simplificada para extraer hashes SHA-256
    hash_pattern = r'\b[A-Fa-f0-9]{64}\b'
    return re.findall(hash_pattern, content)

def upload_iocs(hashes):
    iocs = [{'fileSha256': h, 'description': 'HASH TelegramBot', 'scanAction': 'log', 'riskLevel': 'low', 'daysToExpiration': '30'} for h in hashes]
    response = requests.post(url_base + url_path, headers=headers, json=iocs)
    if response.status_code == 200:
        print("Data uploaded successfully.")
        return json.dumps(response.json(), indent=4)
    else:
        print(f"Failed to upload data. Status code: {response.status_code}")
        return response.text

def get_endpoints(content):
    # Función simplificada para extraer nombres de endpoints (simulando la funcionalidad)
    # Ajusta esta función según tus necesidades
    return content.splitlines()

def isolate_endpoints(endpoints):
    isolate = [{'endpointName': e, 'description': 'Aislado TelegramBot'} for e in endpoints]
    response = requests.post(url_base + url_path_isolate, headers=headers, json=isolate)
    if response.status_code == 200:
        print("Equipo aislado correctamente")
        return json.dumps(response.json(), indent=4)
    else:
        print(f"Equipo no aislado. Status code: {response.status_code}")
        return response.text


def procesar_sha256(hashes: list) -> str:
    # Construye el cuerpo de la solicitud
    body = [
        {
            'description': f'SHA256 hash {i+1}',
            'fileSha256': hash_value
        }
        for i, hash_value in enumerate(hashes)
    ]
    
    # Envía la solicitud POST a la API
    try:
        r = requests.post(url_base + url_path, headers=headers, json=body)
        if r.status_code == 200:
            return "Hashes cargados correctamente."
        else:
            return f"Error al cargar hashes. Código de estado: {r.status_code}"
    except Exception as e:
        return f"Error al conectar con la API: {e}"

def procesar_sha1(hashes: list) -> str:
    # Construye el cuerpo de la solicitud
    body = [
        {
            'description': f'SHA1 hash {i+1}',
            'fileSha1': hash_value
        }
        for i, hash_value in enumerate(hashes)
    ]
    
    # Envía la solicitud POST a la API
    try:
        r = requests.post(url_base + url_path, headers=headers, json=body)
        if r.status_code == 200:
            return "Hashes SHA1 cargados correctamente."
        else:
            return f"Error al cargar hashes SHA1. Código de estado: {r.status_code}"
    except Exception as e:
        return f"Error al conectar con la API: {e}"
    
def procesar_ip(ips: list) -> str:
    # Construye el cuerpo de la solicitud
    body = [
        {
            'description': f'IP {i+1}',
            'ip': ip_value
        }
        for i, ip_value in enumerate(ips)
    ]
    
    # Envía la solicitud POST a la API
    try:
        r = requests.post(url_base + url_path, headers=headers, json=body)
        if r.status_code == 200:
            return "IPs cargadas correctamente."
        else:
            return f"Error al cargar IPs. Código de estado: {r.status_code}"
    except Exception as e:
        return f"Error al conectar con la API: {e}"
    
def procesar_url(urls: list) -> str:
    # Construye el cuerpo de la solicitud
    body = [
        {
            'description': f'URL {i+1}',
            'url': url_value
        }
        for i, url_value in enumerate(urls)
    ]
    
    # Envía la solicitud POST a la API
    try:
        r = requests.post(url_base + url_path, headers=headers, json=body)
        if r.status_code == 200:
            return "URLs cargadas correctamente."
        else:
            return f"Error al cargar URLs. Código de estado: {r.status_code}"
    except Exception as e:
        return f"Error al conectar con la API: {e}"
    
def procesar_domain(domains: list) -> str:
    # Construye el cuerpo de la solicitud
    body = [
        {
            'description': f'Dominio {i+1}',
            'domain': domain_value
        }
        for i, domain_value in enumerate(domains)
    ]
    
    # Envía la solicitud POST a la API
    try:
        r = requests.post(url_base + url_path, headers=headers, json=body)
        if r.status_code == 200:
            return "Dominios cargados correctamente."
        else:
            return f"Error al cargar dominios. Código de estado: {r.status_code}"
    except Exception as e:
        return f"Error al conectar con la API: {e}"
    
def procesar_sender(senders: list) -> str:
    # Construye el cuerpo de la solicitud
    body = [
        {
            'description': f'Remitente {i+1}',
            'senderMailAddress': sender_value
        }
        for i, sender_value in enumerate(senders)
    ]
    
    # Envía la solicitud POST a la API
    try:
        r = requests.post(url_base + url_path, headers=headers, json=body)
        if r.status_code == 200:
            return "Remitentes cargados correctamente."
        else:
            return f"Error al cargar remitentes. Código de estado: {r.status_code}"
    except Exception as e:
        return f"Error al conectar con la API: {e}"
