import os
import pandas as pd

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--obs_prefix", type=str, default="obs")
    parser.add_argument("--savename", type=str,
                        default="L2x2_mu_data_aggregate.pkl")
    args = parser.parse_args()

    SAVENAME = f"{args.obs_prefix}/{args.savename}"

    dfs = []
    for fn in os.listdir(args.obs_prefix):
        if fn == SAVENAME:
            continue
        if fn.split(".")[-1] == "pkl":
            dfs.append(pd.read_pickle(f"{args.obs_prefix}/{fn}"))

    df = pd.concat(dfs)
    df.to_pickle(SAVENAME)
