import base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import time

start_time = time.time()
show_mess = True

def number_to_fernet_key(number):
    number_bytes = number.to_bytes((number.bit_length() + 7) // 8, 'big')
    key_bytes = number_bytes.ljust(32, b'\0')
    return base64.urlsafe_b64encode(key_bytes)

def decrypt_message(guess_number, cipher_text):
    key = number_to_fernet_key(guess_number)
    cipher_suite = Fernet(key)
    try:
        message = cipher_suite.decrypt(cipher_text)
        return message
    except InvalidToken:
        return None

with open('encrypted_message.txt', 'rb') as f:
    cipher_text = f.read()

for guess_number in range(1, 100000000):  # guessing numbers between 1 and 1,000,000,000
    elapsed_secs = int((time.time() - start_time) % 60)
    elapsed_mins = int((time.time() - start_time) / 60)

    if elapsed_secs % 60 == 0 and show_mess == True:
        print("\nElapsed time: " + str(elapsed_mins) + " minutes, " + str(elapsed_secs) + " seconds.")
        print("Guesses: " + str(guess_number))
        show_mess = False

    if elapsed_secs % 60 != 0:
        show_mess = True

    decrypted_message = decrypt_message(guess_number, cipher_text)
    if decrypted_message and decrypted_message[:20] == b'0'*20:
        decrypted_message_text = decrypted_message[20:].decode()
        print(f"Decrypted message: {decrypted_message_text}")
        with open('decrypted_message.txt', 'w') as file:
            file.write(decrypted_message_text)
        break
