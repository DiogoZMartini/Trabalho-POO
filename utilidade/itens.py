from tinydb import Query
import random

def criarItemComRaridade (nomeBase, tipoItem, efeitoBase, valorBase):
    raridades = ["Comum", "Raro", "Épico", "Lendário"]
    chances = [70,20,8,2]
    raridadeSorteada = random.choice(raridades, weights = chances, k=1)[0]
    if raridadeSorteada == 'Comum':
        multiplicador = 1.0
    elif raridadeSorteada == "Raro":
        multiplicador = 1.5
    elif raridadeSorteada == "Épico":
        multiplicador = 2.0
    elif raridadeSorteada == "Lendário":
        multiplicador = 3.0
    valorFinal = int(valorBase * multiplicador)
    novoItem = {
        "nome": f"{nomeBase} ({raridadeSorteada})",
        "tipo": tipoItem,
        "efeito": efeitoBase,
        "valor_efeito": valorFinal,
        "raridade": raridadeSorteada
    }
    return novoItem

def aplicarEfeitoItem(item, dadosJogador):
    efeito = item.get('efeito')
    tipo = item.get('tipo')
    if tipo == 'Consumivel':
        if efeito == 'Cura':
            vida_atual = dadosJogador['vida']
            vida_maxima = dadosJogador['vidaMaxima']
            if vida_atual >= vida_maxima:
                print("Vida já está cheia!")
                return False
            dadosJogador['vida'] = min(vida_maxima, vida_atual + 20)
            print(f"Curou! Vida atual: {dadosJogador['vida']}/{vida_maxima}")
            return True

        elif efeito == 'Segundo Ataque':
            print("Buff de segundo ataque ativado!")
            return True

        elif efeito == 'Causa Dano':
            print("Poção de dano ativada!")
            return True
    return False