from networkx import DiGraph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = DiGraph()
        self._nodes = []
        self._idMapAO = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategorie(self):
        return DAO.getAllCategorie()

    def buildGraph(self, anno1, anno2, categoria):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(categoria)
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.product_id] = n

        self._graph.add_nodes_from(self._nodes)
        self.addEdges(anno1, anno2, categoria)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def addEdges(self, anno1, anno2, categoria):
        # filtri scelti dall'utente nella UI (range date/anni + eventuale categoria/store)
        # ADATTA: nomi e numero di parametri in base a cosa raccoglie la tua UI

        venditeMap = {}
        # QUERY 1 - VALORI SINGOLI: quanto vale ciascuna entità presa da sola
        # (somma vendite, somma salario, count gare... dipende dal testo)
        # restituisce lista di tuple (oggetto, numero) -> le "apro" nel for
        for prodotto, peso in DAO.getVendite(anno1, anno2, categoria, self._idMapAO):
            # ADATTA: nome metodo DAO (getVendite -> getSalari/getPopolarita/...)
            # ADATTA: nome attributo id (.product_id -> .driverId/.constructorId/...)
            venditeMap[prodotto.product_id] = peso
            # chiave = id dell'entità (numero), valore = il suo valore aggregato

        # QUERY 2 - COPPIE: quali coppie di entità sono collegabili
        # (self-join con le condizioni del testo: stessa categoria/store/anno/squadra...)
        # restituisce lista di tuple (oggetto1, oggetto2) -> le "apro" nel for
        for n1, n2 in DAO.getAllCoppie(anno1, anno2, categoria, self._idMapAO):
            # ADATTA: nome metodo DAO

            # guardo quanto vale ciascuno dei due nella mappa costruita sopra
            # .get(chiave, 0) = se l'id non c'è nella mappa, uso 0 invece di crashare
            # (succede se un'entità non ha vendite/gare nel range scelto)
            v1 = venditeMap.get(n1.product_id, 0)
            v2 = venditeMap.get(n2.product_id, 0)
            # ADATTA: nome attributo id, uguale a quello usato sopra

            peso = v1 + v2
            # ADATTA SEMPRE CON ATTENZIONE: questa è la formula del peso scritta nel testo
            # esempi possibili: v1 + v2  |  (v1 + v2) / giorni  |  v1 - v2  |  count gare...

            # decido IL VERSO dell'arco confrontando v1 e v2
            # ADATTA SEMPRE: leggi bene la frase del testo su "chi riceve l'arco"
            if v1 > v2:
                self._graph.add_edge(n1, n2, weight=peso)
                # ESEMPIO: "arco entrante nel nodo con valore maggiore" -> arco verso n1
            elif v2 > v1:
                self._graph.add_edge(n2, n1, weight=peso)
            else:
                # PARITA': qui il testo chiedeva "inserire entrambi gli archi"
                # ADATTA: altri testi potrebbero chiedere "nessun arco" o "verso fisso" in caso di parità
                self._graph.add_edge(n1, n2, weight=peso)
                self._graph.add_edge(n2, n1, weight=peso)

        # NOTA: se il grafo è NON orientato (nx.Graph() invece di DiGraph()),
        # spesso questo if/elif/else non serve: basta
        # self._graph.add_edge(n1, n2, weight=peso)  una sola volta, senza decidere il verso

    def getNumEdges(self):
        return len(self._graph.edges)

    def getTopProdotti(self):
        scores = []
        for n in self._graph.nodes:
            uscenti = sum(self._graph[n][v]["weight"] for v in self._graph.successors(n))
            entranti = sum(self._graph[u][n]["weight"] for u in self._graph.predecessors(n))
            score = uscenti - entranti
            scores.append((n, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]