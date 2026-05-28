import pygame
from .base import EstadoBase
from entidades.jogador import Jogador

class Teste(EstadoBase):
    def __init__(self):
        super().__init__()
        self.jogador = Jogador(100,100)
    def desenhar(self,tela):
        tela.fill('red')
        self.jogador.desenhar(tela)
    def tratarEventos(self, eventos):  # Metodo para tratar todos os eventos (inputs) no frame específico.
        for evento in eventos:
            if evento.type == pygame.QUIT:
                #fechar o jogo
                pass
    def atualizar(self,dt):  # <--- NOVO MÉTODO
        # Captura todas as teclas pressionadas NESTE frame
        comandos = pygame.key.get_pressed()
        # Passa a lista de comandos correta para o jogador
        self.jogador.mover(comandos,dt)
