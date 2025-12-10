import pandas as pd

df = pd.read_csv("C:/Users/USER/Desktop/Football-XAI-suite/data/master_football_xai_dataset.csv")

print("\nCOLUMNS IN DATASET:\n")
for col in df.columns:
    print(col)
