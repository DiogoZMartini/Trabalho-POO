import pygame
from .estado_base import EstadoBase
from estados.estado_tela_derrota import Derrota

class Exemplo(EstadoBase):
    def __init__(self):
        super().__init__()
        self.fonte = pygame.font.SysFont('Arial', 40)
        self.vitoria = False
        self.derrota = False
        self.objeto_derrota = Derrota()
    def tratarEventos(self, lista_eventos): # Metodo para tratar todos os eventos (inputs) no frame específico.
        for evento in lista_eventos:
            if self.vitoria:
                self.objeto_vitoria.tratarEventos(lista_eventos)
            if self.derrota:
                self.objeto_derrota.tratarEventos(lista_eventos)
            # 3. Se houve clique em qualquer momento do frame, checa as colisões
            if evento.type == pygame.KEYDOWN: # Verifica se o tipo do evento atual é o pressionamento de QUALQUER tecla do teclado.
                if evento.key == pygame.K_ESCAPE: # Se uma tecla foi pressionada, verifica especificamente se essa tecla é o ESCAPE (ESC)
                    self.proximo_estado = "teste" # Define qual será o texto de identificação da próxima tela
                    self.concluido = True # Muda a flag para True. Isso avisa o Gerenciador que a tela acabou e que pode mudar de estado"
                elif evento.key == pygame.K_CAPSLOCK:
                    self.vitoria = True
                elif evento.key == pygame.K_END:
                    self.derrota = True


    def desenhar(self, tela):
        tela.fill((30, 30, 40)) # Limpa e pinta o fundo da janela inteira
        texto = self.fonte.render("Pagina De Template - Aperte ESC", True, (255, 255, 255)) # Transforma o texto em uma imagem (superfície). O argumento 'True' ativa o Anti-Aliasing, que deixa as bordas das letras suaves e sem serrilhado.
        rect = texto.get_rect(center=tela.get_rect().center) # Cria um retângulo invisível (`rect`) com o tamanho exato da imagem do texto gerada acima e posiciona o centro desse retângulo exatamente no centro do retângulo da janela do jogo.
        tela.blit(texto, rect) # Faz o desenho da imagem do 'texto' na 'tela' do jogo, utilizando a posição do retângulo (`rect`) que calculamos na linha anterior.
        if self.vitoria:
            self.objeto_vitoria.desenhar(tela)
        if self.derrota:
            self.objeto_derrota.desenhar(tela)