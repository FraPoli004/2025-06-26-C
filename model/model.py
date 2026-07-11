import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._optList = None
        self._bestScore = None
        self._grafo = nx.Graph()  # <-- nx.DiGraph() se ORIENTATO
        self._nodes = []
        self._idMap = {}
        self._valori = {}
        self._valoriNull = {}

    def getNodes(self):
        return self._grafo.nodes()

    def getDDvalue(self):
        return DAO.getDDvalue()

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self, ai,af):  # <-- ADATTA parametri = input dell'esame
        self._grafo.clear()
        self._idMap.clear()

        #modo1
        self._valori.clear()
        for v in DAO.getPeso(ai,af):
            self._valori[v[0]] = v[1]

        self._valoriNull.clear()
        for v in DAO.getPesoNull(ai, af):
            self._valoriNull[v[0]] = v[1]
        # {idNodo: valore}

        #modo2
        #self._valori.clear()
        #for c in self.getNodes():
            #self._valori[c.constructorId] = sum(len(lst) for lst in c.results.values())

        # NODI
        self._nodes = DAO.getAllNodes()  # <-- ADATTA
        for n in self._nodes:
            self._grafo.add_node(n)
            self._idMap[n.constructorId] = n  # <-- ADATTA: chiave = id del nodo (stesso formato dei tipi in getAllEdges!)

        for c in self.getNodes():
            for y in DAO.getValoriNodo(c.constructorId,ai,af):
                for p in DAO.getValoriNodo2(c.constructorId,y):
                    c.results.setdefault(y,[]).append(p)


        # ARCHI
        self.addEdgesPesati(ai,af)

    def addEdgesPesati(self, ai,af):  # archi PESATI
        for e in DAO.getAllEdges(ai,af):
            n1 = self._idMap.get(e[0])
            n2 = self._idMap.get(e[1])
            if n1 is None or n2 is None:
                continue
            self._grafo.add_edge(n1, n2, weight=self._valori.get(e[0])+self._valori.get(e[1]))

    def get_componente_max_per_peso(self):
        componenti = list(nx.connected_components(self._grafo))  # DiGraph -> weakly_connected_components
        piu_grande = max(componenti, key=len)
        nodi = sorted(piu_grande, key=lambda n: self._peso_incidente_max(n), reverse=True)
        return len(componenti), piu_grande, nodi

    def _peso_incidente_max(self, nodo):  # min -> sostituisci max con min (traccia F1-B)
        pesi = [self._grafo.get_edge_data(nodo, v)["weight"]
                for v in self._grafo.neighbors(nodo)]
        return max(pesi) if pesi else 0

    def getSottoinsiemeOttimo(self, soglia, dim):
        self._bestScore = 0  # <------- float("inf") se MINIMIZZI
        self._optList = []
        piu_grande = max(list(nx.connected_components(self._grafo)), key=len)
        candidati = [n for n in piu_grande
                     if len(n.results.keys())>=dim]  # <------- PRE-FILTRO intrinseco (se assente: tutti i nodi)
        self._ricorsione_sub(candidati, soglia, [], 0)
        return self._optList, self._bestScore

    def _ricorsione_sub(self, candidati, soglia, parziale, index):
        if len(parziale) == soglia:  # CASO BASE: raggiunti K elementi
            if self._getScoreSoluzione(parziale) > self._bestScore:  # <------- < se MINIMIZZI
                self._bestScore = self._getScoreSoluzione(parziale)
                self._optList = copy.deepcopy(parziale)  # <------- deepcopy: NON togliere
            return
        if index >= len(candidati):  # CASO BASE: candidati finiti
            return
        if len(candidati) - index < soglia - len(parziale):  # POTATURA: rimasti < mancanti
            return

        self._ricorsione_sub(candidati, soglia, parziale, index + 1)  # SCELTA A: ESCLUDO candidati[index]
        parziale.append(candidati[index])  # SCELTA B: INCLUDO candidati[index]
        self._ricorsione_sub(candidati, soglia, parziale, index + 1)
        parziale.pop()

    def _getScoreSoluzione(self, listaElems):
        score = 0
        for e in listaElems:
            score+= 1-(len(e.results.values())/len(e.resultsNull.values()))
        return score





