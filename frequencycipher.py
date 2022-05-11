import copy

# English Letter Frequency (from sample of 40,000 words) (A-Z)
# Source: http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
freqTableEnglish = dict()
freqTableEnglish.update({1:"e",2:"t",3:"a",4:"o",5:"i",6:"n",7:"s",8:"r",9:"h",10:"d",11:"l",12:"u",13:"c",14:"m",15:"f",16:"y",17:"w",18:"g",19:"p",20:"b",21:"v",22:"k",23:"x",24:"q",25:"j",26:"z"})

#read ciphertext file into variable
with open('cipherText.txt', 'r') as file:
    ciphertext = file.read().replace('\n', '')

#convert ciphertext to array of separate strings
cipherTextArr = list(ciphertext)

#define english alphabet
cipherAlphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
plainAlphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

#count letter frequencies for ciphertext and store in array 
freqCount = [0] * 26
for i in range (len(cipherAlphabet)):
    for char in ciphertext:
        if char == cipherAlphabet[i]:
            freqCount[i] += 1

#sort frequecies from high to low, store index order
sortedfc = sorted(range(len(freqCount)), key=lambda k: freqCount[k], reverse=True)

#create ordered (decending) map of letter frequecies in ciphertext
freqTableCipherText = dict()
for i in range (len(sortedfc)):
    freqTableCipherText[cipherAlphabet[sortedfc[i]]] = i + 1
for i in  range (len(cipherTextArr)):
    if freqTableCipherText.get(cipherTextArr[i]) != None:
        cipherTextArr[i] = freqTableEnglish.get(freqTableCipherText.get(cipherTextArr[i]))

#create copy of initial attempt using frequency analysis
initialCipherTextArray = copy.copy(cipherTextArr)

#create inital key table
key = dict()
for char in cipherAlphabet:
    key[char] = freqTableEnglish.get(freqTableCipherText.get(char))

print("\nInitial Key:")
print(key)
print("")     
print(*cipherTextArr, sep="")

manualSwaps = 0
decryptState = True
#continue until user is satified with plaintext (no more desired swaps)
while decryptState:
    print("")
    state = input("Finished? (y/n) ")
    if state == "y" or state == "Y":
        decryptState = False
        continue
    
    swap = input("Define swap points. for (a -> b) type (ab)  ")
    
    #swap letters in plaintext
    for i in range (len(cipherTextArr)):
        if cipherTextArr[i] == swap[0]:
            cipherTextArr[i] = "$"

    for i in range (len(cipherTextArr)):
        if cipherTextArr[i] == swap[1]:
            cipherTextArr[i] = swap[0]
        if cipherTextArr[i] == "$":
            cipherTextArr[i] = swap[1]

    #swap letters in key map
    for char in cipherAlphabet:
        if key.get(char) == swap[1]:
            key[char] = "$"

    for char in cipherAlphabet:
        if key.get(char) == swap[0]:
            key[char] = swap[1]
        
    for char in cipherAlphabet:
        if key.get(char) == "$":
            key[char] = swap[0] 

    manualSwaps += 1

    print("")
    print(*cipherTextArr, sep="")
    print("\nUpdated Key:")
    print(key)

#count frequencies in plaintext
freqCountPlain = [0] * 26
for i in range (len(plainAlphabet)):
    for char in cipherTextArr:
        if char == plainAlphabet[i]:
            freqCountPlain[i] += 1

#count total letters in text
textSize = len(initialCipherTextArray)
#count amount of charaters that were correct in the initial guess compared to the final plaintext
correctCharCount = 0
for i in range (textSize):
    if initialCipherTextArray[i] == cipherTextArr[i]:
        correctCharCount += 1
#calculate accuracy of the initial guess (percentance of letters correct)
accuracy = (correctCharCount/textSize)*100

#write to plainText.txt file
f = open("plainText.txt", "w")
temp = "".join(cipherTextArr)
f.write(temp)
f.close()

#write analysis to analysis.txt
f = open("analysis.txt", "w")
f.write("ANALYSIS:\n\nciphertext:\n")
f.write(ciphertext)
f.write("\n\nplaintext:\n")
temp = "".join(cipherTextArr)
f.write(temp)
f.write("\n\nKey:\n")
f.write(str(key))
f.write("\n\nApprox. Accuracy of Initital Frequency Analysis and Substitution: " + "{:.0f}".format(accuracy) + "%")
f.write("\nTotal Char: " + str(textSize) + "   Initally Correct: " + str(correctCharCount) + "   Manual Swaps: " + str(manualSwaps) + "\n\n" + "Ciphertext Letter Frequencies:\n")
for i in range (len(cipherAlphabet)):
    temp = freqCount[i] / textSize
    f.write(cipherAlphabet[i] + "  |  Relative Frequency: " + "{:.4f}".format(temp) + "  |  Frequency: " + str(freqCount[i]) + "\n")
f.write("\nPlaintext Cipher Frequencies:\n")
for i in range (len(plainAlphabet)):
    temp = freqCountPlain[i] / textSize
    f.write(plainAlphabet[i] + "  |  Relative Frequency: " + "{:.4f}".format(temp) + "  |  Frequency: " + str(freqCountPlain[i]) + "\n")
f.close()

#print analysis to terminal
print("")
print("Analysis:")
print("")
print("Cipher Text:")
print(ciphertext)
print("")
print("Plain Text:")
print(*cipherTextArr, sep="")
print("")
print("Key:")
print(key)
print("")
print("Aprox. Accuracy of Initial Frequency Analysis: " + "{:.0f}".format(accuracy) + "%   Total Char: " + str(textSize) + "   Initally Correct: " + str(correctCharCount) + "   Manual Swaps: " + str(manualSwaps))
