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
        self.start = pygame.Rect(150, 300, 150, 300)
        self.start.center = (200, 300)
        self.load = pygame.Rect(300, 300, 150, 300)
        self.load.center = (400, 300)
        self.quit = pygame.Rect(450, 300, 150, 300)
        self.quit.center = (600, 300)

    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.start)
        pygame.draw.rect(tela, 'gray', self.load)
        pygame.draw.rect(tela, 'gray', self.quit)
        # 1. Renderiza os textos (Texto, Antialiasing, Cor do Texto)
        '''
        txt_start = self.fonte.render("Novo jogo", True, (0, 0, 0))
        txt_load = self.fonte.render("Carregar", True, (0, 0, 0))
        txt_quit = self.fonte.render("Sair", True, (0, 0, 0))
        # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_start = txt_start.get_rect(center=self.start.center)
        rect_txt_load = txt_load.get_rect(center=self.load.center)
        rect_txt_quit = txt_quit.get_rect(center=self.quit.center)
        # 3. Desenha os textos na tela
        tela.blit(txt_start, rect_txt_start)
        tela.blit(txt_load, rect_txt_load)
        tela.blit(txt_quit, rect_txt_quit)
'''