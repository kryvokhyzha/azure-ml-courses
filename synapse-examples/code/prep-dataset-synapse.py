import os
import azureml.core
from pyspark.sql import SparkSession
from azureml.core import Run, Dataset, Datastore

print(azureml.core.VERSION)
print(os.environ)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--hday")
parser.add_argument("--out_dataset_name")
parser.add_argument("--out_dataset_desc")
args = parser.parse_args()

# get run context and workspace
run_context = Run.get_context()
ws = run_context.experiment.workspace
ds = Datastore.get_default(ws)

# create spark session
spark = (
    SparkSession.builder
    .getOrCreate()
)

df = spark.sql(f"select * from pps_adm.msc_cdr where hday = '{args.hday}' limit 1").toPandas()
# df = pd.DataFrame({'col1': [1,2,3,4], 'col2': [5,6,7,8]})

tab_dataset = Dataset.Tabular.register_pandas_dataframe(
    dataframe=df,
    target=ds,
    name=args.out_dataset_name,
)

# Register the tabular dataset
try:
    tab_dataset = tab_dataset.register(
        workspace=ws,
        name=args.out_dataset_name,
        description=args.out_dataset_name,
        create_new_version=True
    )
except Exception as ex:
    print(ex)
