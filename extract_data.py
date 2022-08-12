import argparse
import pandas as pd

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--obs_prefix", type=str, default="obs")
    parser.add_argument("--loadname", type=str,
                                default="L2x2_mu_data_aggregate.pkl")
    parser.add_argument("--savename", type=str,
                                default="L2x2_mu_data_extracted.pkl")
    parser.add_argument("--no_rescale", action="store_true")
    parser.add_argument("--Nf", type=int, default=4)
    args = parser.parse_args()

    SEQUENTIALIZE = True

    class Sequence:
        def __init__(self):
            self.c = 0
        def bump(self, *args, **kwargs):
            out = self.c
            self.c += 1
            return out

    param_keys = ["t", "U", "mu", "beta", "dtau", "phi_x", "phi_y"]
    param_names = ["ham_t", "ham_u", "ham_chem", "beta", "dtau",
                    "phi_x", "phi_y"]

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


    df = pd.read_pickle(f"{args.obs_prefix}/{args.loadname}")
    df = df[select].rename(translate, axis=1)
    if SEQUENTIALIZE:
        s = Sequence()
        df = df.rename(s.bump, axis=0)
    if not args.no_rescale:
        df["U"] *= 2 / args.Nf
    df["rescale"] = (not args.no_rescale)
    df.to_pickle(f"{args.obs_prefix}/{args.savename}")
