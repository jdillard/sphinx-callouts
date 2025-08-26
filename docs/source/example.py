# __quick_start_begin__
from ray import tune


def objective(config):  # <1>
    score = config["a"] ** 2 + config["b"]
    return {"score": score}


search_space = {  # <2>
    "a": tune.grid_search([0.001, 0.01, 0.1, 1.0]),
    "b": tune.choice([1, 2, 3]),
}

tuner = tune.Tuner(objective, param_space=search_space)  # <3>

results = tuner.fit()
print(results.get_best_result(metric="score", mode="min").config)
# __quick_start_end__
