import pygame
import sys
pygame.init()
class GerenciadorJogo:
    def __init__(self, largura, altura, titulo, estado, estadoInicial):
        self.tela=pygame.display.set_mode((largura, altura)) # Cria a janela principal do jogo com a largura e altura desejadas.
        pygame.display.set_caption(titulo) # Define o título (texto) que vai aparecer na barra superior da janela do jogo.
        self.relogio=pygame.Clock() # Cria um objeto do tipo Clock (Relógio) para controlá o FPS.
        self.rodade=True # Uma variável de controle (booleana). Enquanto for True, o loop principal do jogo continuará rodando.
        self.estado=estado # Guarda o dicionário com todas as cenas do jogo.
        self.nomeEstadoAtual=estadoInicial # Guarda o nome (texto) da cena que deve começar ativa ao abrir o jogo.
        self.estadoAtual=self.estado[self.nomeEstadoAtual] # Vai até o dicionário de estados, pega a cena correspondente ao nome inicial e a define como a cena ativa.
        self.estadoAtual.abrir() # Executa o método de entrada da cena atual para garantir que suas variáveis internas sejam resetadas/iniciadas.

    def mudarEstado(self):
        if self.estadoAtual.concluido:
            proximo = self.estadoAtual.proximoEstado
            # 1. Se for uma String (ex: "NewGame"), busca no dicionário normalmente
            if isinstance(proximo, str):
                self.nomeEstadoAtual = proximo
                self.estadoAtual = self.estado[self.nomeEstadoAtual]
            # 2. Se já for o Objeto de estado pronto (ex: EstadoCombate), usa ele direto!
            else:
                self.estadoAtual = proximo
            # 3. Abre o novo estado e reseta a propriedade concluído
            self.estadoAtual.abrir()
            self.estadoAtual.concluido = False

    def rodar(self):
        while self.rodade: # Inicia o Game Loop Principal.
            dt = self.relogio.tick(60)/1000.0 # Limita o jogo a 60 FPS e calcula o Delta Time (dt). Dividimos por 1000.0 para transformar o tempo de milissegundos para segundos.
            listaEvento = pygame.event.get() # Captura uma lista com todas as interações do jogador (teclas, cliques, mouse) que aconteceram nesse frame
            for evento in listaEvento:
                if evento.type == pygame.QUIT: # Se o tipo do evento for a ação de clicar no botão "X" para fechar a janela do jogo
                    self.rodade=False # Muda a variável para False, o que fará com que o loop 'while' quebre na próxima verificação
            self.estadoAtual.tratarEventos(listaEvento) # Envia a lista de eventos coletados para a cena ativa processar suas próprias interações (ex: detectar o ESC)
            if self.estadoAtual.concluido: # Verifica se a cena ativa avisou que terminou seu trabalho e quer ser encerrada
                self.mudarEstado() # Chama a função que faz a transição limpa para a próxima tela
            self.estadoAtual.atualizar(dt) # Executa a lógica da cena ativa passando o Delta Time para física fluida
            self.estadoAtual.desenhar(self.tela) # Executa os desenhos da cena ativa, passando a nossa janela principal como o quadro onde ela vai desenhar.
            pygame.display.flip() # Atualiza a tela do monitor mostrando tudo o que foi desenhado e processado nesse frame
        pygame.quit()
        sys.exit()