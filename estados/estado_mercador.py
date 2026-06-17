import pygame
from .estado_base import EstadoBase
from banco import tabela_itens
from utilidade.itens import Item  # Classe que você usa no inventário

class Mercador(EstadoBase):
    def __init__(self, jogador):
        super().__init__()
        pygame.font.init()
        self.fonte = pygame.font.SysFont(None, 35)
        self.fonte_titulo = pygame.font.SysFont(None, 50)
        
        # Guardamos a referência do jogador que entrou na loja
        self.jogador = jogador
        
        # Botão para sair da loja
        self.voltar = pygame.Rect(20, 20, 40, 40)
        
        # Carrega os itens direto do seu catálogo do TinyDB
        self.itens_loja = []
        self.carregar_itens_do_banco()
        
        # Sistema de mensagens visuais
        self.mensagem_feedback = ""
        self.tempo_feedback = 0

    def carregar_itens_do_banco(self):
        """Busca os itens no TinyDB e cria os retângulos de clique dinamicamente"""
        todos_itens = tabela_itens.all()
        
        # Filtra para não colocar o Colar do Aventureiro (que custa 0) na loja se não quiser
        itens_validos = [i for i in todos_itens if i.get('preco', 0) > 0]
        
        # Monta a lista com a posição visual de cada um na tela
        y_inicial = 160
        for idx, item_dados in enumerate(itens_validos):
            # Cria um retângulo para cada item listado, um abaixo do outro
            rect_botao = pygame.Rect(100, y_inicial + (idx * 65), 600, 55)
            
            self.itens_loja.append({
                "dados_brutos": item_dados, # Guarda o dicionário do TinyDB
                "rect": rect_botao
            })

    def tratarEventos(self, listaEventos):
        mx, my = pygame.mouse.get_pos()
        click = False
        
        for event in listaEventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.proximoEstado = "MapaPrincipal" # Mude para o seu estado anterior
                    self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    click = True 
                    
        if click:
            # Clique no botão voltar
            if self.voltar.collidepoint((mx, my)):
                self.proximoEstado = "MapaPrincipal"
                self.concluido = True
                
            # Clique em algum produto da loja
            for item in self.itens_loja:
                if item["rect"].collidepoint((mx, my)):
                    self.processar_compra(item["dados_brutos"])

    def processar_compra(self, dados_item):
        """Valida o dinheiro, limite de espaço e insere o item no inventário"""
        preco = dados_item['preco']
        nome_item = dados_item['nome']
        
        # 1. Verifica se o jogador tem espaço na mochila (Limite de 15 que vimos no seu Inventario)
        if len(self.jogador.inv.mochila) >= 15:
            self.mensagem_feedback = "Mochila cheia!"
            self.tempo_feedback = 90
            return

        # 2. Verifica se o jogador tem dinheiro suficiente
        if self.jogador.getDinheiro() >= preco:
            # Deduz o dinheiro do seu objeto jogador
            self.jogador.setDinheiro(self.jogador.getDinheiro() - preco)
            
            # Cria a instância correta do objeto Item usando sua função/classe utilitária
            novo_item = Item(
                nome=dados_item['nome'],
                dano=int(dados_item.get('dano', 0)),
                descricao=dados_item['descricao'],
                quantidadeMaxima=dados_item.get('quantidadeMaxima', 1),
                efeito=dados_item['efeito'],
                preco=dados_item['preco'],
                raridade=dados_item.get('raridade', 'Comum'),
                tipo=dados_item['tipo'],
                img=dados_item.get('img', None),
                uso=dados_item.get('uso', None)
            )
            
            # Adiciona o item direto na mochila do jogador
            self.jogador.inv.mochila.append(novo_item)
            
            # Força o inventário a sincronizar e salvar no TinyDB imediatamente!
            self.jogador.inv.salvarInventario()
            
            self.mensagem_feedback = f"Comprou {nome_item}!"
            print(f"[LOJA] {nome_item} comprado. Dinheiro restante: {self.jogador.getDinheiro()}g")
        else:
            self.mensagem_feedback = "Dinheiro insuficiente!"
            
        self.tempo_feedback = 90 # Tempo em frames que a mensagem fica ativa

    def desenhar(self, tela):
        # Fundo marrom escuro estilo RPG medieval
        tela.fill((45, 30, 20))
        
        # Desenha a seta de voltar usando os pontos dinâmicos que acertamos antes
        pygame.draw.polygon(tela, 'gray', [self.voltar.midleft, self.voltar.topright, self.voltar.bottomright])
        
        # Títulos e exibição do ouro dinâmico do seu jogador
        txt_titulo = self.fonte_titulo.render("MERCADOR DO COLO", True, (240, 190, 60))
        txt_dinheiro = self.fonte.render(f"Seu Dinheiro: {self.jogador.getDinheiro()}g", True, (255, 215, 0))
        tela.blit(txt_titulo, (100, 40))
        tela.blit(txt_dinheiro, (500, 45))
        
        # Subtítulo explicativo
        txt_sub = self.fonte.render("Clique em um artigo para comprar:", True, (180, 180, 180))
        tela.blit(txt_sub, (100, 110))
        
        # Renderiza a lista de produtos
        for item in self.itens_loja:
            dados = item["dados_brutos"]
            pode_comprar = self.jogador.getDinheiro() >= dados["preco"]
            
            # Muda a cor do slot do botão: escuro se for pobre, claro se puder pagar
            cor_botao = (90, 70, 50) if pode_comprar else (55, 45, 40)
            pygame.draw.rect(tela, cor_botao, item["rect"], border_radius=6)
            pygame.draw.rect(tela, (160, 120, 80), item["rect"], width=2, border_radius=6) # Borda metálica
            
            # Renderiza Nome, Tipo e Preço do item
            txt_nome = self.fonte.render(f"{dados['nome']} ({dados['tipo']})", True, (255, 255, 255))
            txt_preco = self.fonte.render(f"{dados['preco']}g", True, (255, 215, 0) if pode_comprar else (240, 100, 100))
            
            # Desenha os textos centralizados verticalmente no retângulo do slot
            tela.blit(txt_nome, (item["rect"].x + 20, item["rect"].y + 15))
            tela.blit(txt_preco, (item["rect"].x + 480, item["rect"].y + 15))

        # Desenha os avisos flutuantes na parte inferior (Ex: "Mochila cheia!")
        if self.tempo_feedback > 0:
            cor_msg = (100, 255, 100) if "Comprou" in self.mensagem_feedback else (255, 100, 100)
            txt_msg = self.fonte.render(self.mensagem_feedback, True, cor_msg)
            rect_msg = txt_msg.get_rect(center=(400, 560))
            tela.blit(txt_msg, rect_msg)
            self.tempo_feedback -= 1
