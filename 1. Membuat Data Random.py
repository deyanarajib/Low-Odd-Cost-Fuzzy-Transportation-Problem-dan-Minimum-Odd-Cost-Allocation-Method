import numpy as np, pandas as pd

def line():
    print('-'*70)

def integrate(a,b,c,d):
    return (((1/2)*a)+b)+(c-((1/2)*d))

def dataframe(arr,sup,dem,lr,lc,prin):
    x = np.copy(arr).tolist()
    x.append(dem)
    
    x = (np.asarray(x).T).tolist()
    x.append(list(sup)+[''])

    x = np.asarray(x).T

    df = pd.DataFrame(x)
    df.columns = ['D'+str(i) for i in lr]+['Supply']
    df.index = ['   S'+str(i) for i in lc]+['   Demand']

    if prin:
        print(df,'\n')
    else:
        return df

print('\nMEMBUAT DATA RANDOM'); line()
x = input('Input Banyak Baris: '); x = int(x)
y = input('Input Banyak Kolom: '); y = int(y)

lc = np.arange(x)+1
lr = np.arange(y)+1

while True:
    sup = [np.random.randint(20,100) for i in range(x)]
    dem = [np.random.randint(20,100) for i in range(y)]
    if sum(sup) == sum(dem):
        break

name = ['GANJIL','GENAP','CAMPUR']

for opt,z in enumerate(name):
    writer = pd.ExcelWriter('data '+z.lower()+'.xlsx')
    while True:
        print(''); line(); print('MEMBUAT DATA '+z+' RANDOM'); line()

        value = 1 if opt == 0 else 0
        
        data = []
        rank = []
        for i in range(x):
            temp1,temp2 = [],[]
            for j in range(y):
                while True:
                    dif1 = np.random.randint(2,10)
                    dif2 = np.random.randint(2,6)
                    m = np.random.randint(50)
                    n = m+dif1
                    a = n+dif2
                    b = a+dif1
                    res = np.int(np.ceil(integrate((n-m),m,b,(b-a))*0.5))
                    if res % 2 == value or opt == 2:
                        break
                temp1.append([m,n,a,b])
                temp2.append(res)
        
            data.append(temp1)
            rank.append(temp2)

        data = np.asarray(data)
        rank = np.asarray(rank)

        print('\n>> DATA FUZZY:')
        dataframe(data,sup,dem,lr,lc,True)

        print('>> RANK DATA:')
        dataframe(rank,sup,dem,lr,lc,True)

        print('Simpan Data Sebagai Data '+z.title()+'?')
        print('0. Buat Ulang Data',z.title())
        print('1. Simpan Data',z.title())

        ulang = ' '
        while ulang not in '01':
            ulang = input('input opsi: ')

        if ulang == '1':
            df1 = dataframe(data,sup,dem,lr,lc,False)
            df2 = dataframe(rank,sup,dem,lr,lc,False)
            df1.to_excel(writer,sheet_name='FUZZY')
            df2.to_excel(writer,sheet_name='RANK')
            writer.close()
            break
