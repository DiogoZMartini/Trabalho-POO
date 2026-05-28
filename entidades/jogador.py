import pygame

class Jogador:
    def __init__(self,x,y):
        self.forma = pygame.Rect(x, y, 300, 200)
        self.velocidade = 300
        self.x = float(x)
        self.y = float(y)
    def mover(self, comandos,dt):
        deslocamento = self.velocidade * dt
        if comandos[pygame.K_UP] or comandos[pygame.K_w]:
            self.y -= deslocamento
        if comandos[pygame.K_DOWN] or comandos[pygame.K_s]:
            self.y += deslocamento
        if comandos[pygame.K_LEFT] or comandos[pygame.K_a]:
            self.x -= deslocamento
        if comandos[pygame.K_RIGHT] or comandos[pygame.K_d]:
            self.x += deslocamento
        self.forma.x = int(self.x)
        self.forma.y = int(self.y)
    def desenhar(self, tela):
        pygame.draw.rect(tela, (2, 120, 200), self.forma)