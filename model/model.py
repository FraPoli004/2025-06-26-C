import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # <-- nx.DiGraph() se ORIENTATO
        self._nodes = []
        self._idMap = {}
        self._valori = {}

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


        self._valori.clear()
        for v in DAO.getPeso():
            self._valori[v[0]] = v[1]            # {idNodo: valore}

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
        return max(pesi) if pesi else 0  #

