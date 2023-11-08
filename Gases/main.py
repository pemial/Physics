from molecule import *


if __name__=="__main__":
    sim=Simulation(name="kinetic_theory_simulation",
                   box_dim=[1.0,1.0],
                   t_step=1e-2,
                   particle_radius=1e-2)
    
    #Add N2 molecules to the box
    sim.add_molecules(n=1000, 
                      v_mean=1.0, 
                      v_std=0.2, 
                      v_distrib="maxwell")
    
    #Run the simulation and store the pressure output in P
    P=sim.run_simulation(1)
    
    #Make the box animation
    sim.make_animation()

        
        
        