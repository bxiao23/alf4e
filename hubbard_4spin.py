import time
import datetime
import itertools
import os
import sys

import yaml
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm

LOOPABLE_KEYS = ["dtaus", "betas", "ts", "Us", "mus", "phis"]
SCALAR_KEYS = ["Nsweep", "Nbin", "Lx", "Ly", "Nf"]

DEFAULTS = {
                "overwrite_obs": False,
                "no_tqdm": True,
                "rescale_U": True,
                "use_Mz": False,
                "projector": False,
                "theta": 20,
                "N_auto": 0,
                "Nwrap": 10,
            }

def regularize_loopable_param(param, scalar_type=float):
    if isinstance(param, (list, tuple, set)):
        return [scalar_type(p) for p in param]
    if isinstance(param, (float, int)):
        return [scalar_type(param)]
    if isinstance(param, str) and param[:8] == "linspace":
        plist = param.split()
        # syntax: "linspace <start> <stop> <step>"
        if len(plist) != 4:
            raise ValueError(f"could not parse linspace specifier {param}")
        _, start, stop, res = plist
        return np.linspace(float(start), float(stop), int(res),
                                endpoint=True).tolist()
    raise ValueError(f"could not interpret key {param}")

def parse_config(fn):
    with open(fn) as f:
        config = yaml.safe_load(f)
    # ensure all required keys are present
    missing = [k for k in LOOPABLE_KEYS + SCALAR_KEYS if k not in config]
    if missing:
        raise ValueError(f"missing keys: {missing}")
    # set default parameters when applicable
    for k, v in DEFAULTS.items():
        config.setdefault(k, v)
    # regularize loopable keys
    for k in LOOPABLE_KEYS:
        config[k] = regularize_loopable_param(config[k])
    # turn phi into (phi_x, phi_y)
    config["phis"] = [(phi, phi) for phi in config["phis"]]

    return config

def savename(*, config, t, U, dtau, beta, mu, phi_x=None, phi_y=None,
                prefix=None):
    # {Nf}f_L{Lx}x{Ly}_t{t}_U{U}_mu{mu}[_pth{theta}]_phix{phi_x}_phiy{phi_y}
    if prefix is None:
        out = ""
    else:
        out = prefix
        if out[-1] != "/": out += "/"
    out += f"{config['Nf']}f_L{config['Lx']}x{config['Ly']}_t{t}_U{U}_mu{mu}"
    if config["projector"]: out += f"_pth{config['theta']}"

    if phi_x is not None: out += f"_phix{phi_x}"
    if phi_y is not None: out += f"_phiy{phi_y}"

    return out + ".pkl"


if __name__ == '__main__':
    from py_alf import ALF_source, Simulation

    parser = argparse.ArgumentParser()
    parser.add_argument("--obs_prefix", type=str, default="obs")
    parser.add_argument("--skip_run", action="store_true")
    parser.add_argument("--skip_config_report", action="store_true")
    parser.add_argument("config", type=str)
    args = parser.parse_args()

    print("RUN STARTED AT",
            datetime.datetime.today().strftime("%Y-%m-%d @ %H:%M:%S"))

    # load the config
    config = parse_config(args.config)
    NSUN = config["Nf"]
    NFL = 1

    if not args.skip_config_report:
        print("configuration dump below:")
        print(yaml.dump(config))

    # ==== actually do the run ====
    tot_runs = np.prod([len(l) for l in (config["dtaus"],
                                         config["betas"],
                                         config["ts"],
                                         config["Us"],
                                         config["mus"],
                                         config["phis"])])

    print(f"Nsweep, Nbin: {config['Nsweep']}, {config['Nbin']}")

    print("total number of runs:", tot_runs)

    alf_src = ALF_source()
    start = time.time()
    data_dirs = []
    for dtau in config["dtaus"]:
        for beta in config["betas"]:
            for t in config["ts"]:
                for U in config["Us"]:
                    for mu in tqdm(config["mus"], disable=config["no_tqdm"]):
                        for phi_x, phi_y in config["phis"]:
                            desc = f"t={t} U={U} mu={mu} dt={dtau} b={beta} phi=({phi_x},{phi_y})"
                            print("="*20, "STARTING", desc, "="*20)
                            print(f"elapsed time from run start: {time.time() - start:.1f} s")
                            obslist = []
                            save = savename(config=config,
                                        t=t, U=U, dtau=dtau, beta=beta, mu=mu,
                                        phi_x=phi_x, phi_y=phi_y,
                                        prefix=args.obs_prefix)
                            print("result file:", save)
                            if os.path.exists(save):
                                if not config["overwrite_obs"]:
                                    print("obs exists; skipping")
                                    continue
                                else:
                                    print("obs exists; overwriting")
                            sim = Simulation(
                                alf_src,
                                "Hubbard",
                                {
                                    "Lattice_type": "Square",
                                    "L1": config["Lx"],
                                    "L2": config["Ly"],
                                    "ham_u": (U * NSUN / 2 if config["rescale_U"] else U),
                                    "ham_chem": mu,
                                    "ham_T": t,
                                    "Projector": config["projector"],
                                    "Theta": config["theta"],
                                    "N_SUN": NSUN,
                                    "N_FL": NFL,
                                    "Mz": config["use_Mz"],
                                    "Dtau": dtau,
                                    "beta": beta,
                                    "NSweep": config["Nsweep"],
                                    "NBin": config["Nbin"],
                                    "N_auto": config["N_auto"],
                                    "Nwrap": config["Nwrap"],
                                    "Phi_X": phi_x,
                                    "Phi_Y": phi_y,
                                },
                                machine="GNU"
                            )
                            data_dirs.append(sim.sim_dir)

                            if not args.skip_run:
                                sim.run()
                                sim.analysis()

                            sim.get_obs().to_pickle(save)

                        print("="*20 + " DONE " + "="*20 + "\n")

    print("overall run complete; list of generated directories follows:")
    for d in data_dirs:
        print(d)
