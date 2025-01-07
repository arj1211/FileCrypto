import base64

from cryptography.fernet import Fernet


# Function to create a base64 representation of a file in chunks
def file_to_base64(file_path, chunk_size=64 * 1024):
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            yield base64.b64encode(chunk)


# Function to encrypt data using Fernet symmetric encryption
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    return encrypted_data


# Function to save data to a plaintext file
def save_to_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)


# Specify the file path (replace 'your_file.txt' with the path to your file)
file_path = "cryptosave.py"  # Replace with your file path

# Generate a key for encryption
key = Fernet.generate_key()

# Encrypt and save the file in chunks
with open("encrypted_file.txt", "wb") as encrypted_file:
    for base64_chunk in file_to_base64(file_path):
        encrypted_chunk = encrypt_data(base64_chunk, key)
        encrypted_file.write(encrypted_chunk + b"\n")

# Save the encryption key to a plaintext file
save_to_file("encryption_key.txt", key)

print("The file has been successfully encrypted and saved as 'encrypted_file.txt'.")
print(
    "The encryption key has been saved as 'encryption_key.txt'. Please share this key securely with the intended recipient."
)

