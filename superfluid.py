import argparse
import numpy as np
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("loadname", type=str)
    parser.add_argument("--cmp_phi", type=float, nargs=2, default=(0,0.25))
    parser.add_argument("--savename", type=str)
    args = parser.parse_args()

    SEL = {"U": -4.0, "mu": -0.25, "Lx": 8}

    df = pd.read_pickle(args.loadname)
    for k, v in SEL.items():
        df = df[df[k] == v]

    phi0, phi1 = args.cmp_phi
    df_phi0 = df[df["phi_x"] == phi0].set_index("beta")
    df_phi1 = df[df["phi_x"] == phi1].set_index("beta")

    E_diff = df_phi1["E"] - df_phi0["E"]
    E_diff_err = np.sqrt(df_phi0["dE"].pow(2) + df_phi1["dE"].pow(2))
    E_diff_err_pct = E_diff_err / E_diff.abs() * 100
    N0 = df_phi1["N"]
    dN0 = df_phi1["dN"]
    N1 = df_phi0["N"]
    dN1 = df_phi0["dN"]
    N_diff = N1 - N0
    N_diff_pct = N_diff / N0 * 100

    result = pd.DataFrame({
                "E_diff": E_diff,
                "E_diff_err": E_diff_err,
                "E_diff_err_pct": E_diff_err_pct,
                "N0": N0,
                "dN0": dN0,
                "N1": N1,
                "dN1": dN1,
                "N_diff": N_diff,
                "N_diff_pct": N_diff_pct,
             })

    print(result)

    if args.savename is not None:
        result.to_pickle(args.savename)
        print("saved to", args.savename)
