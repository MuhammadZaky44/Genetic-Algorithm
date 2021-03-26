import math
import random


#Fungsi - fungsi yang dipakai

def buatGene():
    #Membuat kromosom individu dengan 15 gene yang berbentuk biner
    individu = []
    for i in range(0,30):
        individu.append(random.randint(0,1))
    return individu




def biner_X(individu):
    #fungsi ini berfungsi untuk mengubah 15 gene pertama menjadi kromosom X yang berbentuk bilangan real
    pembilang = 0
    penyebut = 0
    for i in range (0, 15):
        kuadratik = 2 ** (-1 * (i+1))
        pembilang += individu[i+15] * kuadratik
        penyebut += kuadratik
    return -1 + (((2 - (-1))/penyebut) * pembilang)





def biner_Y(individu):
    #fungsi ini berfungsi untuk mengubah 15 gene selanjutnya menjadi kromosom Y yang berbentuk bilangan real
    pembilang = 0
    penyebut = 0
    for i in range (0, 15):
        kuadratik = 2 ** (-1 * (i+1))
        pembilang += individu[i] * kuadratik
        penyebut += kuadratik
    return -1 + (((1 - (-1))/penyebut) * pembilang)





def initializePopulation():
#fungsi ini berfungsi untuk membuat 20 populasi awal
    pop_krom = []
    pop_fit = []
    for i in range (0,20):
        
        while True: #Menjamin nilai fitness agar tidak negatif
            individu = buatGene() #membuat kromosom dengan buatGene() dan dimasukkan kedalam individu

            x = biner_X(individu)
            y = biner_Y(individu)
            nilai_fitness = rumus(x,y)
            if (nilai_fitness >= 0):
                pop_fit.append(nilai_fitness) 
                pop_krom.append(individu) 
                break        
    return pop_krom, pop_fit




def rumus(x,y):
    #fungsi ini berfungsi untuk mencari nilai fitness
    #rumus sudah diberikan pada petunjuk penugasan
    return (math.cos(x) ** 2) * (math.sin(y) ** 2) + (x + y)




def parentSelection(pop_fit):
    #Kami menggunakan roulette wheel dalam pemilihan orang tua
    #Roulette wheel akan menggunakan variable acak
    total_fit = 0
    for n in range (0, len(pop_fit)):
        total_fit += pop_fit[n]

    acak = random.uniform(0, total_fit)

    for n in range (0, len(pop_fit)):
        acak -= pop_fit[n]
        if (acak <= 0):
            return n




def gacha(chance):
    #fungsi ini akan menentukan peluang untuk ke crossover atau mutasi
    randomin = random.randint(1,100)
    if (1 <= randomin <= chance):
        return True
    else:
        return False




def crossOver(kromosom_1, kromosom_2):
    #pemotongan ada di titik 9 dan 19 
    hasilcross_1 = []
    hasilcross_2 = []
    if (gacha(70)):    #Peluang CrossOver 70% / 0.7 -> dari responsi
        for i in range(0, 30):
            if (i < 9 or i > 19):
                hasilcross_1.append(kromosom_2[i])
                hasilcross_2.append(kromosom_1[i])
            else:
                hasilcross_1.append(kromosom_1[i])
                hasilcross_2.append(kromosom_2[i])
    else:
        for i in range(0, 30):
            hasilcross_1.append(kromosom_1[i])
            hasilcross_2.append(kromosom_2[i])

    return hasilcross_1, hasilcross_2




def mutation(offSpring):
    #Mutasi Biner 0 --> 1 dan 1 --> 0
    hasil_mutation = []
    if (gacha(15)):     #Peluang Mutasi 10% / 0.1 -> dari responsi
        gen = random.randint(0, len(offSpring)) 
        for i in range(0, len(offSpring)):
            if (i == gen):
                if (offSpring[i] == 1):
                    hasil_mutation.append(0)
                else:
                    hasil_mutation.append(1)
            else:
                hasil_mutation.append(offSpring[i])
    else:
        for i in range(0, len(offSpring)):
            hasil_mutation.append(offSpring[i])
    
    return hasil_mutation




def bestIndividu(pop_fit):
    #fungsi yang bertujuan untuk menyeleksi nilai fitness yang terbaik
    maximum = 0
    for i in range(0, len(pop_fit)):
        if (pop_fit[i] >= maximum):
            maximum = pop_fit[i]
            bestInd_1 = i

    maximum = 0
    for i in range(0, len(pop_fit)):
        if ((pop_fit[i] >= maximum) and (i != bestInd_1)):
            maximum = pop_fit[i]
            bestInd_2 = i

    return bestInd_1, bestInd_2











#Main Program


pop_krom, pop_fit = initializePopulation()

#proses akan terus berjalan hingga generasi ke 30
for i in range (1,30):
    next_fit = []
    next_krom = []
    #array diatas digunakan untuk menampung generasi yang berikutnya
    while (len(next_krom) < 18):
        # Ini dibawah 18 dikarenakan pada initializePopulation kami memberikan nilai 20, dan sudah di return bestInd_1 dan bestInd_2 
        #sehingga total menjadi 20

        #Memanggil parentSelection 
        orangTua1 = parentSelection(pop_fit)
        orangTua2 = parentSelection(pop_fit)

        #Memanggil crossOver
        anak1, anak2 = crossOver(pop_krom[orangTua1], pop_krom[orangTua2])
       
        #Memanggil mutation
        anak1 = mutation(anak1)
        anak2 = mutation(anak2)


        #offSpring akan dimasukan ke generasi berikutnya
        next_krom.append(anak1)
        next_krom.append(anak2)
        

        #memasukan nilai fitness offSpring 1 ke generasi berikutnya 
        x = biner_X(anak1)
        y = biner_Y(anak1)
        nilai_fitness = rumus(x,y)
        if (nilai_fitness >= 0):    #nilai fitness tidak negatif
            next_fit.append(nilai_fitness)
        else:
            next_fit.append(0)      #jika negatif akan jadi 0

        #memasukan nilai fitness offSpring 2 ke generasi berikutnya 
        x = biner_X(anak2)
        y = biner_Y(anak2)
        nilai_fitness = rumus(x,y)
        if (nilai_fitness >= 0):    
            next_fit.append(nilai_fitness)
        else:
            next_fit.append(0)



    #nilai fitness generasi berikutnya
    bestInd_1, bestInd_2 = bestIndividu(pop_fit)

    #memasukkan nilai fitness kedalam populasi fitness
    next_fit.append(pop_fit[bestInd_1])
    next_fit.append(pop_fit[bestInd_2])

    #memasukkan kromosom kedalam populasi kromosom 
    next_krom.append(pop_krom[bestInd_1])
    next_krom.append(pop_krom[bestInd_2])
    
    #Pergantian generasi lama ke generasi baru
    pop_krom.clear()
    pop_fit = next_fit

    pop_krom.clear()
    pop_krom = next_krom

#solusi untuk individu dengan kromosom terbaik
bestInd_1, bestInd_2 = bestIndividu(pop_fit)

x = biner_X(pop_krom[bestInd_1])
y = biner_Y(pop_krom[bestInd_1])



print("Kromosom dari individu yang terbaik adalah : \n", pop_krom[bestInd_1])
print("\nNilai fitness terbaik sebesar: ", rumus(x, y))
print("\nDengan hasil x = ", x, " dan y = ", y)
print("----------------------------------------------------------------------------")