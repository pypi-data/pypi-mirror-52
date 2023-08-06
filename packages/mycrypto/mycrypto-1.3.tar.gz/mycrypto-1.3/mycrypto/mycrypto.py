# -- coding:UTF-8 --
keymap=['password','pass','crypto','key','keyword','admin']
Standard = {'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,'F':0.02228,'G':0.02015,'H':0.06094,'I':0.06966,'J':0.00153,'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,'U':0.02758,'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,'Z':0.00074}
#def Caesar_en(strings,offset):

#Caesar password
def Caesar_encode(plaintext,offset):
	plaintext=plaintext.lower()
	ciphertext=''
	offset=int(offset)
	for i in plaintext:
		tmp=ord(i)
		if(tmp>=97 and tmp<=122):
			if(tmp+offset>122):
				ciphertext+=chr(tmp+offset-26)
			else:
				ciphertext+=chr(tmp+offset)
		else:
			ciphertext+=i
	print("The ciphertext is :",ciphertext)
	return ciphertext

def Caesar_decode(ciphertext,offset):
	ciphertext=ciphertext.lower()
	offset=int(offset)
	plaintext=''
	for i in ciphertext:
		tmp=ord(i)
		if(tmp>=97 and tmp<=122):
			if(tmp-offset<97):
				plaintext+=chr(tmp-offset+26)
			else:
				plaintext+=chr(tmp-offset)
		else:
			plaintext+=i
	print("The plaintext is :",plaintext)
	return plaintext		




# Affine password
#get the inverse element
def InverseElement(a):
    for i in range(1,27):
        if (a*i%26)==1:
            return i

#encrypt
def en_radiation(word,m,n):
	if(ord(word)>=97 and ord(word)<=122):
		offset=97
	elif(ord(word)>=65 and ord(word)<=90):
		offset=65
	else:
	    print("invilad input")
	word=((ord(word)-offset)*m+n)%26+65
	return chr(word)

def Affine_encode(strings,m,n):
    m=int(m)
    if(m%2==0):
        print("m must be a odd number")
    else:	
        n=int(n)
        ciphertext=''
        for i in strings:
            if(i==' '):
                ciphertext+=''
            else:
                ciphertext+=en_radiation(i,m,n)
        print("The ciphertext is : ",ciphertext)
        return ciphertext 
     

#decrypt
def de_radiation(word,m,n):
    m=InverseElement(m)
    if(ord(word)>=97 and ord(word)<=122):
        offset=97
    elif(ord(word)>=65 and ord(word)<=90):
        offset=65
    else:
        print("invilad input")
    word=((ord(word)-offset)-n)*m%26+offset
    return chr(word)

def Affine_decode(strings,m,n):
    m=int(m)
    n=int(n)
    plaintext=''
    for i in strings:
        if (i==' '):
       	    plaintext+=''
        else:
            plaintext+=de_radiation(i,m,n)
    print("The plaintext is  : ",plaintext)
    return plaintext


# Virginia password
#get the length of the keyword
def length(Ciphertext):
    ListCiphertext=list(Ciphertext)
    Keylength=1
    while True:
        CoincidenceIndex = 0
        for i in range(Keylength):
            Numerator = 0
            PresentCipherList = ListCiphertext[i::Keylength]
            for Letter in set(PresentCipherList):
                Numerator += PresentCipherList.count(Letter) * (PresentCipherList.count(Letter)-1)
            CoincidenceIndex += Numerator/(len(PresentCipherList) * (len(PresentCipherList)-1)) 
        Average=CoincidenceIndex / Keylength
        Keylength += 1
        print(str.format("The offset is {0},and the IC is {1}",Keylength,Average))
        if Average > 0.06:
            break 
    Keylength -= 1
    return Keylength

#get key
def keyword(Ciphertext,keylength):
    ListCiphertext = list(Ciphertext)
    Standard = {'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,'F':0.02228,'G':0.02015,'H':0.06094,'I':0.06966,'J':0.00153,'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,'U':0.02758,'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,'Z':0.00074}
    while True:
        KeyResult = [] 
        for i in range(keylength):
            PresentCipherList = ListCiphertext[i::keylength]
            QuCoincidenceMax = 0
            KeyLetter = "*"
            for m in range(26):
                QuCoincidencePresent = 0
                for Letter in set(PresentCipherList):
                    LetterFrequency = PresentCipherList.count(Letter) / len(PresentCipherList)
                    k = chr( ( ord(Letter) - 65 - m ) % 26 + 65 )
                    StandardFrequency = Standard[k]
                    QuCoincidencePresent = QuCoincidencePresent + LetterFrequency * StandardFrequency
                if QuCoincidencePresent > QuCoincidenceMax:
                    QuCoincidenceMax = QuCoincidencePresent
                    KeyLetter = chr( m + 65 )
            KeyResult.append( KeyLetter )
        Key = "".join(KeyResult)
        break
    return Key


def viger_encrypt(word,key):
    word=ord(word)
    key=ord(key)
    if(word>=97 and word<=122):
        w_offset=97
    elif(word>=65 and word<=90):
        w_offset=65
    else:
        print("invilad input")
    if(key>=97 and key<=122):
        k_offset=97
    elif(key>=65 and key<=90):
        k_offset=65
    else:
        print("invilad input")
    return chr(((word-w_offset+key-k_offset)%26)+97)

def viger_decrypt(word,key):
    word=ord(word)
    key=ord(key)
    if(word>=97 and word<=122):
        w_offset=97
    elif(word>=65 and word<=90):
        w_offset=65
    else:
        print("invilad input")
    if(key>=97 and key<=122):
        k_offset=97
    elif(key>=65 and key<=90):
        k_offset=65
    else:
        print("invilad input")
    return chr(((word-w_offset-key+k_offset)%26)+97)


def viger_decode(ciphertext,key):
	flag=0
	plaintext=''
	length=len(key)
	for i in ciphertext:
		if i==' ':
			ciphertext+=i
		else:
			if(flag>=length):
				flag=0
				plaintext+=viger_decrypt(i,key[flag])
			else:
				plaintext+=viger_decrypt(i,key[flag])
			flag+=1
	print("The plaintext is : ",plaintext)
	return plaintext

def viger_encode(plaintext,key):
	flag=0
	ciphertext=''
	length=len(key)
	for i in plaintext:
		if i==' ':
			plaintext+=i
		else:
			if(flag>=length):
				flag=0
				ciphertext+=viger_encrypt(i,key[flag])
			else:
				ciphertext+=viger_encrypt(i,key[flag])
			flag+=1
	print("The ciphertext is : ",ciphertext)
	return ciphertext


def viger_nokey(ciphertext,choice):
	global keymap
	Ciphertext=ciphertext.upper()
	if (choice=='0'):
		keylength=length(Ciphertext)
		if(keylength<40):
			print("The ciphertext is so short so it could be wrong,u can try it by my dictionary")
		key=keyword(Ciphertext,keylength)
		print("length of the key is :",keylength)
		print("The key is： " , key)
		print("The plaintext is : ",viger_decode(Ciphertext,key))
	if (choice=='1'):
		print("We will test the all of the keys in our dictionary")
		for i in range(len(keymap)):
			print(str.format("The key is : {0},and the plaintext is {1}!",keymap[i],viger_decode(Ciphertext,keymap[i])))




def main():
	plaintext="hello world"
	affpl=Affine_encode(plaintext,3,4)
	Affine_decode(affpl,3,4)
	ap=viger_encode(plaintext,"keyword")
	viger_nokey(ap,'1')
	viger_nokey(ap,'0')

if __name__=="__main__":
	main()