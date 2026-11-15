import os
import sys


def main():
    bin_dir, script_file = sys.argv[1:3]
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    import gmatpy

    gmatpy.Setup(os.path.join(bin_dir, "gmat_startup_file.txt"))
    if hasattr(gmatpy, "Clear"):
        gmatpy.Clear()
    if gmatpy.LoadScript(script_file) is False:
        raise RuntimeError("GMAT could not load Ex_OFI_LunarTransfer")
    if gmatpy.RunScript() is False:
        raise RuntimeError("GMAT could not run Ex_OFI_LunarTransfer")


if __name__ == "__main__":
    main()
