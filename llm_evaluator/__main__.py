import typer
from loguru import logger
from llm_evaluator import ENVFILE
from llm_evaluator.cli import evaluate, synthesize
from llm_evaluator.core.app_models.env_configs import EnvVarEnum

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
    import os

    shutil.copy(env_path, APPDIR)
    os.environ["env_file"] = str(os.path.join(APPDIR, "launch.json"))
    os.environ["default_run"] = "True"


@app.command(help="Env var update", name="env")
def change_env_var(
    var_type: EnvVarEnum = typer.Option(
        case_sensitive=False,
        default=EnvVarEnum.sv,
        help="Type of the env variable needs editing",
    ),
    name: str = typer.Argument(
        help="Name of variable",
    ),
    value: str = typer.Argument(
        help="Value of the variable",
    ),
):
    from llm_evaluator import ENVFILE
    from llm_evaluator.utils.fileio import FileReader, FileWriter
    from llm_evaluator.utils.secrets import encode, decode

    try:
        assert name, "Missing var name"
        assert value, "Missing var value"
        typed_value = eval(value)
    except AssertionError as e:
        raise e
    except Exception as e:
        typed_value = value
    else:
        logger.info(
            f"Updating {var_type.value} {name=} with new {value=} to file {ENVFILE}"
        )

    try:
        env_cfg_dict = decode(FileReader().read(ENVFILE)["env"])
        env_cfg_dict[var_type.value][name] = typed_value
        env_cfg_dict = encode(env_cfg_dict, ignored=["env"])
        FileWriter().write(ENVFILE, dict(env=env_cfg_dict))

    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e


@app.command(help="Temporary peek at true env file structure", name="env-peek")
def peek(
    env_file: str = typer.Option(default=ENVFILE, help="Env file path")
):
    from llm_evaluator.utils.fileio import FileReader, FileWriter
    from llm_evaluator.utils.secrets import encode, decode

    from rich.table import Table
    from rich.console import Console

    console = Console()

    env_cfg_dict = decode(FileReader().read(env_file)["env"])
    for k, inner_dict in env_cfg_dict.items():
        env_table = Table(title=k, show_lines=True, expand=True)
        env_table.add_column(
            "Key", style="yellow", justify="center", header_style="yellow"
        )
        env_table.add_column("Value", justify="left")
        if isinstance(inner_dict, str):
            env_table.add_row(k, inner_dict)
            console.print(env_table)
            continue

        for k, v in inner_dict.items():
            env_table.add_row(k, str(v))
        console.print(env_table)


@app.command(help="Trigger API", name="api-run")
def run_api(
    worker: int = typer.Option(
        default=2,
        help="Number of worker in API",
    ),
    main_api: str = typer.Option(
        default="llm_evaluator.backend.__main__:app",
        help="Main API app",
    ),
):
    # default to be gunicorn
    run_cmd = f"gunicorn --workers {worker} --preload --worker-class=uvicorn.workers.UvicornWorker {main_api}"
    import os

    os.system(run_cmd)


if __name__ == "__main__":
    app()
