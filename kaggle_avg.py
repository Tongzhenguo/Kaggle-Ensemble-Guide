# coding=utf-8
from collections import defaultdict
from glob import glob
import sys

"""
普通平均可以很好的解决一系列问题(二分类与回归问题)与指标(AUC,误差平方或对数损失)。
与其说平均，不如说采用了多个个体模型预测值的平均。
平均预测常常会降低过拟合。在类与类间，你想要理想的平滑的将其分离，而单一模型的预测在边界间可能会有一些粗糙。
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
          scores[(e,row[0])] += float(row[1])
    for j,k in sorted(scores):
      outfile.write("%s,%f\n"%(k,scores[(j,k)]/(i+1)))
    print("wrote to %s"%loc_outfile)

if __name__ == "__main__":
  print( '回归问题多个模型均值平滑' )
  path = 'D:/code/Kaggle-Ensemble-Guide/'
  glob_files = path+"samples/method*.csv"
  loc_outfile = path+"samples/kaggle_avg.csv"
  kaggle_bag(glob_files, loc_outfile)