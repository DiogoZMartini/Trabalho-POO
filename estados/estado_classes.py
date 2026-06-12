import pygame
from .estado_base import EstadoBase

class Classes(EstadoBase):
    def __init__(self):
        super().__init__()
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        #guardar a classe selecionada
        self.classe_selecionada = ""
        # Seus botões originais
        self.guerreiro = pygame.Rect(150, 300, 150, 300)
        self.guerreiro.center = (200, 300)
        self.mago = pygame.Rect(300, 300, 150, 300)
        self.mago.center = (400, 300)
        self.pelado = pygame.Rect(450, 300, 150, 300)
        self.pelado.center = (600, 300)
        self.voltar = pygame.Rect(20,20,40,40)      
    def tratarEventos(self, listaEventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in listaEventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.proximoEstado = "NewGame"
                    self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True
            # 3. Se houve clique em qualquer momento do frame, checa as colisões
        if click:
            if self.voltar.collidepoint((mx, my)):
                self.proximoEstado = "NewGame"
                self.concluido = True
            
            elif self.guerreiro.collidepoint((mx, my)):
                self.classe_selecionada = "guerreiro"
                print(self.classe_selecionada)
            elif self.mago.collidepoint((mx, my)):
                self.classe_selecionada = "mago"
                print(self.classe_selecionada)
            elif self.pelado.collidepoint((mx, my)):
                self.classe_selecionada = "pelado"
                print(self.classe_selecionada)
                
    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.guerreiro)
        pygame.draw.rect(tela, 'gray', self.mago)
        pygame.draw.rect(tela, 'gray', self.pelado)
        pygame.draw.polygon(tela, 'gray', [(20, 40), (60, 20), (60, 60)])
        
        txt_guerreiro = self.fonte.render("Guerreiro", True, (0, 0, 0))
        txt_mago = self.fonte.render("Mago", True, (0, 0, 0))
        txt_pelado = self.fonte.render("Pelado", True, (0, 0, 0))
        
        # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_guerreiro = txt_guerreiro.get_rect(center= self.guerreiro.center)
        rect_txt_mago = txt_mago.get_rect(center= self.mago.center)
        rect_txt_pelado = txt_pelado.get_rect(center= self.pelado.center)
        
        # 3. Desenha os textos na tela
        tela.blit(txt_guerreiro, rect_txt_guerreiro)
        tela.blit(txt_mago, rect_txt_mago)
        tela.blit(txt_pelado, rect_txt_pelado)