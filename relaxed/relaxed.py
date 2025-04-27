from openmm import LangevinIntegrator, CustomExternalForce
from openmm.app import AmberPrmtopFile, AmberInpcrdFile, PDBFile, Simulation, HBonds, NoCutoff
from openmm.unit import kelvin, picosecond, kilocalories_per_mole
import os

tolerance = 2.39
ENERGY = kilocalories_per_mole
tolerance = tolerance * ENERGY

os.system('tleap -f leap.in')

prmtop = AmberPrmtopFile('system.prmtop')
inpcrd = AmberInpcrdFile('system.inpcrd')

system = prmtop.createSystem(nonbondedMethod=NoCutoff, constraints=HBonds)

force = CustomExternalForce("0.5*k*((x-x0)^2 + (y-y0)^2 + (z-z0)^2)")
force.addGlobalParameter("k", 20000.0)  
force.addPerParticleParameter("x0")
force.addPerParticleParameter("y0")
force.addPerParticleParameter("z0")

for i, atom in enumerate(prmtop.topology.atoms()):
    if atom.name in ["CA", "C", "N","O"]:  
        force.addParticle(i, inpcrd.positions[i])

system.addForce(force)

integrator = LangevinIntegrator(0, 0.01, 0.0)
simulation = Simulation(prmtop.topology, system, integrator)
simulation.context.setPositions(inpcrd.positions)

simulation.minimizeEnergy()
state = simulation.context.getState(getEnergy=True)

positions = simulation.context.getState(getPositions=True).getPositions()
with open('/data/lab/czg/alphafold_finetune/relaxed/relaxpdb_result_pdbs_fape_2500_the_finetune_no_marix_predict_have_marix/D11.1_relax_addO2000012.pdb', 'w') as f:
    PDBFile.writeFile(prmtop.topology, positions, f)
