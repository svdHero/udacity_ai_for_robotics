# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either "R" (for red cell) or "G" (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either "R" or "G"
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# prob_sensor_correct:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-prob_sensor_correct
#
# prob_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-prob_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up


STAY = [0, 0]
RIGHT = [0, 1]
LEFT = [0, -1]
DOWN = [1, 0]
UP = [-1, 0]


def localize(colored_map, measurements, motions, prob_sensor_correct, prob_move):
    # initializes prop_map to a uniform distribution over a grid of the same dimensions as colored_map
    NUM_ROWS = len(colored_map)
    NUM_COLS = len(colored_map[0])
    pinit = 1.0 / (float(NUM_ROWS) * float(NUM_COLS))
    prob_map = [[pinit for col in range(NUM_COLS)] for row in range(NUM_ROWS)]

    for motion, measurement in zip(motions, measurements):
        prob_map = move(prob_map, motion, prob_move)
        prob_map = sense(prob_map, colored_map, measurement, prob_sensor_correct)

    return prob_map


def move(prob_map, motion, prob_move):
    NUM_ROWS = len(prob_map)
    NUM_COLS = len(prob_map[0])
    prob_filtered = [[0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
    for rowIndex in range(NUM_ROWS):
        for colIndex in range(NUM_COLS):
            prob_sucessful = prob_move * prob_map[(rowIndex-motion[0]) % NUM_ROWS][(colIndex-motion[1]) % NUM_COLS]
            prob_not_sucessful = (1-prob_move)*prob_map[rowIndex][colIndex]
            prob_filtered[rowIndex][colIndex] = prob_sucessful + prob_not_sucessful
    return prob_filtered


def sense(prob_map, colored_map, measurement, prob_sensor_correct):
    NUM_ROWS = len(prob_map)
    NUM_COLS = len(prob_map[0])
    prob_updated = [[0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
    for rowIndex in range(NUM_ROWS):
        for colIndex in range(NUM_COLS):
            is_measurement_hit = (colored_map[rowIndex][colIndex] == measurement)
            if is_measurement_hit:
                p = prob_sensor_correct
            else:
                p = 1-prob_sensor_correct
            prob_updated[rowIndex][colIndex] = prob_map[rowIndex][colIndex]*p
    s = sum([sum(x) for x in prob_updated])
    for rowIndex in range(NUM_ROWS):
        for colIndex in range(NUM_COLS):
            prob_updated[rowIndex][colIndex] /= s
    return prob_updated


def show(matrix):
    rows = ["[" + ",".join(map(lambda x: "{0:.5f}".format(x), row)) + "]" for row in matrix]
    print("[" + ",\n ".join(rows) + "]")


#############################################################
# For the following test case, your output should be
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)


def main():
    colored_map = [["R", "G", "G", "R", "R"],
                   ["R", "R", "G", "R", "R"],
                   ["R", "R", "G", "G", "R"],
                   ["R", "R", "R", "R", "R"]]
    measurements = ["G", "G", "G", "G", "G"]
    motions = [STAY, RIGHT, DOWN, DOWN, RIGHT]
    location_prob_dist = localize(colored_map, measurements, motions, prob_sensor_correct=0.7, prob_move=0.8)
    show(location_prob_dist)


if __name__ == "__main__":
    main()
