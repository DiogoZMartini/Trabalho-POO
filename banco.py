from tinydb import TinyDB, Query
import os

diretorio_banco = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(diretorio_banco, 'dados', 'banco.json')
os.makedirs(os.path.join(diretorio_banco, 'dados'), exist_ok=True)
db = TinyDB(caminho)

tabela_jogador = db.table("jogador")
tabela_inimigos = db.table("catalogo_inimigos")
tabela_itens = db.table("catalogo_itens")


def inicializacaoDeCatalogos():
    tabela_inimigos.truncate()
    tabela_itens.truncate()

    lista_inimigos = [
        {'nome': 'Zumbie', 'vida': 30, 'spa': 'Mordida', 'dano': 5},
        {'nome': 'Esqueleto', 'vida': 20, 'spa': 'Quebra ossos', 'dano': 7},
        {'nome': 'Fantasma', 'vida': 10, 'spa': 'Susto', 'dano': 10},
        {'nome': 'Aranha', 'vida': 20, 'spa': 'Teia', 'dano': 5},
        {'nome': 'Mercador', 'vida': 100, 'spa': 'Arremesso de moedas', 'dano': 20}
    ]
    tabela_inimigos.insert_multiple(lista_inimigos)

    lista_itens = [
        {'nome':'Poção de Vida','descricao':'Uma poção de cura que cura 20 pontos de vida','quantidadeMaxima': 5,'efeito':'Cura','preco':12,'tipo':'Consumivel','raridade': 'Comum'},
        {'nome':'Poção de Velocidade','descricao':'Uma poção que faz o seu próximo ataque atingir o alvo uma vez adicional','quantidadeMaxima':2,'efeito':'Segundo Ataque','preco':50,'tipo':'Consumivel','raridade': 'Comum'},
        {'nome':'Poção de dano','descricao':'Uma poção instável que ao jogar no inimigo causa 20 de dano','quantidadeMaxima':1,'efeito': 'Causa Dano','preco':25,'tipo':'Consumivel','raridade': 'Comum'},
        {'nome':'Espada de Madeira','descricao':'Uma espada de madeira','quantidadeMaxima':1,'efeito':'Aumenta o Dano','preco':14,'tipo':'Espada','raridade': 'Comum'},
        {'nome':'Armadura de Couro','descricao':'Uma armadura de coiro','quantidadeMaxima':1,'efeito':'Aumenta a Defesa','preco':20,'tipo':'Peitoral','raridade': 'Comum'}
    ]
    tabela_itens.insert_multiple(lista_itens)
    print("Catálogo carregado com sucesso!")

def salvarJogo(nome, vida, vidaMaxima, lvl, exp, classe, inv, dinheiro):
    tabela_jogador.upsert({'nome':nome,'vida':vida,'vidaMaxima': vidaMaxima,'lvl':lvl,'exp':exp,'classe':classe,'inv':inv,'dinheiro':dinheiro}, Query().name == nome)