import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleBuildGraph(self, e):
        ai = self._view._ddYear1.value
        af = self._view._ddYear2.value
        if  ai is None or af is None:  # <-- ADATTA nome dropdown; valida TUTTI gli input
            self._txtGraphDetails.controls.clear()
            self._txtGraphDetails.controls.append(ft.Text("Seleziona un valore da entrambe i menù a tendina.", color="red"))
            self._view.update_page()
            return

        ai = int(ai)
        af = int(af)

        if af < ai:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("seleziona un anno iniziale minore di quello finale", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(ai,af)

        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txtGraphDetails.controls.append(ft.Text(f"Numero di nodi: {self._model.get_numnodi()}"))
        self._view._txtGraphDetails.controls.append(ft.Text(f"Numero di archi: {self._model.get_numarchi()}"))
        self._view.update_page()


    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        num, massima, nodi = self._model.get_componente_max_per_peso()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Nel grafo sono presenti {num} componenti connesse, la più lunga ha {len(massima)} nodi"))
        self._view._txtGraphDetails.controls.append(
            ft.Text(f"Ecco la componente connessa massima in ordine decrescente per peso massimo degli archi incidenti:"))
        for n in nodi:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{n}-----> peso: {self._model._peso_incidente_max(n)}"))
        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):
        pass

    def fillDDs(self):
        valori = self._model.getDDvalue()
        for v in valori:
            self._view._ddYear1.options.append(ft.dropdown.Option(v))
            self._view._ddYear2.options.append(ft.dropdown.Option(v))
        self._view.update_page()
