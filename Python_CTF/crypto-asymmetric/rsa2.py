# 2. Fermat_Factorization.py

from gmpy2 import isqrt
from Crypto.Util.number import long_to_bytes

def fermat(n):
    print("init")

    a = isqrt(n)
    b = a
    b2 = pow(a,2) - n

    print("a= "+str(a))
    print("b= " + str(b))

    print("b2=" + str(b2))
    print("delta-->" + str(pow(b, 2) - b2 % n)+"\n-----------")
    print("iterate")
    i = 0

    while True:
        if b2 == pow(b,2):
            print("found at iteration "+str(i))
            break;
        else:
            a +=1
            b2 = pow(a, 2) - n
            b = isqrt(b2)
        i+=1
        print("iteration="+str(i))
        print("a= " + str(a))
        print("b= " + str(b))
    print("b2 =" + str(b2))
    print("delta-->" + str(pow(b, 2) - b2 % n) + "\n-----------")

    p = a+b
    q = a-b

    return p,q

if __name__ == '__main__':
    
    n = 84579385253850209980531118129485716360575269582423585759001305965013034395499445816183248675447710453177558996114910965695049824431833160231360553529286419317374940825879760576417322050461035628520331998356731488662783964882867470865445762024182798458285340930223702904421982112483822508094601373760076526513
    c = 17668912838657324025145974741772418705042500725249546941532860274474967308105880488339989276944955996505219230783445824255159192918050910923274393622976856688164873271519593664637389313627158186713709798641755794557335453137110328826176249263923330675599181311888750799280794535134718146446678320514719996743
    e = 65537
    
    p, q = fermat(n)
    
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    print(long_to_bytes(m))