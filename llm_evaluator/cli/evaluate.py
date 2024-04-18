import typer
from llm_evaluator.core.enums import QuestionTypeEnum

app = typer.Typer(name="evaluator", 
                  help="Wanna find out if your model or RAG passed the test case?", 
                  no_args_is_help=True)


@app.command()
def eval_model(
    config_file: str = typer.Option(
        default="llm_evaluator/configs/qa_eval.json",
        help="Directory to your eval config file for tweaking metrics and threshold",
    ),
    judge_model: str = typer.Option(
        default="gpt-3.5-turbo-0125", 
        help="Your judge model. Remember judging model can be self-bias!"
    ), 
    dataset: str = typer.Option(
        default="dataset/5dc2197f-bb11-4e87-81d2-64dc317b6ced.json",
        help="Path to the generated dataset."
    ), 
    question_type: str = typer.Option(
        default= QuestionTypeEnum.qa,
        help="Dataset question type"
    )
):
    pass

@app.command()
def eval_rag(
    config_file: str = typer.Option(
        default="llm_evaluator/configs/qa_eval.json",
        help="Directory to your eval config file for tweaking metrics and threshold",
    ), 
    dataset: str = typer.Option(
        default="dataset/5dc2197f-bb11-4e87-81d2-64dc317b6ced.json",
        help="Path to the generated dataset."
    ), 
): 
    pass

if __name__ == "__main__":
    app()
