# Development with Jupyter Notebooks 

## Environment setup for exploratory analysis

The `requirements.txt` file in the notebooks folder contains the packages required to run the EDA code. An environment can be set up using conda as follows:

```bash
conda create -n new-boss python=3.7
conda activate new-boss
pip install -r requirements.txt
```

Once the environment is created, please activate the environment before running any scripts.

```bash
conda activate new-boss
```

### Add previously created environment as a kernel

`python -m ipykernel install --user --name new-boss --display-name "new-boss"`

Next, start a Jupyter notebook server by running: 

`jupyter notebook`
