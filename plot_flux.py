# TODO: redo architecture

import argparse
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

FILENAME = "obs_remote/phi/phi_extr.pkl"

mpl.rcParams["font.size"] = 18
FIGSIZE = (12,10)

NTICKS = (0, 1/16, 1/8, 1/4, 1/2)
NTICKLABELS = ("0", "1/16", "1/8", "1/4", "1/2")

def parse_dens_sel(s):
    if s[:2] == "mu":
        return (True, float(s.strip().split("=")[1]))
    elif s[:1] == "N":
        return (False, int(s.strip().split("=")[1]))
    raise ValueError("failed to parse density selection spec")

def plot_NE_vert_stack(df, param,  param_str=None, dens=True,
                         draw_dens_lines=True, figsize=FIGSIZE):

    if param_str is None:
        param_str = str(param)
    Ps = sorted(set(df[param]))
    fig, axs = plt.subplots(len(Ps), 1, figsize=figsize)
    if len(Ps) == 1:
        axs = [axs]     # ew
    for i, P in enumerate(Ps):
        s = df.loc[df[param] == P]

        # not sure if this correction should be here
#            s.loc[:,"E"] -= (s["mu"])*s["N"]

        print(f"{param_str}={P} N stdev: {s['N'].std()}")
        print(f"{param_str}={P} N spread: {s['N'].max() - s['N'].min()}")

        s.loc[:,"E"] -= s["E"].min()

        X = 2*np.pi*s["phi_x"]
        axs[i].scatter(x=X, y=s["E"], marker="o")
        axs[i].set_xlabel("φ")
        axs[i].set_ylabel("E")
        axN = axs[i].twinx()
        if dens:
            Ys = s["N"] / (args.Nf * s.Lx * s.Ly)
            axN.set_ylabel("n")
            axN.set_ylim((0, max(NTICKS)*1.08))
            axN.set_yticks(NTICKS, labels=NTICKLABELS)
            if draw_dens_lines:
                for n in NTICKS:
                    axN.axhline(n, c="tab:red", alpha=0.1, linestyle="--")
        else:
            Ys = s["N"]
            axN.set_ylabel("N")
            axN.set_ylim((0, s["N"].max()*1.08))
        axN.scatter(x=X, y=Ys, marker="x", c="tab:red")
        axs[i].set_title(f"{param_str} = {P}")
    return fig, axs

if __name__ == "__main__":

    # ===== CONFIG PARSE AND INITIAL SETUP =====

    parser = argparse.ArgumentParser()
    parser.add_argument("--loadname", type=str, default=FILENAME,
                            help="DataFrame containing MC results")
    parser.add_argument("--savename", type=str,
                            help="filename for saving plot")
    parser.add_argument("--mode", type=str, default="stack_mu",
                            help="plot mode")
    parser.add_argument("--dens_sel", type=str,
                            help="select a value of N or mu " + \
                                 "(mostly for flux_vs_U mode)")
    parser.add_argument("--Nf", type=int, default=4,
                            help="number of fermion flavors")
    # TODO: automatically read from DataFrame when possible
    parser.add_argument("--L_sel", type=int, nargs=2,
                            help="lattice size")
    parser.add_argument("--true_N", action="store_true",
                            help="for stacked plots, plot N instead of n")
    parser.add_argument("--figsize", type=int, nargs=2, default=FIGSIZE)
    args = parser.parse_args()

    if args.L_sel is not None:
        if args.mode in ("stack_mu", "flux_vs_U"):
            raise RuntimeError("provide L_sel if using mu_stack or flux_vs_U")

    if args.dens_sel is not None:
        sel_mu, sel_val = parse_dens_sel(args.dens_sel)
    elif args.mode == "flux_vs_U":
        raise RuntimeError("provide dens_sel if using flux_vs_U")


    df = pd.read_pickle(args.loadname)
    if args.L_sel is not None:
        df = df[(df.Lx == args.L_sel[0]) & (df.Ly == args.L_sel[1])]

    # ===== ACTUAL PLOTTING =====

    # stack plots vertically; each plot is a dispersion and N-vs-phi curve
    #   for a given value of mu.
    if args.mode == "stack_mu":
        fig, axs = plot_NE_vert_stack(df, param="mu", param_str="μ",
                                        dens=(not args.true_N), figsize=args.figsize)

    # plot multiple dispersions on the same axes; each line is for a given
    #   value of mu or N.
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

    elif args.mode == "flux_vs_L":
        if not (df.Lx == df.Ly).all():
            raise NotImplementedError("flux_vs_L mode currently only supports square lattices")
        fig, axs = plot_NE_vert_stack(df, param="Lx", param_str="L",
                                        dens=(not args.true_N), figsize=args.figsize)

    else:
        raise ValueError(f"mode {args.mode} not recognized")

    if args.savename is not None:
        plt.tight_layout()
        plt.savefig(args.savename)
    plt.show()
