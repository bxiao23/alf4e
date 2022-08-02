from py_alf import ALF_source, Simulation

alf_src = ALF_source()
Simulation(alf_src, "Hubbard", {}, machine="GNU").compile()
