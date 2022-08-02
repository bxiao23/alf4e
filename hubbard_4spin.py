import itertools
import os

from py_alf import ALF_source, Simulation
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from tqdm import tqdm

#===================== USER-DEFINED PARAMETERS ================================

NO_TQDM = True


Lx = Ly = 2
Nf = 4
rescale_U = True
use_Mz = False

projector = False
theta = 20

#===================== AUTOMATIC PARAMETER SETUP ==============================

NSUN = Nf
NFL = 1

"""
Dtaus = {
        1: [0.2],
        2: [0.1],
        3: [0.05],
        4: [0.01]
     }

Betas = {
        1: [10],
        2: [20],
        3: [40]
     }
"""
Dtaus = {1: [0.1]}
Betas = {1: [20]}

Ts = {
      1: [0.01, 0.1],
      2: [1.0, 2.0],
     }
Us = {
      1: [4.0, 2.0, 1.0],
      2: [0.5, 0.1, -0.1, -0.5],
      3: [-1.0, -2.0, -4.0],
     }
Mus = np.linspace(-4,4,41)

#============================ THE RUN =========================================

alf_src = ALF_source()
for curr_t, Tc in Ts.items():
    for curr_U, Uc in Us.items():
        for curr_dtau, DTc in Dtaus.items():
            for curr_beta, Bc in Betas.items():

                obslist = []

                tot = len(Tc)*len(Uc)*len(DTc)*len(Bc)*len(Mus)
                desc=f"TUDB:{curr_t}{curr_U}{curr_dtau}{curr_beta}"

                for t, U, dtau, beta, mu in tqdm(itertools.product(Tc, Uc, DTc, Bc, Mus), total=tot,desc=desc, disable=NO_TQDM):
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

        res = pd.concat(obslist)
        res.to_pickle(f"obs/L2x2_mu_data_T{curr_t}_U{curr_U}_dt{curr_dtau}_b{curr_beta}.pkl")
