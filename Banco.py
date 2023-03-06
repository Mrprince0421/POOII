import datetime
import abc
import random
import mysql.connector

contas={}
clientes={}
class cadastro:
        def __init__(self):
            self.pessoas =[]

        def preencher(self, cpf, pessoas):
            res = self.buscar(cpf)
            if res == None:
                self.pessoas.append(pessoas)
                return True
            else:
                return None

        def buscar(self, cpf):
            for i in self.pessoas:
                if i.cpf == cpf:
                    return i
                else:
                    return None


        def excluir(self, cpf):
            self.pessoas.pop(cpf)
class Cliente:
    __slots__ = ['nome','cpf','sobrenome','_email','_senha']
    def __init__(self,nome, sobrenome, cpf,email,senha ):
        self.nome=nome
        self.cpf=cpf
        self.sobrenome=sobrenome
        self._email=email
        self._senha=senha
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self,valor):
        self._email=valor
    @property
    def senha(self):
        return self._senha
    @senha.setter
    def senha(self,valor):
        self._senha=valor
class autenticavel(abc.ABC):
    @abc.abstractmethod
    def autentica(self,email,senha):
        pass
class Banco():
  def __init__(self):
      self.conexao=mysql.connector.connect(host='localhost', db='sysBanco', user='root', password='')
      self.cursor = self.conexao.cursor()
      self.conta=Conta
  def cadastrar(self,num,nome,snome,cpf,email,senha,saldo,limite):
    self.cursor.execute(f'SELECT cpf FROM cliente WHERE cpf = "{cpf}"')
    exists = self.cursor.fetchall()
    if exists:
        return False, 'cpf ja esta cadastrado'
    else:
        data = datetime.datetime.today().strftime("%d/%m/%y %H:%M")
        while True:
            num = random.randint(100, 999)
            if not self.verificarNumero(num):
                self.num = num
                break
        query = f'INSERT INTO cliente(num, nome, snome,cpf,email, senha, saldo, limite, historico) VALUES ("{num}", "{nome}", "{snome}","{cpf}","{email}", "{senha}", {saldo}, {limite}, "Data de de abertura: {data}\n\n")'
        self.cursor.execute(query)
        return True, 'Cadastro realizado com sucesso.'
  def login(self,email,senha):
      if (self.verificarsenha(senha) == True):
          if (self.verificarusuario(email) == True):
              self.cursor.execute(f'SELECT num FROM cliente WHERE email = "{email}"')
              query=self.cursor.fetchall()
              return True, f'login realido com sucesso {query}',
          else:
              return False, 'email incorreto'
      else:
          return False,'senha incorreta'
  def verificarsenha(self,senha):
      self.cursor.execute(f'SELECT senha FROM cliente WHERE senha = "{senha}"')
      exists = self.cursor.fetchall()
      if exists:
          return True
      else:
          return False

  def sacar(self,num,senha,valor,flag=True):
      if self.verificarsenha(senha) == True:
          valor = float(valor)
          flag = self.get_saldo(num)
          if valor > flag[0][0] or valor <= 0:
              return False, "Valor maior que o saldo ou valor menor que 0."
          else:
              if self.verificarsenha(senha):
                  self.set_saldo(num, valor, False)
                  data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
                  if flag:
                      his = f" Saque:\n      Valor: {valor:.2f}\n       Data: {data}\n\n"
                      self.set_historico(num, his)
                  return True, "Saque realizado com sucesso."
              else:
                return False, "Senha invalida."

  def transferir(self, num, senha, destino, valor):
      valor = float(valor)
      retirou = self.sacar(num, senha, valor, False)
      print(retirou)
      if retirou[0] :
          self.depositar(destino, valor, False)
          data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
          his = f" Transferencia:\n       Enviou para: {destino}\n       Valor: {valor:.2f}\n       Data: {data}\n\n"
          self.set_historico(num, his)
          his = f" Transferencia:\n       Recebeu de: {num}\n       Valor: {valor:.2f}\n       Data: {data}\n\n"
          self.set_historico(destino, his)
          return True, "Transferencia realizada com sucesso."
      else:
          return False, "Não foi possivel finalizar a transferencia."

  def depositar(self,num,valor,senha,flag=True):
      if self.verificarsenha(senha):
          valor = float(valor)
          flag = self.get_saldo(num)
          print(flag)
          if flag[0][1] < valor or valor <= 0 or flag[0][0] + valor > flag[0][1]:
              return False, "Não foi possível fazer o deposito."
          else:
              self.set_saldo(num, valor)
              data = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
              if flag:
                  his = f" Deposito:\n      Valor: {valor:.2f}\n       Data: {data}\n\n"
                  self.set_historico(num, his)
              return True, "Deposito realizado com sucesso."
      else:
          return False,'senha esta incorretaa!'
  def get_saldo(self, num):
    self.cursor.execute(f'SELECT saldo, limite FROM cliente WHERE num = {num}')
    flag = self.cursor.fetchall()
    if flag:
        return flag
    else:
        return False

  def set_saldo(self, num, valor, flag=True):
    saldo = self.get_saldo(num)
    if flag:
        valor += saldo[0][0]
    else:
        valor = saldo[0][0] - valor
    self.cursor.execute(f'update cliente set saldo = {valor} where num = {num}')
  def verificarusuario(self,email):
      self.cursor.execute(f'SELECT email FROM cliente WHERE email = "{email}"')
      exists = self.cursor.fetchall()
      if exists:
          return True
      else:
          return False
  def verificarNumero(self,num):
    self.cursor.execute(f'SELECT num FROM cliente WHERE num = {num}')
    exists = self.cursor.fetchall()
    if exists:
        return True
    else:
        return False

  def get_historico(self, num):
          self.cursor.execute(f'SELECT historico FROM cliente WHERE num = {num}')
          flag = self.cursor.fetchall()
          if flag:
              return flag
          else:
              return False

  def set_historico(self, num, his):
      flag = self.get_historico(num)
      his = flag[0][0] + his
      self.cursor.execute(f'update cliente set historico = "{his}" where num = "{num}"')

