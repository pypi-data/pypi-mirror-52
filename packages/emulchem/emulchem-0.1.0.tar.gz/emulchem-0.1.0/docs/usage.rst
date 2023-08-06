=====
Usage
=====

Emulchem is a python wrapper for astrochemical emulators. The module contains emulators for astrochemcial models of molecules. These can be accessed by instantiating a python object associated to the molecule as follows::

    import emulchem
    CS = emulchem.ChemistryEmulator(specie="CS")
    
To get a list of all of the molecules included in the package, the following command can be run::

    emulchem.molecule_list()
    
Predictions can be obtained through the instantiated object as follows::
    
    CS.get_prediction(radfield,zeta,density,av,temperature,metallicity)


Notice that it is possible to see the units expected by the emulator (the units are consistent between molecules) by calling::

    help(CS.get_prediction)

The module also contains emulators for the radiative transfer module RADEX. These are useful for prototyping but are not perfectly accurate and are run over a limited grid. As such they should not be run in final analysis!!!

Here is a more complicated example of using the module that involves running an MCMC grid using the emcee python package::

    import emcee
    
    def something():
        pass

The associated posteriors are then as follows


