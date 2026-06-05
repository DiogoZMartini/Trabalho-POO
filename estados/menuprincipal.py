import pygame
from .estado_base import EstadoBase

class MenuPrincipal(EstadoBase):
    def __init__(self):
        super().__init__()
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        self.start = pygame.Rect(250, 50, 250, 100)
        self.start.center = (400, 100)
        self.load = pygame.Rect(250, 30, 250, 100)
        self.load.center = (400, 300)
        self.quit = pygame.Rect(250, 10, 250, 100)
        self.quit.center = (400, 500)
    def tratarEventos(self, lista_eventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True 
        
        # 3. Se houve clique em qualquer momento do frame, checa as colisões
        if click:
            if self.start.collidepoint((mx, my)):
                self.proximo_estado = "Saves" 
                self.concluido = True
            elif self.load.collidepoint((mx, my)):
                self.proximo_estado = "Saves" 
                self.concluido = True
            elif self.quit.collidepoint((mx, my)):
                pygame.quit()
                import sys; sys.exit()

    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.start)
        pygame.draw.rect(tela, 'gray', self.load)
        pygame.draw.rect(tela, 'gray', self.quit)
        
        # 1. Renderiza os textos (Texto, Antialiasing, Cor do Texto)
        txt_start = self.fonte.render("Novo jogo", True, (0, 0, 0))
        txt_load = self.fonte.render("Carregar", True, (0, 0, 0))
        txt_quit = self.fonte.render("Sair", True, (0, 0, 0))
        
        # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_start = txt_start.get_rect(center= self.start.center)
        rect_txt_load = txt_load.get_rect(center= self.load.center)
        rect_txt_quit = txt_quit.get_rect(center= self.quit.center)
        
        # 3. Desenha os textos na tela
        tela.blit(txt_start, rect_txt_start)
        tela.blit(txt_load, rect_txt_load)
        tela.blit(txt_quit, rect_txt_quit)
