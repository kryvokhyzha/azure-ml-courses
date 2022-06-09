# Set up and manage Azure Data Factory

## Example - Set-up Azure Data Factory

It is easy to set up Azure Data Factory from within the Azure portal, you only require the following information:

+ **Name:** The name of the Azure Data Factory instance
+ **Subscription:** The subscription in which the ADF instance is created
+ **Resource group:** The resource group where the ADF instance will reside
+ **Version:** select V2 for the latest features
+ **Location:** The datacenter location in which the instance is stored

Enable Git provides the capability to integrate the code that you create with a Git repository enabling you to source control the code that you would create. Define the GIT URL, repository name, branch name, and the root folder.

Alternatively, there are a number of different ways that you can provision the service programmatically. In this example, you can see PowerShell at work to set up the environment.

```bash
PowerShell
######################################################################
##                PART I: Creating an Azure Data Factory            ##
######################################################################


# Sign in to Azure and set the WINDOWS AZURE subscription to work with
$SubscriptionId = "add your subscription in the quotes"

Add-AzureRmAccount
Set-AzureRmContext -SubscriptionId $SubscriptionId

# register the Microsoft Azure Data Factory resource provider
Register-AzureRmResourceProvider -ProviderNamespace Microsoft.DataFactory

# DEFINE RESOURCE GROUP NAME AND LOCATION PARAMETERS
$resourceGroupName = "cto_ignite"
$rglocation = "West US 2"

# CREATE AZURE DATA FACTORY
New-AzureRmDataFactoryV2 -ResourceGroupName $resourceGroupName -Name "ctoigniteADF" -Location $rglocation
```

## Example - Create linked services

Before you create a dataset, you must create a **linked service** to link your data store to the data factory. Linked services are much like connection strings, which define the connection information needed for Data Factory to connect to external resources. There are over 100 connectors that can be used to define a linked service.

A linked service in Data Factory can be defined using the Copy Data Activity in the ADF designer, or you can create them independently to point to a data store or a compute resources. The Copy Activity copies data between the source and destination, and when you run this activity you are asked to define a linked service as part of the copy activity definition

Alternatively you can programmatically define a linked service in the JSON format to be used via REST APIs or the SDK, using the following notation:

```json
{
    "name": "<Name of the linked service>",
    "properties": {
        "type": "<Type of the linked service>",
        "typeProperties": {
              "<data store or compute-specific type properties>"
        },
        "connectVia": {
            "referenceName": "<name of Integration Runtime>",
            "type": "IntegrationRuntimeReference"
        }
    }
}
```

The following table describes properties in the above JSON:

