import typer
from backend.routes import app


def main(
        host: str = typer.Option("0.0.0.0", "--host", ),
        port: int = typer.Option(5001, "--port"),
        debug: bool = typer.Option(False, "--debug")
):
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
     typer.run(main)