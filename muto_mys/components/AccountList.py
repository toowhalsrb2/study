from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label

class AccountList(ListView):

    def __init__(self):
        super().__init__()
        self._add_child(ListItem(Label("KGMS")))
        self._add_child(ListItem(Label("ODIN")))
        self._add_child(ListItem(Label("TWOD")))
        self._add_child(ListItem(Label("JPOD")))
        