import typer

app = typer.Typer(name="synthesizer")

@app.command()
def create_mqc_dataset(
    dataset_metadata_dir: str,
    model: str, 
    ): 

    pass

@app.command()
def create_qa_dataset(
    dataset_metadata_dir: str, 
    model: str, 
): 
    pass 

if __name__ == "__main__":
    app()

