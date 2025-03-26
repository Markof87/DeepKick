import secrets

def generate_api_key():
    # Genera una chiave URL-safe di 32 byte
    return secrets.token_urlsafe(32)

api_key = generate_api_key()
print("La tua API key:", api_key)