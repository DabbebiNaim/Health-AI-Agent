import pandas as pd
import json
import os

# --- Configuration ---
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "medical_graph_data.json")

def clean_text(text):
    if isinstance(text, str):
        # Fix common typos in this specific dataset
        text = text.strip()
        text = text.replace("dischromic _patches", "dischromic patches")
        text = text.replace("spotting_ urination", "spotting urination")
        return text
    return text

def main():
    print("Loading data...")
    try:
        # 1. Load the CSV files from the 'data' folder
        df_dataset = pd.read_csv(os.path.join(DATA_DIR, "dataset.csv"))
        df_desc = pd.read_csv(os.path.join(DATA_DIR, "symptom_Description.csv"))
        df_prec = pd.read_csv(os.path.join(DATA_DIR, "symptom_precaution.csv"))
        df_sev = pd.read_csv(os.path.join(DATA_DIR, "Symptom-severity.csv"))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure your CSV files are inside the 'data' folder!")
        return

    # 2. Apply cleaning
    print("Cleaning text...")
    df_dataset = df_dataset.map(clean_text)
    df_desc['Disease'] = df_desc['Disease'].apply(clean_text)
    df_prec['Disease'] = df_prec['Disease'].apply(clean_text)
    df_sev['Symptom'] = df_sev['Symptom'].apply(clean_text)

    # 3. Restructure Data
    print("Merging and structuring data...")
    graph_data = []
    
    # Get unique diseases
    unique_diseases = df_dataset['Disease'].unique()

    for disease in unique_diseases:
        # Get Description
        desc_row = df_desc[df_desc['Disease'] == disease]
        description = desc_row.iloc[0]['Description'] if not desc_row.empty else "No description available."

        # Get Precautions
        prec_row = df_prec[df_prec['Disease'] == disease]
        precautions = []
        if not prec_row.empty:
            p_list = prec_row.iloc[0][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].dropna().tolist()
            precautions = [p for p in p_list if isinstance(p, str)]

        # Get Symptoms
        d_rows = df_dataset[df_dataset['Disease'] == disease]
        all_symptoms = set()
        for _, row in d_rows.iterrows():
            for i in range(1, 18):
                col_name = f"Symptom_{i}"
                if col_name in row and pd.notna(row[col_name]):
                    all_symptoms.add(row[col_name])
        
        # Add weights to symptoms
        final_symptoms = []
        for sym in all_symptoms:
            weight_row = df_sev[df_sev['Symptom'] == sym]
            weight = int(weight_row.iloc[0]['weight']) if not weight_row.empty else 1
            final_symptoms.append({"name": sym, "weight": weight})

        # Build Object
        disease_obj = {
            "name": disease,
            "description": description,
            "symptoms": final_symptoms,
            "precautions": precautions
        }
        graph_data.append(disease_obj)

    # 4. Save to JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(graph_data, f, indent=2)

    print(f"✅ Success! Processed {len(graph_data)} diseases.")
    print(f"📁 Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()