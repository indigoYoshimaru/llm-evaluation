import typer
from llm_evaluator.cli import evaluate, synthesize

app = typer.Typer(no_args_is_help=True)
app.add_typer(evaluate.app)
app.add_typer(synthesize.app)


@app.command(help="Gimme your Envfile path and I'll do the rest!")
def init(
    env_path: str = typer.Argument(
        default=".vscode/launch.json",
        help="Envfile path",
    ),
):
    import shutil
    from llm_evaluator import APPDIR

    shutil.copy(env_path, APPDIR)


if __name__ == "__main__":
    app()
