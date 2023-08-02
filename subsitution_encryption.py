from Substitution import *
import re

standardSubs = [["Fibonacci", {"a":"ab", "b":"a"}], 
                ["2-component Rauzy Fractal", {"a":"acb", "b":"c", "c":"a"}],
                ["A->AB, B->C, C->A", {"a":"ab", "b":"c", "c":"a"}],
                ["Central Fibonacci", {"a":"ac", "b":"db", "c":"b", "d":"a"}],
                ["Infinite component Rauzy Fractal", {"a":"baca", "b":"aac", "c":"a"}],
                ["Kidney and its dual", {"a":"ab", "b":"cb", "c":"a" }],
                ["Kolakoski-(3,1) symmmetric variant, dual", {"a":"aca", "b":"a", "c":"b"}],
                ["Kolakoski-(3,1) variant A, with dual", {"a":"bcc", "b":"ba", "c":"bc"}],
                ["Kolakoski-(3,1) variant B, with dual", {"a":"abcc", "b":"a", "c":"bc"}],
                ["Kolakoski-(3,1), with dual", {"a":"abc", "b":"ab", "c":"b"}],
                ["Non-invertible connected Rauzy Fractal", {"a":"bacb", "b":"abc", "c":"ba"}],
                ["Non-reducible 4-letter", {"a":"aad", "b":"cd", "c":"cb", "d":"ab"}],
                ["Period Doubling", {"a":"ab", "b":"aa"}],
                ["Smallest PV", {"a":"bc", "b":"c", "c":"a"}],
                ["Thue Morse", {"a":"ab", "b":"ba"}],
                ["Tribonacci", {"a":"ab", "b":"ac", "c":"a"}]
]

DEBUG = True

def reverse_substitution(substitution, subs_str, iterations):

    if iterations == 0:
        return subs_str
    
    if len(subs_str) <= 1:
        return None
    p = re.compile("01")
    indexes = [m.start(0) for m in p.finditer(subs_str)]

    i = 0
    ab_s_replaced = 0
    reversed_subs_str = ""
    if len(indexes) == 0:
        reversed_subs_str += "0"*len(subs_str)
        return reverse_substitution(substitution, reversed_subs_str, iterations - 1)

    while(i < len(subs_str)):
        if ab_s_replaced == len(indexes):
            reversed_subs_str += "1"*len(subs_str[i:])
            break
        if indexes[ab_s_replaced] == i:
            reversed_subs_str += "0"
            i += 2
            ab_s_replaced += 1
        else:
            reversed_subs_str += "1"
            i += 1

    return reverse_substitution(substitution, reversed_subs_str, iterations - 1)



def encrypt(message, substitution, iterations = 5, padding = ""):
    if DEBUG:
        print(f"message: {message}")
    
    message = padding + message

    #put string into binary
    binary_message = ""
    for char in message:
        binary_message += bin(ord(char))[2:].zfill(8)

    if DEBUG:
        print(f"binary message: {binary_message}")

    if DEBUG:
        print(f"substitution: {substitution}")

    #encrypt
    encrypted_message = Substitution(substitution, binary_message, iterations)
    if DEBUG:
        print(f"encrypted message: {encrypted_message}")

    return encrypted_message


def decrypt(message, substitution, iterations, padding = ""):
    #return string from binary
        
    #decrypt
    decrypted_message = reverse_substitution("none", message, iterations)
    if DEBUG: 
        print(f"reversed subsitution {iterations} times: {decrypted_message}")

    #return string from binary
    decrypted_message = "".join([chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8)])
    if DEBUG:
        print(f"decrypted message: {decrypted_message}")

    #remove padding
    decrypted_message = decrypted_message[len(padding):]
    if DEBUG:
        print(f"decrypted message without padding: {decrypted_message}")
    return decrypted_message




def test_1():
    print("test 1:")

    # #create fibbonacci substitution of depth 5
    # fib = Substitution(standardSubs[0][1], "a", 5)
    # print(f"standard substitution: {fib}")
    # #print the substitution
    # rev = reverse_substitution(fib)
    # print(f"reversed substitution: {rev}")
    

    test_list = []
    for i in range(10):
        test_list.append(Substitution(standardSubs[0][1], "a", i))
    test_list.reverse()

    for i in range(10):
        print(f"standard substitution {i}:", test_list[i])
        print(f"reversed substitution {i}:", reverse_substitution("none", test_list[i], 1))
    
    print("test 1 complete\n")


def test_2():
    print("test 2:")
    #create fibbonacci substitution of depth 5
    fib = Substitution(standardSubs[0][1], "bbbbaaabbbb", 5)
    print(f"standard substitution: {fib}")
    #print the substitution
    rev = reverse_substitution("none", fib, 5)
    print(f"reversed substitution: {rev}")
    print("test 2 complete\n")



def test_3():
    print("test 3:")

    message = "hello"
    fib_sub_binary = {"0": "01", "1": "0"}
    encrypted_message = encrypt(message, fib_sub_binary, 2)
    decrypted_message = decrypt(encrypted_message, fib_sub_binary, 2)
    print("test 3 complete\n")

def test_4():
    print("test 4:")

    message = "mayo moose"
    fib_sub_binary = {"0": "01", "1": "0"}
    padding = ""



    encrypted_message = encrypt(message, fib_sub_binary, 2, padding)
    # print(f"encrypted message: {encrypted_message}")
    decrypted_message = decrypt(encrypted_message, fib_sub_binary, 2, padding)
    # print(f"decrypted message: {decrypted_message}")
    print("test 4 complete\n")

if __name__ == "__main__": 
    # test_1()
    # test_2()
    # test_3()
    test_4()