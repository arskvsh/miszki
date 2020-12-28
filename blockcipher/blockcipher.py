import binascii

#Feistel cipher by Arseniy Koveshnikov from BIVT-18-3
#ITKN APD, NUST MISIS

#XOR для бинарного кода в виде строк
def stringXOR(a, b): 
    out = ""
    for i in range(min(len(a), len(b))):
        if (a[i] == b[i]):
            out += "0"
        else:
            out += "1"
    return out

#конвертация строки в бинарный код
def convertToBin(inp):
    output = ''.join(format(ord(i), 'b') for i in inp)
    return output

#конвертация бинарного кода в читаемую строку
"""def convertToReadable(inp):
    output = ''.join([chr([int(x,2)]) for x in [inp[i:i+8] for i in range(0, len(inp), 8)]])
    print(output)
    return output"""

def convertToReadable(inp):
    chars = u''.join([chr(int(x,2)) for x in [inp[i:i+8] for i in range(0, len(inp), 8)]])
    print(chars)
    return chars

#генерация ключа
def generateKey(roundnumber):
    global length
    output = ""
    for i in range(length // 8):
        output += chr(i + 10 + roundnumber*10)
    output = convertToBin(output)
    return output

#функция F (просто XOR)
def F(a, b):
    return stringXOR(a, b)

#удлинение сообщения до длины блока
def prolongue(inp, target):
    output = inp
    while(len(output) < target):
        output += "0"
    return output

#разделение входного сообщения на блоки
def splitIntoBlocks(inp):
    global length
    output = [inp[i:i+length] for i in range(0, len(inp), length)]
    return output

#соединение массива блоков в одну строку
def decAndConnect(inp):
    output = ""
    for i in inp:
        #output += convertToReadable(i)
        print(convertToReadable(i))
    return output

#msg = input("Введите шифруемое сообщение: ")
msg = "V lesu rodilas yelochka, v lesu ona rosla!"
print(msg)

#длина блока
length = 128
#кол-во раундов
rounds = 16

#преобразуем строку в последовательность битов, разделим на блоки и удлиним при необходимости
msg_bin = convertToBin(str(msg))
msg_blocks = splitIntoBlocks(msg_bin)
for m in range(len(msg_blocks)):
    msg_blocks[m] = prolongue(msg_blocks[m], length)
print(msg_blocks)


#шифрование блоков по отдельности
msg_encoded = []
for B in msg_blocks:
    n = len(B)//2
    L = B[:n]
    R = B[n:]
    X = ""

    for i in range(rounds):
        Key = generateKey(i)
        X = F(R, Key)
        X = stringXOR(X, L)
        L = R
        R = X

    msg_encoded.append(L+R)

print(msg_encoded)

#расшифрование блоков по отдельности
msg_decoded = []
for B in msg_encoded:
    n = len(B)//2
    L = B[:n]
    R = B[n:]
    X = ""

    for i in reversed(range(rounds)):
        Key = generateKey(i)
        X = F(L, Key)
        X = stringXOR(X, R)
        R = L
        L = X

    msg_decoded.append(L+R)

print(decAndConnect(msg_decoded))

"""    
#сохраняем необходимые переменные
n = len(msg_bin)//2
L = msg_bin[:n]
R = msg_bin[n:]
X = ""

#шифруем сообщение
for i in range(rounds):
    Key = generateKey(i)
    X = F(R, Key)
    X = stringXOR(X, L)
    L = R
    R = X

print(msg_bin)
encrypted_msg = convertToReadable(L+R)
print(encrypted_msg)

#расшифровываем сообщение
for i in reversed(range(rounds)):
    Key = generateKey(i)
    X = F(L, Key)
    X = stringXOR(X, R)
    R = L
    L = X

decrypted_msg = L+R
print(decrypted_msg)"""