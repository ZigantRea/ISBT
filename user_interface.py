from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Static, Input
from web3.exceptions import ValidationError
from token_function import TokenFunction


class UserInterface(App):
    """A working 'desktop' calculator."""

    CSS_PATH = "style.css"

    balance = var("BALANCE")
    output = var("Welcome to Rea and Danci coin!")

    amount_0 = Input
    address = Input

    amount_1 = Input
    amount_2 = Input

    function = TokenFunction

    def watch_balance(self, value: str) -> None:
        """Called when balance is updated."""
        self.query_one("#balance", Static).update(value)

    def watch_output(self, value: str) -> None:
        """Called when output is updated."""
        self.query_one("#output", Static).update(value)

    def successful_action(self):
        output_element = self.query_one("#output", Static)
        output_element.remove_class("error")
        output_element.add_class("success")
        self.output = "You action was successfully executed!"

    def unsuccessful_action(self, error):
        output_element = self.query_one("#output", Static)
        output_element.remove_class("success")
        output_element.add_class("error")
        self.output = error
    
    def compose(self) -> ComposeResult:
        """Add our buttons."""
        self.function = TokenFunction()

        yield Container(
            Static(id="balance"),
            Button("Transact", id="transact", variant="primary"),
            Input(placeholder="amount", id="amount_0"),
            Input(placeholder="wallet", id="address"),
            Button("Mint", id="mint", variant="primary"),
            Input(placeholder="amount", id="amount_1"),
            Button("Burn", id="burn", variant="primary"),
            Input(placeholder="amount", id="amount_2"),
            Button("Get balance", id="get_balance", variant="primary"),
            Input(placeholder="wallet", id="address_1"),
            Static(id="output"),
            id="user_interface",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "transact":
            try:
                amount = self.query_one("#amount_0", Input).value
                address = self.query_one("#address", Input).value

                my_balance, to_balance = self.function.transact(amount, address)
                self.balance = f"My balance: {my_balance} RDC\nReceivers balance: {to_balance} RDC"

                self.successful_action()
            except ValueError:
                self.unsuccessful_action("Amount and wallet are required!")
            except ValidationError:
                self.unsuccessful_action("Insert correct wallet")
            except Exception as error:
                self.unsuccessful_action(str(error))

        if event.button.id == "mint":
            try:
                amount = self.query_one("#amount_1", Input).value
                my_balance = self.function.mint(amount)
                self.balance = f"My balance: {my_balance} RDC"
                self.successful_action()

            except ValueError:
                self.unsuccessful_action("Amount is required and have to be integer!")
            except ValidationError:
                self.unsuccessful_action("Insert valid amount!")
            except Exception as error:
                self.unsuccessful_action(str(error))

        if event.button.id == "burn":
            try:
                amount = self.query_one("#amount_2", Input).value
                my_balance = self.function.burn(amount)
                self.balance = f"My balance: {my_balance} RDC"
                self.successful_action()

            except Exception as error:
                self.unsuccessful_action(str(error))

        if event.button.id == "get_balance":
            try:
                address = self.query_one("#address_1", Input).value
                balance = self.function.get_balance(address)
                self.balance = f"Balance of wallet {address}: {balance} RDC"
                self.successful_action()

            except ValidationError:
                self.unsuccessful_action("Insert a valid wallet address")
            except Exception as error:
                self.unsuccessful_action(str(error))

if __name__ == "__main__":
    UserInterface().run()
