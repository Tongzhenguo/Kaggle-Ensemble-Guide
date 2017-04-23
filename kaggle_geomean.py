# coding=utf-8
from __future__ import division
from collections import defaultdict
from glob import glob
import sys
import math

"""
几何平均能比普通平均表现的更好。
"""
def kaggle_bag(glob_files, loc_outfile, method="average", weights="uniform"):
  if method == "average":
    scores = defaultdict(float)
  with open(loc_outfile,"wb") as outfile:
    for i, glob_file in enumerate( glob(glob_files) ):
      print "parsing:", glob_file
      # sort glob_file by first column, ignoring the first line
      lines = open(glob_file).readlines()
      lines = [lines[0]] + sorted(lines[1:])
      for e, line in enumerate( lines ):
        if i == 0 and e == 0:
          outfile.write(line)
        if e > 0:
          row = line.strip().split(",")
          if scores[(e,row[0])] == 0:
            scores[(e,row[0])] = 1
          scores[(e,row[0])] *= float(row[1])
    for j,k in sorted(scores):
      outfile.write("%s,%f\n"%(k,math.pow(scores[(j,k)],1/(i+1)))) ###公式
    print("wrote to %s"%loc_outfile)

if __name__ == "__main__":
  print( '回归问题多个模型均值平滑，几何平均比普通平均效果要好' )
  path = 'D:/code/Kaggle-Ensemble-Guide/'
  glob_files = path+"samples/method*.csv"
  loc_outfile = path+"samples/kaggle_avg.csv"
  kaggle_bag(glob_files, loc_outfile)
