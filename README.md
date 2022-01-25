# stellapackage

**Currently under development**

This package is for reading and visualizing outputs of STELLA code (Blinnikov et al. 1998; https://iopscience.iop.org/article/10.1086/305375/)

## Requirements

Python package
- numpy
- matplotlib
- speclite (https://speclite.readthedocs.io/en/latest/index.html)
> 1. Install speclite following the description in the link above
> 2. Copy ZTF-g.ecsv and ZTF-r.ecsv and paste them inside _$speclite_DIR/speclite/data/filters/_
> 3. Copy filters.py and paste it inside _$speclite_DIR/speclite/_, replacing the original filters.py


## Capability

1. Read following inputs: .abn .hyd
2. Read following outputs: .res .swd .tt .ph


.abn: zone number, mass fraction of elements (H, He, C, N, O, Ne, Mg, Si, S, Ar, Ca, Fe, Ni)

  (*to adjust elements, modify abnkeys in STLkeys.py*)
  
.hyd: zone number, dm, radius, rho, temperature, velocity, mass

.tt: time, Tbb, rbb, Teff, Rlast_sc, R(tau2/3), bolometric and UBVRI magnitudes, gdepos

.ph: spectral evolution of the model (~100 frequency zones)

.res: time serial data of various energies (kinetic, thermal, total, etc.), physical properties of the shells at each time stamp (velocity, radius, density, pressure, opacity, baryon/electron # density, luminosity, neutral hydrogen fraction, temperature, radiation temperature), energy of the shells at each time stamp (radiation energy, thermal energy, kinetic energy, gravitational energy; calculated afterwards)

.swd: physical properties of shells at each time stamp

  (*similar to .res file but more efficient for time epoch after SBO*)
  
  
3. Obtain the location of photosphere/thermalization depth during the evolution
4. Obtain photometry of bands other than bolUBVRI (currently supported: SDSS-ugriz, ZTF-gr)
5. Plot: basic initial chemical/hydrodynamical structure, light curves, internal structure evolution between given times (also in Kippenhahn diagram style)

For more specific explanation, refer to individual python files in the package


## How to use

1. Setting your STELLA working directory as root
> stellapkg.STLROOT.croot($STELLA_DIR)

2. If STELLA models are saved as $STELLA_DIR/dir1/dir2/.../filename.{res,swd,tt,ph,abn,hyd}, you can use stellapkg like:
> hyd = stellapkg.HYDparser.hyd_data(dir1,dir2,...,filename)
> 
> res = stellapkg.RESparser.res_data(dir1,dir2,...,filename,kwargs).get_phots()
> 
> stellapkg.StructureEvolution.KPHplot(dir1,dir2,...,filename,kwargs)

or just:
> hyd = stellapkg.HYDparser.hyd_data('$STELLA_DIR/dir1/dir2/.../filename.res')
