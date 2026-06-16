from tinydb import TinyDB, Query
import os

diretorio_banco = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(diretorio_banco, 'dados', 'banco.json')
os.makedirs(os.path.join(diretorio_banco, 'dados'), exist_ok=True)
db = TinyDB(caminho)

tabela_jogador = db.table("jogador")
tabela_inimigos = db.table("catalogo_inimigos")
tabela_itens = db.table("catalogo_itens")
tabela_classe = db.table("classe")


def inicializacaoDeCatalogos():
    tabela_inimigos.truncate()
    tabela_itens.truncate()
    tabela_classe.truncate()

    lista_inimigos = [
        {'nome': 'Zumbie', 'vida': 30, 'spa': 'Mordida', 'dano': 5},
        {'nome': 'Esqueleto', 'vida': 20, 'spa': 'Quebra ossos', 'dano': 7},
        {'nome': 'Fantasma', 'vida': 10, 'spa': 'Susto', 'dano': 10},
        {'nome': 'Aranha', 'vida': 20, 'spa': 'Teia', 'dano': 5},
        {'nome': 'Mercador', 'vida': 100, 'spa': 'Arremesso de moedas', 'dano': 20}
    ]
    tabela_inimigos.insert_multiple(lista_inimigos)

    lista_itens = [
        {'nome':'Poção de Vida','dano':20,'descricao':'Uma poção de cura ao utilizar cura pontos de vida','quantidadeMaxima': 5,'efeito':'Cura'
            ,'preco':12,'tipo':'Consumivel','raridade':'Comum','img':'assets/img/itens/pocaoDeVida.jpg','uso':'Cura 20 de vida'},
        {'nome':'Poção de dano','dano':20,'descricao':'Uma poção instável que ao jogar no inimigo causando dano','quantidadeMaxima':1,'efeito':'Causa Dano'
            ,'preco':25,'tipo':'Consumivel','raridade':'Comum','uso':'Causa 20 de dano ao inimigo'},
        {'nome':'Espada de Madeira','dano':2,'descricao':'Uma espada de madeira','quantidadeMaxima':1,'efeito':'Aumenta o Dano'
            ,'preco':14,'tipo':'Arma','raridade':'Comum','uso': '+2 de dano'},
        {'nome':'Armadura de Couro','dano':-3,'descricao':'Uma armadura de couro','quantidadeMaxima':1,'efeito':'Aumenta a Defesa'
            ,'preco':20,'tipo':'Armadura','raridade': 'Comum','uso':'+3 de defesa'},
        {'nome':'Capacete de Couro','dano':-2,'descricao':'Um capacete de couro','quantidadeMaxima':1, 'efeito':'Aumenta a Defesa'
            ,'preco':12,'tipo':'Capacete','raridade':'Comum','uso':'+2 de defesa'},
        {'nome':'Bota de Couro','dano':-1,'descricao':'Uma bota de couro','quantidadeMaxima':1,'efeito':'Aumenta a Defesa'
            ,'preco':12,'tipo':'Armadura', 'raridade': 'Comum','uso': '+1 de defesa'},
        {'nome':'Colar do Aventureiro','dano':1,'descricao':'Um colar que pertencia a um aventureiro','quantidadeMaxima':1,'efeito':'Aumenta o Dano'
            ,'preco':0,'tipo':'Colar','raridade': 'Comum','uso': '+1 de dano'},
        {'nome':'Anel do Gigante','dano':5,'descricao':'Um anel que contem a força de um gigante','quantidadeMaxima':1,'efeito':'Aumenta o Dano'
            ,'preco':100,'tipo':'Anel','raridade':'Comum','uso': '+5 de dano'}
    ]
    tabela_itens.insert_multiple(lista_itens)
    print("Catálogo carregado com sucesso!")

    # Template classe = {'nome':'','dano':,'vida':,'vidaMaxima':,'spa':''}
    lista_classe = [
        {'nome':'Guerreiro','dano':2,'vida':50,'vidaMaxima':50,'spa':'Força Máxima'},
        {'nome':'Mago','dano':4,'vida':30,'vidaMaxima':30,'spa':'Golpe Magico'},
        {'nome':'Pelado','dano':1,'vida':40,'vidaMaxima':40,'spa':'Improviso'}
    ]
    tabela_classe.insert_multiple(lista_classe)

def salvarJogo(slot,nome, vida, dano, vidaMaxima, lvl, spa, spaEnergia, exp, classe, inv, equipamentos, dinheiro, maxXp):
    tabela_jogador.upsert({'slot': slot,'nome':nome,'vida':vida,'dano':dano,'vidaMaxima': vidaMaxima,'lvl':lvl,'spa':spa,'spaEnergia':spaEnergia,'exp':exp,'classe':classe,'inv':inv, 'equipamentos':equipamentos,'dinheiro':dinheiro,'maxXp':maxXp}, Query().nome == nome)

def carregarJogo(slot):
    resultado = tabela_jogador.search(Query().slot == slot)
    if resultado:
        return resultado[0] # Retorna o dicionário com os dados do personagem
    return None

inicializacaoDeCatalogos()