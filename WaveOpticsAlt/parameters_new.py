import numpy as np

LOWER_HOLE_Y_COORD = -5e-6
HIGHER_HOLE_Y_COORD = 5e-6

SCREEN_POINTS_NUM = int(1e7)
SCREEN_SIZE = 1e-1

BARRIER_SCREEN_DISTANCE = 2e-3 # 1e-2

SCREEN_POINTS = np.array([np.arange(-SCREEN_SIZE / 2, SCREEN_SIZE / 2,
                          SCREEN_SIZE / SCREEN_POINTS_NUM)
                          [:SCREEN_POINTS_NUM]]).transpose()
print(f"SCREEN_POINTS shape: {SCREEN_POINTS.shape}")

HOLE_POINTS = np.array([[LOWER_HOLE_Y_COORD, HIGHER_HOLE_Y_COORD]]).transpose()
print(f"HOLE_POINTS shape: {HOLE_POINTS.shape}")

DISTANCES = np.sqrt(
    np.square(BARRIER_SCREEN_DISTANCE) + np.square(
        HOLE_POINTS - SCREEN_POINTS.transpose()
    )
)
print(f"DISTANCES shape: {DISTANCES.shape}")
print(f"DISTANCES:\n{DISTANCES}")

WAVE_LENGTH = 4e-7
START_MAGNITUDE = 1

PHASES_DELTA = np.remainder(DISTANCES * (2 * np.pi / WAVE_LENGTH), 2 * np.pi)
print(f"PHASES_DELTA:\n{PHASES_DELTA}")

INTENSITIES = np.square(np.sum(np.multiply(1 / DISTANCES, np.cos(PHASES_DELTA)), axis=0))

# some kind of internet magic
RESHAPE_FACTOR = int(1e2) # 4e5
AVG_INTENSITIES = np.mean(INTENSITIES.reshape(-1, RESHAPE_FACTOR), axis=1)
AVG_SCREEN_POINTS = np.mean(SCREEN_POINTS.transpose()[0].reshape(-1, RESHAPE_FACTOR), axis=1)

ENVELOPE_FACTOR = 1

X_POINTS = SCREEN_POINTS.transpose()[0]
Y_POINTS = INTENSITIES

MAKE_ENVELOPE = True # otherwise will make AVG points

