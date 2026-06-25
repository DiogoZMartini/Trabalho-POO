import pygame
from .estado_base import EstadoBase
from .estado_menupause import MenuPause
import random
from .estado_mercador import EstadoMercador

class Vitoria(EstadoBase):
    def __init__(self, jogador, exp_ganha, dinheiro_ganho, item_ganho):
        super().__init__()
        self.jogador = jogador
        self.exp_ganha = exp_ganha
        self.dinheiro_ganho = dinheiro_ganho
        self.itemGanho = item_ganho
        self.itemColetado = False
        self.mensagemErro = ""
        self.mostrarInventario = False
        self.menuPause = MenuPause()
        self.jogoPausado = False
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 40)
        self.fonteDrops = pygame.font.SysFont(None, 32)
        self.fonteItem = pygame.font.SysFont(None, 24)
        self.concluir = pygame.Rect(250, 50, 200, 75)
        self.concluir.center = (400, 515)
        self.vitory = pygame.Rect(250, 50, 450, 90)
        self.vitory.center = (400, 70)
        self.pause = True
        # Cria uma caixa de 400x500 pixels
        self.pop_vitoria = pygame.Rect(0, 0, 450, 550)
        #Centraliza ela no meio da tela (400, 300)
        self.pop_vitoria.center = (400, 300)
        self.rectItemClicavel = pygame.Rect(self.pop_vitoria.x + 20, 250, 410, 42)
    
    def tratarEventos(self, listaEventos):
        if self.jogoPausado:
            self.menuPause.tratarEventos(listaEventos, self.jogador)
            # Verifica se o jogador clicou em "Resume" lá dentro
            if not self.menuPause.pause:
                self.jogoPausado = False
                self.menuPause.pause = True
            # Se o menu de pause acionou uma mudança de estado (voltou pro menu principal)
            if self.menuPause.concluido:
                self.proximoEstado = self.menuPause.proximoEstado
                self.concluido = True
            return

        # Se o inentario estiver aberto faz os eventos dele
        if self.mostrarInventario:
            self.jogador.inv.tratarEventos(listaEventos)

        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in listaEventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                        # Só permite clicar nos botões de vitória se o inventário estiver fechado
                    if not self.mostrarInventario:
                        click = True
                #Abre e fecha o inventário no modo padrão ao apertar "I"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.jogador.inv.modo = "padrao"
                    self.mostrarInventario = not self.mostrarInventario
                    # Se apertar ESC com o inventário aberto, apenas fecha o inventário
                elif event.key == pygame.K_ESCAPE:
                    if self.mostrarInventario:
                        self.mostrarInventario = False  # Se o inventário estiver aberto, apenas fecha ele
                    else:
                        self.jogoPausado = True  # Se estiver fechado, abre o Menu de Pause
                        self.menuPause.pause = True
        
        # 3. Se houve clique em qualquer momento do frame, checa as colisões
        if click:
            if self.concluir.collidepoint((mx, my)):
                if random.random() <= 0.90:  # 90% de chance de aparecer
                    self.proximoEstado = EstadoMercador(self.jogador)
                else:
                    from .estado_combate import EstadoCombate
                    self.proximoEstado = EstadoCombate(self.jogador)
                self.concluido = True
            elif self.itemGanho and not self.itemColetado and self.rectItemClicavel.collidepoint((mx, my)):
                if hasattr(self.jogador, 'getInventario') and len(self.jogador.getInv()) >= 15:
                    self.mensagemErro = "Inventário Cheio! (Máx 15)"
                else:
                    if hasattr(self.jogador, 'addItem'):
                        self.jogador.addItem(self.itemGanho)
                        self.itemColetado = True
                        self.mensagemErro = ""
            
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
            
            # 4. Renderização dos Drops Dinâmicos recebidos do Combate
        xAlinhamento = self.pop_vitoria.x + 50
        txtExp = self.fonteDrops.render(f"XP Ganho: +{self.exp_ganha}", True, (255, 255, 255))
        tela.blit(txtExp, (xAlinhamento, 160))
        txtDinheiro = self.fonteDrops.render(f"Dinheiro: +R$ {self.dinheiro_ganho}", True, (255, 215, 0))
        tela.blit(txtDinheiro, (xAlinhamento, 210))
            #  Drop de Item
        if self.itemGanho:
            nomeItem = self.itemGanho.getNome() if hasattr(self.itemGanho, 'getNome') else str(self.itemGanho)
            if self.itemColetado:
                txtItem = self.fonteItem.render(f"[Coletado] {nomeItem}", True, (120, 120, 120))
            else:
                pygame.draw.rect(tela, (0, 60, 150), self.rectItemClicavel, border_radius=5)
                txtItem = self.fonteItem.render(f"Clique para pegar: {nomeItem}", True, (0, 255, 100))
        else:
            txtItem = self.fonteItem.render("Item Dropado: Nenhum", True, (180, 180, 180))

            # Desenha o texto do item na posição correta
        tela.blit(txtItem, (self.rectItemClicavel.x + 10, self.rectItemClicavel.y + 8))

            # Exibe mensagem de erro vermelha se o inventário tentar estourar os 15 slots
        if self.mensagemErro:
            txt_erro = self.fonteDrops.render(self.mensagemErro, True, (255, 50, 50))
            tela.blit(txt_erro, (xAlinhamento, 310))

            # Linha Divisória e Status do Alfredo
        pygame.draw.line(tela, (200, 200, 200), (xAlinhamento, 360), (self.pop_vitoria.right - 50, 360), 2)

            # Status Atualizado do Jogador (mostra que o valor de fato subiu)
        txtStatusAtual = self.fonteDrops.render(f"{self.jogador.getNome()} Total: R$ {self.jogador.getDinheiro()} | XP: {self.jogador.getExp()}", True,(230, 230, 230))
        tela.blit(txtStatusAtual, (xAlinhamento, 390))

        if self.mostrarInventario:
            superficie_fundo = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
            superficie_fundo.fill((0, 0, 0, 180))
            tela.blit(superficie_fundo, (0, 0))
            self.jogador.inv.desenhar(tela)

        if self.jogoPausado:
            # Cria a película escura transparente
            superficieEscuro = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
            superficieEscuro.fill((0, 0, 0, 150))
            tela.blit(superficieEscuro, (0, 0))
            # Desenha o menu de pause
            self.menuPause.desenhar(tela)