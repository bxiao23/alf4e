import os
import sys
import argparse
import numpy as np

sys.path.append(os.path.expanduser('~/miscutils'))
import chi2

def exp_func(x, A, t):
    return A * np.exp(-t * x)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("loadname", type=str)
    parser.add_argument("--savename", type=str)
    args = parser.parse_args()

    with open(args.loadname, "r") as f:
        lines = f.readlines()

    Os = []
    dOs = []
    for line in lines:
        line = line.strip().split()
        if len(line) == 3:
            _, O, dO = line
            Os.append(float(O))
            dOs.append(float(dO))

    Os = np.array(Os)
    dOs = np.array(dOs)
    X = np.arange(len(Os))
    (_, t), (_, dt), _, c2prob, _ = chi2.fit_chi2(exp_func, X, Os, sig=dOs)
    print("t:", t)
    print("dt:", dt)
    print("chi2 prob:", c2prob)

    if args.savename is not None:
        np.save(args.savename, np.stack((Os, dOs)))
