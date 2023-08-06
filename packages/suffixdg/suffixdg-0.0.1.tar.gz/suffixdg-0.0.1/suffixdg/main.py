import re,sys
def nextvertix(array,i,L,k): # go to the next vertex of the tree
    if i<L:
        array.append(1)
        return array,i+1
    else:
        for j in range(L,0,-1):
            if array[j-1]<k:
                array[j-1]+=1
                return array,len(array)
            else:
                array[j-1]=1
                array[-1:]=[]
    return array,0

q = [2,4,4,4]
z = nextvertix(q,len(q),5,4)
#print(z)


def byPass(a,i,L,k): #bypass in the tree
    for j in range(i,0,-1):
        if a[j-1]<k:
            a[j-1]+=1
            return a,len(a)
        a[j-1]=1
        a[-1:]=[]
    return a,0

a = [2,4,4,3,3]
d = byPass(a,5,5,4)
#print(d)

def kmer(length,string):# split the string into k-mers
    lis = []
    for i in range(0,len(string)-length+1):
        lis.append(string[i:length+i])
    return lis

def lettreDiffrent(l,n):#calculate the num of different letter between two string
    dis = 0
    for i,j in zip(l,n):
        if i!=j:
            dis+=1
    return dis

def hammingDistance(s,DNA):#calculate the hamming distance
    liss = []
    for i in DNA:
        lis = kmer(len(s),i)
        if s in lis:
            liss.append(0)
        else:
             liss.append(min([lettreDiffrent(s, i) for i in lis]))

    return sum(liss)
b = 'GCTTAGCCGGCCTGGCCAAT'
d = 'ACTTGCAGAGCGGCGGTTAA'
f = 'GGTTGCGTCCCAACTGGACC'

'''b = 'GCTTAGCCGGCCTGGCCAATGG'
d = 'AC'
f = 'GGTTGCGTCCCAACTGGACCAA'
i = 'AGTTGCGTCACTTCCTGGGCC'
'''
DNA = [b,d,f]
#DNA=['CGGGCCTG','ACCTGGCA','CACCTGGC','GCCAACGT']



def arrayToStr(array):#convert the 1,2,3,4 to letters
    dic = {1:'A',2:'C',3:'G',4:'T'}
    a = ''.join([dic[i] for i in array])
    return a


def branchAndBound(DNA,l):# main algorithm with prefix and suffix
    liste = []
    s = [1]
    bestDis = 10000000
    i = 1
    bestWord= ''
    while i>0:
        if i<l:
            prefix = s[:i]
            #print(s,i)
            suffix = bestWord[i:]
            #print(arrayToStr(prefix),suffix,bestWord)
            #print(prefix)
            #print(arrayToStr(prefix))
            optimalDis = hammingDistance(arrayToStr(prefix),DNA)
            optimalSuffixDis = hammingDistance(suffix,DNA)
            #print(optimalDis,bestDis)
            if optimalDis+optimalSuffixDis>bestDis:
                s,i= byPass(s,len(s),l,4)
                #print('bypass')
                #print(prefix)
                #print(s)
                #print('o')

            else:
                #print(prefix)

                s,i= nextvertix(s,i,l,4)
                #print(s)


        else:
            word = arrayToStr(s)
            #print(s)
            #print(word)
            liste.append(word)
            if hammingDistance(word,DNA)<bestDis:
                bestDis=hammingDistance(word,DNA)
                #print(bestDis)
                bestWord = word
                #print(bestWord)
            #print(word)
            s,i= nextvertix(s,i,l,4)
            #print(i)
    return bestWord, liste
import time

print('你好，欢迎使用由高端设计的DNA功能域搜索器，该程序使用的是分支界定的suffix算法')
print('请输入你想发现功能域的DNA序列，请每次输入一条DNA序列，按回车键继续下一条DNA序列输入')
print('='*37,'菜单','='*37)
print('1.输入DNA序列,输入q结束输入,接下来输入功能域长度')
print('2.关闭程序')

lis=[]
userinput=input('>>>>>')
if userinput=='2':
    sys.exit(0)
    
while userinput!='2':
    try:
        userinput=input('请输入DNA序列或者输入q(Q)退出序列输入:').upper()
        if userinput=='':
            raise Exception
        if userinput=='Q' and len(lis)>=2:
            break
        elif userinput=='Q' and len(lis)<2:
            print('你好，请至少输入2条DNA序列，程序才能进行比对')
        result=re.findall(r'[^ATCG]',userinput)
        if result!=[] and result!='[Q]':
            raise Exception
        if userinput!='Q':
            lis.append(userinput)

    except Exception:
        print('请输入有效的DNA序列')
    
print(lis)
min_len=min([len(i) for i in lis])
print(min_len)
loop=True
while loop:
    try:
        lengths=int(input('>>>>>长度:'))
        if lengths>min_len:
            raise Exception
        loop=False
    except Exception:
        print('对不起，你希望的功能域长度大于你序列最短的长度，请重新输入')
    


print('开始运算<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')



start_time = time.time()

a,liste = branchAndBound(lis,lengths)
print('发现功能域',a)
#print(len(liste))
print('寻找功能域消耗的运算时间为:',round(time.time()-start_time,3),'秒')



