import numpy as np
import parameters_new as p
import matplotlib.pyplot as plt


def hl_envelopes_idx(s, dmin=1, dmax=1, split=False):
    """
    Input :
    s: 1d-array, data signal from which to extract high and low envelopes
    dmin, dmax: int, optional, size of chunks, use this if the size of the input signal is too big
    split: bool, optional, if True, split the signal in half along its mean, might help to generate the envelope in some cases
    Output :
    lmin,lmax : high/low envelope idx of input signal s
    """

    # locals min
    lmin = (np.diff(np.sign(np.diff(s))) > 0).nonzero()[0] + 1
    # locals max
    lmax = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[0] + 1

    if split:
        # s_mid is zero if s centered around x-axis or more generally mean of signal
        s_mid = np.mean(s)
        # pre-sorting of locals min based on relative position with respect to s_mid
        lmin = lmin[s[lmin] < s_mid]
        # pre-sorting of local max based on relative position with respect to s_mid
        lmax = lmax[s[lmax] > s_mid]

    # global min of dmin-chunks of locals min
    lmin = lmin[[i + np.argmin(s[lmin[i:i + dmin]]) for i in
                 range(0, len(lmin), dmin)]]
    # global max of dmax-chunks of locals max
    lmax = lmax[[i + np.argmax(s[lmax[i:i + dmax]]) for i in
                 range(0, len(lmax), dmax)]]

    return lmin, lmax


def make_envelope():
    for i in range(p.ENVELOPE_FACTOR):
        lmin, lmax = hl_envelopes_idx(p.Y_POINTS)
        p.X_POINTS = p.X_POINTS[lmax]
        p.Y_POINTS = p.Y_POINTS[lmax]


def make_picture():
    make_envelope()
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot()

    if p.MAKE_ENVELOPE:
        make_envelope()
    else:
        p.X_POINTS = p.AVG_SCREEN_POINTS
        p.Y_POINTS = p.AVG_INTENSITIES

    ax.plot(p.X_POINTS, p.Y_POINTS)
    ax.set_xlim([-p.SCREEN_SIZE/2, p.SCREEN_SIZE/2])
    ax.set_xlabel("screen points coordinates in meters")
    ax.set_ylabel("intensity")
    plt.show()


def main():
    make_picture()
    pass


main()
