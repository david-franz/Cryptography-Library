from collections import Counter
import json, string, time, re

class Kryptos:

    letter_frequency_table = [
        'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 
        'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']

    alphabet = {}
    n = None

    def __init__(self, alphabet_string):
        n = 0
        for c in alphabet_string:
            if c == ' ': self.letter_frequency_table.insert(0, ' ')
            self.alphabet[c] = n
            n += 1

        self.n = n


    ########
    # misc #
    ########

    def find_character_from_number(self, n):
        for c in self.alphabet.keys():
            if(self.alphabet[c] == n): return c

        raise Exception


    ############# 
    # frequency #
    #############

    def build_swap_table(self, letter_frequencies):
        swap_table = {}
        
        index = 0
        for c in letter_frequencies.keys():
            print(self.letter_frequency_table[index])
            swap_table[c] = self.letter_frequency_table[index]
            index += 1
        
        return swap_table

    def sub_letter_frequency(self, encrypted_string, spaces_included = False):
        if type(spaces_included) is not bool: raise Exception
        if spaces_included and ' ' not in self.alphabet: self.letter_frequency_table.insert(0, ' ')
        
        letter_frequencies = Counter(encrypted_string)
        swap_table = self.build_swap_table(letter_frequencies)

        decrypted_string = []
        for c in encrypted_string:
            decrypted_string.append(swap_table[c])

        return ''.join(decrypted_string)


    ########## 
    # caeser #
    ##########

    def caeser_encrypt_string(self, plaintext, displacement):
        encrypted_string = []

        for c in plaintext:
            n_plaintext = self.alphabet[c]
            n_encrypted = (n_plaintext + displacement) % self.n
            c_encrypted = self.find_character_from_number(n_encrypted)
            encrypted_string.append(c_encrypted)
        
        return ''.join(encrypted_string)

    def caeser_decrypt_string(self, encrypted_string, displacement):
        plaintext = []
        
        for c in encrypted_string:
            n_encrypted = self.alphabet[c]
            n_decrypted = (n_encrypted - displacement) % self.n
            c_decrypted = self.find_character_from_number(n_decrypted)
            plaintext.append(c_decrypted)

        return ''.join(plaintext)


    ##########
    # affine #
    ##########

    def find_affine_decryption_function(self, a, b):
        a_inverse = None
        for i in range(self.n):
            if(a * i % self.n == 1):
                a_inverse = i

        if a_inverse == None: raise Exception

        return lambda f_x : a_inverse * (f_x + b) % self.n

    # test if all plaintext chracters in alphabet
    def affine_encrypt_string(self, plaintext, a, b):
        if plaintext == None or a == None or b == None: raise Exception

        '''
        for c in plaintext:
            if c not in self.alphabet:
                self.alphabet[c] = self.n
                self.n += 1

        self.n = len(self.alphabet)

        print(self.n)
        print(self.alphabet)
        '''
        
        plaintext = plaintext.strip("\n")
        plaintext = re.sub(r'[^\w\s]', '', plaintext)

        #plaintext = plaintext.translate(str.maketrans('', '', string.punctuation))

        encryption_function = lambda x : (a * x + b) % self.n

        encrypted_string = []
        for c in plaintext:
            if c is '\n':
                continue

            n_plaintext = self.alphabet[c]
            n_encrypted = encryption_function(n_plaintext)
            c_encrypted = self.find_character_from_number(n_encrypted)
            encrypted_string.append(c_encrypted)

        return ''.join(encrypted_string)

    # test if all plaintext chracters in alphabet
    def affine_decrypt_string(self, encrypted_string, a, b):
        if encrypted_string is None or a is None or b is None: raise Exception

        decryption_function = self.find_affine_decryption_function(a, b)

        plaintext = []
        for c in encrypted_string:
            n_encrypted = self.alphabet[c] 
            n_decrypted = decryption_function(n_encrypted)
            c_decrypted = self.find_character_from_number(n_decrypted)
            plaintext.append(c_decrypted)

        return ''.join(plaintext)


# k = Kryptos(" abcdefghijklmnopqrstuvwxyz")

'''
with open('oldmanandthesea.txt') as f:
    plaintext = f.read()

plaintext = plaintext.lower()

encrypted_string = k.affine_encrypt_string(plaintext, 7, 5)

f = open('output.txt', 'w')

f.write(k.sub_letter_frequency(encrypted_string))

f.close()
'''