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

    # 2. INSTANCIAÇÃO DOS OBJETOS DE ITENS
    objeto_arma = Item(
        nome="Espada de Aço (Épica)",
        dano=5,
        tipo="Arma",
        descricao="Uma espada afiada feita de puro aço.",
        quantidadeMaxima=1,
        efeito="Nenhum",
        preco=150,
        raridade="Épica"
    )

    objeto_amuleto = Item(
        nome="Amuleto de Fogo",
        dano=2,
        tipo="Colar",
        descricao="Um amuleto que pulsa com energia quente.",
        quantidadeMaxima=1,
        efeito="Dano de Fogo",
        preco=200,
        raridade="Raro"
    )

    objeto_anel = Item(
        nome="Anel do Guerreador",
        dano=2,
        tipo="Anel",
        descricao="Um anel pesado de ferro.",
        quantidadeMaxima=1,
        efeito="Nenhum",
        preco=50,
        raridade="Comum"
    )

    # 3. DADOS BASE DO JOGADOR
    dados_jogador_ficticio = {
        "nome": "Diogo Herói",
        "dano": 2,
        "vida": 120,
        "lvl": 3,
        "recurso": 50,
        "exp": 120,
        "classe": "Guerreiro",
        "dinheiro": 350,
        "spa": "Impacto Devastador"
    }

    # 4. CRIAÇÃO DO OBJETO JOGADOR
    objetoJogador = Jogador(
        nome=dados_jogador_ficticio["nome"],
        dano=dados_jogador_ficticio["dano"],
        vida=dados_jogador_ficticio["vida"],
        lvl=dados_jogador_ficticio["lvl"],
        recurso=dados_jogador_ficticio["recurso"],
        exp=dados_jogador_ficticio["exp"],
        classe=dados_jogador_ficticio["classe"],
        dinheiro=dados_jogador_ficticio["dinheiro"],
        spa=dados_jogador_ficticio["spa"],
        spaEnergia=0
    )

    # 5. ASSIGNAÇÃO RÍGIDA DOS OBJETOS NO INVENTÁRIO DO JOGADOR
    objetoJogador.inv.equipamentos = {
        "Arma": objeto_arma,
        "Colar": objeto_amuleto,
        "Anel": objeto_anel
    }

    print(f"Jogador '{objetoJogador.getNome()}' criado com sucesso!")

    # 6. CONFIGURAÇÃO DO GERENCIADOR DE JOGO
    telaCombate = EstadoCombate(objetoJogador)
    dicionario_estados = {"Combate": telaCombate}

    # PASSANDO POR POSIÇÃO (Sem usar nomes de argumentos como 'tela=')
    # Ordem padrão baseada nos seus erros anteriores:
    # 1º: A tela do Pygame
    # 2º: A altura (600)
    # 3º: O título ("RPG - Teste de Combate")
    # 4º: O dicionário de estados
    # 5º: A string do estado inicial
    try:
        jogo = GerenciadorJogo(
            tela,
            altura,
            "RPG - Teste de Combate",
            dicionario_estados,
            "Combate"
        )
    except TypeError:
        # CASO DÊ ERRO DE ORDEM: Se o seu construtor começar com largura e altura, tenta essa alternativa:
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