import pygame
class EstadoBase:
    def __init__(self):
        self.proximo_estado = None #Vai dizer para qual estado o gerenciador deve ir.
        self.concluido = False #Vai avisar se o estado atual terminou.

    def abrir(self): #Executa sempre que um estado se torna ativo (reseta variaveis).
        self.concluido = False
    def fechar(self): #Executado antes de sair de um estado.
        pass
    def tratarEventos(self, evento): #Gerencia os imputs (teclado, mause).
        pass
    def atualizar(self, dt): #Atualiza a lógica do estado, "dt" é o Delta Time para movimentalção fluida.
        pass
    def desenhar(self, tela): #Desenhas os elementos visuais na tela.
        pass