from classe import Personagem

class Jogador(Personagem):
    def __init__(self, nome, dano, vida, lvl, recurso, spa, exp, classe, dinheiro, spaEnergia):
        super().__init__(nome, dano, vida, lvl, recurso, spa, spaEnergia)
        self.exp = exp
        self.classe = classe
        from componentes.inventario import Inventario
        self.inv = Inventario(jogador=self, modo="padrao")
        self.dinheiro = dinheiro

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getLvl(self):
        return super().getLvl()
    def getRecurso(self):
        return super().getRecurso()
    def getSpa(self):
        return super().getSpa()
    def getExp(self):
        return self.exp
    def getClasse(self):
        return self.classe
    def getInv(self):
        return self.inv
    def getDinheiro(self):
        return self.dinheiro
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        super().setVida(vida)
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setRecurso(self, recurso):
        super().setRecurso(recurso)
    def setSpa(self, spa):
        super().setSpa(spa)
    def setExp(self, exp):
        self.exp = exp
    def setClasse(self, classe):
        self.classe = classe
    def setInv(self, lista_itens):
        if isinstance(lista_itens, list):
            if hasattr(self, 'inv') and self.inv is not None:
                self.inv.mochila = lista_itens
        else:
            self.inv = lista_itens
    def setDinheiro(self, dinheiro):
        self.dinheiro = dinheiro

    def ataque(self, dano):
        super().ataque(dano)

    def ataqueSpe(self, dano):
        super().ataqueSpe(dano)

    def curarVida(self, dano):
        super().curarVida(dano)

    def tomarDano(self, dano):
        super().tomarDano(dano)

    def addItem(self, item):
        if len(self.inv.mochila) < 15:
            self.inv.mochila.append(item)
            self.inv.salvarInventario()
            return True
        print("Mochila cheia! Não foi possível adicionar o item.")
        return False

    def defesa(self):
        defesaTotal = 0
        slotsDeDefesa = ["Capacete", "Armadura", "Bota"]
        for slot in slotsDeDefesa:
            item = self.inv.equipamentos.get(slot)
            if item:
                defesaTotal += item.getDano()
        return defesaTotal