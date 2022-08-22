import time
import itertools
import os
import sys

import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    from py_alf import ALF_source, Simulation

#===================== PARAMETER SEARCH SPACE =================================

PARAMS = 3
Lsel = 12        # currently only used when PARAMS == 3

if PARAMS == 1:
    # 2-fermion check run for the first phi sweep
    DTAUS = [0.02]
    BETAS = [20]
    TS = [1.0]
    US = [-1.0]
    MUS = [0.0, -1.0, -2.0]
    PHI_VALS = np.linspace(0,1,21,endpoint=True).tolist()
    Nsweep = 150
    Nbin = 15
    Lx = Ly = 4
    Nf = 2
elif PARAMS == 2:
    # in-depth mu sweep at high U
    DTAUS = [0.02]
    BETAS = [20]
    TS = [1.0]
    US = [-5.0, -7.0, -9.0]
#    MUS = [-1.0, -1.5, -2.0, -2.5]
    MUS = [-1.0, -1.25, -1.5, -1.75, -2.0, -2.25, -2.5]
    PHI_VALS = np.linspace(0,1,17,endpoint=True).tolist()
    Nsweep = 150
    Nbin = 15
    Lx = Ly = 4
    Nf = 4
elif PARAMS == 3:
    # t = -U = 1.0 and mu = -2.0 with large lattice size
    DTAUS = [0.04]
    BETAS = [20]
    TS = [1.0]
    US = [-1.0]
    MUS = [-2.0]
    PHI_VALS = np.linspace(0,1,17,endpoint=True).tolist()
    Nsweep = 60
    Nbin = 6
    Lx = Ly = Lsel
    Nf = 4
elif PARAMS == 4:
    # in-depth mu sweep at lower U
    DTAUS = [0.04]
    BETAS = [20]
    TS = [1.0]
    US = [-0.5, -1.0, -2.0]
    MUS = [-1.0, -1.25, -1.5, -1.75, -2.0, -2.25, -2.5]
    PHI_VALS = np.linspace(0,1,17,endpoint=True).tolist()
    Nsweep = 150
    Nbin = 15
    Lx = Ly = 4
    Nf = 4
else:
    raise RuntimeError()

#PHIS = [(phi, 0) for phi in PHI_VALS] + [(phi, phi) for phi in PHI_VALS]
PHIS = [(phi, phi) for phi in PHI_VALS]

tot_runs = np.prod([len(l) for l in (DTAUS, BETAS, TS, US, MUS, PHIS)])

#======================== OTHER PARAMETERS ===================================

OVERWRITE_OBS = False

NO_TQDM = True

rescale_U = True
use_Mz = False

projector = False
theta = 20

# don't change these
NSUN = Nf
NFL = 1

#==============================================================================

def savename(t, U, dtau, beta, mu, proj=False, theta=theta, prefix=None,
                phi_x=None, phi_y=None):
    if prefix is None:
        out = ""
    else:
        out = prefix
        if out[-1] != "/": out += "/"
    out += f"L{Lx}x{Ly}_t{t}_U{U}_mu{mu}"
    if proj: out += f"_pth{theta}"

    if phi_x is not None: out += f"_phix{phi_x}"
    if phi_y is not None: out += f"_phiy{phi_y}"

    return out + ".pkl"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--obs_prefix", type=str, default="obs")
    parser.add_argument("--skip_run", action="store_true")
    args = parser.parse_args()

#============================ THE RUN =========================================

    print(f"Nsweep, Nbin: {Nsweep}, {Nbin}")

    print("total number of runs:", tot_runs)

    alf_src = ALF_source()
    start = time.time()
    for dtau in DTAUS:
        for beta in BETAS:
            for t in TS:
                for U in US:
                    for mu in tqdm(MUS, disable=NO_TQDM):
                        for phi_x, phi_y in PHIS:
                            desc = f"t={t} U={U} mu={mu} dt={dtau} b={beta} phi=({phi_x},{phi_y})"
                            print("="*20, "STARTING", desc, "="*20)
                            print(f"elapsed time from run start: {time.time() - start:.1f} s")
                            obslist = []
                            save = savename(t=t, U=U, dtau=dtau, beta=beta,
                                        proj=projector, theta=theta,
                                        mu=mu, phi_x=phi_x, phi_y=phi_y,
                                        prefix=args.obs_prefix)
                            print("result file:", save)
                            if os.path.exists(save):
                                if not OVERWRITE_OBS:
                                    print("obs exists; skipping")
                                    continue
                                else:
                                    print("obs exists; overwriting")
                            sim = Simulation(
                                alf_src,
                                "Hubbard",
                                {
                                    "Lattice_type": "Square",
                                    "L1": Lx,
                                    "L2": Ly,
                                    "ham_u": (U * Nf / 2 if rescale_U else U),
                                    "ham_chem": mu,
                                    "ham_T": t,
                                    "Projector": projector,
                                    "Theta": theta,
                                    "N_SUN": NSUN,
                                    "N_FL": NFL,
                                    "Mz": use_Mz,
                                    "Dtau": dtau,
                                    "beta": beta,
                                    "NSweep": Nsweep,
                                    "NBin": Nbin,
                                    "Phi_X": phi_x,
                                    "Phi_Y": phi_y,
                                },
                                machine="GNU"
                            )

                            if not args.skip_run:
                                sim.run()
                                sim.analysis()

                            sim.get_obs().to_pickle(save)

                        print("="*20 + " DONE " + "="*20 + "\n")
