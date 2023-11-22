import numpy as np

HOLE_LOWER_BOUND_COORD = -1e-2
HOLE_HIGHER_BOUND_COORD = 1e-2
HOLE_SIZE = HOLE_HIGHER_BOUND_COORD - HOLE_LOWER_BOUND_COORD
SCREEN_LOWER_BOUND_COORD = -1e-5
SCREEN_HIGHER_BOUND_COORD = 1e-5
SCREEN_SIZE = SCREEN_HIGHER_BOUND_COORD - SCREEN_LOWER_BOUND_COORD
SCREEN_POINTS_NUM = 300000
HOLE_POINTS_NUM = 2

BARRIER_X_COORD = 0
SCREEN_X_COORD = 0.001

# HOLE_POINTS = np.array([np.arange(HOLE_LOWER_BOUND_COORD,
#                                   HOLE_HIGHER_BOUND_COORD + 1e-9, HOLE_SIZE
#                                   / HOLE_POINTS_NUM)[:HOLE_POINTS_NUM]]).transpose()
HOLE_POINTS = np.array([[HOLE_LOWER_BOUND_COORD / 2, HOLE_HIGHER_BOUND_COORD / 2]]).transpose()
SCREEN_POINTS = np.array([np.arange(SCREEN_LOWER_BOUND_COORD,
                                    SCREEN_HIGHER_BOUND_COORD, SCREEN_SIZE
                                    / SCREEN_POINTS_NUM)]).transpose()

WAVE_LENGTH = 4e-7
START_PHASE = 0
WAVE_NUMBER = 2 * np.pi / WAVE_LENGTH

HOLE_TO_SCREEN_POINTS_DISTANCES = np.sqrt(
    np.square(SCREEN_X_COORD - BARRIER_X_COORD)
    + np.square(HOLE_POINTS - SCREEN_POINTS.transpose()))
DISTANCES = HOLE_TO_SCREEN_POINTS_DISTANCES

# PHASES = np.remainder((DISTANCES * WAVE_NUMBER + START_PHASE), 2 * np.pi)
PHASES = DISTANCES * WAVE_NUMBER + START_PHASE

FIRST_SOURCE_MAGNITUDE = 1
SECOND_SOURCE_MAGNITUDE = 1
MAGNITUDES = np.array([[0.001 for i in range(HOLE_POINTS_NUM)]]).transpose()
# SCREEN_POINTS_MAGNITUDES = np.multiply(1 / DISTANCES, np.cos(PHASES))
# MAGNITUDES = SCREEN_POINTS_MAGNITUDES
#
# SCREEN_POINTS_INTENSITIES = (np.square(FIRST_SOURCE_MAGNITUDE)
#                              + np.square(SECOND_SOURCE_MAGNITUDE)
#                      + 2 * FIRST_SOURCE_MAGNITUDE * SECOND_SOURCE_MAGNITUDE
#                      * np.cos(PHASES[0] - PHASES[1]))

# INTENSITIES = SCREEN_POINTS_INTENSITIES
#
# ILLUMINATION = 2 * (1 + np.cos(WAVE_NUMBER * (PHASES[0]-PHASES[1])))
#
# INTENSITIES = np.square(FIRST_SOURCE_MAGNITUDE * np.cos(WAVE_NUMBER * PHASES[0])
#                + SECOND_SOURCE_MAGNITUDE * np.cos(WAVE_NUMBER * PHASES[1]))
INTENSITIES = np.square(
    np.sum(
        np.multiply(
            MAGNITUDES / DISTANCES, np.cos(WAVE_NUMBER * PHASES)
        ), axis=0
    )
)