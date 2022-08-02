import os
import pandas as pd

OBS_DIR = "obs"

SAVENAME = f"{OBS_DIR}/L2x2_mu_data_aggregate.pkl"

dfs = []
for fn in os.listdir(OBS_DIR):
    if fn == SAVENAME:
        continue
    if fn.split(".")[-1] == "pkl":
        dfs.append(pd.read_pickle(fn))

df = pd.concat(dfs)
df.to_pickle(SAVENAME)
