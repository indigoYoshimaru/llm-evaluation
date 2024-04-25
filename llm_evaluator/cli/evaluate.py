import typer
import os
from llm_evaluator import APPDIR
from llm_evaluator.core.evaluator import Evaluator
from llm_evaluator.core.enums import QuestionTypeEnum
from llm_evaluator.core.app_models.public_configs import EvaluatorConfig

app = typer.Typer(
    name="evaluate",
    help="Wanna find out if your model or RAG passed the test case?",
    no_args_is_help=True,
)


@app.command()
def eval_model(
    config_file: str = typer.Option(
        default="./configs/model_eval.json",
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

    cfg = EvaluatorConfig(config_path=str(os.path.join(APPDIR, config_file)))
    evaluator = Evaluator(
        config=cfg,
        question_type=question_type.name,
        judge_model=judge_model,
    )
    test_results = evaluator.evaluate(
        dataset_path=str(
            os.path.join(
                os.getcwd(),
                dataset,
            )
        )
    )


@app.command()
def eval_rag(
    config_file: str = typer.Option(
        default="./configs/rag_eval.json",
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
):

    cfg = EvaluatorConfig(config_path=str(os.path.join(APPDIR, config_file)))
    evaluator = Evaluator(
        config=cfg,
        question_type="rag",
        judge_model=judge_model,
    )
    test_results = evaluator.evaluate(
        dataset_path=str(
            os.path.join(
                os.getcwd(),
                dataset,
            )
        )
    )


if __name__ == "__main__":
    app()
