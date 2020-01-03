import numpy as np, pandas as pd

def integrate(a,b,c,d):
    return (((1/2)*a)+b)+(c-((1/2)*d))

def ada_ganjil_genap(arr,opt):
    val = 1 if opt == '1' else 0
    for i in arr:
        if i%2 == val:
            return True
    return False

def find_ganjil_genap(arr,opt):
    val = 1 if opt == '1' else 0
    gangen = []
    for x,i in enumerate(arr):
        if i%2 == val:
            gangen.append((x,i))
    return gangen

def Print(arr,sup,dem,lr,lc):
    x = np.copy(arr)
    x = np.vstack((arr,dem))
    x = np.vstack((x.T,list(sup)+[''])).T

    df = pd.DataFrame(x)
    df.columns = ['D'+str(i) for i in lr]+['Supply']
    df.index = ['   S'+str(i) for i in lc]+['   Demand']
    print(df,'\n')

print('PILIH DATASET')
print('1. Data Ganjil')
print('2. Data Genap')
print('3. Data Campur')
dset = ' '
while dset not in '123':
    dset = input('input opsi: ')
names = 'ganjil genap campur'.split()
print('')

raws = pd.read_excel('data '+names[int(dset)-1]+'.xlsx',sheet_name='RANK')
raws = np.int32(raws.values)

demand = raws[-1][:-1]
supply = raws[:,-1][:-1]


N = len(raws)-1
V = len(raws[0])-1

lc = np.arange(N)+1
lr = np.arange(V)+1

data = raws[0:-1]
data = data[:,:-1]

rank = np.hstack(raws[:-1][:,:-1])
rankori = np.asarray(rank).reshape(N,V)

print('PILIH METODE')
print('A. LOCFTP')
print('B. MOCAM')
met = ' '
while met not in 'AB':
    met = input('input opsi: ')
menu = 'LOCFTP' if met == 'A' else 'MOCAM'
print('')

print('PILIH VARIANSI METODE')
print('1. Ganjil')
print('2. Genap')
print('3. Minimum')
print('4. Maksimum')
opt = ' '
while opt not in '1234':
    opt = input('input opsi: ')
print('')

if opt == '1':
    mystr1 = ' Ganjil'
    mystr2 = ' Minimum'
    subm = 'GANJIL'
elif opt == '2':
    mystr1 = ' Genap'
    mystr2 = ' Minimum'
    subm = 'GENAP'
elif opt == '3':
    mystr1 = ''
    mystr2 = ' Minimum'
    subm = 'MINIMUM'
else:
    mystr1 = ''
    mystr2 = ' Maksimum'
    subm = 'MAKSIMUM'

print('\n'+menu+' '+subm+' PADA DATASET '+names[int(dset)-1].upper())
print('-'*70)

print('RANKING AWAL:')
Print(np.asarray(rank).reshape(N,V),supply,demand,lr,lc)

alokasi =[]
stop = False; I = 1
while True:
    print('ITERASI',I)
    print('-'*70)

    if opt in '12':

        show = False
        gngn = 1

        dikali = 1/2 if opt == '1' else 2
        while not ada_ganjil_genap(rank,opt) and not sum(rank) == 0:
            show = True
            rank = rank*dikali
            gngn = gngn*dikali

        if show:
            print('>> Tidak Terdapat Rank'+mystr1+', Rank Dikali '+str(gngn)+', Rank Sekarang:')
            Print(np.asarray(rank).reshape(N,V),supply,demand,lr,lc)

        gangen = find_ganjil_genap(rank,opt)
    
        indx,vals = np.asarray(gangen).T
        indx = np.int32(indx)
        
    if opt in '12':
        gangen = min(vals)
    elif opt == '3':
        gangen = int(np.min(rank))
    else:
        gangen = int(np.max(rank))
        
    print('>> Nilai'+mystr1+mystr2+':',gangen,'\n')

    indx = indx if opt in '12' else np.arange(len(rank))
    vals = vals if opt in '12' else rank

    if met == 'A':
        print('>> Pengurangan Rank'+mystr1+' oleh Nilai'+mystr1+mystr2+':')
        for x,i in enumerate(indx):
            rank[i] = vals[x]-gangen
        Print(np.asarray(rank).reshape(N,V),supply,demand,lr,lc)
        pick = 0
    else:
        pick = gangen

    data = np.asarray(rank).reshape(N,V)

    while True:

        x,y = np.where(data==pick)
        if len(x) == 0 and len(y) == 0:
            break
        x,y = x[0],y[0]

        if supply[x] > demand[y]:
            print('>> Hapus Kolom D'+str(lr[y]))
            data = np.delete(data,y,1)
            alokasi.append([lc[x],lr[y],demand[y]])
            supply[x] = supply[x]-demand[y]

            demand = np.delete(demand,y)
            lr = np.delete(lr,y)
        elif supply[x] < demand[y]:
            print('>> Hapus Baris S'+str(lc[x]))
            data = np.delete(data,x,0)

            alokasi.append([lc[x],lr[y],supply[x]])
            demand[y] = demand[y]-supply[x]

            supply = np.delete(supply,x)
            lc = np.delete(lc,x)
        else:
            print('>> Hapus Kolom D'+str(lr[y])+' dan Baris S'+str(lc[x]))
            data = np.delete(data,y,1)
            data = np.delete(data,x,0)

            alokasi.append([lc[x],lr[y],demand[y]])
        
            demand = np.delete(demand,y)
            supply = np.delete(supply,x)

            lr = np.delete(lr,y)
            lc = np.delete(lc,x)
            
        Print(data,supply,demand,lr,lc)

        try:
            rank = np.hstack(data)
            N = len(data)
            V = len(data[0])
            I += 1
        except:
            stop = True
            break
    if stop:
        break

print('ALOKASI')
print('-'*70)
for a,b,c in alokasi:
    print('S'+str(a)+' ke D'+str(b)+' sebanyak',c)

print('\nHASIL')
print('-'*70)
jumlah = 0
mystr = []
for a,b,c in alokasi:
    jumlah += rankori[a-1,b-1]*c
    mystr.append('('+str(rankori[a-1,b-1])+' x '+str(c)+')')
print(' + '.join(mystr)+' =',jumlah)
