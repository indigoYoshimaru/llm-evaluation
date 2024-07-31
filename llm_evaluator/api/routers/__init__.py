def get_all_routers():
    from llm_evaluator.api.routers import health, synthesize, dataset_handle, evaluate

    all_routers = [
        health.router,
        synthesize.router,
        dataset_handle.router,
        evaluate.router,
    ]
    return all_routers
