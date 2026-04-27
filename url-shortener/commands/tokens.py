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
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists.[/green]"
            if redis_tokens.token_exist(token)
            else "[red]does not exist.[/red]"
        ),
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    List all tokens
    """
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join([""] + redis_tokens.get_tokens())))
    print()
