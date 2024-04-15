import typer
from llm_evaluator.cli import evaluate, synthesize

app = typer.Typer()

app.add_typer(evaluate.app)
app.add_typer(synthesize.app)

if __name__ == "__main__":
    app()
