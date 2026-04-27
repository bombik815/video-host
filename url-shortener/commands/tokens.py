from typing import Annotated

import typer
from rich.console import Console
from api.api_v1.auth.services import redis_tokens as tokens

app = typer.Typer(
    name="token",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="the token to check"),
    ],
):
    """
    Check the  token
    """

    console.print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists.[/green]"
            if tokens.token_exist(token)
            else "[red]does not exist.[/red]"
        ),
    )


@app.command()
def create() -> None:
    """
    Create new the token
    """

    token = tokens.generate_and_save_token()
    console.print("[bold green]New API Token[/bold green]")
    console.print(f"- [cyan]{token}[/cyan]")


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="the token to add"),
    ],
):
    """
    Add the new token to db
    """

    tokens.add_token(token)
    console.print(f"Token [bold cyan]{token}[/bold cyan] [green]added.[/green]")


@app.command(name="remove")
def remove(
    token: Annotated[
        str,
        typer.Argument(help="The token to delete"),
    ],
):
    """
    Remove the token
    """
    if not tokens.token_exist(token):
        console.print(f"Token [bold]{token} [red]does not exist.[/red][/bold]")
        return

    tokens.delete_token(token)
    console.print(
        f"Token [bold cyan]{token}[/bold cyan] [green]removed from db.[/green]"
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    List all tokens
    """
    tokens_ = tokens.get_tokens()
    if not tokens_:
        console.print("[bold yellow]Available API Tokens[/bold yellow]")
        console.print("[italic]No tokens found.[/italic]")
        return

    console.print("[bold green]Available API Tokens[/bold green]")
    for token in tokens_:
        console.print(f"- [cyan]{token}[/cyan]")
    console.print()
