import pygame
from .estado_base import EstadoBase

class NewGame(EstadoBase):
    def __init__(self):
        super().__init__()
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        # salvar o nome do jogador
        self.nome_jogador = ""
        # botões
        self.nome = pygame.Rect(150, 300, 450, 80)
        self.nome.center = (400, 300)
        self.confirmar = pygame.Rect(150, 300, 200, 50)
        self.confirmar.center = (400, 550)
        self.voltar = pygame.Rect(20, 20, 40, 40)

    def tratarEventos(self, listaEventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in listaEventos:
            # CORREÇÃO: Toda a checagem de teclado deve ficar DENTRO deste bloco KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.proximoEstado = "Saves"
                    self.concluido = True
                # apagar letras do nome
                elif event.key == pygame.K_BACKSPACE:
                    self.nome_jogador = self.nome_jogador[:-1]
                else:
                    if event.unicode.isprintable() and len(self.nome_jogador) < 15:
                        self.nome_jogador += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True 
            
            # 3. Se houve clique em qualquer momento do frame, checa as colisões
            if click:
                if self.voltar.collidepoint((mx, my)):
                    self.proximoEstado = "Saves"
                    self.concluido = True
                # AJUSTE: Mudei para self.confirmar para fazer sentido com o botão da tela
                if self.confirmar.collidepoint((mx, my)) and len(self.nome_jogador) > 0:
                    print(f"Nome salvo temporariamente: {self.nome_jogador}")
                    self.proximoEstado = "Classes"
                    self.concluido = True
                    # Adicione aqui para onde o jogo deve ir ao confirmar, ex:
                    # self.proximo_estado = "JogoPrincipal"
                    # self.concluido = True

    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.nome)
        pygame.draw.rect(tela, 'gray', self.confirmar)
        # AJUSTE: Usando o self.voltar dinâmico que combinamos antes
        pygame.draw.polygon(tela, 'gray', [self.voltar.midleft, self.voltar.topright, self.voltar.bottomright])
      
        txt_confirmar = self.fonte.render("Confirmar", True, (0, 0, 0))
        txt_nome = self.fonte.render("Qual o seu nome?", True, (255, 255, 255))
        # TEXTO DINÂMICO: Renderiza o nome que está sendo digitado
        txt_digitado = self.fonte.render(self.nome_jogador, True, (0, 0, 0))
        
        # 2. Cria retângulos para os textos e centraliza nos botões
        rect_txt_confirmar = txt_confirmar.get_rect(center=self.confirmar.center)
        rect_txt_nome = txt_nome.get_rect(midbottom=self.nome.midtop)
        rect_txt_nome.y -= 10
        # Centraliza o texto digitado no meio do retângulo do nome
        rect_txt_digitado = txt_digitado.get_rect(center=self.nome.center)
        
        # 3. Desenha os textos na tela
        tela.blit(txt_confirmar, rect_txt_confirmar)
        tela.blit(txt_nome, rect_txt_nome)
        tela.blit(txt_digitado, rect_txt_digitado) # Desenha o texto digitado
