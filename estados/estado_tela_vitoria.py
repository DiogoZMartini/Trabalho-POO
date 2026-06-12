import pygame
from .estado_base import EstadoBase

class Vitoria(EstadoBase):
    def __init__(self, jogador):
        super().__init__()
        self.jogador = jogador
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        self.concluir = pygame.Rect(250, 50, 200, 75)
        self.concluir.center = (400, 515)
        self.vitory = pygame.Rect(250, 50, 450, 90)
        self.vitory.center = (400, 70)
        self.pause = True
        # Cria uma caixa de 400x500 pixels
        self.pop_vitoria = pygame.Rect(0, 0, 450, 550)
        #Centraliza ela no meio da tela (400, 300)
        self.pop_vitoria.center = (400, 300)
    
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
            if self.concluir.collidepoint((mx, my)):
                from .estado_combate import EstadoCombate
                self.proximoEstado = EstadoCombate(self.jogador)
                self.concluido = True
            
    def desenhar(self, tela):
            # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'blue', self.pop_vitoria)
        pygame.draw.rect(tela, 'gray', self.concluir)
        pygame.draw.rect(tela, 'gray', self.vitory)
            
            # 1. Renderiza os textos (Texto, Antialiasing, Cor do Texto)
        txt_concluir = self.fonte.render("Concluir", True, (0, 0, 0))
        txt_vitoria = self.fonte.render("Vitória!", True, (0, 0, 0))
          
            # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_concluir = txt_concluir.get_rect(center= self.concluir.center)
        rect_txt_vitoria = txt_vitoria.get_rect(center= self.vitory.center)    
            
            # 3. Desenha os textos na tela
        tela.blit(txt_concluir, rect_txt_concluir)
        tela.blit(txt_vitoria, rect_txt_vitoria)