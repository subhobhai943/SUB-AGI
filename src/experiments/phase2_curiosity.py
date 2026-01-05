"""Phase 2 Experiment: Curiosity-Driven Exploration.

Goal: Demonstrate that SUB-AGI explores autonomously when bored.
1. Setup a GridWorld with one hidden object.
2. Initialize SUB-AGI in a "bored" state (empty area).
3. Loop:
    - SUB-AGI predicts next state.
    - SUB-AGI chooses an action (explore vs stay).
    - Environment steps.
    - SUB-AGI perceives and calculates surprise.
4. Verify that Boredom decreases when it finds the object.
"""

import time
import random
from environment.grid_world import GridWorld, GridObject, SHAPE_A
from mind_kernel.core import MindKernel

def run_experiment():
    print("=== Phase 2: Curiosity & Exploration Experiment ===\n")
    
    # 1. Setup Environment: 7x7 grid, Object far from start
    env = GridWorld()
    env.config.rows = 7
    env.config.cols = 7
    env.reset()
    
    # Force Agent to (0,0) and Object to (6,6)
    env.agent.position = (0, 0)
    hidden_obj = GridObject(id="hidden-treasure", kind="treasure", position=(5, 5), shape=SHAPE_A)
    env.objects = [hidden_obj]
    env._render_to_grid() # refresh grid
    
    kernel = MindKernel()
    
    print(f"Start Position: {env.agent.position}")
    print(f"Hidden Object at: {hidden_obj.position}")
    print("SUB-AGI is starting to explore...\n")
    
    max_steps = 30
    found_object = False
    
    for t in range(max_steps):
        # 1. Observation
        obs = env.observe()
        
        # 2. Mind Step (Perceive, Feel, Think)
        # Note: We pass empty string as user_input since this is autonomous
        reply, state = kernel.step("", observation=obs)
        
        boredom = state.affect.drives.boredom
        surprise = state.affect.drives.surprise_last_tick
        vis_count = len(state.perception.visual_objects)
        
        print(f"Step {t+1}: Pos {obs.agent_position} | Boredom: {boredom:.2f} | Surprise: {surprise:.1f} | Visible: {vis_count}")
        
        if vis_count > 0:
            print("\n!!! OBJECT FOUND !!!")
            print(f"SUB-AGI says: {reply}")
            found_object = True
            break
            
        # 3. Decide Action based on Boredom/Curiosity
        action = kernel.choose_action(obs)
        
        # 4. Form Prediction (Crucial for next step's surprise)
        kernel.predict_next(action)
        
        # 5. Act
        env.step(action)
        
    if found_object:
        print("\nSUCCESS: SUB-AGI found the object autonomously!")
    else:
        print("\nFAILURE: SUB-AGI did not find the object in time.")

if __name__ == "__main__":
    run_experiment()
