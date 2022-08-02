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

DTAUS = [0.1, 0.07, 0.05, 0.01]
BETAS = [10, 20, 40]
TS = [0.01, 0.1, 1.0, 2.0]
US = [4.0, 2.0, 1.0, 0.5, 0.1, -0.1, -0.5, -1.0, -2.0, -4.0]
MUS = np.linspace(-4,4,21)

#===================== USER-DEFINED PARAMETERS ================================

OVERWRITE_OBS = False

NO_TQDM = True

Lx = Ly = 2
Nf = 4
rescale_U = True
use_Mz = False

projector = False
theta = 20

# don't change these
NSUN = Nf
NFL = 1

#==============================================================================

def savename(t, U, dtau, beta):
    return f"obs/L2x2_t{t}_U{U}_dt{dtau}_b{beta}.pkl"

if __name__ == '__main__':

#============================ THE RUN =========================================

    print("total number of t/U/dt/b loops:", len(DTAUS)*len(BETAS)*len(TS)*len(US))

    alf_src = ALF_source()
    for dtau in DTAUS:
        for beta in BETAS:
            for t in TS:
                for U in US:
                    print("="*20 + f" STARTING t={t} U={U} dt={dtau} b={beta} " + "="*20)
                    if os.path.exists(savename(t, U, dtau, beta)):
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
                            },
                            machine="GNU"
                        )

                        sim.run()

                        sim.analysis()
                        obslist.append(sim.get_obs())

                    pd.concat(obslist).to_pickle(savename(t, U, dtau, beta))
                    print("="*20 + " DONE " + "="*20 + "\n")
