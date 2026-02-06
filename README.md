# customer-churn-prediction

## How to run this project

### Create the virtual environment

```bash
conda create -n customer_churn python=3.11 -y
```

### Activate the virtual environment

```bash
conda activate customer_churn
```

### Install all the requirements in virtual environment


```bash
pip install -r requirements.txt
```

### Initialize the Git repository if there is no Git repository

```bash
git init
```

### Initialize the DVC

```bash
dvc init
```

### Execute the pipeline by the DVC ( run where dvc.yaml file exist )

```bash
dvc repro
```

