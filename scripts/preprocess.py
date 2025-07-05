import pandas as pd

import sys

def preprocess(dataPATH, outputPATH):
    print("\n===       PREPROCESS EXECUTION STARTED      ===\n")

    try:
        data = pd.read_csv(dataPATH, sep=",")
    except FileNotFoundError:
        print(f"\nError: File not found at {dataPATH}\n")
        print("\n===        PREPROCESS EXECUTION FAILED      ===\n")
        sys.exit(1)
    beforeSize=data.shape
    print(f"\nData size before preprocessing: {beforeSize[0]}x{beforeSize[1]}")

    missing_values = data.isnull().sum().sum()
    if missing_values > 0:
        print("\nMissing Values Before Cleaning\n")
        print(data.isnull().sum())

        for col in data.columns:
            if data[col].dtype in ['float64', 'int64']:  
                data[col] = data[col].fillna(data[col].mean())
            else:  
                data[col] = data[col].fillna(data[col].mode()[0])

        print("\nMissing Values After Cleaning\n")
        print(data.isnull().sum())
    else:
        print("\nNo missing values detected.\n")

    duplicates = data.duplicated().sum()
    if duplicates > 0:
        print("\nDuplicates Before Cleaning\n")
        print(data.duplicated().sum())

        data = data.drop_duplicates()

        print("\nDuplicates After Cleaning\n")
        print(data.duplicated().sum())
    else:
        print("\nNo duplicate values detected.\n")

    for col in data.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        rows_before = data.shape[0]

        data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]

        rows_after = data.shape[0]

        print(f"Column '{col}': Removed {rows_before - rows_after} rows due to outliers.")

    afterSize=data.shape
    print(f"\nData size after preprocessing: {afterSize[0]}x{afterSize[1]}")
    print(f"\n{beforeSize[0]-afterSize[0]} columns removed.")
    
    data.to_csv(outputPATH, index=False)
    print(f"\n{outputPATH} saved successfully.\n")

    print("\n=== PREPROCESS EXECUTION ENDED SUCCESSFULLY ===\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nUsage: python preprocess.py <input_file> <output_file>\n")
        sys.exit(1)

    dataPATH = sys.argv[1]
    outputPATH = sys.argv[2]
    preprocess(dataPATH, outputPATH)