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

def plot_common_E(df, param, param_str=None, sel=None,
                    normalize_E=False, base_phi=None, errorbars=True,
                    plot_reflected=False,
                    figsize=FIGSIZE):
    if param_str is None:
        param_str = str(param)
    fig, ax = plt.subplots(figsize=figsize)
    if sel is not None:
        for key, val in sel.items():
            df = df[df[key] == val]
    Ps = sorted(set(df[param]))
    for P in Ps:
        s = df.loc[df[param] == P]
        if base_phi is None:
            s.loc[:,"E"] -= s["E"].min()
        else:
            phi_idx = s[s["phi_x"] == base_phi].index.tolist()[0]
            base_E = s.loc[phi_idx]["E"]
            s.loc[:,"E"] = s.loc[:,"E"] - base_E
        print(s[["phi_x", param, "E"]])
        if normalize_E:
            s.loc[:,"E"] /= s["E"].max()
        s = s.sort_values(by="phi_x")
        yerr = s["dE"] if errorbars else 0
        ax.errorbar(x=s["phi_x"], y=s["E"], yerr=yerr,
                            label=f"{param_str} = {P}",
                            marker="o")

        # symmetry check
        if plot_reflected:
            s = s[s["phi_x"] <= 0.5]
            s["phi_x"] = 1 - s["phi_x"]
            yerr = s["dE"] if errorbars else 0
            ax.errorbar(x=s["phi_x"], y=s["E"], yerr=yerr,
                                label=f"{param_str} = {P} reflected",
                                marker="o")

        ax.set_xlabel("φ")
        ylabel = "E"
        if base_phi is not None:
            ylabel += f" - E[phi={base_phi}]"
        if normalize_E:
            ylabel += f" (normalized)"
        ax.set_ylabel(ylabel)
    plt.legend()
    return fig, ax

def plot_NE_vert_stack(df, param, Nf=4, param_str=None, dens=True,
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
            Ys = s["N"] / (Nf * s.Lx * s.Ly)
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
                            help="plot mode (note these are custom-defined)")
    parser.add_argument("--true_N", action='store_true',
                            help="for plots involving N, use total number instead of avg. density")
    parser.add_argument("--figsize", type=int, nargs=2, default=FIGSIZE)
    args = parser.parse_args()

    df = pd.read_pickle(args.loadname)

    # ===== ACTUAL PLOTTING =====

    # stack plots vertically; each plot is a dispersion and N-vs-phi curve
    #   for a given value of mu.
    if args.mode == "stack_mu":
        fig, axs = plot_NE_vert_stack(df, param="mu", param_str="μ",
                                        dens=(not args.true_N), figsize=args.figsize)

    elif args.mode == "stack_L":
        if not (df.Lx == df.Ly).all():
            raise NotImplementedError("flux_vs_L mode currently only supports square lattices")
        fig, axs = plot_NE_vert_stack(df, param="Lx", param_str="L",
                                        dens=(not args.true_N), figsize=args.figsize)

    # plot multiple dispersions on the same axes; each line is for a given
    #   value of whatever parameter.
    elif args.mode == "mult_U":
        sel = {}
        fig, ax = plot_common_E(df, param="U", sel=sel, normalize_E=False,
                                    base_phi=0.0,
                                    figsize=args.figsize)

    elif args.mode == "mult_L":
        sel = {}
        df = df[df.Lx == 4]
        df = df[df.dE < 3]
        fig, ax = plot_common_E(df, param="Lx", sel=sel, normalize_E=False,
                                    base_phi=0.0, errorbars=True,
                                    plot_reflected=False,
                                    figsize=args.figsize)

    else:
        raise ValueError(f"mode {args.mode} not recognized")

    if args.savename is not None:
        plt.tight_layout()
        plt.savefig(args.savename)
    plt.show()
