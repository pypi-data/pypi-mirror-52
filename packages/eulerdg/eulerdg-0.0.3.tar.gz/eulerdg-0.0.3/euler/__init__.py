name = "euler"
print('程序开始运行，使用欧拉回路算法组装测序后的碎片序列')

#encoding: utf-8
# coding: utf8
import time # Counting running time
import re
def startPosition(graphs): # The function diffrent from exaustive search
    start=[]
    liste=[]
    lis=list(graphs.values())
    for i in lis:
        for k in i:
            liste.append(k)
    for i in graphs:  # determine if the vertice is odd or even
        if (len(graphs[i])+liste.count(i))%2==1:
            start.append(i)
    if len(start)==1:  # Case speciaux, it may contains AAA duplicate, add it into start!
        for i in graphs:
            if len(set(i))==1:
                start.append(i)
    elif len(start)==0:# No odd vertices, all even
        start=list(graphs.keys())

    return start


def edges(length,string):
    'split the string into k-substrings'
    liste = []
    for i in range(0,len(string)-length+1):
        liste.append(string[i:length+i])
    return liste


import random


def randomSequenceGenerator(length): #The name of the function saying!
    sequence=[]
    dic=['A','C','T','G']
    for i in range(length):
        index=random.randint(0,3)
        sequence.append(dic[index])
    return ''.join(sequence)


	
a = ['ATG','GGG','GGT','GTA','GTG','TAT','TGG']    #Dataset from the book


#a=['ATG','TGG','TGC','GTG','GGC','GCA','GCG','CGT'] #Dataset from the book
#Or you can use function edges to generate this k-mer list
#a=edges(3,'ATTGCGGAGTGACGATG')
#a=edges(3,'AAAAGGGCAAGCGTACGATGGGCCATGCCCGGAGCGGGCCCAAGGGCCCGTGCAATTGCGGAGTGACGATG') #Complicated sequence
#a=randomSequenceGenerator(100)  # If you use this, you have to make the loop parameter big enough

next=True
while(next):
	print('程序菜单')
	print('1.是否使用默认DNA序列碎片:',a)
	print('2.输入你想打碎的DNA序列')
	print('3.随机生成DNA序列并打碎')
	try:
		answer=int(input('请输入数字选择菜单选项，并按回车键执行'))
		if answer not in [1,2,3]:
			raise Exception
		elif answer==1:
			a = ['ATG','GGG','GGT','GTA','GTG','TAT','TGG']
		elif answer==2:
			try:
				seq=input('请输入你想打碎的序列').upper()
				print(seq)
				result=re.findall(r'[^A^T^C^G]{1,}',seq)
				if result!=[]:
					raise Exception
				
				a=edges(3,seq)
			
			except Exception:
				print('请输入有效的DNA序列')
				print('输入有误，并不是有效的DNA序列，将使用默认序列碎片',a)

		else:
			try:
				length=int(input('请输入你希望的DNA序列长度,请输入3-69之间的有效数字'))
				if length not in range(3,70):
					raise Exception
				seq=randomSequenceGenerator(length)
				print()
				print('随机生成的DNA序列为',seq)
				a=edges(3,seq)
			except Exception:
				print('请输入3-69之间的有效数字,输入有误,使用默认序列碎片',a)
				next=True
			
		next=False

			
		
	except Exception:
		print()
		print('对不起，程序无法执行，请输入有效菜单选项数字')
		print()
	
def vertices(length,lis):
    li=[]
    for i in lis:
        li.append(i[:length])
        li.append(i[length-1:])
    return list(set(li))

b = vertices(2,a)

def merge(str1,str2):
    length=len(str1)
    string=''
    if str1[-length+1:]==str2[:length-1]:
        string=str1+str2[-1]
    return string

def graph(vertice,edge):
    dic={}
    for i in vertice:
        dic[i]=[]
    for w in range(4): # This loop handles situation with AAAA.... duplicate
        for k in vertice: # the num in the range is 4, but for more duplications
            for j in vertice:# it should increase accordingly
                if merge(k,j) in edge:
                    dic[k].append(j)
                    edge.remove(merge(k,j))


    return dic
s=graph(b,a[:])
#print(s)
start=startPosition(s)

def findPath(vertice,edge,graphs,start):
    import random
    i=random.randint(0,len(vertice)-1)
    #start = vertice.pop()
    #print(start)
    path = []

    for k in range(len(edge)):

        if start in graphs[start]:
            path.append(start + start[-1])
            graphs[start].remove(start)
        elif graphs[start] == []:
            #print('Attention!!!This path has reached its end,program termine!!!')
            # path=[]
            break
        else:
            index = random.randint(0, len(graphs[start]) - 1)
            nextVertice = graphs[start][index]
            mergedWord = merge(start, nextVertice)
            path.append(mergedWord)
            graphs[start].remove(nextVertice)
            start = nextVertice

    '''if len(path) < len(edge):
        print('Pardon!!!This time I did not find the path, try again!')
    else:
        print(path)
        print('Path found!!!Please run again until you cannot find new path???')'''
    suffix = ''.join([path[i][-1] for i in range(1, len(path))])
    if len(path)==0:
        str=''
    else:
        str = path[0] + suffix

    return str

lis=[]

'''k = random.randint(0, len(b) - 1)
s = graph(b, a[:])
q = findPath(b, a, s, b[k])
print(q)'''
start_time = time.time()

loops=3000 # important parameter, you need to change it frequently
if len(start)==2:
    print()
    #print(start)
    print('正在进行运算')
    print('当前序列碎片为','\n',a)
    for i in range(loops):
        k=random.randint(0,1)
        s=graph(b,a[:])
        q = findPath(b, a, s, start[k])
        if len(q) == len(a) + 2 and q not in lis:
            lis.append(q)

else:
    for i in range(1500):  #The looping time is critical, if is too samll, then not all sequence will be detected
        k=random.randint(0,len(b)-1)
        s=graph(b,a[:])
        q = findPath(b, a, s,b[k])
        if len(q)==len(a)+2 and q not in lis:
            lis.append(q)
print()
print('由序列碎片组装后所有可能的序列:',len(lis),'个')
#print(lis)
print()
for i in lis:
    print(i)
print('运行结束')
print('运行时间: ',round(time.time()-start_time,2),'秒')
#print('循环次数: ',loops)
#print('可能的序列数量: ',len(lis))
