# Train a machine learning model with Azure Machine Learning

## Run a training script

You can use a ScriptRunConfig to run a script-based experiment that trains a machine learning model.

### Writing a script to train a model

When using an experiment to train a model, your script should save the trained model in the **outputs** folder. For example, the following script trains a model using Scikit-Learn, and saves it in the **outputs** folder using the **joblib** package:

```python
from azureml.core import Run
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Get the experiment run context
run = Run.get_context()

# Prepare the dataset
diabetes = pd.read_csv('data.csv')
X, y = diabetes[['Feature1','Feature2','Feature3']].values, diabetes['Label'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# Train a logistic regression model
reg = 0.1
model = LogisticRegression(C=1/reg, solver="liblinear").fit(X_train, y_train)

# calculate accuracy
y_hat = model.predict(X_test)
acc = np.average(y_hat == y_test)
run.log('Accuracy', np.float(acc))

# Save the trained model
os.makedirs('outputs', exist_ok=True)
joblib.dump(value=model, filename='outputs/model.pkl')

run.complete()
```

To prepare for an experiment that trains a model, a script like this is created and saved in a folder. For example, you could save this script as **training_script.py** in a folder named **training_folder**. Since the script includes code to load training data from **data.csv**, this file should also be saved in the folder.

### Running the script as an experiment

To run the script, create a **ScriptRunConfig** that references the folder and script file. You generally also need to define a Python (Conda) environment that includes any packages required by the script. In this example, the script uses Scikit-Learn so you must create an environment that includes that.

The script also uses Azure Machine Learning to log metrics, so you need to remember to include the **azureml-defaults** package in the environment.

```python
from azureml.core import Experiment, ScriptRunConfig, Environment
from azureml.core.conda_dependencies import CondaDependencies

# Create a Python environment for the experiment
sklearn_env = Environment("sklearn-env")

# Ensure the required packages are installed
packages = CondaDependencies.create(conda_packages=['scikit-learn','pip'],
                                    pip_packages=['azureml-defaults'])
sklearn_env.python.conda_dependencies = packages

# Create a script config
script_config = ScriptRunConfig(source_directory='training_folder',
                                script='training.py',
                                environment=sklearn_env) 

# Submit the experiment
experiment = Experiment(workspace=ws, name='training-experiment')
run = experiment.submit(config=script_config)
run.wait_for_completion()
```

## Using script parameters

You can increase the flexibility of script-based experiments by using arguments to set variables in the script.

### Working with script arguments

To use parameters in a script, you must use a library such as **argparse** to read the arguments passed to the script and assign them to variables. For example, the following script reads an argument named **--reg-rate**, which is used to set the regularization rate hyperparameter for the logistic regression algorithm used to train a model.

```python
from azureml.core import Run
import argparse
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Get the experiment run context
run = Run.get_context()

# Set regularization hyperparameter
parser = argparse.ArgumentParser()
parser.add_argument('--reg-rate', type=float, dest='reg_rate', default=0.01)
args = parser.parse_args()
reg = args.reg_rate

# Prepare the dataset
diabetes = pd.read_csv('data.csv')
X, y = data[['Feature1','Feature2','Feature3']].values, data['Label'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# Train a logistic regression model
model = LogisticRegression(C=1/reg, solver="liblinear").fit(X_train, y_train)

# calculate accuracy
y_hat = model.predict(X_test)
acc = np.average(y_hat == y_test)
run.log('Accuracy', np.float(acc))

# Save the trained model
os.makedirs('outputs', exist_ok=True)
joblib.dump(value=model, filename='outputs/model.pkl')

run.complete()
```

### Passing arguments to an experiment script

To pass parameter values to a script being run in an experiment, you need to provide an **arguments** value containing a list of comma-separated arguments and their values to the **ScriptRunConfig**, like this:

```python
# Create a script config
script_config = ScriptRunConfig(source_directory='training_folder',
                                script='training.py',
                                arguments = ['--reg-rate', 0.1],
                                environment=sklearn_env)
```

## Registering models

After running an experiment that trains a model you can use a reference to the Run object to retrieve its outputs, including the trained model.

### Retrieving model files

After an experiment run has completed, you can use the run objects **get_file_names** method to list the files generated. Standard practice is for scripts that train models to save them in the run's **outputs** folder.

You can also use the run object's **download_file** and **download_files** methods to download output files to the local file system.

```python
# "run" is a reference to a completed experiment run

# List the files generated by the experiment
for file in run.get_file_names():
    print(file)

# Download a named file
run.download_file(name='outputs/model.pkl', output_file_path='model.pkl')
```

### Registering a model

Model registration enables you to track multiple versions of a model, and retrieve models for inferencing (predicting label values from new data). When you register a model, you can specify a name, description, tags, framework (such as Scikit-Learn or PyTorch), framework version, custom properties, and other useful metadata. Registering a model with the same name as an existing model automatically creates a new version of the model, starting with 1 and increasing in units of 1.

To register a model from a local file, you can use the **register** method of the **Model** object as shown here:

```python
model = Model.register(workspace=ws,
                       model_name='classification_model',
                       model_path='model.pkl', # local path
                       description='A classification model',
                       tags={'data-format': 'CSV'},
                       model_framework=Model.Framework.SCIKITLEARN,
                       model_framework_version='0.20.3')
```

Alternatively, if you have a reference to the Run used to train the model, you can use its register_model method as shown here:

```pyhton
run.register_model( model_name='classification_model',
                    model_path='outputs/model.pkl', # run outputs path
                    description='A classification model',
                    tags={'data-format': 'CSV'},
                    model_framework=Model.Framework.SCIKITLEARN,
                    model_framework_version='0.20.3')
```

### Viewing registered models

You can view registered models in Azure Machine Learning studio. You can also use the Model object to retrieve details of registered models like this:

```python
from azureml.core import Model

for model in Model.list(ws):
    # Get model name and auto-generated version
    print(model.name, 'version:', model.version)
```
