from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.keyvault.keys import KeyClient
import base64

# Key Vault Configuration
TENANT_ID = "TENANT_ID"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
KV_URI = "https://zoho-new.vault.azure.net/"
KEY_NAME = "my-rsa-key"  # Name of the RSA key in Key Vault

# Authentication in Key Vault
credential = ClientSecretCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
key_client = KeyClient(vault_url=KV_URI, credential=credential)
secret_client = SecretClient(vault_url=KV_URI, credential=credential)

# Create a cryptography client
key = key_client.get_key(KEY_NAME)
crypto_client = CryptographyClient(key, credential)

def encrypt_data(plaintext):
    """Encrypts plaintext using the RSA key in Azure Key Vault."""
    print("Plain text "+plaintext)
    plaintext_bytes = plaintext.encode('utf-8')
    encrypted_result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext_bytes)
    return base64.b64encode(encrypted_result.ciphertext).decode('utf-8')

def decrypt_data(encrypted_text):
    """Decrypts encrypted text using the RSA key in Azure Key Vault."""
    encrypted_bytes = base64.b64decode(encrypted_text)
    decrypted_result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, encrypted_bytes)
    return decrypted_result.plaintext.decode('utf-8')

# Encryption and decryption
#plaintext = "SecretData"
#ciphertext = encrypt_data(plaintext)
#print(f"Encrypted: {ciphertext}")
#decrypted_text = decrypt_data(ciphertext)
#print(f"Decrypted: {decrypted_text}")

# Export functions
__all__ = ['encrypt_data', 'decrypt_data']