# Dummy REMIND run

This folder mimicks a REMIND run folder for testing communications

The title of the run is 'testOneRegi', but the folder name doesn't make a difference because the title is read from cfg.txt
It contains just the basic files needed from a run:
 - `cfg.txt` for obtaining configuration flags, presently just the run title. The paths for python and this interface are also in the cfg since they are set on REMIND.
 - `magicc/REMIND_testOneRegi.SCEN` which is the MAGICC scenario file generated by REMIND. This should be generated by this interface in the future.

`gams_test.gms` reproduces the relevant parts of the REMIND code, including preallocating data input read from `example_temp_data.gms`.
Running `gams_test.gms` from this folder should do the equivalent of `full.gms`, including calling `run_REMIND.py` and assimilating the generated GDX files. It should generate:

 - `p15_magicc_temp.gdx` containing output surface temperature that is assimilated back into GAMS
 - `p15_forc_magicc.gdx` containing output anthropogenic radiative forcing that is assimilated back into GAMS
 - `scm_output.csv` containing all available output from the climate model. Some optional MAGICC outputs, such as carbon stocks, are not available yet.

