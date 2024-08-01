from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static, Input
from textual.containers import Vertical, VerticalScroll
from textual import events
from components.AccountList import AccountList

class VerticalSuppressClicks(Vertical):
    def on_click(self, message: events.Click) -> None:
        message.stop()

class AccountScreen(ModalScreen):
    header_text = "Select Account"
    def compose(self) -> ComposeResult:
        self.accountList = AccountList()
        self.input = Input(placeholder="Enter Account Name or Number")
        self.input.focus()

        with VerticalSuppressClicks(id="account_outer"):
            yield Static(" ".join(self.header_text), id="account_header")
            with VerticalScroll(id="account_inner"):
                yield self.accountList
                yield self.input
            yield Static(
                "Scroll with arrows. Press any other key to continue.", id="help_footer"
            )

    def on_key(self, event: events.Key) -> None:
        event.stop()

        if event.key == "up":
            self.accountList.action_cursor_up()
        elif event.key == "down":
            self.accountList.action_cursor_down()
        elif event.key == "":
            return

        if event.key == "q":
            self.app.pop_screen()

        #self.app.pop_screen()