import typer
from backend.routes import app
from waitress import serve


def main(
        host: str = typer.Option("0.0.0.0", "--host", ),
        port: int = typer.Option(5001, "--port"),
        debug: bool = typer.Option(False, "--debug")
):
    if debug:
        app.run(host=host, port=port, debug=True)
    else:
        serve(app, host=host, port=port, threads=10)


if __name__ == "__main__":
    typer.run(main)
