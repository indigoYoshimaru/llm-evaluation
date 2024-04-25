import typer
from llm_evaluator import APPDIR
from llm_evaluator.core.enums import DataSourceEnum

app = typer.Typer(
    name="synthesize",
    help="Need baseline? Then where's your test set?",
    no_args_is_help=True,
)


@app.command(
    name="mqc",
    help="Wanna create a multiple choice test set?",
)
def create_mqc_dataset(
    config_dir: str = typer.Option(
        default="llm_evaluator/configs/synthesize.json",
        help="Directory to your synthesis config",
    ),
    dataset_save_dir: str = typer.Option(
        default="", help="Where to save the dataset locally"
    ),
    model: str = typer.Option(
        default="gpt-3.5-turbo-0125",
        help="Your dataset generator model! Choose wisely!",
    ),
    data_source: DataSourceEnum = typer.Option(
        case_sensitive=False,
        default=DataSourceEnum.retrieve_context,
        help="Data source to generate test set",
    ),
):
    raise NotImplementedError("Working on this, please wait!")
    # from llm_evaluator.core.app_models.public_configs import SynthesizerConfig
    # from llm_evaluator.core.synthesizer import Synthesizer
    # from llm_evaluator.templates.syn_temp import MQCTemplate

    # synthesizer_cfg = SynthesizerConfig(config_dir, data_source)
    # synthesizer = Synthesizer(config=synthesizer_cfg)
    # document_id, dataset = synthesizer.generate(
    #     syn_model=model,
    #     template=MQCTemplate,
    #     data_source=data_source,
    # )

    # if dataset_save_dir:
    #     import os

    #     dataset_save_dir = os.path.join(dataset_save_dir, "mqc")
    #     if not os.path.exists(dataset_save_dir):
    #         os.mkdir(dataset_save_dir)
    #     synthesizer.save_local(dataset, dataset_save_dir, document_id)


@app.command(
    name="qa",
    help="Generating the good old Q&A test set to evaluate both your LLM and RAG",
)
def create_qa_dataset(
    config_file: str = typer.Option(
        default="./configs/synthesize.json",
        help="Directory to your synthesis config",
    ),
    dataset_save_dir: str = typer.Option(
        default="", help="Where to save the dataset locally"
    ),
    model: str = typer.Option(
        default="gpt-3.5-turbo-0125",
        help="Your dataset generator model! Choose wisely!",
    ),
    data_source: DataSourceEnum = typer.Option(
        case_sensitive=False,
        default=DataSourceEnum.retrieve_context,
        help="Data source to generate test set",
    ),
):
    from llm_evaluator.core.app_models.public_configs import SynthesizerConfig
    from llm_evaluator.core.synthesizer import Synthesizer
    from llm_evaluator.templates.syn_temp import QATemplate
    import os

    synthesizer_cfg = SynthesizerConfig(
        config_path=str(os.path.join(APPDIR, config_file)),
        data_source=data_source,
    )
    synthesizer = Synthesizer(config=synthesizer_cfg)
    document_id, dataset = synthesizer.generate(
        syn_model=model,
        template=QATemplate,
        data_source=data_source,
    )

    if dataset_save_dir:

        dataset_save_dir = os.path.join(
            os.getcwd(),
            dataset_save_dir,
            "qa",
        )
        if not os.path.exists(dataset_save_dir):
            os.mkdir(dataset_save_dir)
        synthesizer.save_local(dataset, dataset_save_dir, document_id)


if __name__ == "__main__":
    app()
