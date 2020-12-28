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
    output = bin(int.from_bytes(inp.encode(), 'big'))[2:]
    return output

#конвертация бинарного кода в читаемую строку
def convertToReadable(inp):
    output = ''.join([chr(int(x,2)) for x in [inp[i:i+7] for i in range(0, len(inp), 8)]])
    return output

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
        output += convertToReadable(i)
    return output

#msg = input("Введите шифруемое сообщение: ")
msg = "Privetiki"
print("Исходное сообщение:", msg)

#длина блока
length = 128
#кол-во раундов
rounds = 8

#преобразуем строку в последовательность битов, разделим на блоки и удлиним при необходимости
msg_bin = convertToBin(str(msg))
msg_blocks = splitIntoBlocks(msg_bin)
for m in range(len(msg_blocks)):
    msg_blocks[m] = prolongue(msg_blocks[m], length)

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

print("Закодированное сообщение:", decAndConnect(msg_encoded))

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

print("Раскодированное сообщение:", decAndConnect(msg_decoded))