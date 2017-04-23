# coding=utf-8
from collections import defaultdict, Counter
from glob import glob
import sys
import re

"""
我们讨论加权投票。为什么要加权？通常我们希望模型越好，其权重就越高。
所以，在这里，我们将表现最好的模型的投票看作3票，其它的4个模型只看作1票。
原因是：当表现较差的模型需要否决表现最好的模型时，唯一的办法是它们集体同意另一种选择。
我们期望这样的集成能够对表现最好的模型进行一些修正，带来一些小的提高。
"""
def kaggle_bag(glob_files, loc_outfile, method="average", weights="uniform"):
  pattern = re.compile(r"(.)*_[w|W](\d*)_[.]*")
  if method == "average":
    scores = defaultdict(list)
  with open(loc_outfile,"wb") as outfile:
    #weight_list may be usefull using a different method
    #glob(filename)=> 返回匹配了的文件名列表
    weight_list = [1]*len(glob(glob_files))
    for i, glob_file in enumerate( glob(glob_files) ):
      print "parsing:", glob_file
      if weights == "weighted":
         weight = pattern.match(glob_file)
         if weight and weight.group(2):
            print "Using weight: ",int(weight.group(2))
            weight_list[i] = weight_list[i]*int(weight.group(2))
         else:
            print "Using weight: 1"
      # sort glob_file by first column, ignoring the first line
      lines = open(glob_file).readlines()
      lines = [lines[0]] + sorted(lines[1:])
      for e, line in enumerate( lines ):
        if i == 0 and e == 0:
          outfile.write(line)
        if e > 0:
          row = line.strip().split(",")
          for l in range(1,weight_list[i]+1):
            scores[(e,row[0])].append(row[1])
    for j,k in sorted(scores):
      outfile.write("%s,%s\n"%(k,Counter(scores[(j,k)]).most_common(1)[0][0]))
    print("wrote to %s"%loc_outfile)

if __name__ == "__main__":
  print( '多数投票的例子' )
  path = 'D:/code/Kaggle-Ensemble-Guide/'
  glob_files = path+"samples/method_*.csv"
  loc_outfile = path+"samples/kaggle_vote.csv"

  # print('权值相当进行投票')
  # kaggle_bag(glob_files, loc_outfile)

  print('指定权重投票')
  kaggle_bag(glob_files, loc_outfile,weights='weighted')