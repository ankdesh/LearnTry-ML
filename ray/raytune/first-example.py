from ray import tune

def objective(x, a, b):
    return a * (x**0.5) + b


def trainable(config):
    # config (dict): A dict of hyperparameters.

    for x in range(20):
        score = objective(x, config["a"], config["b"])

        tune.report(score=score)  # This sends the score to Tune.

analysis = tune.run(
    trainable,
    config={"a": 2, "b": 4}
)

print("best config: ", analysis.get_best_config(metric="score", mode="max"))
