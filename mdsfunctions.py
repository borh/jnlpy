#!/usr/bin/python

import random
import sys
from math import sqrt

def pearson(v1,v2):
  # Simple sums
  sum1=sum(v1)
  sum2=sum(v2)

  # Sums of the squares
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])

  # Sum of the products
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  #if den==0: return 0
  if den==0: return 1 # errata

  return 1.0-num/den

import numpy

def euclid(v1,v2):
    v1 = numpy.array(v1)
    v2 = numpy.array(v2)
    #print ("(%s - %s) = %f") % (v1, v2, numpy.linalg.norm(v1 - v2))
    return numpy.linalg.norm(v1 - v2)

def scaledown(data,distance=euclid,rate=0.01):
  n=len(data)

  # The real distances between every pair of items
  realdist=[[distance(data[i], data[j]) for j in range(n)]
             for i in range(n)]

  # Randomly initialize the starting points of the locations in 2D
  loc=[[random.random(),random.random()] for i in range(n)]
  fakedist=[[0.0 for j in range(n)] for i in range(n)]

  lasterror=None
  for m in range(0,1000):
    # Find projected distances
    for i in range(n):
      for j in range(n):
        fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) 
                                 for x in range(len(loc[i]))]))

    # Move points
    grad=[[0.0,0.0] for i in range(n)]

    totalerror=0
    for k in range(n):
      for j in range(n):
        if j==k: continue
        # The error is percent difference between the distances
        errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]

        # Each point needs to be moved away from or towards the other
        # point in proportion to how much error it has
        grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
        grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm

        # Keep track of the total error
        totalerror+=abs(errorterm)
    #print totalerror

    # If the answer got worse by moving the points, we are done
    if lasterror and lasterror<totalerror: break
    lasterror=totalerror

    # Move each of the points by the learning rate times the gradient
    for k in range(n):
      loc[k][0]-=rate*grad[k][0]
      loc[k][1]-=rate*grad[k][1]

  return loc

def readfile(filename):
  lines=[line for line in file(filename)]

  # First line is the column titles
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
      p=line.strip().split('\t')
      # First column in each row is the rowname
      rownames.append(p[0])
      # The data for this row is the remainder of the row
      #data.append([float(x) for x in p[1:]])
      data.append(numpy.array(float(x) for x in p[1:]))
  return rownames,colnames,data

def export_tsv(data, rownames, colnames, filename):
    with open(filename, "w") as f:
        f.write("Corpus\t" + ("\t").join(colnames) + "\n")
        for i in range(len(data)):
            f.write(rownames[i] + "\t" + ("\t").join(str(d) for d in data[i]) + "\n")

def draw2d(data,labels,jpeg='mds2d.jpg'):
  from PIL import Image, ImageDraw, ImageFont
  img=Image.new('RGB', (2000,2000), (255,255,255))
  draw=ImageDraw.Draw(img)
  font = ImageFont.truetype("msmincho.ttf", 16, encoding="unic")
  for i in range(len(data)):
      x=(data[i][0]+0.5)*10
      y=(data[i][1]+0.5)*10
      print "%s\t(%f, %f)" % (labels[i], x, y)
      draw.text((x, y), unicode(labels[i], 'utf8'), (0, 0, 0), font=font)
  img.save(jpeg, 'JPEG')

if __name__ == "__main__":
    filename = "corpora-modality.tsv"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    rownames, colnames, data = readfile(filename)
    scaled = scaledown(data)
    print scaled
    export_tsv(scaled, rownames, ["x", "y"], "scaled.tsv")
    draw2d(scaled, rownames)

####filename = argv[1]
####
##### words not used?
####tocluster,words,data=readfile(filename)
####clust=hcluster(data)
####drawdendrogram(clust,tocluster,jpeg=filename+'.jpg')
