import pygame
from .estado_base import EstadoBase
from .estado_classes import Classes

class NewGame(EstadoBase):
    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.fonte = pygame.font.SysFont(None, 40)
        
        # Inicia os dados limpos
        self.reiniciar()
        
        # Botões
        self.nome = pygame.Rect(150, 300, 450, 80)
        self.nome.center = (400, 300)
        self.confirmar = pygame.Rect(150, 300, 200, 50)
        self.confirmar.center = (400, 550)
        self.voltar = pygame.Rect(20, 20, 40, 40)

    def reiniciar(self):
        self.nomeJogador = ""
        # Ativa o modo de digitação moderno do pygame-ce
        pygame.key.start_text_input()

    def tratarEventos(self, listaEventos):
        mx, my = pygame.mouse.get_pos()
        click = False
        
        for event in listaEventos:
            # 1. CAPTURA DE TEXTO MODERNA (pygame-ce)
            if event.type == pygame.TEXTINPUT:
                if len(self.nomeJogador) < 15:
                    self.nomeJogador += event.text

            # 2. CAPTURA DE TECLAS DE COMANDO
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.key.stop_text_input() # Para de ouvir o teclado
                    self.proximoEstado = "Saves"
                    self.concluido = True
                    self.reiniciar() # Reseta o nome para a próxima vez
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.nomeJogador = self.nomeJogador[:-1]
                    
                elif event.key == pygame.K_RETURN and len(self.nomeJogador) > 0:
                    pygame.key.stop_text_input()
                    self.proximoEstado = Classes(self.nomeJogador)
                    self.concluido = True
                    self.reiniciar() # Reseta para quando criarem outro jogo

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True 
            
            if click:
                if self.voltar.collidepoint((mx, my)):
                    pygame.key.stop_text_input()
                    self.proximoEstado = "Saves"
                    self.concluido = True
                    self.reiniciar() # Reseta ao clicar em voltar
                    
                if self.confirmar.collidepoint((mx, my)) and len(self.nomeJogador) > 0:
                    pygame.key.stop_text_input()
                    self.proximoEstado = Classes(self.nomeJogador)
                    self.concluido = True
                    self.reiniciar() # Reseta após avançar com sucesso

    def desenhar(self, tela):
        tela.fill((40, 40, 50))
        pygame.draw.rect(tela, 'gray', self.nome)
        pygame.draw.rect(tela, 'gray', self.confirmar)
        pygame.draw.polygon(tela, 'gray', [self.voltar.midleft, self.voltar.topright, self.voltar.bottomright])
      
        txt_confirmar = self.fonte.render("Confirmar", True, (0, 0, 0))
        txt_nome = self.fonte.render("Qual o seu nome?", True, (255, 255, 255))
        
        # Adicionado um caractere '|' no final para simular o cursor de digitação piscando
        txt_digitado = self.fonte.render(self.nomeJogador + "|", True, (0, 0, 0))
        
        rect_txt_confirmar = txt_confirmar.get_rect(center=self.confirmar.center)
        rect_txt_nome = txt_nome.get_rect(midbottom=self.nome.midtop)
        rect_txt_nome.y -= 10
        rect_txt_digitado = txt_digitado.get_rect(center=self.nome.center)
        
        tela.blit(txt_confirmar, rect_txt_confirmar)
        tela.blit(txt_nome, rect_txt_nome)
        tela.blit(txt_digitado, rect_txt_digitado)
