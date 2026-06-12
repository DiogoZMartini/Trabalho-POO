import pygame
from .estado_base import EstadoBase

class Saves(EstadoBase):
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
        self.voltar = pygame.Rect(20,20,40,40)
        #guardar o save selecionado
        self.slot_selecionado = 0

    def tratarEventos(self, listaEventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in listaEventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.proximoEstado = "MenuPrincipal"
                    self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True 
            # 3. Se houve clique em qualquer momento do frame, checa as colisões
        if click:
            if self.voltar.collidepoint((mx, my)):
                self.proximoEstado = "MenuPrincipal"
                self.concproximoEstadoluido = True
            elif self.save1.collidepoint((mx, my)):
                self.slot_selecionado = 1
                self.proximoEstado = "NewGame"
                self.concluido = True
            elif self.save2.collidepoint((mx, my)):
                self.slot_selecionado = 2
                self.proximoEstado = "NewGame"
                self.concluido = True
            elif self.save3.collidepoint((mx, my)):
                self.slot_selecionado = 3
                self.proximoEstado = "NewGame"
                self.concluido = True
    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.save1)
        pygame.draw.rect(tela, 'gray', self.save2)
        pygame.draw.rect(tela, 'gray', self.save3)
        pygame.draw.polygon(tela, 'gray', [(20, 40), (60, 20), (60, 60)])
        
        txt_save1 = self.fonte.render("SAVE 1", True, (0, 0, 0))
        txt_save2 = self.fonte.render("SAVE 2", True, (0, 0, 0))
        txt_save3 = self.fonte.render("SAVE 3", True, (0, 0, 0))
        
        # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_save1 = txt_save1.get_rect(center= self.save1.center)
        rect_txt_save2 = txt_save2.get_rect(center= self.save2.center)
        rect_txt_save3 = txt_save3.get_rect(center= self.save3.center)
        
        # 3. Desenha os textos na tela
        tela.blit(txt_save1, rect_txt_save1)
        tela.blit(txt_save2, rect_txt_save2)
        tela.blit(txt_save3, rect_txt_save3)


