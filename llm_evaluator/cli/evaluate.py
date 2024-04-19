import typer
from llm_evaluator.core.enums import QuestionTypeEnum

app = typer.Typer(
    name="evaluator",
    help="Wanna find out if your model or RAG passed the test case?",
    no_args_is_help=True,
)


@app.command()
def eval_model(
    config_file: str = typer.Option(
        default="llm_evaluator/configs/model_eval.json",
        help="Directory to your eval config file for tweaking metrics and threshold",
    ),
    judge_model: str = typer.Option(
        default="gpt-3.5-turbo-0125",
        help="Your judge model. Remember judging model can be self-bias!",
    ),
    dataset: str = typer.Option(
        default="dataset/qa/c0d8e70d-fcf8-460a-8bb0-33c6809a5936.json",
        help="Path to the generated dataset.",
    ),
    question_type: QuestionTypeEnum = typer.Option(
        default=QuestionTypeEnum.qa, help="Dataset question type"
    ),
):
    from llm_evaluator.core.app_models.public_configs import EvaluatorConfig
    from llm_evaluator.core.evaluator import Evaluator

    cfg = EvaluatorConfig(config_path=config_file)
    evaluator = Evaluator(config=cfg, question_type=question_type.name)
    test_results = evaluator.eval_gen_model(dataset_path = dataset, judge_model=judge_model)
    print(test_results)

@app.command()
def eval_rag(
    config_file: str = typer.Option(
        default="llm_evaluator/configs/qa_eval.json",
        help="Directory to your eval config file for tweaking metrics and threshold",
    ),
    dataset: str = typer.Option(
        default="dataset/5dc2197f-bb11-4e87-81d2-64dc317b6ced.json",
        help="Path to the generated dataset.",
    ),
):
    pass


if __name__ == "__main__":
    app()
