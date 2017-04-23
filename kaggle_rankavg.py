# coding=utf-8
from __future__ import division
from collections import defaultdict
from glob import glob
import sys

glob_files = sys.argv[1]
loc_outfile = sys.argv[2]

"""
当平均多个来自不同模型的输出时，会出现一些问题。
并不是所有的预测器的结果是完美校准的,它们可能会产生过高或过低的预测概率，或者预测在一定的范围里非常混乱。

当评估指标是ranking或者像AUC一样的阈值时;如果排名很集中;
Id,Rank,Prediction
1,1,0.35000056
2,0,0.35000002
3,2,0.35000098
4,3,0.35000111
集成并不会改变什么

解决方案是：首先将预测结果进行一个排名，然后去平均这个排名。
在标准化平均排名在0到1之间后，你肯定会得到一个均匀分布预测。排名平均结果：
Id,Prediction
1,0.33
2,0.0
3,0.66
4,1.0

排名需要一个测试集，所以当你要预测一个新样本时，你该怎么办？你可以与老的测试集一起，重新计算排名，但这会增加你的解决方案的复杂性。
一个解决方案是使用历史排名。存储旧的测试集预测及其排名，现在当你预测一个新的测试样例如“0.35000110”，
你去找到最接近的历史预测并取其历史排名(在这里最接近的历史预测是“0.35000111”其历史排名为“3”)。

"""
def kaggle_bag(glob_files, loc_outfile):
  with open(loc_outfile,"wb") as outfile:
    all_ranks = defaultdict(list)
    for i, glob_file in enumerate( glob(glob_files) ):
      file_ranks = []
      print "parsing:", glob_file
      # sort glob_file by first column, ignoring the first line
      lines = open(glob_file).readlines()
      lines = [lines[0]] + sorted(lines[1:])
      for e, line in enumerate( lines ):
        if e == 0 and i == 0:
          outfile.write( line )
        elif e > 0:
          r = line.strip().split(",")
          file_ranks.append( (float(r[1]), e, r[0]) )
      for rank, item in enumerate( sorted(file_ranks) ):
        all_ranks[(item[1],item[2])].append(rank)
    average_ranks = []
    for k in sorted(all_ranks):
      average_ranks.append((sum(all_ranks[k])/len(all_ranks[k]),k))
    ranked_ranks = []
    for rank, k in enumerate(sorted(average_ranks)):
      ranked_ranks.append((k[1][0],k[1][1],rank/(len(average_ranks)-1)))
    for k in sorted(ranked_ranks):
      outfile.write("%s,%s\n"%(k[1],k[2]))
    print("wrote to %s"%loc_outfile)

if __name__ == "__main__":
  print( '回归问题多个模型均值平滑' )
  path = 'D:/code/Kaggle-Ensemble-Guide/'
  glob_files = path+"samples/method*.csv"
  loc_outfile = path+"samples/kaggle_avg.csv"

kaggle_bag(glob_files, loc_outfile)