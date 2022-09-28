import os
import argparse
import pandas as pd

NF_IS_NSUN = True       # whether flavors are incorporated via N_SUN or N_FL

def is_agg_or_ext(filename):
    return (filename[:2] == "AG" or filename[:2] == "EX")

def add_affixes(filename, prefix=None, suffix=None):
    if prefix is not None and filename[:(len(prefix))] != prefix:
        filename = prefix + filename
    if suffix is not None and filename[-(len(suffix)):] != suffix:
        filename = filename + suffix
    return filename

def regularize_agg_fn(filename):
    return add_affixes(filename, prefix="AG_", suffix=".pkl")

def regularize_extr_fn(filename):
    return add_affixes(filename, prefix="EX_", suffix=".pkl")

class Sequence:
    def __init__(self):
        self.c = 0
    def bump(self, *args, **kwargs):
        out = self.c
        self.c += 1
        return out

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--obs_prefix", type=str, default="obs")
    parser.add_argument("--save_agg", type=str,
                            help="where to save aggregated dataset")
    parser.add_argument("--save_extr", type=str,
                            help="where to save processed dataset")
    parser.add_argument("--no_rescale", action="store_true")
    parser.add_argument("--Nf", type=int)
    parser.add_argument("--shift_mu", type=float,
                            help="apply an add'l shift to mu")
    parser.add_argument("--no_seq", action="store_true",
                            help="do not rename rows of processed dataset")
    args = parser.parse_args()

    if args.Nf is not None:
        print("notice: args.Nf no longer being used; reading Nf directly from dataframe instead")

    args.obs_prefix = add_affixes(args.obs_prefix, suffix="/")

    # ===== dataset aggregation =====
    dfs = []
    for fn in os.listdir(args.obs_prefix):
        if is_agg_or_ext(fn):
            continue
        if fn.split(".")[-1] == "pkl":
            dfs.append(pd.read_pickle(f"{args.obs_prefix}{fn}"))

    df = pd.concat(dfs)
    if args.save_agg is not None:
        df.to_pickle(f"{args.obs_prefix}{regularize_agg_fn(args.save_agg)}")

    # ===== dataset processing/extraction =====

    param_keys = ["t", "U", "mu", "beta", "dtau", "phi_x", "phi_y",
                        "Lx", "Ly", "Nf"]
    param_names = ["ham_t", "ham_u", "ham_chem", "beta", "dtau",
                    "phi_x", "phi_y", "l1", "l2",
                    "n_sun" if NF_IS_NSUN else "n_fl"]

    observables = ["N", "E", "T", "V"]
    obs_names_base = ["Part", "Ener", "Kin", "Pot"]

    obs_errs = ["d"+o for o in observables]
    obs_signs = ["s"+o for o in observables]
    obs_names = [o + "_scal0" for o in obs_names_base]
    obs_err_names = [o + "_scal0_err" for o in obs_names_base]
    obs_sign_names = [o + "_scal_sign" for o in obs_names_base]

    lattice_obs = ["DC"]
    lattice_obs_names = ["Den_eqR_sum"]
    lattice_obs_errs = ["d" + o for o in lattice_obs]
    lattice_obs_err_names = [o + "_err" for o in lattice_obs_names]

    select = param_names + obs_names   + obs_err_names + obs_sign_names + \
                lattice_obs_names + lattice_obs_err_names
    labels = param_keys  + observables + obs_errs      + obs_signs      + \
                lattice_obs       + lattice_obs_errs
    translate = {old:new for old, new in zip(select, labels)}

    df = df[select].rename(translate, axis=1)
    if not args.no_seq:
        s = Sequence()
        df = df.rename(s.bump, axis=0)
    if not args.no_rescale:
#        df["U"] *= 2 / args.Nf
        df["U"] *= 2 / df["Nf"]
    if args.shift_mu is not None:
        df["mu"] += args.shift_mu
    df["rescale"] = (not args.no_rescale)

    if args.save_extr is not None:
        df.to_pickle(f"{args.obs_prefix}{regularize_extr_fn(args.save_extr)}")
