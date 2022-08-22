# TODO: split into two files for the two different plot modes

import argparse
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

FILENAME = "obs_remote/phi/phi_extr.pkl"

FIGSIZE = (12,10)

def parse_dens_sel(s):
    if s[:2] == "mu":
        return (True, float(s.strip().split("=")[1]))
    elif s[:1] == "N":
        return (False, int(s.strip().split("=")[1]))
    raise ValueError("failed to parse density selection spec")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--loadname", type=str, default=FILENAME)
    parser.add_argument("--savename", type=str)
    parser.add_argument("--mode", type=str, default="stack_mu")
    parser.add_argument("--dens_sel", type=str)
    parser.add_argument("--Nf", type=int, default=4)
    # TODO: automatically read from DataFrame when possible
    parser.add_argument("--Nsites", type=int, default=16)
    parser.add_argument("--L_sel", type=int, nargs=2)
    args = parser.parse_args()

    if args.L_sel is not None:
        args.Nsites = args.L_sel[0] * args.L_sel[1]
        print(f"--L_sel given; overriding Nsites to {args.Nsites}")

    if args.dens_sel is not None:
        sel_mu, sel_val = parse_dens_sel(args.dens_sel)
    elif args.mode == "flux_vs_U":
        raise RuntimeError("provide dens_sel if using flux_vs_U mode")

    mpl.rcParams["font.size"] = 18

    df = pd.read_pickle(args.loadname)
    if args.L_sel is not None:
        df = df[(df.Lx == args.L_sel[0]) & (df.Ly == args.L_sel[1])]

    if args.mode == "stack_mu":
        mus = sorted(set(df.mu))
        fig, axs = plt.subplots(len(mus), 1, figsize=FIGSIZE)
        if len(mus) == 1:
            axs = [axs]     # ew
        for i, mu in enumerate(mus):
            s = df.loc[df.mu == mu]

            # not sure if this correction should be here
#            s.loc[:,"E"] -= (s["mu"])*s["N"]

            s.loc[:,"E"] -= s["E"].min()

            X = 2*np.pi*s["phi_x"]
            axs[i].scatter(x=X, y=s["E"], marker="o")
            axs[i].set_xlabel("φ")
            axs[i].set_ylabel("E")
            axN = axs[i].twinx()
            axN.scatter(x=X, y=s["N"] / (args.Nsites * args.Nf),
                                                    marker="x", c="tab:red")
            axN.set_ylabel("n")
            axN.set_ylim((0,0.53))
            axN.set_yticks([0, 1/16,1/8,1/4,1/2], labels=["0", "1/16", "1/8", "1/4", "1/2"])
            axs[i].set_title(f"μ = {mu}")
    elif args.mode == "flux_vs_U":
        Us = sorted(set(df.U))
        fig, ax = plt.subplots(figsize=FIGSIZE)
        for U in Us:
            s = df.loc[df.U == U]
            if sel_mu:
                s = s.loc[s.mu == sel_val]
            else:
                s = s.loc[(s.N < sel_val+1) & (s.N > sel_val-1)]
            s.loc[:,"E"] -= s["E"].min()
            s.loc[:,"E"] /= s["E"].max()
            ax.scatter(s["phi_x"], s["E"], label=f"U = {U}")
            ax.set_xlabel("φ")
            ax.set_ylabel("E / (maximum)")
        plt.legend()
    else:
        raise ValueError(f"mode {args.mode} not recognized")


    if args.savename is not None:
        plt.tight_layout()
        plt.savefig(args.savename)
    plt.show()
