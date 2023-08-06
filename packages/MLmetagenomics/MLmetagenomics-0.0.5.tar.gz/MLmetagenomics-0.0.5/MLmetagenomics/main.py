import warnings
import pandas as pd
import random
import sys
from sklearn.ensemble import RandomForestClassifier
import numpy as np, numpy.random
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

print('请稍等，正在读取数据','<-'*5)
warnings.filterwarnings('ignore')
df=pd.read_csv('abundance.txt',sep=None,header=None)
print('你好，欢迎使用由高端设计的人体微生物宏基因组机器学习软件')
print('本软件希望使用机器学习的来建立人体微生物菌群环境的变化和糖尿病2型的预测模型,一共有400多名实验样本参与，包括健康的患病的')
print('='*35,'软件菜单','='*35)
print('1.浏览数据的前5行')
print('2.随机挑选出1个样本')
print('3.使用Random Forest分类方法建立模型')
print('4.使用Support Vector分类方法建立模型')
print('5.使用Logistic Regression分类方法建立模型')
print('6.使用Neuron Network分类方法建立模型')


print('7.退出软件')
#print(df.iloc[1,])
#lis={i for i in df.iloc[1,]}
#print(lis)
#print(df.iloc[607,1])
#print(df.iloc[2,440])

#print(len(lis))
#df3=pd.DataFrame([[1,2],[3,3],[4,1]])
#r=[0,1,0]

#print(clf)

choice=input('请从菜单选择你需要的选项->>>')
while choice!='7':
    if choice=='7':
        sys.exit(0)
    elif choice=='1':
        print(df.head())
    elif choice=='2':
        print(df.iloc[:,[0,random.randint(0,440)]])
    elif choice=='3':
        df2=df.iloc[2:608,1:441].T
        dic={'n':0,'t2d':1}
        lis=[dic[i] for i in df.iloc[1,1:]]
        clf = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0)
        clf.fit(df2,lis)
        print('模型已经建立完毕')
        print('1.使用随机的一个样本进行预测患病与否')
        print('2.使用随机生成的虚拟样本进行预测患病与否')
        user=input('请选择>>>>>>')
        if user=='1':
            sample=df2.iloc[random.randint(0,440),:]
            print('样本为\n',sample)
            result=clf.predict([sample])
            print(len(sample))
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
            #print({'0':'该样本健康','1':'该样本患病'}result)


        else:
            
            sample=np.random.dirichlet(np.ones(606),size=1)
            print('样本为\n',sample)
            result=clf.predict(sample)
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
    elif choice=='4':
        df2=df.iloc[2:608,1:441].T
        dic={'n':0,'t2d':1}
        lis=[dic[i] for i in df.iloc[1,1:]]
        clf = svm.SVC()
        clf.fit(df2,lis)
        print('模型已经建立完毕')
        print('1.使用随机的一个样本进行预测患病与否')
        print('2.使用随机生成的虚拟样本进行预测患病与否')
        user=input('请选择>>>>>>')
        if user=='1':
            sample=df2.iloc[random.randint(0,440),:]
            print('样本为\n',sample)
            result=clf.predict([sample])
            print(len(sample))
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
            #print({'0':'该样本健康','1':'该样本患病'}result)


        else:
            
            sample=np.random.dirichlet(np.ones(606),size=1)
            print('样本为\n',sample)
            result=clf.predict(sample)
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')    
    elif choice=='5':
        df2=df.iloc[2:608,1:441].T
        dic={'n':0,'t2d':1}
        lis=[dic[i] for i in df.iloc[1,1:]]
        clf = LogisticRegression()
        clf.fit(df2,lis)
        print('模型已经建立完毕')
        print('1.使用随机的一个样本进行预测患病与否')
        print('2.使用随机生成的虚拟样本进行预测患病与否')
        user=input('请选择>>>>>>')
        if user=='1':
            sample=df2.iloc[random.randint(0,440),:]
            print('样本为\n',sample)
            result=clf.predict([sample])
            print(len(sample))
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
            #print({'0':'该样本健康','1':'该样本患病'}result)


        else:
            
            sample=np.random.dirichlet(np.ones(606),size=1)
            print('样本为\n',sample)
            result=clf.predict(sample)
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
    elif choice=='6':
        df2=df.iloc[2:608,1:441].T
        dic={'n':0,'t2d':1}
        lis=[dic[i] for i in df.iloc[1,1:]]
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
        clf.fit(df2,lis)
        print('模型已经建立完毕')
        print('1.使用随机的一个样本进行预测患病与否')
        print('2.使用随机生成的虚拟样本进行预测患病与否')
        user=input('请选择>>>>>>')
        if user=='1':
            sample=df2.iloc[random.randint(0,440),:]
            print('样本为\n',sample)
            result=clf.predict([sample])
            print(len(sample))
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
            #print({'0':'该样本健康','1':'该样本患病'}result)


        else:
            
            sample=np.random.dirichlet(np.ones(606),size=1)
            print('样本为\n',sample)
            result=clf.predict(sample)
            if result==[0]:
                print('该样本健康')
            else:
                print('该样本患病')
    
    print('1.浏览数据的前5行')
    print('2.随机挑选出1个样本')
    print('3.使用Random Forest分类方法建立模型')
    print('4.使用Support Vector分类方法建立模型')
    print('5.使用Logistic Regression分类方法建立模型')
    print('6.使用Neuron Network分类方法建立模型')


    print('7.退出软件')
    choice=input('请从菜单选择你需要的选项->>>')

    
        



