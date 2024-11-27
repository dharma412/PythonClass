import sys
import math

# width: columns in the game grid
# height: rows in the game grid
width, height = [int(i) for i in input().split()]

# game loop
while True:
    entity_count = int(input())  # Number of entities in the game grid
    my_organs = []  # List to store your organs
    protein_sources = []  # List to store protein sources on the grid

    # Loop to process all entities
    for i in range(entity_count):
        inputs = input().split()
        x = int(inputs[0])
        y = int(inputs[1])  # grid coordinate
        _type = inputs[2]  # Type of entity (ROOT, BASIC, etc.)
        owner = int(inputs[3])  # Owner (1 = you, 0 = opponent, -1 = neutral)
        organ_id = int(inputs[4])  # ID of the organ
        organ_dir = inputs[5]  # Direction (N, E, S, W, or X)
        organ_parent_id = int(inputs[6])
        organ_root_id = int(inputs[7])

        if owner == 1:  # If the organ belongs to you
            my_organs.append((x, y, organ_id, _type))

        if _type in ['A', 'B', 'C', 'D']:  # Protein source
            protein_sources.append((x, y, _type))

    # Your protein stock (A, B, C, D)
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]

    # Opponent's protein stock (A, B, C, D)
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]

    required_actions_count = int(input())  # Number of actions you need to output

    # Strategy to grow or wait
    for i in range(required_actions_count):
        if my_a > 0:  # If you have proteins available
            # Example logic: try to grow towards the closest protein source
            target_x, target_y, _ = protein_sources[0]  # Just picking the first protein source for simplicity
            # Grow an organ towards this protein source
            print(f"GROW {my_organs[0][2]} {target_x} {target_y} BASIC")
        else:
            print("WAIT")  # If no proteins are available, wait
