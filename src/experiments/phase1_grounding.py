"""Phase 1 Experiment: Symbol Grounding.

This script runs a scenario where:
1. SUB-AGI explores a GridWorld.
2. It encounters a shape (Pattern A).
3. Human says "This is A".
4. It encounters a different shape (Pattern B).
5. Human says "This is B".
6. It encounters Pattern A again.
7. Human asks "What is this?".
8. SUB-AGI must identify it as "A" based on the grounded visual experience.
"""

from environment.grid_world import GridWorld, GridObject, SHAPE_A, SHAPE_B
from mind_kernel.core import MindKernel

def run_experiment():
    print("=== Phase 1: Symbol Grounding Experiment ===\n")
    
    # 1. Init
    env = GridWorld()
    kernel = MindKernel()
    
    # Helper to print conversation
    def chat(user_text, visual_obs=None):
        reply, _ = kernel.step(user_text, observation=visual_obs)
        print(f"User: {user_text}")
        print(f"SUB-AGI: {reply}\n")

    # 2. Setup Scene 1: Agent sees Object A
    print("--- Scene 1: Learning 'A' ---")
    env.reset()
    # Manually place Object A near the agent
    agent_pos = env.agent.position
    # Place object at +1 row
    obj_pos = (min(env.config.rows-1, agent_pos[0]+1), agent_pos[1])
    
    obj_a = GridObject(id="obj-A", kind="block", position=obj_pos, shape=SHAPE_A)
    env.objects = [obj_a] # Clear random objects, place ours
    
    obs = env.observe()
    print("(SUB-AGI sees a shape pattern)")
    
    # Dialog
    chat("This is A", visual_obs=obs)

    # 3. Setup Scene 2: Agent sees Object B
    print("--- Scene 2: Learning 'B' ---")
    # Move object B to same relative spot for consistency
    obj_b = GridObject(id="obj-B", kind="block", position=obj_pos, shape=SHAPE_B)
    env.objects = [obj_b]
    
    obs = env.observe()
    print("(SUB-AGI sees a different shape pattern)")
    
    chat("This is B", visual_obs=obs)
    
    # 4. Test: Show A again
    print("--- Scene 3: Testing Memory ---")
    env.objects = [obj_a] # Show A again
    obs = env.observe()
    
    print("(SUB-AGI sees the first shape again)")
    chat("What is this?", visual_obs=obs)
    
    # Verify internal state
    memories = kernel.state.long_term_memory.semantic_concepts
    print(f"Internal Concepts Learned: {[c.symbol for c in memories]}")

if __name__ == "__main__":
    run_experiment()
