# 4ealf
ALF (Algorithms for Lattice Fermions) AFQMC scripts for four-election project

## Installation

1. Install [ALF](https://git.physik.uni-wuerzburg.de/ALF/ALF) and [pyALF](https://git.physik.uni-wuerzburg.de/ALF/pyALF). For reference we call these `ALF_HOME` and `PYALF_HOME`.
2. If using the modifications (right now I'm not) run `stow -d modified_files -t ALF_HOME alf` to install them.
3. Edit `prep.sh` so that it sets `ALF_DIR` to `ALF_HOME` and adds `PYALF_HOME` to `PYTHONPATH`.
4. Run `compile_alf.py`.
