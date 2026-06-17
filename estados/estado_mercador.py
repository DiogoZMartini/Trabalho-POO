import pygame
from .estado_base import EstadoBase
from banco import tabela_itens
from utilidade.itens import Item  
from .estado_combate import EstadoCombate # Importa para iniciar a luta caso o jogador ataque

class Mercador(EstadoBase):
    def __init__(self, jogador):
        super().__init__()
        pygame.font.init()
        self.fonte = pygame.font.SysFont(None, 30)
        self.fonte_titulo = pygame.font.SysFont(None, 50)
        
        self.jogador = jogador
        self.voltar = pygame.Rect(20, 20, 40, 40)
        
        # Abas da Loja: "COMPRAR", "VENDER" ou iniciar "ATAQUE"
        self.aba_atual = "COMPRAR" 
        self.tab_comprar = pygame.Rect(100, 100, 150, 40)
        self.tab_vender = pygame.Rect(260, 100, 150, 40)
        self.btn_atacar = pygame.Rect(600, 100, 100, 40) # Botão de agressão externa
        
        self.itens_loja = []
        self.carregar_itens_do_banco()
        
        self.mensagem_feedback = ""
        self.tempo_feedback = 0

    def carregar_itens_do_banco(self):
        """Busca catálogo e gera posições fixas para os botões de COMPRA"""
        todos_itens = tabela_itens.all()
        itens_validos = [i for i in todos_itens if i.get('preco', 0) > 0]
        
        y_inicial = 170
        for idx, item_dados in enumerate(itens_validos):
            rect_botao = pygame.Rect(100, y_inicial + (idx * 60), 600, 50)
            self.itens_loja.append({"dados_brutos": item_dados, "rect": rect_botao})

    def tratarEventos(self, listaEventos):
        mx, my = pygame.mouse.get_pos()
        click = False
        
        for event in listaEventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.proximoEstado = "MapaPrincipal"
                self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                click = True 
                    
        if click:
            if self.voltar.collidepoint((mx, my)):
                self.proximoEstado = "MapaPrincipal"
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
        preco = dados_item['preco']
        if len(self.jogador.inv.mochila) >= 15:
            self.mensagem_feedback = "Mochila cheia!"
            self.tempo_feedback = 90
            return

        if self.jogador.getDinheiro() >= preco:
            self.jogador.setDinheiro(self.jogador.getDinheiro() - preco)
            
            novo_item = Item(
                nome=dados_item['nome'], dano=int(dados_item.get('dano', 0)),
                descricao=dados_item['descricao'], quantidadeMaxima=dados_item.get('quantidadeMaxima', 1),
                efeito=dados_item['efeito'], preco=dados_item['preco'],
                raridade=dados_item.get('raridade', 'Comum'), tipo=dados_item['tipo'],
                img=dados_item.get('img', None), uso=dados_item.get('uso', None)
            )
            self.jogador.inv.mochila.append(novo_item)
            self.jogador.inv.salvarInventario()
            self.mensagem_feedback = f"Comprou {dados_item['nome']}!"
        else:
            self.mensagem_feedback = "Dinheiro insuficiente!"
        self.tempo_feedback = 90

    def processar_venda(self, index_item):
        """Remove o item selecionado e reembolsa metade do preço de catálogo do item"""
        item_para_vender = self.jogador.inv.mochila[index_item]
        # Calcula taxa de revenda (Ex: 50% do valor de compra)
        valor_venda = max(1, int(item_para_vender.getPreco() // 2))
        
        self.jogador.setDinheiro(self.jogador.getDinheiro() + valor_venda)
        nome_removido = item_para_vender.getNome()
        
        # Remove da mochila real do jogador
        self.jogador.inv.mochila.pop(index_item)
        self.jogador.inv.salvarInventario()
        
        self.mensagem_feedback = f"Vendeu {nome_removido} por {valor_venda}g!"
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
        
        pygame.draw.rect(tela, cor_compra, self.tab_comprar, border_radius=4)
        pygame.draw.rect(tela, cor_venda, self.tab_vender, border_radius=4)
        pygame.draw.rect(tela, (200, 50, 50), self.btn_atacar, border_radius=4) # Botão Perigo
        
        tela.blit(self.fonte.render("Comprar Itens", True, (255, 255, 255)), (self.tab_comprar.x + 15, self.tab_comprar.y + 10))
        tela.blit(self.fonte.render("Vender Bolsa", True, (255, 255, 255)), (self.tab_vender.x + 20, self.tab_vender.y + 10))
        tela.blit(self.fonte.render("ATACAR", True, (255, 255, 255)), (self.btn_atacar.x + 12, self.btn_atacar.y + 10))

        # Renderização condicional da lista de itens
        y_inicial = 170
        if self.aba_atual == "COMPRAR":
            for item in self.itens_loja:
                dados = item["dados_brutos"]
                pode_comprar = self.jogador.getDinheiro() >= dados["preco"]
                cor_rect = (90, 70, 50) if pode_comprar else (55, 45, 40)
                
                pygame.draw.rect(tela, cor_rect, item["rect"], border_radius=5)
                pygame.draw.rect(tela, (160, 120, 80), item["rect"], width=1, border_radius=5)
                
                txt_nome = self.fonte.render(f"{dados['nome']} ({dados['tipo']})", True, (255, 255, 255))
                txt_preco = self.fonte.render(f"{dados['preco']}g", True, (255, 215, 0) if pode_comprar else (240, 100, 100))
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
                    
                    valor_reembolso = max(1, int(item_objeto.getPreco() // 2))
                    txt_nome = self.fonte.render(f"{item_objeto.getNome()} ({item_objeto.getTipo()})", True, (255, 255, 255))
                    txt_preco = self.fonte.render(f"+{valor_reembolso}g", True, (100, 255, 100))
                    tela.blit(txt_nome, (rect_venda.x + 20, rect_venda.y + 15))
                    tela.blit(txt_preco, (rect_venda.x + 500, rect_venda.y + 15))

        if self.tempo_feedback > 0:
            cor_msg = (100, 255, 100) if "Comprou" in self.mensagem_feedback or "Vendeu" in self.mensagem_feedback else (255, 100, 100)
            txt_msg = self.fonte.render(self.mensagem_feedback, True, cor_msg)
            tela.blit(txt_msg, txt_msg.get_rect(center=(400, 565)))
            self.tempo_feedback -= 1
