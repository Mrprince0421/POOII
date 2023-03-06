import datetime
import hashlib
import random
import sys
import socket

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from login import tela_login
from cadastro import tela_cadastro
from deposito import tela_deposito
from home import tela_home
from historico import tela_hitorico
from saque import tela_saque
from transferir import tela_transferir
from extrato import tela_extrato

class Ui_Main(QtWidgets.QWidget):
    def setupUI(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.Stack0 = QtWidgets.QMainWindow()
        self.Stack1 = QtWidgets.QMainWindow()
        self.Stack2 = QtWidgets.QMainWindow()
        self.Stack3 = QtWidgets.QMainWindow()
        self.Stack4 = QtWidgets.QMainWindow()
        self.Stack5 = QtWidgets.QMainWindow()
        self.Stack6 = QtWidgets.QMainWindow()
        self.Stack7 = QtWidgets.QMainWindow()

        self.tela_login = tela_login()
        self.tela_login.setupUi(self.Stack0)
        self.tela_cadastro = tela_cadastro()
        self.tela_cadastro.setupUi(self.Stack1)
        self.tela_home = tela_home()
        self.tela_home.setupUi(self.Stack2)
        self.tela_saque = tela_saque()
        self.tela_saque.setupUi(self.Stack3)
        self.tela_deposito = tela_deposito()
        self.tela_deposito.setupUi(self.Stack4)
        self.tela_historico = tela_hitorico()
        self.tela_historico.setupUi(self.Stack5)
        self.tela_transferir = tela_transferir()
        self.tela_transferir.setupUi(self.Stack6)
        self.tela_extrato = tela_extrato()
        self.tela_extrato.setupUi(self.Stack7)

        self.QtStack.addWidget(self.Stack0)
        self.QtStack.addWidget(self.Stack1)
        self.QtStack.addWidget(self.Stack2)
        self.QtStack.addWidget(self.Stack3)
        self.QtStack.addWidget(self.Stack4)
        self.QtStack.addWidget(self.Stack5)
        self.QtStack.addWidget(self.Stack6)
        self.QtStack.addWidget(self.Stack7)


class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUI(self)

        self.host='localhost'
        self.port = 8006
        self.addr = ((self.host, self.port))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.addr)
        print('adfsfadfsd')

        self.tela_login.pushButton.clicked.connect(self.login)
        self.tela_login.pushButton_2.clicked.connect(self.abri_telacadastro)
        self.tela_login.pushButton_3.clicked.connect(self.sair)
        self.tela_cadastro.pushButton.clicked.connect(self.cadastro)
        self.tela_cadastro.pushButton_2.clicked.connect(self.voltar)
        self.tela_home.pushButton.clicked.connect(self.abri_telasacar)
        self.tela_home.pushButton_2.clicked.connect(self.abri_teladeposita)
        self.tela_home.pushButton_3.clicked.connect(self.abri_telatransferir)
        self.tela_home.pushButton_4.clicked.connect(self.abri_telaextrato)
        self.tela_home.pushButton_5.clicked.connect(self.abri_telahistorico)
        self.tela_home.pushButton_6.clicked.connect(self.voltar)
        self.tela_saque.pushButton_2.clicked.connect(self.saque)
        self.tela_saque.pushButton_3.clicked.connect(self.voltar_home)
        self.tela_deposito.pushButton_2.clicked.connect(self.deposito)
        self.tela_deposito.pushButton_3.clicked.connect(self.voltar_home)
        self.tela_transferir.pushButton_2.clicked.connect(self.tranferir)
        self.tela_transferir.pushButton_3.clicked.connect(self.voltar_home)
        self.tela_historico.pushButton.clicked.connect(self.historico)
        self.tela_historico.pushButton_2.clicked.connect(self.voltar_home)
        self.tela_extrato.pushButton.clicked.connect(self.extarto)
        self.tela_extrato.pushButton_2.clicked.connect(self.voltar_home)


    def login(self):
        email = self.tela_login.lineEdit_3.text()
        senha = self.tela_login.lineEdit_2.text()
        if not(email=='' and senha==''):
            senha_hex = hashlib.md5(senha.encode())
            senha_hex = senha_hex.hexdigest()
            # Enviar pedido de login ao servidor, parâmetros (tipo do pedido,login,senha)
            self.client_socket.send(f'1,{email},{senha_hex}')
            # Recebimento dos dados e separação
            dados = self.client_socket.recv(1024).decode()
            dados = dados.split(',')
            if dados[0] == '1':
                global conta_atual
                conta_atual = dados[1]
                # Limpa os campos e abre a tela de login
                self.tela_login.lineEdit_3.setText('')
                self.tela_login.lineEdit_2.setText('')
                self.abri_telahome()
            else:
                QMessageBox().information(None, 'L-Bank', 'Login/Senha incorreto!')

        else:
            QMessageBox().information(None, 'L-Bank', 'Todos os dados devem ser preenchidos!')


    def cadastro(self):
        nome = self.tela_cadastro.lineEdit.text()
        snome = self.tela_cadastro.lineEdit_2.text()
        cpf = self.tela_cadastro.lineEdit_3.text()
        email = self.tela_cadastro.lineEdit_4.text()
        senha = self.tela_cadastro.lineEdit_5.text()
        num = str(random.randint(1000, 9999))
        saldo=0
        print('macumba')
        if not (nome == '' or snome == '' or cpf == '' or email == '' or senha == ''):
            senha_hex = hashlib.md5(senha.encode())
            senha_hex = senha_hex.hexdigest()
            self.client_socket.send(f'0,{num},{nome},{snome},{cpf},{email},{senha_hex},{saldo}'.encode())
            mensagem = self.client_socket.recv(1024).decode()
            print('macumba')
            mensagem = mensagem.split(',')
            print(mensagem[0])
            if mensagem[0]== '1':
                QMessageBox.information(None, 'teste', 'conta cadastrada com sucesso!')
                self.tela_cadastro.lineEdit.setText('')
                self.tela_cadastro.lineEdit_2.setText('')
                self.tela_cadastro.lineEdit_3.setText('')
                self.tela_cadastro.lineEdit_4.setText('')
                self.tela_cadastro.lineEdit_5.setText('')
            elif mensagem[0] == '0':
                QMessageBox.information(None, 'teste', 'conta ja esta cadastrada no banco')
        else:
            QMessageBox.information(None, 'teste', 'todos os valores devem ser preenchidos!')
    def saque(self):
        global p
        senha = self.tela_saque.lineEdit.text()
        valor = float(self.tela_saque.lineEdit_4.text())

        if not (senha == '' and valor == ''):
            senha_hex = hashlib.md5(senha.encode())
            senha_hex = senha_hex.hexdigest()
            self.client_socket.send(f'3,{senha_hex},{conta_atual},{valor}')
            mensagem = self.client_socket.recv(1024).decode()
            mensagem = mensagem.split(',')
            if mensagem == '1':
                QMessageBox().information(None, 'L-Bank', 'Saque feito com sucesso!')



    def deposito(self):
        global p
        senha = self.tela_deposito.lineEdit.text()
        valor = float(self.tela_deposito.lineEdit_4.text())
        if not (valor == ''):
            # Enviar pedido de deposito ao servidor, parâmetros (tipo do pedido,numero,valor)
            self.client_socket.send(f'2,{conta_atual},{valor},{senha}'.encode())
            # Recebimento dos dados e separação
            mensagem = self.client_socket.recv(1024).decode()
            mensagem = mensagem.split(',')
            if mensagem == '1':
                QMessageBox.information(None, 'teste', 'deposito realizado com sucesso!')
                self.tela_deposito.lineEdit.setText('')
                self.tela_deposito.lineEdit_4.setText('')
                self.abri_telahome()
            elif mensagem == '-1':
                QMessageBox.information(None, 'teste', 'a senha esta incorreta!')
                self.tela_deposito.lineEdit.setText('')
                self.tela_deposito.lineEdit_4.setText('')
                self.abri_telahome()
            else:
                QMessageBox.information(None, 'teste', 'valor acima do limite!')
                self.tela_deposito.lineEdit.setText('')
                self.tela_deposito.lineEdit_4.setText('')
                self.abri_telahome()


    def tranferir(self):
        global p
        senha = self.tela_transferir.lineEdit.text()
        d = self.tela_transferir.lineEdit_5.text()
        valor = float(self.tela_transferir.lineEdit_4.text())
        if not(senha=='' and d == '' and valor ==''):
            senha_hex = hashlib.md5(senha.encode())
            senha_hex = senha_hex.hexdigest()
            self.client_socket.send(f'4,{senha_hex},{conta_atual},{d},{valor}'.encode())
            mensagem = self.client_socket.recv(1024).decode()
            mensagem = mensagem.split(',')
            if mensagem == '1':
                QMessageBox().information(None, 'teste', 'Transferência feita com sucesso!')
                self.tela_transferir.lineEdit.setText('')
                self.tela_transferir.lineEdit_4.setText('')
                self.tela_transferir.lineEdit_5.setText('')
            else:
                QMessageBox().information(None, 'teste', 'falha na operaçao!')
                self.tela_transferir.lineEdit.setText('')
                self.tela_transferir.lineEdit_4.setText('')
                self.tela_transferir.lineEdit_5.setText('')
        else:
            QMessageBox.information(None, 'teste', 'valores n podem ser nulos!')

    def historico(self):
        global p
        senha = self.tela_historico.lineEdit.text()
        for i in Banco.contas.keys():
            if Banco.contas[i].titular.senha == senha and senha == self.num :
                p = i
        for i in Banco.contas[p].historico.transacoes:
            self.tela_historico.textEdit.append('-{}\n'.format(i))



    def extarto(self):
        global p
        senha= self.tela_extrato.lineEdit.text()
        for i in Banco.contas.keys():
            if Banco.contas[i].titular.senha == senha and senha == self.num :
                p = i
        if p != None:
            self.tela_extrato.textEdit.setText('nome = {} {}\nnumero = {}\nsaldo = {}\nlimite= {}'.format(Banco.contas[p].titular.nome, Banco.contas[p].titular.sobrenome,Banco.contas[p].numero,Banco.contas[p].saldo, Banco.contas[p].limite))
            Banco.contas[p].historico.transacoes.append('Extrato no dia {}'.format(datetime.datetime.today()))

        else:
            QMessageBox.information(None, 'teste', 'conta não encontrada')
            self.voltar_home()

    def abri_telacadastro(self):
        self.QtStack.setCurrentIndex(1)

    def abri_telahome(self):
        self.QtStack.setCurrentIndex(2)

    def voltar(self):
        self.QtStack.setCurrentIndex(0)

    def abri_telasacar(self):
        self.QtStack.setCurrentIndex(3)

    def abri_teladeposita(self):
        self.QtStack.setCurrentIndex(4)

    def abri_telatransferir(self):
        self.QtStack.setCurrentIndex(6)

    def abri_telaextrato(self):
        self.QtStack.setCurrentIndex(7)

    def abri_telahistorico(self):
        self.QtStack.setCurrentIndex(5)

    def voltar_home(self):
        self.QtStack.setCurrentIndex(2)

    def sair(self):
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())
