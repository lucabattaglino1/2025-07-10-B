import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCategoria(self):
        categorie = self._model.getCategorie()
        for c in categorie:
            self._view._ddcategory.options.append(ft.dropdown.Option(str(c)))
        self._view.update_page()

    def handleCreaGrafo(self, e):

        r1 = self._view._ddcategory.value
        r2 = self._view._dp1.value
        r3 = self._view._dp2.value

        if r1 is None:
            self._view.create_alert("Seleziona un valore")
            return

        if r2 is None:
            self._view.create_alert("Seleziona un valore")
            return

        if r3 is None:
            self._view.create_alert("Seleziona un valore")
            return

        self._model.buildGraph(r2, r3, r1)

        # pulisco la lista risultati
        self._view.txt_result.controls.clear()

        # stampo le info
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))

        self._view.update_page()

    def handleBestProdotti(self, e):
        for prodotto, score in self._model.getTopProdotti():
            self._view.txt_result.controls.append(ft.Text(f"{prodotto.product_name} with score {score}"))

        self._view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
