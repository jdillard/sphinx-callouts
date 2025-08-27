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

# __multi_lang_begin__
def python_function():  # <1>
    pass

// This would be JavaScript or C++  // <2>
console.log("test");

; This would be Clojure  ;; <3>
(println "hello")

% This would be Erlang  % <4>
hello() -> ok.

-- This would be SQL  -- <5>
SELECT * FROM table;

! This would be Fortran  ! <6>
WRITE(*,*) 'Hello'

<!-- This would be XML --> <!--<7>-->
<element>content</element>
# __multi_lang_end__
