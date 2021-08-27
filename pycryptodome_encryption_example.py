from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
def generate_key():
    # Your key must be 16, 24 or 32 bytes long
    key = get_random_bytes(32)
    return key

def encrypt( message, key ):
    byte_array = message.encode("utf-8")
    # If we were given a string, convert it to a bytes array
    if type(key) == str:
        key = key.encode("utf-8")
    if len(key) not in [16,24,32]:
        print("Key must be 16, 24 or 32 bytes long")
        exit()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(byte_array)
    return ciphertext, tag, cipher.nonce

def decrypt( encrypted, key, tag, nonce):
    key = key.encode("utf-8")
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    byte_array = cipher.decrypt_and_verify(encrypted, tag)
    return byte_array.decode('utf-8')

def main():
    while True:
        task = input("(e)ncrypt, (d)ecrypt or (q)uit?")
        if task == "e": # Encrypt
            message = input("Your secret message: ")
            key = input("Your encryption key: ")
            ciphertext, tag, nonce = encrypt(message, key)
            print("You can safely send these...")
            print("Cipher text: "+ciphertext.hex())
            print("Tag: "+tag.hex())
            print("Nonce: "+nonce.hex())
        elif task == "d": # Decrypt
            ciphertext = input("Encrypted text (hex): ")
            tag = input("Your ciphertext tag (hex): ")
            nonce = input("Your ciphertext nonce (hex): ")
            key = input("Your encryption key: ")
            # Convert from hex strings to byte array
            ciphertext = bytearray.fromhex(ciphertext)
            tag = bytearray.fromhex(tag)
            nonce = bytearray.fromhex(nonce)
            message = decrypt(ciphertext, key, tag, nonce)
            print(message)
        elif task == "q": # Quit
            return()
main()