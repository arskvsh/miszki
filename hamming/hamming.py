#Hamming code 8-12 implementation by Arseniy Koveshnikov from BIVT-18-3
#ITKN APD, NUST MISIS

import random

def addPlacesForControlBits(message):
    ands = [15, 112, 128]
    parts = []
    for i in range(3):
        parts += [message & ands[i]]
    result = parts[0] | parts[1]*2 | parts[2]*4
    return result

def calcEs(cbmessage):
    patterns = [2730, 1638, 481, 31]
    e = []
    for i in range(4):
        e += [calcE(cbmessage & patterns[i])]
    return e
     
def calcE(econtrolled):
    countof1s = 0
    while (econtrolled): 
        countof1s += econtrolled & 1
        econtrolled >>= 1
    return countof1s % 2

def insertEs(cbmessage):
    fincbmessage = cbmessage | e[0]*2048 | e[1]*1024 | e[2]*256 | e[3]*16
    return fincbmessage

def addError(msg):
    errorPow = random.randint(0,11)
    error = 2 ** errorPow
    errmsg = msg
    if (msg & error > 0):
        errmsg = msg - error
    else:
        errmsg = msg + error
    print('Помехи внесли ошибку в разряд', 12-errorPow)
    return errmsg

def calcK(msg):
    extractedEs = [(msg & 2048) // 2048, (msg & 1024) // 1024, (msg & 256) // 256, (msg & 16) // 16]
    newEs = calcEs(msg & 751)
    k = 0
    for i in range(4):
        k += (extractedEs[i] ^ newEs[i]) * (2 ** i)
    return k

def fixError(msg, errorPow):
    fixedmsg = msg
    error = 2 ** (12 - errorPow)
    if (msg & error > 0):
        fixedmsg = msg - error
    else:
        fixedmsg = msg + error
    return fixedmsg

# e1 = 0b101010101010
# e2 = 0b011001100110
# e3 = 0b000111100001
# e4 = 0b000000011111

message = int("10001011", 2)
message = 0

while len(bin(message)[2:]) != 8:
    try:
        message = int(input('Введите 8-битное двоичное число: '), 2)
    except:
        print("Неверный ввод!")

print("Исходные данные")
print(bin(message)[2:])

cbmsg = addPlacesForControlBits(message)
e = calcEs(cbmsg)
fincbmsg = insertEs(cbmsg)

print("\nСообщение с вычисленными контрольными битами:")
print(bin(fincbmsg)[2:])

print("\n***ПРОИСХОДИТ ПЕРЕДАЧА ДАННЫХ***")
errmsg = addError(fincbmsg)

print("\nДанные получены на другой стороне. Удастся ли выяснить, где ошибка?")
print(bin(errmsg)[2:])
k = calcK(errmsg)

print(f"\nАлгоритм обнаружил ошибку в разряде {k}...")
print("...и даже исправил её:")
print(bin(fixError(errmsg, k))[2:])