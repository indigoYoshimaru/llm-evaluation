from rich.console import Console
from rich.table import Table


def _create_inner_table(metrics):
    table = Table(pad_edge=True, expand=True)
    table.add_column("Name", justify="left")
    table.add_column("Score", justify="center")
    table.add_column("Reason", justify="left")
    for metric in metrics:
        success = "✅" if metric.success else "❌"
        table.add_row(
            metric.__name__,
            f"{success} - {metric.score}",
            metric.reason,
        )
    return table


def view_result(result):
    table = Table(title="test-result", show_lines=True, expand=True)
    table.add_column("Input", justify="left", ratio=0.5, style="red")
    table.add_column("Actual output", justify="left", ratio=1, style="cyan")
    table.add_column("Org context", justify="left", ratio=1)
    table.add_column("Retrieved context ", justify="left", ratio=1)
    table.add_column("Metric", justify="center", ratio=2, style="yellow")
    for test_result in result:
        inner_table = _create_inner_table(test_result.metrics)
        context = ". ".join(test_result.context)
        retrieved_context = ". ".join(test_result.retrieval_context)
        table.add_row(
            test_result.input,
            test_result.actual_output,
            context[:1000],
            retrieved_context[:1000],
            inner_table,
        )

    console = Console()
    console.print(table)
