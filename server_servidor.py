import socket
import threading
from Banco import *


class ClientThread(threading.Thread):
    '''
    Objetos para instanciar o Servidor
    '''

    def __init__(self, clientesock, clienteaddress):
        threading.Thread.__init__(self)
        self.clientesock = clientesock
        self.clienteaddress = clienteaddress

    def run(self):
        '''
        o servidor recebe uma mensagem do cliente e retorna uma resposta se necessario.
        se a mensagem recebida for uma string vazia, o servidor é encerrado.
        '''
        flag = True
        while flag:
            try:
                recebe = self.clientesock.recv(1024 * 1024).decode().split(
                    "*")  # define o tamanho dos pacotes recebidos
                print(f"recebe completo: {recebe}")
                metodo = recebe.pop(0)
                print(metodo)
                if (metodo):
                    if metodo == 'exit':
                        self.clientesock.close()
                        flag = False
                    else:
                        banco = Banco()
                        print(banco)
                        print(f"recebe sem o metodo: {recebe}")
                        func = getattr(banco, metodo)
                        re = func(*recebe)
                        print(f"re {re}")
                        self.clientesock.send(f'{re}'.encode())  # 'utf-8'
            except Exception as e:
                print(e)


class Servidor():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.bind((self.host, self.port))

    def go(self):
        '''
        Inicia conexão e abre para receber os metodos do cliente
        enviar para o servidor e retornar o desejo que o cliente pede.
        '''
        flag = True
        while (flag):
            try:
                self.serv_socket.listen(10)
                print('[WAITING CONNECTION...]')
                clientesock, clienteaddress = self.serv_socket.accept()
                print(f'{clienteaddress} CONNECTED')
                novo = ClientThread(clientesock, clienteaddress)
                novo.start()
            except Exception as error:
                print(error)
                return False, 'CONNECTION ERROR'


if __name__ == "__main__":
    server = Servidor('localhost', 8004)  # 10.180.47.34
    server.go()
