#########################################################################
# Scorer for the SEMEVAL-2013 Task 2: Twitter Sentiment Analysis
# Author: ves@cs.jhu.edu
#
# This script takes a prediction file and a gold standard file
# (i.e., tweeti-a.dist.tsv) and produces scores. The prediction file
# should be in the same format as the gold standard file.
#########################################################################

import sys

classes = ['positive','negative','neutral']
if len(sys.argv)==4:
    verify=False
elif len(sys.argv)==3:
    verify=True
else:
    print "Usage:"
    print "To run scorer: python "+sys.argv[0]+" a|b <predictions> <gold_standard>"
    print "To verify format: python "+sys.argv[0]+" a|b <predictions> "
    exit(-1)

if sys.argv[1]=='a' or sys.argv[1]=='A':
    print "TASK A"
    taskA = True
elif sys.argv[1]=='b' or sys.argv[1]=='B':
    print "TASK B"
    taskA = False
else:
    print "Unknown task: "+sys.argv[1]
    exit(-1)

if taskA:
    minlen = 5
    idlen = 4
else:
    minlen = 3
    idlen = 2
    
predFile = sys.argv[2]

if verify:
    print "Checking format of file "+predFile
else:
    gsFile = sys.argv[3]
    print "Comparing predictions "+predFile+" to gold standard "+gsFile+"."

def readfile(filename):
    counts={}
    for cl in classes:
        counts[cl]=0
    inputfile = open(filename,'r')
    lines = 0
    dups = 0
    newlines = 0
    result = {}
    errors = 0
    for line in inputfile:
        if not '\t' in line:
            newlines+=1
            continue
        else:
            lines+=1
            words = line.strip().split('\t')
            if len(words)<minlen:
                errors+=1
                print "Line "+line+" has the wrong number of tokens"
            else:
                key = "*".join(words[0:idlen])
                #print key
                label = words[idlen]
                if not label in classes:
                    errors+=1
                    print "Label "+label+" in line:\n"+line+"\nnot recognized"
                else:
                    if key in result:
                        dups+=1
                    result[key]=label
                    counts[label]+=1
    print "File: "+filename+" -- "+("no" if errors<1 else str(errors))+" errors found"
    #print str(dups)+" duplicates"
    return (result, lines,counts)

def fscore(conftable):
    if conftable[0]==0 or conftable[1]==0 or conftable[2]==0:
        return [0.0,0.0,0.0]
    precision = float(conftable[0])/float(conftable[2])
    recall = float(conftable[0])/float(conftable[1])
    fscore = (2*precision*recall)/(precision+recall)
    return [precision, recall, fscore]

def prettyprint(score):
    result = ""
    for s in score:
        result+= "{0:1.4f}\t".format(s)
    return result

def printscore(conf_table):
    score = fscore(conf_table)
    res= printratio(conf_table[0],conf_table[2])+' '+prettyprint([score[0]])+' '
    res+= printratio(conf_table[0],conf_table[1])+' '+prettyprint([score[1]])+' '
    res+= prettyprint([score[2]])
    return res

def printratio(nom,denom):
    result = '('+str(nom)+'/'+str(denom)+')'
    return "%12s" %result

def printconfmatrix(matrix):
    print "Confusion table:"
    print "gs \ pred|%9s|%9s|%9s" %tuple(classes) 
    print "---------------------------------------"
    for k in range(0,len(classes)):
        strs = (classes[k],)+tuple(matrix[k]) 
        print "%9s|%9d|%9d|%9d" %strs
    
def printbreakdown(counts):
    for key,count in counts.iteritems():
        print key+" \t"+str(count)
#Read in the predictions and the gold standard
(predictions, pred_lines, counts) = readfile(predFile)
print "Prediction file: "+str(pred_lines)+" lines"
print "                 "+str(len(predictions))+" unique"
print "Breakdown by class:"
printbreakdown(counts)
if verify:
    exit(0);
(gs, gs_lines, counts) = readfile(gsFile)
print "\n\nGold standard: "+str(gs_lines)+" lines"
print "               "+str(len(gs))+" unique"
print "Breakdown by class:"
printbreakdown(counts)

confusion_tables = {}
confusion_matrix = [[0,0,0],[0,0,0],[0,0,0]]
for cl in classes:
    confusion_tables[cl]=[0,0,0]

#Confusion table is expressed as [correct, total_positive, predicted_positive] 
for iden, key in gs.iteritems():
    #key = 'neutral' if key=='objective' else key
    #increment total positives for the gs class
    confusion_tables[key][1]+=1
    if not iden in predictions:
        print "Identifier "+iden+" not found in predictions file"
        continue
    prediction = predictions[iden]
    #prediction = 'neutral' if prediction=='objective' else prediction
    #if correct prediction, increment the corresponding correct number
    if key == prediction:
        confusion_tables[key][0]+=1
    confusion_tables[prediction][2]+=1
    index1 = classes.index(key)
    index2 = classes.index(prediction)
    confusion_matrix[index1][index2]+=1

print "\n"
printconfmatrix(confusion_matrix)


print "\n\nScores:"
print "class\t                       prec\t              recall     fscore"
total=0.0
for cl in classes:
    score = fscore(confusion_tables[cl])
    print cl+' \t'+printscore(confusion_tables[cl])
    if cl in ['positive','negative']:
        total+=score[2]
f = total/2.0
print '-----------------------------------------------------------------------'
print 'average(pos and neg)                                             '+prettyprint([f])
        
