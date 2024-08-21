#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: Jeremy M. Stober
Program: MDS.PY
Description: Multidimensional Scaling
"""

import sys, getopt, pdb
from numpy import mean, transpose, array, mat, sqrt, zeros
from numpy.linalg import svd
#from scipy import sparse
import pylab

def mds(d, dimensions = 2):
    """
    Multidimensional Scaling - Given a matrix of interpoint distances,
    find a set of low dimensional points that have similar interpoint
    distances.
    """

    (n,n) = d.shape
    E = (-0.5 * d**2)

    # Use mat to get column and row means to act as column and row means.
    Er = mat(mean(E,1))
    Es = mat(mean(E,0))

    # From Principles of Multivariate Analysis: A User's Perspective (page 107).
    F = array(E - transpose(Er) - Es + mean(E))

    U, S, V = svd(F)

    Y = U * sqrt(S)

    return (Y[:,0:dimensions], S)

def norm(vec):
    return sqrt(sum(vec**2))

def square_points(size):
    nsensors = size ** 2
    return array([(i / size, i % size) for i in range(nsensors)])

def test():

    points = square_points(10)
    print points

    distance = zeros((100,100))
    print distance
    for (i, pointi) in enumerate(points):
        for (j, pointj) in enumerate(points):
            distance[i,j] = norm(pointi - pointj)

    Y, eigs = mds(distance)

    pylab.figure(1)
    pylab.plot(Y[:,0],Y[:,1],'.')

    pylab.figure(2)
    pylab.plot(points[:,0], points[:,1], '.')

    pylab.show()

def main():

    def usage():
        print sys.argv[0] + "[-h] [-d]"

    try:
        (options, args) = getopt.getopt(sys.argv[1:], 'dhf:', ['help','debug','file'])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    print options
    filename = "corpora-modality.tsv"
    for o, a in options:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-d', '--debug'):
            pdb.set_trace()
        elif o in ('-f', '--file'):
            filename = a
            print filename

    #test()
    rownames = []
    colnames = []
    data = []
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if i == 0:
                colnames = line.strip().split("\t")
            else:
                values = line.strip().split("\t")
                data.append(values[1:])
                rownames.append(values[0])
    points = array([[float(p) for p in line] for line in data])
    print colnames
    print points

    distance = zeros((len(rownames), len(rownames)))
    for (i, pointi) in enumerate(points):
        for (j, pointj) in enumerate(points):
            distance[i, j] = norm(pointi - pointj)

    Y, eigs = mds(distance)
    print Y
    print eigs

    with open(filename + ".scaled.tsv", "w") as f:
        f.write("Corpus\tx\ty\n")
        for i, rowname in enumerate(rownames):
            f.write("%s\t%s\n" % (rowname, "\t".join(str(value) for value in Y[i])))

    #pylab.figure(1)
    #pylab.plot(Y[:,0],Y[:,1],'.')

    #pylab.figure(2)
    #pylab.plot(points[:,0], points[:,1], '.')

    #pylab.show()


if __name__ == "__main__":
    main()
