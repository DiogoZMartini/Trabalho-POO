from classe import Geral
from banco import tabela_itens
from tinydb import Query
import random


class Item(Geral):
    def __init__(self, nome, dano, descricao, quantidadeMaxima, efeito, preco, raridade, tipo, img=None,
                 uso=None):
        super().__init__(nome, dano)
        self.descricao = descricao
        self.quantidadeMaxima = quantidadeMaxima
        self.efeito = efeito
        self.preco = preco
        self.raridade = raridade
        self.tipo = tipo
        self.img = img
        self.uso = uso

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getDescricao(self):
        return self.descricao
    def getQuantidadeMaxima(self):
        return self.quantidadeMaxima
    def getEfeito(self):
        return self.efeito
    def getPreco(self):
        return self.preco
    def getRaridade(self):
        return self.raridade
    def getTipo(self):
        return self.tipo
    def getImg(self):
        return self.img
    def getUso(self):
        return self.uso
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setDescricao(self, descricao):
        self.descricao = descricao
    def setQuantidadeMaxima(self, quantidade):
        self.quantidadeMaxima = quantidade
    def setEfeito(self, efeito):
        self.efeito = efeito
    def setPreco(self, preco):
        self.preco = preco
    def setRaridade(self, raridade):
        self.raridade = raridade
    def setTipo(self, tipo):
        self.tipo = tipo
    def setImg(self, img):
        self.img = img
    def setUso(self, uso):
        self.uso = uso

    @classmethod
    def gerarItemAleatorio(cls):
        todosItensCatalogo = tabela_itens.all()
        if not todosItensCatalogo:
            return cls.criarItemComRaridade("Poção de Vida")
        dadosItemBanco = random.choice(todosItensCatalogo)
        # Passa o valor original do banco para a sua função de raridade
        itemFinal = cls.criarItemComRaridade(nomeBase=dadosItemBanco['nome'],)
        # o preço calculado por lá pode ficar negativo. Aqui garantimos que seja positivo)
        if itemFinal.getPreco() < 0:
            itemFinal.setPreco(abs(itemFinal.getPreco()))
        # Preserva o resto das informações customizadas que você cadastrou no banco
        itemFinal.setDescricao(dadosItemBanco['descricao'])
        itemFinal.setQuantidadeMaxima(dadosItemBanco['quantidadeMaxima'])
        itemFinal.setImg(dadosItemBanco.get('img', None))
        itemFinal.recalcularUso()
        return itemFinal

    def recalcularUso(self):
        valAbs = abs(self.dano)
        if self.efeito == 'Cura':
            self.uso = f"Cura {valAbs} de vida"
        elif self.efeito == "Aumenta a Defesa":
            self.uso = f"+{valAbs} de defesa"
        else:
            self.uso = f"+{valAbs} de dano"

    @classmethod
    def criarItemComRaridade(cls, nomeBase):
        # 1. Busca os dados brutos cadastrados lá na lista_itens do seu banco.py
        resultado = tabela_itens.search(Query().nome == nomeBase)
        if not resultado:
            return None
        dadosBanco = resultado[0]
        # 2. Sorteia a raridade do item
        raridades = ["Comum", "Raro", "Epico", "Lendário", "Divino"]
        chances = [83.499, 15, 1, 0.5, 0.001]
        raridadeSorteada = random.choices(raridades, weights=chances, k=1)[0]
        # 3. Define os multiplicadores de atributos
        multiplicadores = {"Comum": 1.0, "Raro": 1.25, "Epico": 1.8, "Lendário": 2.5, "Divino": 10.0}
        multiplicador = multiplicadores[raridadeSorteada]
        # 4. Modifica os valores base do banco usando o multiplicador da raridade
        if abs(dadosBanco['dano']) == 1:
            valoresFixos = {"Comum": 1, "Raro": 2, "Epico": 3, "Lendário": 4, "Divino": 10}
            sinal = 1 if dadosBanco['dano'] > 0 else -1
            valorFinal = valoresFixos[raridadeSorteada] * sinal
        else:
            valorFinal = int(dadosBanco['dano'] * multiplicador)
        precoFinal = int(dadosBanco['preco'] * multiplicador * 2)
        qtdMax = 5 if dadosBanco['tipo'] == 'Consumivel' else 1
        valorExibicaoStr = str(abs(valorFinal))
        efeito_base = dadosBanco['efeito']
        if efeito_base == 'Cura':
            usoFinal = f"Cura {valorExibicaoStr} de vida"
        elif efeito_base == "Aumenta a Defesa":
            usoFinal = f"+{valorExibicaoStr} de defesa"
        else:
            usoFinal = f"+{valorExibicaoStr} de dano"
        return cls(
            nome=f"{nomeBase} ({raridadeSorteada})",
            dano=valorFinal,
            descricao=f"{dadosBanco['descricao']} (Raridade: {raridadeSorteada})",
            quantidadeMaxima=qtdMax,
            efeito=dadosBanco['efeito'],
            preco=precoFinal,
            raridade=raridadeSorteada,
            tipo=dadosBanco['tipo'],
            img=dadosBanco.get('img'),
            uso=usoFinal
        )

    def aplicarEfeitoItem(self, dadosJogador, alvo=None):
        tipo = self.getTipo()
        efeito = self.getEfeito()
        if tipo == 'Consumivel':
            if efeito == 'Cura':
                poderCura = self.getDano()
                vida_atual = dadosJogador.getVida()
                vida_maxima = dadosJogador.getVidaMaxima()
                nova_vida = min(vida_maxima, vida_atual + poderCura)
                dadosJogador.setVida(nova_vida)
                return True

            elif efeito == 'Causa Dano':
                if alvo is not None:
                    danoItem = self.getDano()
                    if hasattr(alvo, 'tomarDano'):
                        alvo.tomarDano(danoItem)
                    else:
                        vidaAtualInimigo = alvo.getVida()
                        novaVidaInimigo = max(0, vidaAtualInimigo - danoItem)
                        alvo.setVida(novaVidaInimigo)
                    return True
                else:
                    return False
        return False