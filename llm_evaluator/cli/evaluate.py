import typer

app = typer.Typer(name="evaluator")


@app.command()
def eval_single(
    config_file: str,
    metric: str,
):
    pass

if __name__ == "__main__":
    app()
