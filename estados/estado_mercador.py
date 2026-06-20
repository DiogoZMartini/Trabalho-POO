import pygame
from .estado_base import EstadoBase
from utilidade.itens import Item
from entidades.inimigo import Mercador

class EstadoMercador(EstadoBase):
    def __init__(self, jogador):
        super().__init__()
        pygame.font.init()
        self.fonte = pygame.font.SysFont(None, 30)
        self.fonte_titulo = pygame.font.SysFont(None, 50)
        
        self.jogador = jogador
        self.voltar = pygame.Rect(20, 20, 40, 40)
        
        # Abas da Loja: "COMPRAR", "VENDER" ou iniciar "ATAQUE"
        self.aba_atual = "COMPRAR" 
        self.tab_comprar = pygame.Rect(130, 100, 160, 40) # Posições que acertamos para não sobrepor
        self.tab_vender = pygame.Rect(300, 100, 160, 40)
        self.btn_atacar = pygame.Rect(600, 100, 100, 40) # Botão de agressão externa
        
        # Sistema de mensagens visuais
        self.mensagem_feedback = ""
        self.tempo_feedback = 0

        # CONFIGURAÇÃO DE ITENS (Ordem corrigida):
        self.quantidade_itens_loja = 5  # 1º Define a quantidade primeiro
        self.itens_loja = []            # 2º Cria a lista vazia
        self.carregar_itens_do_banco()  # 3º Só agora carrega do banco de dados!

        self.mercador = Mercador.gerarInimigoAleatorio(jogador.getLvl(), 'Mercador')


    def carregar_itens_do_banco(self):
        y_inicial = 170
        for idx in range(0,5):
            rect_botao = pygame.Rect(100, y_inicial + (idx * 60), 600, 50)
            idx = Item.gerarItemAleatorio()
            if idx.preco == 0:
                while True:
                    idx = Item.gerarItemAleatorio()
                    if idx.preco != 0:
                        break
            for item in self.itens_loja:
                dados = item["dados_brutos"]
                if idx.nome == dados.nome:
                    while True:
                        idx = Item.gerarItemAleatorio()
                        if idx.nome != dados.nome:
                            break
            self.itens_loja.append({
                "dados_brutos": idx,
                "rect": rect_botao
            })


    def tratarEventos(self, listaEventos):
        mx, my = pygame.mouse.get_pos()
        click = False
        from .estado_combate import EstadoCombate
        for event in listaEventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.proximoEstado = EstadoCombate(self.jogador)
                self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                click = True 
                    
        if click:
            if self.voltar.collidepoint((mx, my)):
                self.proximoEstado = EstadoCombate(self.jogador)
                self.concluido = True
                return

            # Alternar Abas e Ações Principais
            if self.tab_comprar.collidepoint((mx, my)):
                self.aba_atual = "COMPRAR"
            elif self.tab_vender.collidepoint((mx, my)):
                self.aba_atual = "VENDER"
            elif self.btn_atacar.collidepoint((mx, my)):
                print(f"[COMBATE] Você atacou o Mercador! Iniciando batalha de vida ou morte...")
                # Redireciona direto para a tela de Luta puxando o Mercador do banco!
                self.proximoEstado = EstadoCombate(self.jogador, nomeInimigoAlvo="Mercador")
                self.concluido = True
                return
                
            # Interação com as listagens baseado na Aba Ativa
            if self.aba_atual == "COMPRAR":
                for item in self.itens_loja:
                    if item["rect"].collidepoint((mx, my)):
                        self.processar_compra(item["dados_brutos"])
            
            elif self.aba_atual == "VENDER":
                # Mapeia cliques dinâmicos nos itens reais da mochila do jogador
                y_inicial = 170
                for idx, item_objeto in enumerate(self.jogador.inv.mochila):
                    rect_venda = pygame.Rect(100, y_inicial + (idx * 60), 600, 50)
                    if rect_venda.collidepoint((mx, my)):
                        self.processar_venda(idx)
                        break

    def processar_compra(self, dados_item):
        sucesso, mensagem = self.mercador.comparItem(dados_item, self.jogador)
        self.mensagem_feedback = mensagem
        self.tempo_feedback = 90

    def processar_venda(self, index_item):
        sucesso, mensagem = self.mercador.venderItem(index_item, self.jogador)
        self.mensagem_feedback = mensagem
        self.tempo_feedback = 90

    def desenhar(self, tela):
        tela.fill((45, 30, 20)) # Fundo taverna
        pygame.draw.polygon(tela, 'gray', [self.voltar.midleft, self.voltar.topright, self.voltar.bottomright])
        
        # Render Cabeçalho Geral
        txt_titulo = self.fonte_titulo.render("MERCADOR", True, (240, 190, 60))
        txt_dinheiro = self.fonte.render(f"Seu Dinheiro: {self.jogador.getDinheiro()}g", True, (255, 215, 0))
        tela.blit(txt_titulo, (100, 40))
        tela.blit(txt_dinheiro, (520, 45))
        
        # Desenhar Abas Superiores de Navegação
        cor_compra = (140, 100, 70) if self.aba_atual == "COMPRAR" else (70, 55, 45)
        cor_venda = (140, 100, 70) if self.aba_atual == "VENDER" else (70, 55, 45)
        
        # Desenho físico dos botões de fundo
        pygame.draw.rect(tela, cor_compra, self.tab_comprar, border_radius=4)
        pygame.draw.rect(tela, cor_venda, self.tab_vender, border_radius=4)
        pygame.draw.rect(tela, (200, 50, 50), self.btn_atacar, border_radius=4) # Botão Perigo
        
        # 1. Renderiza os textos na memória
        txt_aba_comprar = self.fonte.render("Comprar Itens", True, (255, 255, 255))
        txt_aba_vender = self.fonte.render("Vender Bolsa", True, (255, 255, 255))
        txt_aba_atacar = self.fonte.render("ATACAR", True, (255, 255, 255))

        # 2. Desenha na tela calculando o centro automático de cada botão
        tela.blit(txt_aba_comprar, txt_aba_comprar.get_rect(center=self.tab_comprar.center))
        tela.blit(txt_aba_vender, txt_aba_vender.get_rect(center=self.tab_vender.center))
        tela.blit(txt_aba_atacar, txt_aba_atacar.get_rect(center=self.btn_atacar.center))

        # Renderização condicional da lista de itens
        y_inicial = 170
        if self.aba_atual == "COMPRAR":
            for item in self.itens_loja:
                dados = item["dados_brutos"]
                pode_comprar = self.jogador.getDinheiro() >= int(dados.preco)
                cor_rect = (90, 70, 50) if pode_comprar else (55, 45, 40)
                
                pygame.draw.rect(tela, cor_rect, item["rect"], border_radius=5)
                pygame.draw.rect(tela, (160, 120, 80), item["rect"], width=1, border_radius=5)
                
                # --- SISTEMA DE CORES POR RARIDADE (COMPRA) ---
                raridade = dados.raridade
                if raridade == "Raro":
                    cor_nome = (30, 144, 255)     # Azul
                elif raridade == "Epico":
                    cor_nome = (163, 73, 164)    # Roxo
                elif raridade == "Lendario":
                    cor_nome = (255, 127, 39)    # Laranja
                else:
                    cor_nome = (255, 255, 255)   # Branco
                txt_nome = self.fonte.render(f"{dados.nome} ({dados.tipo})", True, cor_nome)
                txt_preco = self.fonte.render(f"{dados.preco}g", True, (255, 215, 0) if pode_comprar else (240, 100, 100))
                tela.blit(txt_nome, (item["rect"].x + 20, item["rect"].y + 15))
                tela.blit(txt_preco, (item["rect"].x + 500, item["rect"].y + 15))

        elif self.aba_atual == "VENDER":
            if not self.jogador.inv.mochila:
                tela.blit(self.fonte.render("Sua mochila está vazia!", True, (150, 150, 150)), (100, 200))
            else:
                for idx, item_objeto in enumerate(self.jogador.inv.mochila):
                    rect_venda = pygame.Rect(100, y_inicial + (idx * 60), 600, 50)
                    pygame.draw.rect(tela, (75, 85, 75), rect_venda, border_radius=5)
                    pygame.draw.rect(tela, (100, 130, 100), rect_venda, width=1, border_radius=5)
                    
                    # --- SISTEMA DE CORES POR RARIDADE (VENDA) ---
                    raridade = item_objeto.getRaridade()
                    if raridade == "Raro":
                        cor_nome = (30, 144, 255)
                    elif raridade == "Epico":
                        cor_nome = (163, 73, 164)
                    elif raridade == "Lendario":
                        cor_nome = (255, 127, 39)
                    else:
                        cor_nome = (255, 255, 255)
                    
                    valor_reembolso = max(1, int(item_objeto.getPreco() // 2))
                    txt_nome = self.fonte.render(f"{item_objeto.getNome()} ({item_objeto.getTipo()})", True, cor_nome)
                    txt_preco = self.fonte.render(f"+{valor_reembolso}g", True, (100, 255, 100))
                    tela.blit(txt_nome, (rect_venda.x + 20, rect_venda.y + 15))
                    tela.blit(txt_preco, (rect_venda.x + 500, rect_venda.y + 15))

        if self.tempo_feedback > 0:
            cor_msg = (100, 255, 100) if "Comprou" in self.mensagem_feedback or "Vendeu" in self.mensagem_feedback else (255, 100, 100)
            txt_msg = self.fonte.render(self.mensagem_feedback, True, cor_msg)
            tela.blit(txt_msg, txt_msg.get_rect(center=(400, 565)))
            self.tempo_feedback -= 1
