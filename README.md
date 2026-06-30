# Debugger Tutorial

## Table of Contents
---

- [1. Process](#1-process)
- [2. .zed/debug.json](#2-zeddebugjson)

---

## 1. Process

____

I hate printing variables, but I need it, so I'll be doing it in a smarter way. So why not just mark a point in our script and checking the variable value at that point? *Boom, we call it a **breakpoint.*** The breakpoint is signified by a red dot. 

> ⌨️ Press `F9` to toggle a breakpoint.

Let's observe the following directory and 2 scripts.

---

Directory structure:
```plaintext
.
├── data
│   └── iris.csv
├── main.py
├── models
│   ├── __init__.py
│   └── model.py
├── storage
│   ├── graphs
│   │   └── iris_scatter.png
│   └── models
│       └── iris_model.pkl
└── utils
    ├── __init__.py
    ├── preprocess.py
    └── visualize.py

7 directories, 9 files
```

`root/main.py`
```python 
import os

from models.model import train_and_save_model
from utils.preprocess import load_and_split_data
from utils.visualize import save_scatter_plot


def main():
    csv_path = "data/iris.csv"
    graph_dir = "storage/graphs"
    model_dir = "storage/models"

    print("Step 1: Visualizing data...")
    save_scatter_plot(csv_path, graph_dir)

    print("Step 2: Loading and splitting data...")
    X_train, X_test, y_train, y_test = load_and_split_data(csv_path)

    print("Step 3: Training model...")
    model = train_and_save_model(X_train, y_train, model_dir)

    # Score accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy on test set: {accuracy:.2f}")


if __name__ == "__main__":
    main()
```
---

`root/utils/visualize.py`

```python
import os

import matplotlib.pyplot as plt
import pandas as pd


def save_scatter_plot(filepath, output_dir):
    df = pd.read_csv(filepath)
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 4))
    for variety, group in df.groupby("variety"):
        plt.scatter(group["sepal_length"], group["sepal_width"], label=variety)

    plt.xlabel("Sepal Length")
    plt.ylabel("Sepal Width")
    plt.legend()
    plt.title("Iris Sepal Dimensions")
    plt.savefig(os.path.join(output_dir, "iris_scatter.png"))
    plt.close()

```
---

We intend to see if the `csv_path`/`graph_dir` is right and see if the visualization is right. Now let's put a breakpoint in `main.py`, to be precise, here:

```python
    print("Step 1: Visualizing data...")
    save_scatter_plot(csv_path, graph_dir)  # <- Here
```

Then we start debugging. 

> ⌨️ Press `F4` to start debugging.

Now you will see 3 tabs
- the Frames/Breakpoints
- Console/Variables
- Terminal

There are some buttons above, we'll get there, but first let's see the tabs.

### Frames/Breakpoints
---

The Breakpoints tab shows you the breakpoints you have set in your code. that's pretty straightforward. The Frames tab shows you the **call stack**. It shows the order of files/functions it traverses when executing your code. In this instance, you will get the following 2 Frames in the follwoing order.

**main**\
root/main.py:14 
```python
13  >   print("Step 1: Visualizing data...")
14  >   save_scatter_plot(csv_path, graph_dir)
```

**\<module\>**\
root/main.py:28
```python
27  >   if __name__ == "__main__":
28  >        main()
```

The first entry is the `main` function, and the second entry is the `__module__` function. The `main` is the line of code we are currently breaking on, which to get here, we went through the `__name__ == "__main__"` check in the `__module__` function. Hence, the 2nd entry.

That's quite intuitive!

### Console/Variables

The Console is like a .ipynb cell, meaning you can type code and execute it. For instance, you can check the type of a var! Let's try `type(csv_path)`, we'll get a `str`. Then we can see all the variables initiated in the Variables tab. For instance, we will get the Local Variables `df, filepath, output_dir` in the Variables tab.

In the case of an error, you'll see an exception in the Variables tab. To demonstrate, let's purposefully raise an error by trying to access a non-existent column in the DataFrame.

```python
    for variety, group in df.groupby("species"): # <- It should be variety, not species
        plt.scatter(group["sepal_length"], group["sepal_width"], label=variety)
```

When you run this code, you'll see a `special variables` in the Variables tab. Inspecting this will show the `__exception__` and the traceback. Try seeing the `visualize.py` script and you will see a lot more detail, you'll see the `df` column names, that helps you debug it.

### Terminal

The terminal shows you the terminal output and the error message if the error is right in the main script.

---

## 2. .zed/debug.json
---

Tired of choosing the option when you `F4` to debug? let's do a fancier and more structured `F4` option.

First of all, make sure you Zed `settings.json` can detect `venv`. Add the following besides the other options.

`settings.json`
```json
{
  "key_1":"value_1",
  "terminal": {
    "detect_venv": {
      "on": {
        "directories": [".venv", "venv"],
        "activate_script": "default",
      },
    },
  "key_2":"value_2",
  "key_3":"value_3",
}
```

Then make the following `json` file, we'll go through it and what it means

`root/.zed/debug.json`
```json
[
  {
    "label": "Debug Iris Project",
    "adapter": "Debugpy",
    "request": "launch",
    "program": "main.py",
    "cwd": "$ZED_WORKTREE_ROOT",
    "env": {
      "PYTHONPATH": "$ZED_WORKTREE_ROOT",
    },
    "redirectOutput": true,
    "subProcess": true,
  },
]
```
- We use the `Debugpy` adapter because well, that's the debug option for python.
- Then we have a `launch` request because we want to start this debugging session, other options include `attach` to a running process.
- The label is just a name we see when we press `F4`.
- We use `$ZED_WORKTREE_ROOT` as the `cwd` to make sure we're in the right directory, this affects imports from files.
- We set a `PYTHONPATH` as the `env` and this works with the `settings.json` to detect the `venv`.
- `subProcess` is set to detect any `subprocess.run()` calls in the code.
- `redirectOutput` is set to `true` so print statements make it to the Console and not only the Terminal.

You can also add `args` and `env` keys to the `debug.json` file. It strikes a resemblance to debugging in VSCode too. https://code.visualstudio.com/docs/debugtest/debugging-configuration

<!--TODO, Future update explain env (like load_dotenv) and args (for argparse) in debug.json-->
