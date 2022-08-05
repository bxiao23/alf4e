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

"""
DTAUS = [0.02, 0.05, 0.07, 0.1]
BETAS = [40, 30, 20, 10]
TS = [0.01, 0.1, 1.0, 2.0]
US = [-0.01, -0.1, -0.5, -1.0, -2.0, -4.0]
MUS = np.linspace(-4,4,11)
"""
DTAUS = [0.02]
BETAS = [10]
TS = [0.01, 0.1, 1.0, 2.0]
US = [-0.01, -0.1, -0.5, -1.0, -2.0, -4.0]
MUS = [0.0]

#===================== USER-DEFINED PARAMETERS ================================

OVERWRITE_OBS = False

NO_TQDM = True

Lx = Ly = 2
Nf = 4
rescale_U = True
use_Mz = False

projector = True
theta = 20

Nsweep = 40
Nbin = 5

# don't change these
NSUN = Nf
NFL = 1

#==============================================================================

def savename(t, U, dtau, beta, mu=None, proj=False, theta=theta):
    mu_str = f"_mu{mu}" if mu is not None else ""
    proj_str = f"_pth{theta}" if proj else ""
    pref = f"L{Lx}x{Ly}"
    if mu is not None:
        pref = "singlepoint_" + pref
    return f"obs/{pref}_t{t}_U{U}{mu_str}_dt{dtau}_b{beta}{proj_str}.pkl"

if __name__ == '__main__':

#============================ THE RUN =========================================

    print("total number of t/U/dt/b loops:", len(DTAUS)*len(BETAS)*len(TS)*len(US))

    alf_src = ALF_source()
    for dtau in DTAUS:
        for beta in BETAS:
            for t in TS:
                for U in US:
                    print("="*20 + f" STARTING t={t} U={U} dt={dtau} b={beta} " + "="*20)
                    save = savename(t=t, U=U, dtau=dtau, beta=beta,
                                    proj=projector, theta=theta,
                                    mu=(None if len(MUS) > 1 else MUS[0]))
                    if os.path.exists(save):
                        if not OVERWRITE_OBS:
                            print("obs exists; skipping")
                            continue
                        else:
                            print("obs exists; overwriting")
                    obslist = []
                    for mu in tqdm(MUS, disable=NO_TQDM):
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
                            },
                            machine="GNU"
                        )

                        sim.run()

                        sim.analysis()
                        obslist.append(sim.get_obs())

                    pd.concat(obslist).to_pickle(savename(save))
                    print("="*20 + " DONE " + "="*20 + "\n")
