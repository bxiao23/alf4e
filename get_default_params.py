def print_nested_dict(d, nesting=0, sep="  "):
    for k, v in d.items():
        print(nesting*sep + f"{k}: ", end="")
        if isinstance(v, dict):
            print("[dict]")
            print_nested_dict(v, nesting=nesting+1, sep=sep)
        else:
            print(f"{v}")
        if not nesting:
            print("")

if __name__ == '__main__':
    from py_alf import ALF_source
    alf_src = ALF_source()
    print_nested_dict(alf_src.get_default_params("Hubbard"))
