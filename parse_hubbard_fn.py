ALF_FMT_KEYS = ["ham_u", "ham_chem", "T", "Dtau", "beta"]
KEYS = ["U", "mu", "t", "dtau", "beta"]

def parse_fn(fn):
    entries = fn.split("_")
    entries = dict(e.split("=") for e in entries if "=" in e)
    return {k:entries[alf_k] for alf_k, k in zip(ALF_FMT_KEYS, KEYS)}

if __name__ == "__main__":
    pass
