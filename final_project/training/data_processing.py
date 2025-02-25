import pandas as pd
from pyspark.sql import SparkSession
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(file_path):
    """
    Load and preprocess data from a csv
    """

    data = pd.read_csv(file_path)

    # Here are some example of preprocess
    # Cut missing data
    data = data.dropna()
    # Normalize data
    data = (data - data.mean()) / data.std()

    return data

def split_data(data, test_size=0.2):
    """
    Divise data in test and train dataset
    """
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=42)
    return train_data, test_data

def process_data_with_spark(file_path):
    """
    Process data with Apache Sparks
    """
    # Initialize a Spark session
    spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

    # Load data
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Example of preprocess
    # filter data
    df = df.filter(df["column_name"] > 0)

    #select columns
    df = df.select("column1", "column2")

    return df

if __name__ == "__main__":
    
    file_path = "data.csv"  # a csv with some data must be placed in the same folders than this code

    # Load and preprocess data
    data = load_and_preprocess_data(file_path)
    print("Preproceed data :")
    print(data.head())

    # Divide data
    train_data, test_data = split_data(data)
    print(f"Train data length : {len(train_data)}")
    print(f"Test data length : {len(test_data)}")

    # Process data with Sparks
    spark_df = process_data_with_spark(file_path)
    print("Données traitées avec Spark :")
    spark_df.show()