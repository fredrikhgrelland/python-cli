import typer

app = typer.Typer()


@app.command()
def hello(name: str = typer.Argument(help="The name to say hello to", default=None)):
    if name is None:
        name = typer.prompt("What's your name?", default="random")

    if name == "random":
        import python_cli.lib.funny_name_generator as fng

        typer.echo(f"Hello {fng.generate_name()}")
    else:
        typer.echo(f"Hello {name}")
