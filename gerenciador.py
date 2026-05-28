import pygame
import sys
pygame.init()
class GerenciadorJogo:
    def __init__(self, largura, altura, titulo, estado, estado_inicial):
        self.tela=pygame.display.set_mode((largura, altura)) # Cria a janela principal do jogo com a largura e altura desejadas.
        pygame.display.set_caption(titulo) # Define o título (texto) que vai aparecer na barra superior da janela do jogo.
        self.relogio=pygame.Clock() # Cria um objeto do tipo Clock (Relógio) para controlá o FPS.
        self.rodade=True # Uma variável de controle (booleana). Enquanto for True, o loop principal do jogo continuará rodando.
        self.estado=estado # Guarda o dicionário com todas as cenas do jogo.
        self.nome_estado_atual=estado_inicial # Guarda o nome (texto) da cena que deve começar ativa ao abrir o jogo.
        self.estado_atual=self.estado[self.nome_estado_atual] # Vai até o dicionário de estados, pega a cena correspondente ao nome inicial e a define como a cena ativa.
        self.estado_atual.abrir() # Executa o método de entrada da cena atual para garantir que suas variáveis internas sejam resetadas/iniciadas.

    def mudarEstado(self):
        proximo = self.estado_atual.proximo_estado # Pergunta para a cena que está fechando qual é o nome (string) da próxima cena que deve abrir.
        self.estado_atual.fechar() # Executa a rotina de encerramento da cena atual (útil para salvar dados ou parar músicas daquela tela).
        self.nome_estado_atual=proximo # Atualiza a variável com o nome da nova cena que passará a comandar o jogo.
        self.estado_atual=self.estado[self.nome_estado_atual] # Vai no dicionário de estados, busca a nova cena pelo nome e substitui a cena ativa antiga por ela.
        self.estado_atual.abrir() # Executa o método de abertura da nova cena para prepará-la para aparecer na tela.

    def rodar(self):
        while self.rodade: # Inicia o Game Loop Principal.
            dt = self.relogio.tick(60)/1000.0 # Limita o jogo a 60 FPS e calcula o Delta Time (dt). Dividimos por 1000.0 para transformar o tempo de milissegundos para segundos.
            listaEvento = pygame.event.get() # Captura uma lista com todas as interações do jogador (teclas, cliques, mouse) que aconteceram nesse frame
            for evento in listaEvento:
                if evento.type == pygame.QUIT: # Se o tipo do evento for a ação de clicar no botão "X" para fechar a janela do jogo
                    self.rodade=False # Muda a variável para False, o que fará com que o loop 'while' quebre na próxima verificação
            self.estado_atual.tratarEventos(listaEvento) # Envia a lista de eventos coletados para a cena ativa processar suas próprias interações (ex: detectar o ESC)
            if self.estado_atual.concluido: # Verifica se a cena ativa avisou que terminou seu trabalho e quer ser encerrada
                self.mudarEstado() # Chama a função que faz a transição limpa para a próxima tela
            self.estado_atual.atualizar(dt) # Executa a lógica da cena ativa passando o Delta Time para física fluida
            self.estado_atual.desenhar(self.tela) # Executa os desenhos da cena ativa, passando a nossa janela principal como o quadro onde ela vai desenhar.
            pygame.display.flip() # Atualiza a tela do monitor mostrando tudo o que foi desenhado e processado nesse frame
            sbdajdhsjdosadsapak
        pygame.quit()
        sys.exit()