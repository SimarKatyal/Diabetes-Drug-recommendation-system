import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
dataset = pd.read_csv("C:/Users/sinha/OneDrive/Desktop/Khushi/6th sem/projectfrontend/sugar-wise/BackEnd/diabetic_data2.csv")

# Select relevant columns
cols = ['insulin', 'metformin', 'glipizide', 'glyburide', 'pioglitazone', 
        'rosiglitazone', 'glimepiride', 'repaglinide', 'glyburide-metformin', 'nateglinide']
df = dataset[cols]

# Label encoding
df = df.replace({'No': 0, 'Yes': 1, 'Steady': -1, 'Up': 1, 'Down': 0})
df = df.dropna()

# Convert data to numpy array
patient_drug_matrix = df.to_numpy()

# Calculate cosine similarity matrix
cosine_similarities = cosine_similarity(patient_drug_matrix)

# New Patient Medication Information
new_patient_info = {}
print("Please enter whether the new patient is using each medication (Yes/No):")
for medication in cols:
    response = input(f"Is the new patient using {medication}? (Yes/No): ").strip().lower()
    if response == 'yes':
        new_patient_info[medication] = 1
    elif response == 'no':
        new_patient_info[medication] = 0
    else:
        print("Invalid response. Please enter 'Yes' or 'No'.")
        exit()

# Convert new patient info to numpy array
new_patient_array = np.array([list(new_patient_info.values())])

# Calculate similarity scores with existing patients
similarity_scores = cosine_similarity(new_patient_array, patient_drug_matrix)

# Find top similar patients
top_similar_patients_indices = np.argsort(similarity_scores[0])[::-1][:5]  # Assuming top 5 similar patients
top_similar_patients_data = patient_drug_matrix[top_similar_patients_indices]

# Aggregate drug recommendations from similar patients
recommendation = np.mean(top_similar_patients_data, axis=0)

# Get drug names for recommended drugs
recommended_drugs = [cols[i] for i, val in enumerate(recommendation) if val > 0]

# Print or return recommendations
if recommended_drugs:
    print("Recommended drugs:", recommended_drugs)
else:
    print("No recommendations based on similar patients.")