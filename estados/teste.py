import pygame
import sys
from estados.base import EstadoBase

class MenuPrincipal(EstadoBase):
    def __init__(self):
        super().__init__()
        self.start = pygame.Rect(250,50,300,100)
        self.start.center = (400, 100)
    def desenhar(self, tela):
        # Pinta o fundo com uma cor cinza escura bem fuleira para destacar o texto
        tela.fill((40, 40, 50))
        pygame.draw.rect(tela,'gray',self.start)
