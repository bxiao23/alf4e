# some tags have underscores in them -- very annoying
# this still works for now but be careful when adding new things
ALF_FMT_KEYS = ["L1", "L2",
                "u", "chem", "T",
                "Dtau", "beta",
                "Projector", "Theta",
                "X", "Y"]
KEYS =         ["Lx", "Ly",
                "U", "mu", "t",
                "dtau", "beta",
                "projector", "theta",
                "phi_x", "phi_y"]

def parse_fn(fn):
    entries = fn.split("_")
    entries = dict(e.split("=") for e in entries if "=" in e)
    return {k:entries.get(alf_k, None) for alf_k, k in zip(ALF_FMT_KEYS, KEYS)}

def make_fn(name="Hubbard", params=None):
    from py_alf import ALF_source, Simulation
    if params is None:
        params = {}
    sim = Simulation(ALF_source(), name, params)
    return sim.sim_dir

if __name__ == "__main__":
    pass
