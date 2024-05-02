from llm_evaluator.backend.routers import synthesize


def get_all_routers():
    from llm_evaluator.backend.routers import health, evaluate

    all_routers = [
        health.router,
        evaluate.router,
        synthesize.router,
    ]
    return all_routers
