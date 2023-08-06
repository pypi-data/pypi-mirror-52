import numpy as np


def majority_vote_proba(x):
    # count how many proba x are greater than 0.5
    cnt = np.sum(x >= 0.5, axis=1).astype(np.uint16)

    # the vote per example
    vote = cnt > int(x.shape[1] / 2)

    # initialize proba y
    y = np.ones(shape=vote.shape, dtype=np.float16) * .5

    # set x<0.5 to zero and add sum(x-0.5)/n
    x0 = (x - .5).astype(np.float16)
    y += np.maximum(0, x0).mean(axis=1) * vote

    # set x>=0.5 to zero and add sum(x-0.5)/n
    y += np.minimum(0, x0).mean(axis=1) * ~vote
    del x0

    # done
    return y, vote.astype(np.uint8), cnt
