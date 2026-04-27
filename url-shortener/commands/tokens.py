from typing import Annotated

import typer
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from api.api_v1.auth.services import redis_tokens

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
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists.[/green]"
            if redis_tokens.token_exist(token)
            else "[red]does not exist.[/red]"
        ),
    )


@app.command("list")
def list_tokens() -> None:
    tokens = redis_tokens.get_tokens()

    if not tokens:
        console.print(Markdown("## Tokens\n\n_No tokens found._"))
        return

    token_lines = "\n".join(f"- `{token}`" for token in tokens)
    console.print(Markdown(f"## Tokens\n\n{token_lines}"))
