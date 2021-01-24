import os


def df_to_csv(df, directory, filename):
    path = os.path.join(directory, filename)
    print(f"Saving file to {path}")
    df.to_csv(path, index=False)