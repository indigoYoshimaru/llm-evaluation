def get_all_routers(): 
    from llm_evaluator.backend.routers import health
    all_routers = [health.router]
    return all_routers