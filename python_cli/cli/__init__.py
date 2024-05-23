import typer
from python_cli.lib.weather import Provider

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


@app.command()
def weather(
    city: str = typer.Argument(help="The city to get the weather for", default=None),
    provider: Provider = typer.Option(
        help="The weather provider to use",
        default=Provider.wttr,
        case_sensitive=False,
    ),
):
    if city is None:
        city = typer.prompt("Which city's weather do you want to know?", default="Oslo")

    if provider == "wttr":
        import python_cli.lib.weather.wttr as wttr

        typer.echo(wttr.get_weather(city))
    elif provider == "yr":
        import python_cli.lib.weather.yr as yr

        typer.echo(yr.get_weather(city))
