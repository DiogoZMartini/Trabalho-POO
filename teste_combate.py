import os
import sys
import pygame

# Garante que o Python encontre as pastas do projeto (entidades, estados, componentes, etc.)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- IMPORTS DO SEU SISTEMA ---
from gerenciador import GerenciadorJogo
from entidades.jogador import Jogador
from estados.estado_combate import EstadoCombate

# --- IMPORT DA CLASSE ITEM ---
from utilidade.itens import Item


def rodar_teste_combate():
    # 1. Inicialização Padrão do Pygame
    pygame.init()
    pygame.font.init()

    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("RPG - Teste de Combate Rígido POO")

    print("=== Inicializando Dados de Teste (Fluxo POO) ===")

    # 2. INSTANCIAÇÃO DOS OBJETOS DE ITENS (EQUIPAMENTOS)
    objeto_arma = Item(
        nome="Espada de Aço (Épica)",
        dano=1,
        tipo="Arma",
        descricao="Uma espada afiada feita de puro aço.",
        quantidadeMaxima=1,
        efeito="Nenhum",
        preco=150,
        raridade="Épica"
    )

    objeto_amuleto = Item(
        nome="Amuleto de Fogo",
        dano=1,
        tipo="Colar",
        descricao="Um amuleto que pulsa com energia quente.",
        quantidadeMaxima=1,
        efeito="Dano de Fogo",
        preco=200,
        raridade="Raro"
    )

    objeto_anel = Item(
        nome="Anel do Guerreador",
        dano=1,
        tipo="Anel",
        descricao="Um anel pesado de ferro.",
        quantidadeMaxima=1,
        efeito="Nenhum",
        preco=50,
        raridade="Comum"
    )

    # =================================================================
    # CONSUMÍVEIS PARA A MOCHILA (EFEITO ALTERADO PARA "Cura")
    # =================================================================
    pocao_vida = Item(
        nome="Poção de Vida P",
        dano=30,  # O poder de cura é definido pelo "dano" no seu sistema original
        tipo="Consumivel",
        descricao="Recupera 30 pontos de vida instantaneamente.",
        quantidadeMaxima=5,
        efeito="Cura",  # ALTERADO: Agora bate certinho com o if do itens.py
        preco=25,
        raridade="Comum",
        uso="Cura 30 HP",
        img='assets/img/itens/pocaoDeVida.jpg'
    )

    elixir_energia = Item(
        nome="Elixir de Energia",
        dano=0,
        tipo="Consumivel",
        descricao="Restaura totalmente seus pontos de recurso.",
        quantidadeMaxima=3,
        efeito="RestauraRecurso",
        preco=45,
        raridade="Incomum",
        uso="Restaura Recurso"
    )

    bombinha = Item(
        nome="Bomba de Fumaça",
        dano=15,
        tipo="Consumivel",
        descricao="Causa 15 de dano fixo e confunde o inimigo.",
        quantidadeMaxima=2,
        efeito="Causa Dano",  # Ajustado para bater com seu itens.py padrão
        preco=60,
        raridade="Raro",
        uso="Causa 15 de Dano"
    )

    antidoto = Item(
        nome="Antídoto",
        dano=0,
        tipo="Consumivel",
        descricao="Cura qualquer efeito de veneno ou status negativo.",
        quantidadeMaxima=5,
        efeito="CuraStatus",
        preco=15,
        raridade="Comum",
        uso="Cura Veneno"
    )

    # 3. DADOS BASE DO JOGADOR
    dados_jogador_ficticio = {
        "nome": "Herói",
        "dano": 1,
        "vida": 80,         # Iniciamos com 80 para poder testar a cura até 120!
        "vidaMaxima": 120,   # Guardamos a referência do limite máximo
        "lvl": 3,
        "exp": 120,
        "classe": "Guerreiro",
        "dinheiro": 350,
        "spa": "Impacto Devastador",
        "maxXp": 500
    }

    # 4. CRIAÇÃO DO OBJETO JOGADOR
    objetoJogador = Jogador(
        nome=dados_jogador_ficticio["nome"],
        dano=dados_jogador_ficticio["dano"],
        vida=dados_jogador_ficticio["vida"],
        vidaMaxima=dados_jogador_ficticio["vidaMaxima"],
        lvl=dados_jogador_ficticio["lvl"],
        exp=dados_jogador_ficticio["exp"],
        classe=dados_jogador_ficticio["classe"],
        dinheiro=dados_jogador_ficticio["dinheiro"],
        spa=dados_jogador_ficticio["spa"],
        spaEnergia=0,
    )

    # 5. ASSIGNAÇÃO RÍGIDA DOS OBJETOS NO INVENTÁRIO DO JOGADOR
    objetoJogador.inv.equipamentos = {
        "Capacete": None,
        "Colar": objeto_amuleto,
        "Arma": objeto_arma,
        "Armadura": None,
        "Bota": None,
        "Anel": objeto_anel
    }

    # Injeta os itens na mochila do inventário gráfico
    objetoJogador.inv.mochila = [
        pocao_vida,
        elixir_energia,
        bombinha,
        antidoto
    ]

    # Sincroniza a lista de itens com a entidade Jogador
    objetoJogador.setInv(objetoJogador.inv.mochila)

    # INJEÇÃO CRUCIAL: Alimenta o dicionário interno do inventário para simular o banco
    objetoJogador.inv.dadosJogador = {
        "nome": dados_jogador_ficticio["nome"],
        "vida": dados_jogador_ficticio["vida"],
        "vidaMaxima": dados_jogador_ficticio["vidaMaxima"]
    }

    print(f"Jogador '{objetoJogador.getNome()}' criado com sucesso!")
    print(f"Mochila populada com {len(objetoJogador.inv.mochila)} consumíveis para teste.")

    # 6. CONFIGURAÇÃO DO GERENCIADOR DE JOGO
    telaCombate = EstadoCombate(objetoJogador)
    dicionario_estados = {"Combate": telaCombate}

    try:
        jogo = GerenciadorJogo(
            tela,
            altura,
            "RPG - Teste de Combate",
            dicionario_estados,
            "Combate"
        )
    except TypeError:
        jogo = GerenciadorJogo(
            largura,
            altura,
            "RPG - Teste de Combate",
            dicionario_estados,
            "Combate"
        )

    print("\n[SUCESSO] Sistema pronto! Iniciando Loop de Combate...\n")

    # 7. INICIA O LOOP DO JOGO
    jogo.rodar()


if __name__ == "__main__":
    rodar_teste_combate()