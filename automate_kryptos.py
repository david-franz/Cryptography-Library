import json, string 

from kryptos import Kryptos

class AutomatedKryptos:
    
    kryptos = None
    english_dictionary = list(json.loads(open('dict.json').read()))


    def __init__(self, kryptos):
        if type(kryptos) != Kryptos: raise Exception
        self.kryptos = kryptos


    def caeser_try_all(self, encrypted_string):
        return self.try_all(encrypted_string, k.caeser_decrypt_string)


    def try_all(self, encrypted_string, decryption_function):
        best_guess_of_displacement = [0, float('-inf')]

        for i in range(self.kryptos.n):
            words = []

            decrypted_guess = decryption_function(encrypted_string, i)
            decrypted_guess = ''.join(decrypted_guess.split()) # remove spaces
            # decrypted_guess = decrypted_guess.translate(str.maketrans('', '', string.punctuation)) # remove punctuation

            for word in self.english_dictionary:
                if word in decrypted_guess:
                    words.append(word)

            if len(words) > best_guess_of_displacement[1]:
                best_guess_of_displacement[0] = i
                best_guess_of_displacement[1] = len(words)

        return decryption_function(encrypted_string, best_guess_of_displacement[0])
