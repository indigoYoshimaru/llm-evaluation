import typer
from llm_evaluator.cli import evaluate, synthesize

app = typer.Typer()
app.add_typer(evaluate.app)
app.add_typer(synthesize.app)


@app.command()
def init(env_path: str):
    import shutil
    from llm_evaluator import APPDIR

    shutil.copy(env_path, APPDIR)


if __name__ == "__main__":
    app()
