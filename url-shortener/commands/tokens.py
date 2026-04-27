from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown
from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="token",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


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

    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists.[/green]"
            if redis_tokens.token_exist(token)
            else "[red]does not exist.[/red]"
        ),
    )


@app.command()
def create() -> None:
    """
    Create new the token
    """

    token = redis_tokens.generate_and_save_token()
    print(Markdown(f"# New API Token\n\n- `{token}`"))


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="the token to add"),
    ],
) -> None:
    """
    Add the new token
    """

    redis_tokens.add_token(token)
    print(f"Token [bold]{token}[/bold] [green]added.[/green]")


@app.command(name="remove")
def remove(
    token: Annotated[
        str,
        typer.Argument(help="the token to remove"),
    ],
) -> None:
    """
    Remove the token
    """

    existed = redis_tokens.token_exist(token)
    redis_tokens.delete_token(token)
    print(
        f"Token [bold]{token}[/bold]",
        "[green]removed.[/green]" if existed else "[yellow]was not found.[/yellow]",
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    List all tokens
    """
    tokens = redis_tokens.get_tokens()
    if not tokens:
        print(Markdown("# Available API Tokens\n\n_No tokens found._"))
        return

    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join([""] + tokens)))
    print()
