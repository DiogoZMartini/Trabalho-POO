import pygame
from .estado_base import EstadoBase
from banco import carregarJogo
from .estado_combate import EstadoCombate

class Saves(EstadoBase):
    def __init__(self, modo="novo"):
        super().__init__()
        self.modo = modo
        self.slotAtivo = 1
        # Inicializa o sistema de fontes do Pygame
        pygame.font.init()
        # Define a fonte (Nome da fonte ou None para padrão, Tamanho)
        self.fonte = pygame.font.SysFont(None, 32)
        
        # Seus botões originais
        self.save1 = pygame.Rect(150, 300, 150, 300)
        self.save1.center = (200, 300)
        self.save2 = pygame.Rect(300, 300, 150, 300)
        self.save2.center = (400, 300)
        self.save3 = pygame.Rect(450, 300, 150, 300)
        self.save3.center = (600, 300)
        self.voltar = pygame.Rect(20, 20, 40, 40)
        #guardar o save selecionado
        self.slot_selecionado = 0

    def tratarEventos(self, listaEventos):
        # 1. Pega a posição do mouse uma única vez no frame
        mx, my = pygame.mouse.get_pos()
        click = False
        
        # 2. Varre a lista de eventos que o Gerenciador passou
        for event in listaEventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.proximoEstado = "MenuPrincipal"
                    self.concluido = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique com botão esquerdo
                    click = True 
            # 3. Se houve clique em qualquer momento do frame, checa as colisões
        if click:
            if self.voltar.collidepoint((mx, my)):
                self.proximoEstado = "MenuPrincipal"
                self.concluido = True
                return

            slotClicado = None
            if self.save1.collidepoint((mx, my)):
                slotClicado = 1
            elif self.save2.collidepoint((mx, my)):
                slotClicado = 2
            elif self.save3.collidepoint((mx, my)):
                slotClicado = 3

            if slotClicado is not None:
                Saves.slotAtivo = slotClicado  # Define globalmente qual slot o jogador está usando
                if self.modo == "carregar":
                    dadosSalvos = carregarJogo(slotClicado)
                    if dadosSalvos:
                        from entidades.jogador import Jogador
                        jogadorCarregado = Jogador(
                            nome=dadosSalvos['nome'],
                            classe=dadosSalvos['classe'],
                            dano=dadosSalvos['dano'],
                            vida=dadosSalvos['vida'],
                            vidaMaxima=dadosSalvos['vidaMaxima'],
                            lvl=dadosSalvos['lvl'],
                            spa=dadosSalvos['spa'],
                            spaEnergia=dadosSalvos['spaEnergia'],
                            exp=dadosSalvos['exp'],
                            dinheiro=dadosSalvos['dinheiro']
                        )
                        if 'maxXp' in dadosSalvos:
                            jogadorCarregado.maxXp = dadosSalvos['maxXp']
                            # Reconstrói a mochila
                        if 'inv' in dadosSalvos and hasattr(jogadorCarregado, 'inv'):
                            jogadorCarregado.inv.mochila = []
                            for dados_item in dadosSalvos['inv']:
                                if dados_item:
                                    item_objeto = jogadorCarregado.inv.dicionarioParaObjeto(dados_item)
                                    jogadorCarregado.inv.mochila.append(item_objeto)
                            # Reconstrói os equipamentos
                        if 'equipamentos' in dadosSalvos and hasattr(jogadorCarregado, 'inv') and hasattr(
                                jogadorCarregado.inv, 'equipamentos'):
                            for slot, dados_item in dadosSalvos['equipamentos'].items():
                                if dados_item:
                                    item_objeto = jogadorCarregado.inv.dicionarioParaObjeto(dados_item)
                                    jogadorCarregado.inv.equipamentos[slot] = item_objeto
                                else:
                                    jogadorCarregado.inv.equipamentos[slot] = None
                         # Sincroniza a mochila internamente com o jogador
                        jogadorCarregado.setInv(jogadorCarregado.inv.mochila)
                        self.proximoEstado = EstadoCombate(jogadorCarregado)
                        self.concluido = True
                    else:
                        print(f"O Slot {slotClicado} está vazio! Não é possível carregar.")
                else:
                    # Se o modo for "novo", prossegue para a criação de personagem normalmente
                    self.proximoEstado = "NewGame"
                    self.concluido = True

    def desenhar(self, tela):
        # Pinta o fundo
        tela.fill((40, 40, 50))
        # Desenha os retângulos dos botões
        pygame.draw.rect(tela, 'gray', self.save1)
        pygame.draw.rect(tela, 'gray', self.save2)
        pygame.draw.rect(tela, 'gray', self.save3)
        pygame.draw.polygon(tela, 'gray', [(20, 40), (60, 20), (60, 60)])

        # Busca dinamicamente os dados no TinyDB para exibir na interface
        dados1 = carregarJogo(1)
        dados2 = carregarJogo(2)
        dados3 = carregarJogo(3)
        txt1 = f"{dados1['nome']} (Lvl {dados1['lvl']})" if dados1 else "VAZIO"
        txt2 = f"{dados2['nome']} (Lvl {dados2['lvl']})" if dados2 else "VAZIO"
        txt3 = f"{dados3['nome']} (Lvl {dados3['lvl']})" if dados3 else "VAZIO"
        txtS1Titulo = self.fonte.render("SAVE 1", True, (0, 0, 0))
        txtS1Info = self.fonte.render(txt1, True, (50, 50, 50))
        txtS2Titulo = self.fonte.render("SAVE 2", True, (0, 0, 0))
        txtS2Info = self.fonte.render(txt2, True, (50, 50, 50))
        txtS3Titulo = self.fonte.render("SAVE 3", True, (0, 0, 0))
        txtS3Info = self.fonte.render(txt3, True, (50, 50, 50))
        # Desenha Títulos e Infos centralizados nos respectivos cartões
        tela.blit(txtS1Titulo, txtS1Titulo.get_rect(center=(self.save1.centerx, self.save1.centery - 40)))
        tela.blit(txtS1Info, txtS1Info.get_rect(center=(self.save1.centerx, self.save1.centery + 10)))
        tela.blit(txtS2Titulo, txtS2Titulo.get_rect(center=(self.save2.centerx, self.save2.centery - 40)))
        tela.blit(txtS2Info, txtS2Info.get_rect(center=(self.save2.centerx, self.save2.centery + 10)))
        tela.blit(txtS3Titulo, txtS3Titulo.get_rect(center=(self.save3.centerx, self.save3.centery - 40)))
        tela.blit(txtS3Info, txtS3Info.get_rect(center=(self.save3.centerx, self.save3.centery + 10)))


