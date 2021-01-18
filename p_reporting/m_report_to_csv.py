def df_to_csv(df, path="data/results/report.csv"):
    print(f"Saving file to {path}")
    df.to_csv(path, index=False)