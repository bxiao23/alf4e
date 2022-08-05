import pandas as pd

def extract_mc_series_pd(mc_data, t, U, dtau, beta):
    return mc_data[(mc_data["t"] == t) & (mc_data["U"] == U) & \
                    (mc_data["dtau"] == dtau) & (mc_data["beta"] == beta)]
