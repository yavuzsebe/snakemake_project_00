import pandas as pd
import numpy as np

import scipy.stats as stats

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
import seaborn as sns

import sys
import os

def visualize(dataPATH, outputPATH):
    print("\n===       VISUALIZATION EXECUTION STARTED      ===\n")
    dataALL, geneExpression = importData(dataPATH)
    
    generateSummary(dataALL, outputPATH)
    generatePVAL(dataALL, outputPATH)
    generatePCA(geneExpression, outputPATH)
    generateHeatmap(geneExpression, outputPATH)
    generateBoxplot(geneExpression, outputPATH)
    miscGraph(dataALL, outputPATH)

    print("\n=== VISUALIZATION EXECUTION ENDED SUCCESSFULLY ===\n")

def importData(dataPATH):
    try:
        dataALL = pd.read_csv(dataPATH, sep=",")
    except FileNotFoundError:
        print(f"\nError: File not found at {dataPATH}\n")
        print("\n===        VISUALIZATION EXECUTION FAILED      ===\n")
        sys.exit(1)
    
    geneExpression = dataALL.iloc[:,1:101]

    return dataALL, geneExpression

def generateSummary(dataALL, outputPATH):
    print("Generating summary:\n")

    dataColnames = list(dataALL.columns)
    dataDtypes = list(dataALL.dtypes)

    with open(f"{outputPATH}Summary{dataName}.txt", "w") as file:
        file.write("Summary Information\n")
        file.write("===================\n")
        
        file.write(dataALL.describe().to_string())

        file.write("\nNumerics\n")
        for i in range(0, len(dataColnames)):
            if dataDtypes[i] == 'float64':
                file.write(f"{dataColnames[i]}:\t{len(dataALL[dataColnames[i]].unique())}\n")

        file.write("\nObjects\n\n")
        for i in range(0, len(dataColnames)):
            if dataDtypes[i] != 'float64':
                file.write(f"{dataColnames[i]}:\t{len(dataALL[dataColnames[i]].unique())}\n")
                file.write(f"{dataALL[dataColnames[i]].unique()}\n\n")

    print(f"Information saved as data/Summary{dataName}.txt\n")

def generatePVAL(dataALL, outputPATH):
    print("Generating PVAL information:\n")

    healthySamples = dataALL[dataALL["Diagnosis"] == "Healthy"].iloc[:, 1:101]
    nonHealthySamples = dataALL[dataALL["Diagnosis"] != "Healthy"].iloc[:, 1:101]

    PVAL = []
    for i in range(healthySamples.shape[0]):
        tstat, pval = stats.ttest_ind(healthySamples.iloc[i, :], nonHealthySamples.iloc[i, :], equal_var=False)
        PVAL.append(pval)

    PVAL = np.array(PVAL)
    signpvals01 = np.where(PVAL < 0.01)[0]
    signpvals05 = np.where(PVAL < 0.05)[0]

    with open(f"{outputPATH}PVAL{dataName}.txt", "w") as file:
        file.write("PVAL Information\n")
        file.write("================\n")
        file.write(f"Number of healthy samples:\t{healthySamples.shape[0]}\n")
        file.write(f"Number of non-healthy samples:\t{nonHealthySamples.shape[0]}\n")
        file.write("\nFirst 5 PVALs:\n")
        file.write(f"{PVAL[:5]}\n")
        file.write("\nSignificant PVALs (< 0.01):\n")
        file.write(f"{PVAL[signpvals01]}\n")
        file.write("\nIndices of significant PVALs (< 0.01):\n")
        file.write(f"{signpvals01}\n")
        file.write("\nSignificant PVALs (< 0.05):\n")
        file.write(f"{PVAL[signpvals05]}\n")
        file.write("\nIndices of significant PVALs (< 0.05):\n")
        file.write(f"{signpvals05}\n")

    print(f"Information saved as {outputPATH}PVAL{dataName}.txt\n")

def generatePCA(geneExpression, outputPATH):
    print("Generating PCA:\n")
    scaler = StandardScaler()
    geneExpression_scaled = scaler.fit_transform(geneExpression)

    pca = PCA(n_components=2)
    gene_expression_pca = pca.fit_transform(geneExpression)
    print("Explained variance ratio:", pca.explained_variance_ratio_)

    plt.scatter(gene_expression_pca[:, 0], gene_expression_pca[:, 1], alpha=0.7)
    plt.title("PCA of Gene Expression")
    plt.xlabel(f"Principal Component 1\n(%{round(pca.explained_variance_ratio_[0],4)*100})")
    plt.ylabel(f"Principal Component 2\n(%{round(pca.explained_variance_ratio_[1],4)*100})")

    plt.savefig(f"{outputPATH}PCA{dataName}.png", dpi=300, bbox_inches="tight")
    print(f"Plot saved as data/PCA{dataName}.png\n")

def generateHeatmap(geneExpression, outputPATH):
    print("Generating heatmap:\n")
    plt.figure(figsize=(15, 12))
    
    sns.heatmap(geneExpression.iloc[:50, :50], cmap="viridis", xticklabels=True, yticklabels=True)
    plt.xticks(rotation=90)  
    plt.yticks(rotation=0)   
    plt.title("Heatmap of Gene Expression \n(First 50 Genes for First 50 Samples)")

    plt.savefig(f"{outputPATH}Heatmap{dataName}.png", dpi=300, bbox_inches="tight")
    print(f"Plot saved as data/Heatmap{dataName}.png\n")

def generateBoxplot(geneExpression, outputPATH):
    print("Generating boxplot:\n")
    plt.figure(figsize=(15, 12))
    
    sns.boxplot(data=geneExpression.iloc[:, :50])  
    plt.xticks(rotation=90)
    plt.yticks(rotation=0) 
    plt.title("Boxplot of Gene Expression \n(First 50 Genes)")

    plt.savefig(f"{outputPATH}Boxplot{dataName}.png", dpi=300, bbox_inches="tight")
    print(f"Plot saved as data/Boxplot{dataName}.png\n")

def miscGraph(dataALL, outputPATH):
    print("Generating miscellanous graph:\n")
    survival_by_diagnosis = dataALL.groupby("Diagnosis")["Survival_Months"].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Diagnosis", y="Survival_Months", hue="Diagnosis", data=survival_by_diagnosis, palette="viridis", dodge=False, legend=False)
    plt.title("Average Survival Months by Diagnosis", fontsize=16)
    plt.xlabel("Diagnosis", fontsize=14)
    plt.ylabel("Average Survival Months", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()

    plt.savefig(f"{outputPATH}miscGraph{dataName}.png", dpi=300, bbox_inches="tight")
    print(f"Plot saved as data/miscGraph{dataName}.png\n")

if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print("\nUsage: python preprocess.py <input_file> <output_folder>\n")
        sys.exit(1)
    dataPATH = sys.argv[1]
    outputPATH = sys.argv[2]
    dataName = dataPATH.split("/")[-1].replace("preprocessed", "").replace(".csv", "")

    if not os.path.exists(outputPATH):
        os.makedirs(outputPATH)

    visualize(dataPATH, outputPATH)