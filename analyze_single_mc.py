import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Nf = 4

def read_single_value(df, key):
    vals = set(df[key])
    if len(vals) == 1:
        return vals.pop()
    raise ValueError(f"multiple values of {key} found; please pass a specific value")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", type=float, default=1.0)
    parser.add_argument("--U", type=float, default=-1.0)
    parser.add_argument("--mu", type=float)
    parser.add_argument("--beta", type=float)
    parser.add_argument("--dtau", type=float)
    parser.add_argument("load_fn", type=str)
    args = parser.parse_args()

    df = pd.read_pickle(args.load_fn)

    if args.mu is None:
        args.mu = read_single_value(df, "mu")
        print("detected mu =", args.mu)
    if args.dtau is None:
        args.dtau = read_single_value(df, "dtau")
        print("detected dtau =", args.dtau)
    if args.beta is None:
        args.beta = read_single_value(df, "beta")
        print("detected beta =", args.beta)

    params = vars(args).copy()
    del params["load_fn"]

    sel = pd.concat([df[k] == v for k,v in params.items()], axis=1).all(axis=1)
    entry = df[sel].iloc[0]

    # ENERGY
    print(f"E = {entry['E']} ± {entry['dE']}")
    T = entry["T"] + args.mu * entry["N"]
    dT = np.sqrt(entry["dT"]**2 + (args.mu * entry["dN"])**2)
    print(f"T = {T} ± {dT}")
    print(f"V = {entry['V']} ± {entry['dV']}")

    # CORRS
    print(entry['DC'])
    print(entry['dDC'])