class Conta:
    _total_contas=0
    __slots__ = ['_numero','_titular','_saldo','_limite','historico','banco','conexao','cursor']
    def __init__(self, numero, cliente, saldo, limite=1000.00):
        self._numero = numero
        self._titular = cliente
        self._saldo = saldo
        self._limite = limite
        self.historico=Historico()
        Conta._total_contas+=1


    @staticmethod
    def get_total_contas():
        return Conta._total_contas
    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self,valor):
        self._saldo=valor

    @property
    def titular (self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        self._titular = valor

    @property
    def limite(self):
        return self._limite
    @limite.setter
    def limite(self, valor):
        self._limite = valor
    @property
    def saldo(self):
        return self._saldo
    @saldo.setter
    def saldo(self,valor):
        self._saldo=valor

    def depositar(self, valor,bool=False):
        if bool == False:
            if valor <= self.limite and valor + self._saldo <= self.limite:
                self._saldo += valor
                print('deposito realizado com sucesso!')
                self.historico.transacoes.append('Um deposito no valor de {} no dia {}'.format(valor,datetime.datetime.today()))
                return True
            else:
                print('valor é maior q o limete da conta')
                self.historico.transacoes.append('Uma tentativa de deposito falho no dia {}'.format( datetime.datetime.today()))
                return False
        else:
            if valor <= self.limite and valor + self._saldo <= self.limite:
                self.historico.transacoes.append('Recebeu uma tranferencia no valor de {} no dia {}'.format(valor, datetime.datetime.today()))
                self._saldo += valor
                print('transferiencia realizado com sucesso!')
                return True
            else:
                print('valor é maior q o limete da conta')
                return None

    def sacar(self, valor,bool=False):
        if bool == False:
            if valor <= self._saldo:
                self._saldo -= valor
                print('saque realizado com sucesso')
                self.historico.transacoes.append('Um saque no valor de {} no dia {}'.format(valor, datetime.datetime.today()))
                return True
            else:
                print('valor é maior q o saldo na conta')
                self.historico.transacoes.append('Uma tentativa de saque falho no dia {}'.format(datetime.datetime.today()))
                return False
        else:
            if valor < self._saldo:
                self._saldo -= valor
                self.historico.transacoes.append('tranferencia no valor de {} no dia {}'.format(valor, datetime.datetime.today()))
                return True
            else:
                print('valor é maior q o saldo na conta')
                self.historico.transacoes.append('Uma tentativa de tranferencia falho no dia {}'.format(datetime.datetime.today()))
                return False
    def transferir(self,destino,valor):
        retirou=self.sacar(valor,True)
        if retirou == False:
            self.historico.transacoes.append('Uma tentativa de tranferencia falho no dia {}'.format(datetime.datetime.today()))
            return None
        else:
            res=destino.depositar(valor,True)
            return res
    def extrato(self):
        print('numero : {}'.format(self._numero))
        print('saldo : {}'.format(self._saldo))
        self.historico.transacoes.append('Extrato no dia {}'.format(datetime.datetime.today()))
        return True
    def listar(self):
        print("nome: {} {}".format(self.titular.nome,self.titular.sobrenome))
        print('numero: {}'.format(self.numero))
        print('saldo: {}'.format(self._saldo))

    def autentica(self, email, senha):
        if email == self._titular.email and senha == self._titular.senha:
            return True
        else:
            return False
class Historico:
    __slots__ = ['data_abertura','transacoes']
    def __init__(self):
        self.data_abertura=datetime.datetime.today()
        self.transacoes=[]
    def imprimir(self):
        print('\ndata de abertura {}'.format(self.data_abertura))
        print('transacoes:')
        for i in self.transacoes:
            print('-',i)
class sistema_interno():
    def login(self,obj):
        if isinstance(obj,autenticavel):
            return 'login realizado com sucesso',True
        else:
            return 'email ou senha incorreto',False

