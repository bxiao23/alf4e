import pandas as pd
import matplotlib.pyplot as plt
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fn", type=str, default="obs_remote/L2x2_mu_data_extracted.pkl")
    parser.add_argument("--t", type=float, default=0.01)
    parser.add_argument("--U", type=float, default=-2.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--dtau", type=float, default=0.01)
    parser.add_argument("--beta", type=float, default=40)
    parser.add_argument("--plot", type=str, default="E")
    parser.add_argument("--against", type=str, default="dtau")
    args = parser.parse_args()

    assert args.plot in ("E", "T", "V", "N")
    assert args.against in ("dtau", "beta")

    fixed = "dtau" if args.against == "beta" else "beta"
    fixed_tgt = args.dtau if args.against == "beta" else args.beta

    df = pd.read_pickle(args.fn)
    df = df[(df["U"]==args.U)&(df["t"]==args.t)&(df[fixed]==fixed_tgt)&(df["mu"]==args.mu)]
    plt.errorbar(x=df[args.against], y=df[args.plot], yerr=df["d"+args.plot], linestyle="none", marker="+")
    plt.xlabel(args.against)
    plt.ylabel(args.plot)
    plt.show()
