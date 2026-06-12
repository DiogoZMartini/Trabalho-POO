import pygame
from .estado_base import EstadoBase

class Derrota(EstadoBase):
    def __init__(self):
        super().__init__()
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        self.back = pygame.Rect(250, 50, 200, 75)
        self.back.center = (400, 515)
        self.derrota = pygame.Rect(250, 50, 450, 90)
        self.derrota.center = (400, 70)
        self.pause = True
        # Cria uma caixa de 400x500 pixels
        self.pop_derrota = pygame.Rect(0, 0, 450, 550)
        #Centraliza ela no meio da tela (400, 300)
        self.pop_derrota.center = (400, 300)
    
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
            if self.back.collidepoint((mx, my)):
                self.proximoEstado = "MenuPrincipal"
                self.concluido = True
            
    def desenhar(self, tela):
            # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'blue', self.pop_derrota)
        pygame.draw.rect(tela, 'gray', self.back)
        pygame.draw.rect(tela, 'gray', self.derrota)
            
            # 1. Renderiza os textos (Texto, Antialiasing, Cor do Texto)
        txt_back = self.fonte.render("Voltar", True, (0, 0, 0))
        txt_derrota = self.fonte.render("Derrota!", True, (0, 0, 0))
          
            # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_back = txt_back.get_rect(center= self.back.center)
        rect_txt_derrota = txt_derrota.get_rect(center= self.derrota.center)    
            
            # 3. Desenha os textos na tela
        tela.blit(txt_back, rect_txt_back)
        tela.blit(txt_derrota, rect_txt_derrota)