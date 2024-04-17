import typer
from llm_evaluator.cli import evaluate, synthesize
from llm_evaluator.core.app_models.env_configs import EnvVarEnum
from loguru import logger

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


if __name__ == "__main__":
    app()
