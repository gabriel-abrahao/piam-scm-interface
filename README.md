# piam-scm-interface
This is a very rough prototype of a Python interface for simple climate models (SCMs) to be used by PIAM models. 

This repository is supposed to be independent of the model, with its path and any configurations being communicated to the interface via the model's own configuration files.

Currently this only works for calling MAGICC6 from REMIND. The only advantage over the current (July 2021) REMIND MAGICC implementation is the output of all the SCM's variables instead of just the ones used in the REMIND loop. In the near future, the interface should work transparently with other versions of MAGICC and other SCMs such as FAIR using [openscm-runner](https://github.com/openscm/openscm-runner).

## Setting up the environment
The simplest way to set up an environment to use this interface is running `create_env.sh`. It just generates a venv in the `venv_scm` folder using `pip` and the contents of `requirements.txt`. 

    ./create_env.sh

This is probably not the best solution, but provides an absolute path to a ready to use python interpreter which is set in the REMIND configuration.

## Testing usage using dummy_remind_run
The `dummy_remind_run` mimicks a REMIND run folder with a GAMS file that illustrates how this interface can be called from REMIND. 

To try it out, just go into that directory and run `gams_test.gms` after setting up the environment, no need to activate it.

    cd dummy_remind_run
    gams gams_test.gms

More on this in `dummy_remind_run/README.md`

## Using within REMIND

[This branch of REMIND](https://github.com/gabriel-abrahao/remind/tree/openscm) has a prototype of how this interface can work within it. There are two new flags set in `default.cfg` that point to the python interpreter in the virtual environment (`c15_pythonpath`) and to the interface script `run_REMIND.py` (`c15_scminterfacepath`). 

Values set in the branch currently point to locations in `/p/projects/piam/abrahao/piam-scm-interface/`.

To use it, just set the 15_climate module to the `openscm` realization in any run. It should work just like using the `magicc` realization for now, with the addition of writing the full MAGICC output to a `scm_output.csv` in the run folder.

## Desired improvements
 - [x] MAGICC6 support via [pymagicc](https://github.com/openscm/pymagicc)
 - [x] Export all common SCM output in a CSV/RDS
   - [ ] Include this output in the REMIND reporting workflow
   - [ ] Expand output to include optional variables such as carbon stocks
 - [ ] Move most of the code in the run script into a class to make changes in its behavior via `cfg.txt` more organized
 - [ ] Switch core run to [openscm-runner](https://github.com/openscm/openscm-runner)
   - [ ] FAIR model support
   - [ ] MAGICC7 model support (depends on access to its binary)
 - [ ] Support for running a batch of runs to estimate a Temperature Impulse Response function (TIRF)
 - [ ] Support for statistical runs (depends on extra tuning files)
