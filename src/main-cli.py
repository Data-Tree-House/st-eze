import typer
from loguru import logger

app = typer.Typer()


@app.command()
def run() -> None:
    """Daily scheduled task."""
    logger.info("Starting daily run...")
    # TODO: add daily task logic here
    logger.info("Daily run complete.")


if __name__ == "__main__":
    app()
