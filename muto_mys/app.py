from textual.containers import Horizontal, Vertical
from textual.app import App, ComposeResult
from textual.widgets import Footer
from components.DataCatalog import DataCatalog
from components.AccountScreen import AccountScreen

class MysApp(App):

    CSS_PATH = ["global.tcss", "app.tcss"]

    def __init__(self) -> None:
        super().__init__()


        self.bind(keys="f1", action="push_screenaa", description="Screen")

        return

    def compose(self) -> ComposeResult:
        self.datacatalog = DataCatalog()
        self.footer = Footer()
        #self.push_screen()
        # layout
        with Horizontal():
            yield self.datacatalog
        yield self.footer

    def push_screen(self, screen):
        super().push_screen(screen=screen, )
        self.push_screen()


    def action_push_screenaa(self):
        super().push_screen(AccountScreen(id="account_screen"))