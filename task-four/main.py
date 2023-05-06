#!/usr/bin/python3
from figures import LINE, POLYGON
from cohen_sutherland import cohen_sutherland_clip
from cirus_beck import cyrus_beck_clip
from midpoint import midPoint
import matplotlib.pyplot as plt


def main():
    fig, (beck, suth, mid) = plt.subplots(nrows=1, ncols=3)
    cyrus_beck_clip(POLYGON, LINE, beck)
    cohen_sutherland_clip(POLYGON, LINE, suth)
    midPoint(POLYGON, LINE, mid)
    plt.show()


if __name__ == "__main__":
    main()
