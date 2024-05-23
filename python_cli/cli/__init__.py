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
    hours: int = typer.Option(help="The number of hours to get the forecast for", default=1),
    plot: bool = typer.Option(help="Plot the weather forecast", default=False),
):
    if city is None:
        city = typer.prompt("Which city's weather do you want to know?", default="Oslo")

    if provider == "wttr":
        import python_cli.lib.weather.wttr as wttr
        if hours > 1:
            typer.Exit(message="The wttr provider does not support multi-hour forecasts.")
        if plot:
            typer.Exit(message="The wttr provider does not support multi-hour forecasts, so plotting is disabled")
        typer.echo(wttr.get_weather(city))
    elif provider == "yr":
        import python_cli.lib.weather.yr as yr
        if plot:
            from python_cli.lib.weather.plotter import plot_forecast
            forecast = yr.get_weather(city, hours=hours, return_json=True)
            plot_forecast(location=city,times=forecast["times"], temperatures=forecast["temperatures"])
        else:
            typer.echo(yr.get_weather(city, hours=hours))
