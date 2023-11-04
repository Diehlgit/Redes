import socket
import os

class FTP_TELNETcom():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = None
        self.data_conn = None


    #conecta um socket com o servidor para ser a linha de mensagens de comando
    def connect_command(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        print(f"Connected to server {self.server_host}:{self.server_port}")
        self.receive_msg()

    #comando para conectar um socket com o servidor para ser a linha de dados
    def connect_data(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        print(f"Connected to server {self.server_host}:{self.server_port}")
        
    #menda uma mensagem na linha de comandos
    def send_msg(self, message):
        self.client_socket.sendall(message.encode())
        self.receive_msg()
    
    #recebe uma mensagem
    def receive_msg(self):
        TimeOut = False
        mensagemTotal = ''
        Vazio = 0
        while not TimeOut:
            try:
                self.client_socket.settimeout(0.2)  # Tempo do time out
                resposta = self.client_socket.recv(2048)
                dados = resposta.decode('utf-8')
                if dados in ["","\n","\r","\r\n"]:
                    Vazio += 1
                    if Vazio >= 2:
                        return mensagemTotal
                else:
                    print(dados)
                    mensagemTotal = mensagemTotal + dados
            except:
                TimeOut = True
            return mensagemTotal    

    # faz o login de um usuário do servidor ftp com os comandos USER e PASS
    def login(self, user, pas):
        self.send_msg('USER '+user+'\r\n')
        self.send_msg('PASS '+pas+'\r\n')

    # define uma conexao passiva com o servidor
    def set_PASV(self):
        self.client_socket.send('PASV\r\n'.encode())
        port_id = self.client_socket.recv(1024).decode()
        print(port_id)
        elim = "().\r\n"
        port_id = ''.join([char for char in port_id.split(" ")[-1] if char not in elim]).split(",")

        port_num = int(port_id[-2])*256 + int(port_id[-1])
        self.data_conn = FTP_TELNETcom(self.server_host, port_num)
        self.data_conn.connect_data()

    #comando que pede a lista de arquivos e pastas no diretório virtual atual do servidor
    def rqst_LIST(self):
        self.set_PASV()
        self.send_msg('LIST\r\n')
        data = self.data_conn.receive_msg().split("\n")
        tmp = []
        for i in data:
            tmp.append(" ".join(i.split()))

        self.receive_msg()
        return "\n".join(tmp)

    #comando que pede para abrir uma pasta no diretorio virtual    
    def rqst_CD(self, cd):
        self.send_msg('CWD '+cd+'\r\n')
        self.receive_msg()
        
    #comando que pede tranferencia de um arquivo do servidor para o usuario
    def rqst_GET(self, file_name):
        self.set_PASV()
        self.send_msg('RETR '+file_name+'\r\n')
        data = self.data_conn.receive_msg()
        with open(file_name, 'w', encoding='locale') as file:
            file.write(data)
        self.receive_msg()

    #comando que pede para criar uma pasta no diretorio virtual
    def rqst_MKD(self, file_name):
        self.send_msg('MKD  '+file_name+"\r\n")

    #comando que pede para deletar um arquivo ou pasta no diretorio virtual
    def rqst_DELE(self, file_name):
        if '.' in file_name:
            self.send_msg('DELE '+file_name+"\r\n")
        else:
            self.send_msg('RMD  '+file_name+"\r\n")

    #comando que pede para enviar um arquivo do usuario para o servidor
    def rqst_APPE(self, file_name):
        msg_path = os.getcwd()+'/'+file_name
        msg = open(msg_path)
        self.set_PASV()
        self.send_msg('APPE '+file_name+"\r\n")
        self.data_conn.send_msg(msg.read())
        self.data_conn.close()
        self.receive_msg()

    #termina a conexao do socket com o servidor
    def close(self):
        self.client_socket.close()


#Testes ---------------------------------------------------------------------------
""" cli = FTP_TELNETcom("192.168.1.8", 21) 
cli.connect_command()

cli.login('unb', '12345')

cli.rqst_LIST()

#cli.rqst_GET('Texto.txt')

cli.rqst_CD('PastaGenerica')

cli.rqst_LIST()

cli.rqst_CD('..')

cli.rqst_LIST()

cli.rqst_APPE('TextoParaUpload.txt')

cli.rqst_LIST()
#cli.rqst_GET('EntrouNaPastaComSucesso.txt')
 """