| **Property**   | **Description**                                                                                                                                                                                                                                                                                                                                                         | **Required** |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| name           | Name of the linked service.                                                                                                                                                                                                                                                                                                                                             | Yes          |
| type           | Type of the linked service. For example: AzureStorage (data store) or AzureBatch (compute). See the description for typeProperties.                                                                                                                                                                                                                                     | Yes          |
| typeProperties | The type properties are different for each data store or compute. For the supported data store types and their type properties, see the [dataset type table](https://docs.microsoft.com/en-us/azure/data-factory/concepts-datasets-linked-services#dataset-type). Navigate to the data store connector article to learn about type properties specific to a data store. | Yes          |
| connectVia     | The [Integration Runtime](https://docs.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime) to be used to connect to the data store. You can use Azure Integration Runtime or Self-hosted Integration Runtime (if your data store is located in a private network). If not specified, it uses the default Azure Integration Runtime.                    | No           |

### Example of a Linked Service

#### Azure SQL Database

The following example creates a linked service named "AzureSqlLinkedService" that connects to an Azure SQL Database named "ctosqldb" with the userid of "ctesta-oneill" and the password of "P@ssw0rd".

```json
{
  "name": "AzureSqlLinkedService",
  "properties": {
    "type": "AzureSqlDatabase",
    "typeProperties": {
      "connectionString": "Server=tcp:<server-name>.database.windows.net,1433;Database=ctosqldb;User ID=ctesta-oneill;Password=P@ssw0rd;Trusted_Connection=False;Encrypt=True;Connection Timeout=30"
    }
  }
}
```

#### Azure Blob Storage

The following example creates a linked service named "StorageLinkedService" that connects to an Azure Blob Store named "ctostorageaccount" with the storage account key used to connect to the data store.

```json
{
  "name": "StorageLinkedService",
  "properties": {
    "type": "AzureStorage",
    "typeProperties": {
      "connectionString": "DefaultEndpointsProtocol=https;AccountName=ctostorageaccount;AccountKey=<account-key>"
    }
  }
}
```

### Example - Create datasets

A dataset is a named view of data that simply points or references the data you want to use in your activities as inputs and outputs. Datasets identify data within different data stores, such as tables, files, folders, and documents. For example, an Azure Blob dataset specifies the blob container and folder in Blob storage from which the activity should read the data.

A dataset in Data Factory can be defined as an object within the Copy Data Activity, as a separate object, or in a JSON format for programmatic creation as follows:

```json
{
    "name": "<name of dataset>",
    "properties": {
        "type": "<type of dataset: AzureBlob, AzureSql etc...>",
        "linkedServiceName": {
                "referenceName": "<name of linked service>",
                "type": "LinkedServiceReference",
        },
        "schema": [
            {
                "name": "<Name of the column>",
                "type": "<Name of the type>"
            }
        ],
        "typeProperties": {
            "<type specific property>": "<value>",
            "<type specific property 2>": "<value 2>",
        }
    }
}
```

The following table describes properties in the above JSON:

| **Property**   | **Description**                                                                                                  | **Required** |
|----------------|------------------------------------------------------------------------------------------------------------------|--------------|
| name           | Name of the dataset.                                                                                             | Yes          |
| type           | Type of the dataset. Specify one of the types supported by Data Factory (for example: AzureBlob, AzureSqlTable). | Yes          |
| structure      | Schema of the dataset.                                                                                           | No           |
| typeProperties | The type properties are different for each type (for example: Azure Blob, Azure SQL table).                      | Yes          |

### Example of a dataset

#### Azure Blob

In this procedure, you create two datasets: InputDataset and OutputDataset. These datasets are of type Binary. They refer to the Azure Storage linked service named AzureStorageLinkedService. The input dataset represents the source data in the input folder. In the input dataset definition, you specify the blob container (adftutorial), the folder (input), and the file (emp.txt) that contain the source data. The output dataset represents the data that's copied to the destination. In the output dataset definition, you specify the blob container (adftutorial), the folder (output), and the file to which the data is copied.

1. In your desktop, create a folder named ADFv2QuickStartPSH in your C drive.
2. Create a JSON file named InputDataset.json in the C:\ADFv2QuickStartPSH folder with the following content:

  ```json
  {
        "name": "InputDataset",
        "properties": {
            "linkedServiceName": {
                "referenceName": "AzureStorageLinkedService",
                "type": "LinkedServiceReference"
            },
            "annotations": [],
            "type": "Binary",
            "typeProperties": {
                "location": {
                    "type": "AzureBlobStorageLocation",
                    "fileName": "emp.txt",
                    "folderPath": "input",
                    "container": "adftutorial"
                }
            }
        }
    }
  ```

3. To create the dataset: InputDataset, run the Set-AzDataFactoryV2Dataset cmdlet.

```bash
Set-AzDataFactoryV2Dataset -DataFactoryName $DataFactory.DataFactoryName `
    -ResourceGroupName $ResGrp.ResourceGroupName -Name "InputDataset" `
    -DefinitionFile ".\InputDataset.json"
```

Here is the sample output:

```bash
DatasetName       : InputDataset
ResourceGroupName : <resourceGroupname>
DataFactoryName   : <dataFactoryName>
Structure         :
Properties        : Microsoft.Azure.Management.DataFactory.Models.BinaryDataset
```

4. Repeat the steps to create the output dataset. Create a JSON file named OutputDataset.json in the C:\ADFv2QuickStartPSH folder, with the following content:

```json
{
    "name": "OutputDataset",
    "properties": {
        "linkedServiceName": {
            "referenceName": "AzureStorageLinkedService",
            "type": "LinkedServiceReference"
        },
        "annotations": [],
        "type": "Binary",
        "typeProperties": {
            "location": {
                "type": "AzureBlobStorageLocation",
                "folderPath": "output",
                "container": "adftutorial"
            }
        }
    }
}
```

5. Run the Set-AzDataFactoryV2Dataset cmdlet to create the OutDataset.

```bash
Set-AzDataFactoryV2Dataset -DataFactoryName $DataFactory.DataFactoryName `
    -ResourceGroupName $ResGrp.ResourceGroupName -Name "OutputDataset" `
    -DefinitionFile ".\OutputDataset.json"
```

Here is the sample output:

```bash
DatasetName       : OutputDataset
ResourceGroupName : <resourceGroupname>
DataFactoryName   : <dataFactoryName>
Structure         :
Properties        : Microsoft.Azure.Management.DataFactory.Models.BinaryDataset
```

## Example - Create data factory activities and pipelines

Activities within Azure Data Factory define the actions that will be performed on the data and there are three categories including:

+ Data movement activities
+ Data transformation activities
+ Control activities

### Data movement activities

Data movement activities simply move data from one data store to another. You can use the Copy Activity to perform data movement activities, or by using JSON. There are a wide range of data stores that are supported as a source and as a sink. This list is ever increasing, and you can find the [latest information here](https://docs.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities#data-movement-activities).

### Data transformation activities

Data transformation activities can be performed natively within the authoring tool of Azure Data Factory using the Mapping Data Flow. Alternatively, you can call a compute resource to change or enhance data through transformation, or perform analysis of the data. These include compute technologies such as Azure Databricks, Azure Batch, SQL Database and Azure Synapse Analytics, Machine Learning Services, Azure Virtual machines and HDInsight. You can make use of any existing SQL Server Integration Services (SSIS) Packages stored in a Catalog to execute in Azure

As this list is always evolving, you can get the [latest information here](https://docs.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities#data-transformation-activities).

### Control activities

When graphically authoring ADF solutions, you can use the control flow within the design to orchestrate pipeline activities that include chaining activities in a sequence, branching, defining parameters at the pipeline level, and passing arguments while invoking the pipeline on-demand or from a trigger. The current capabilities include:

| **Control Activity**      | **Description**                                                                                                                                                                                                                                                                                                                                         |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Execute Pipeline Activity | Execute Pipeline activity allows a Data Factory pipeline to invoke another pipeline.                                                                                                                                                                                                                                                                    |
| ForEachActivity           | ForEach Activity defines a repeating control flow in your pipeline. This activity is used to iterate over a collection and executes specified activities in a loop. The loop implementation of this activity is similar to Foreach looping structure in programming languages.                                                                          |
| WebActivity               | Web Activity can be used to call a custom REST endpoint from a Data Factory pipeline. You can pass datasets and linked services to be consumed and accessed by the activity.                                                                                                                                                                            |
| Lookup Activity           | Lookup Activity can be used to read or look up a record/ table name/ value from any external source. This output can further be referenced by succeeding activities.                                                                                                                                                                                    |
| Get Metadata Activity     | GetMetadata activity can be used to retrieve metadata of any data in Azure Data Factory.                                                                                                                                                                                                                                                                |
| Until Activity            | Implements Do-Until loop that is similar to Do-Until looping structure in programming languages. It executes a set of activities in a loop until the condition associated with the activity evaluates to true. You can specify a timeout value for the until activity in Data Factory.                                                                  |
| If Condition Activity     | The If Condition can be used to branch based on condition that evaluates to true or false. The If Condition activity provides the same functionality that an if statement provides in programming languages. It evaluates a set of activities when the condition evaluates to true and another set of activities when the condition evaluates to false. |
| Wait Activity             | When you use a Wait activity in a pipeline, the pipeline waits for the specified period of time before continuing with execution of subsequent activities.                                                                                                                                                                                              |

You can get the [latest information here](https://docs.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities#control-activities).

### Activities and pipelines

#### Defining activities

When using JSON notation, the activities section can have one or more activities defined within it. There are two main types of activities: Execution and Control Activities. Execution (also known as Compute) activities include data movement and data transformation activities. They have the following top-level structure:

```json
{
    "name": "Execution Activity Name",
    "description": "description",
    "type": "<ActivityType>",
    "typeProperties":
    {
    },
    "linkedServiceName": "MyLinkedService",
    "policy":
    {
    },
    "dependsOn":
    {
    }
}
```

The following table describes properties in the above JSON:

| **Control Activity** | **Description**                                                                                                     | **Required**                                                                             |
|----------------------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| name                 | Name of the activity.                                                                                               | Yes                                                                                      |
| description          | Text describing what the activity is used for.                                                                      | Yes                                                                                      |
| type                 | Defines the type of the activity.                                                                                   | Yes                                                                                      |
| linkedServiceName    | Name of the linked service used by the activity.                                                                    | Yes for HDInsight, Machine Learning Batch Scoring Activity and Stored Procedure Activity |
| typeProperties       | Properties in the typeProperties section depend on each type of activity.                                           | No                                                                                       |
| policy               | Policies that affect the run-time behavior of the activity. This property includes timeout and retry behavior.      | No                                                                                       |
| dependsOn            | This property is used to define activity dependencies, and how subsequent activities depend on previous activities. | No                                                                                       |

#### Defining control activities

A Control Activity in Data Factory is defined in JSON format as follows:

```json
{
    "name": "Control Activity Name",
    "description": "description",
    "type": "<ActivityType>",
    "typeProperties":
    {
    },
    "dependsOn":
    {
    }
}
```

The following table describes properties in the above JSON:

| **Control Activity** | **Description**                                                                                                     | **Required**                                                                             |
|----------------------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| name                 | Name of the activity.                                                                                               | Yes                                                                                      |
| description          | Text describing what the activity is used for.                                                                      | Yes                                                                                      |
| type                 | Defines the type of the activity.                                                                                   | Yes                                                                                      |
| linkedServiceName    | Name of the linked service used by the activity.                                                                    | Yes for HDInsight, Machine Learning Batch Scoring Activity and Stored Procedure Activity |
| typeProperties       | Properties in the typeProperties section depend on each type of activity.                                           | No                                                                                       |
| policy               | Policies that affect the run-time behavior of the activity. This property includes timeout and retry behavior.      | No                                                                                       |
| dependsOn            | This property is used to define activity dependencies, and how subsequent activities depend on previous activities. | No                                                                                       |

Defining pipelines

Here is how a pipeline is defined in JSON format:

```json
{
    "name": "PipelineName",
    "properties":
    {
        "description": "pipeline description",
        "activities":
        [
        ],
        "parameters": {
         }
    }
}
```

The following table describes properties in the above JSON:

| **Control Activity** | **Description**                                                                                                              | **Required** |
|----------------------|------------------------------------------------------------------------------------------------------------------------------|--------------|
| name                 | Name of the pipeline.                                                                                                        | Yes          |
| description          | Text describing what the pipeline is used for.                                                                               | No           |
| activities           | The activities section can have one or more activities defined within it.                                                    | Yes          |
| parameters           | The parameters section can have one or more parameters defined within the pipeline, making your pipeline flexible for reuse. | No           |

### Example

The following JSON defines pipeline named "MyFirstPipeline" that contains one activity type of HDInsightHive that will call a query from a script name "partitionweblogs.hql" that is stored in the linked service named "StorageLinkedService", with an input named "AzureBlobInput" and an output named "AzureBlobOutput". It executes this against the compute resource defined in the linked service named "HDInsightOnDemandLinkedService"

The pipeline is scheduled to execute on a monthly basis, and will attempt to execute 3 times should it fail.

```json
{
    "name": "MyFirstPipeline",
    "properties": {
        "description": "My first Azure Data Factory pipeline",
        "activities": [
            {
                "type": "HDInsightHive",
                "typeProperties": {
                    "scriptPath": "adfgetstarted/script/partitionweblogs.hql",
                    "scriptLinkedService": "StorageLinkedService",
                    "defines": {
                        "inputtable": "wasb://adfgetstarted@ctostorageaccount.blob.core.windows.net/inputdata",
                        "partitionedtable": "wasb://adfgetstarted@ctostorageaccount.blob.core.windows.net/partitioneddata"
                    }
                },
                "inputs": [
                    {
                        "name": "AzureBlobInput"
                    }
                ],
                "outputs": [
                    {
                        "name": "AzureBlobOutput"
                    }
                ],
                "policy": {
                    "concurrency": 1,
                    "retry": 3
                },
                "scheduler": {
                    "frequency": "Month",
                    "interval": 1
              },
                "name": "RunSampleHiveActivity",
                "linkedServiceName": "HDInsightOnDemandLinkedService"
            }
        ],
        "start": "2017-04-01T00:00:00Z",
        "end": "2017-04-02T00:00:00Z",
        "isPaused": false,
        "hubName": "ctogetstarteddf_hub",
        "pipelineMode": "Scheduled"
    }
```
