import pygame
from .estado_base import EstadoBase
from entidades.jogador import Jogador
class Teste(EstadoBase):
    def __init__(self):
        super().__init__()
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        
        # Seus botões originais
        self.save1 = pygame.Rect(150, 300, 150, 300)
        self.save1.center = (200, 300)
        self.save2 = pygame.Rect(300, 300, 150, 300)
        self.save2.center = (400, 300)
        self.save3 = pygame.Rect(450, 300, 150, 300)
        self.save3.center = (600, 300)
        self.voltar = pygame

    def tratarEventos(self, lista_eventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in lista_eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.proximo_estado = "Menuprincipal" 
                    self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True 
        
        # 3. Se houve clique em qualquer momento do frame, checa as colisões
        '''
        if click:
            if self.start.collidepoint((mx, my)):
                self.proximo_estado = "teste" 
                self.concluido = True
            elif self.load.collidepoint((mx, my)):
                self.proximo_estado = "teste" 
                self.concluido = True
            elif self.quit.collidepoint((mx, my)):
                pygame.quit()
                import sys; sys.exit()
'''
    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.save1)
        pygame.draw.rect(tela, 'gray', self.save2)
        pygame.draw.rect(tela, 'gray', self.save3)
        pygame.draw.polygon(tela, (0, 0, 0), [(200, 50), (250, 300), (200, 300)])