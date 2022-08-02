import pandas as pd

def extract_mc_series_pd(mc_data, t, U):
    return mc_data.loc[(mc_data["t"] == t) & (mc_data["U"] == U)].drop(columns=["t","U"])
