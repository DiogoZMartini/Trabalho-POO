import pygame
from .estado_base import EstadoBase

class MenuPause(EstadoBase):
    def __init__(self):
        super().__init__()
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        self.resume = pygame.Rect(250, 50, 250, 100)
        self.resume.center = (400, 100)
        self.options = pygame.Rect(250, 30, 250, 100)
        self.options.center = (400, 300)
        self.voltamenu = pygame.Rect(250, 10, 250, 100)
        self.voltamenu.center = (400, 500)
        self.pause = True
        # Cria uma caixa de 400x500 pixels
        self.caixa_pop = pygame.Rect(0, 0, 400, 550)
        #Centraliza ela no meio da tela (400, 300)
        self.caixa_pop.center = (400, 300)
    def tratarEventos(self, listaEventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in listaEventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True 
        
        # 3. Se houve clique em qualquer momento do frame, checa as colisões
        if click:
            if self.resume.collidepoint((mx, my)):
                self.pause = False
                pass
            elif self.options.collidepoint((mx, my)):
                pass
            elif self.voltamenu.collidepoint((mx, my)):
                self.proximo_estado = "Menuprincipal"
                self.concluido = True
    

    def desenhar(self, tela):
            # Desenha os retângulos dos botões
        pygame.draw.rect(tela, (46, 85, 217), self.caixa_pop)
        pygame.draw.rect(tela, 'gray', self.resume)
        pygame.draw.rect(tela, 'gray', self.options)
        pygame.draw.rect(tela, 'gray', self.voltamenu)
            
            # 1. Renderiza os textos (Texto, Antialiasing, Cor do Texto)
        txt_resume = self.fonte.render("Resume", True, (0, 0, 0))
        txt_options = self.fonte.render("Opções", True, (0, 0, 0))
        txt_voltamenu = self.fonte.render("Sair", True, (0, 0, 0))
            
            # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_resume = txt_resume.get_rect(center= self.resume.center)
        rect_txt_options = txt_options.get_rect(center= self.options.center)
        rect_txt_voltamenu = txt_voltamenu.get_rect(center= self.voltamenu.center)
            
            # 3. Desenha os textos na tela
        tela.blit(txt_resume, rect_txt_resume)
        tela.blit(txt_options, rect_txt_options)
        tela.blit(txt_voltamenu, rect_txt_voltamenu)
