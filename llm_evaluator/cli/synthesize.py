import typer
from typing_extensions import Annotated
from llm_evaluator.core.synthesizer import DataSource

app = typer.Typer(name="synthesizer")


@app.command()
def create_mqc_dataset(
    config_dir: str = 'llm_evaluator/configs/synthesize.json',
    dataset_save_dir: str = "dataset",
    model: str = "gpt-3.5-turbo-0125",
    data_source: Annotated[
        DataSource, typer.Option(case_sensitive=False)
    ] = DataSource.retrieve_context,
):

    print(data_source.name)


@app.command()
def create_qa_dataset(
    dataset_metadata_dir: str,
    model: str,
):
    pass


if __name__ == "__main__":
    app()
