import hashlib
import itertools
import os
import threading
import time
import argparse

#####################################################################################################
########################################## Global Variables #########################################
#####################################################################################################
wordlist = []
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=~'
flag = False
lengths = []
threads = []
speed = 1
cores_used = 1
wordlist_file = ''
#####################################################################################################
#####################################################################################################
#####################################################################################################

#####################################################################################################
############################################# Functions #############################################
#####################################################################################################
class ThreadWithResult(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = None

    def run(self):
        self._result = self._target(*self._args)

    def result(self):
        return self._result
    
def get_lengths(length, cores):
    global lengths
    lengths = []
    for n in range(0, cores):
        if n == cores-1 and (length - ((int(length/cores))*cores)) > 0:
            value = int(length/cores) + (length - ((int(length/cores))*cores)) + lengths[n-1]
        elif n!=0: 
            value = int(length/cores) + lengths[n-1]
        else:
            value = int(length/cores)

        lengths.append(value) 

def generate_wordlist(length):
    global wordlist
    

    combinations = itertools.product(alphabet, repeat=length)
    for combination in combinations:
        word = ''.join(combination)
        wordlist.append(word)


def process(len1, len2, hash):
    total_words_checked = 0  # Counter for the number of words checked
    duration_threshold = 1.0

    for i in range(len1, len2):
        total_words_checked += 1
        
        global flag, speed
        if flag == False:
            elapsed_time = time.time() - start_time
            if elapsed_time >= duration_threshold :
                speed = total_words_checked
                flag = True

        word = wordlist[i]
        hashes = []
        
        hashes.extend([hashlib.md5(word.encode()).hexdigest(), hashlib.sha1(word.encode()).hexdigest(), hashlib.sha224(word.encode()).hexdigest(), hashlib.sha256(word.encode()).hexdigest(), hashlib.sha384(word.encode()).hexdigest(), hashlib.sha512(word.encode()).hexdigest()])
        if hash in hashes:
            if flag == False:
                speed = total_words_checked - 1
            return word
        
        
        # Display the counter dynamically
        print(f"Words checked: {total_words_checked}", end="\r", flush=True)

    return None

def load_wordlist(value):
    global wordlist
    global wordlist_file
    wordlist_file = value

    with open(wordlist_file, 'r') as file:
        wordlist = [line.strip() for line in file]

def crack_hash(hash_to_crack, max_length, cores_num):
    
    for length in range(1, max_length+1):
        generate_wordlist(length)
        print("Iteration "+ str(length) + " processing...")
        words_len = len(wordlist)

        get_lengths(words_len, cores_num)

        global threads
        threads = []
        if length > 3:
            old_min = 0
            for n in range(0, cores_num):
                t = ThreadWithResult(target=process, args = (old_min, lengths[n], hash_to_crack))
                old_min = lengths[n]
                threads.append(t)
                t.start()

        else:
            t = ThreadWithResult(target=process, args = (0, words_len, hash_to_crack))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()

        for t in threads:
            if t.result() is not None:
                return t.result()

    return None

def crack_hash_with_wordlist(hash, cores_num):
    global hash_to_crack
    hash_to_crack = hash

    words_len = len(wordlist)
    get_lengths(words_len, cores_num)

    global threads
    threads = []
    old_min = 0
    for n in range(cores_num):
        t = ThreadWithResult(target=process, args=(old_min, lengths[n],hash_to_crack))
        old_min = lengths[n]
        threads.append(t)
        t.start()
    

    for t in threads:
        t.join()

    for t in threads:
        if t.result() is not None:
            return t.result()

    return None
#####################################################################################################
#####################################################################################################
#####################################################################################################


#####################################################################################################
############################################### Main ################################################
#####################################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hash Cracker')
    parser.add_argument('-ha', '--hash', type=str, help='Hash to crack')
    parser.add_argument('-c', '--cores', type=int, default=1, help='Number of processor cores to use')
    parser.add_argument('-th', '--to-hash', type=str, help='Word to hash')
    parser.add_argument('-m', '--method', choices=['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'], default='md5', help='Hashing algorithm method to use')
    parser.add_argument('-w', '--wordlist', dest='wordlist', metavar='WORDLIST',help='Path to the wordlist file')
    args = parser.parse_args()


    if args.to_hash:
        word = args.to_hash
        method = args.method.lower()
        if method == 'md5':
            hash_value = hashlib.md5(word.encode()).hexdigest()
        elif method == 'sha1':
            hash_value = hashlib.sha1(word.encode()).hexdigest()
        elif method == 'sha224':
            hash_value = hashlib.sha224(word.encode()).hexdigest()
        elif method == 'sha256':
            hash_value = hashlib.sha256(word.encode()).hexdigest()
        elif method == 'sha384':
            hash_value = hashlib.sha384(word.encode()).hexdigest()
        elif method == 'sha512':
            hash_value = hashlib.sha512(word.encode()).hexdigest()
        else:
            print('Invalid hashing algorithm')
            exit(1)

        print(f"{method.upper()} hash for '{word}': {hash_value}")

    else:
        hash = args.hash
        max_length = 4  # Maximum word length to try
        cores_num = args.cores

        num_cores = os.cpu_count()
        print("-----------------------------------------------")
        print("Number of available processor cores:", num_cores)
        if (cores_num > num_cores):
            avb_cores = num_cores
            print("Number of processor cores used by this code:", avb_cores)
        elif (cores_num < 0):
            avb_cores = 1
            print("Number of processor cores used by this code:", avb_cores)
        else:
            avb_cores = int(cores_num)
            print("Number of processor cores used by this code:", avb_cores)
        print("-----------------------------------------------\n")
        start_time = time.time()

        if args.wordlist:
            load_wordlist(args.wordlist)
            cracked_password = crack_hash_with_wordlist(hash, avb_cores)
        else:
            cracked_password = crack_hash(hash, 5, avb_cores)

        if cracked_password:
            print("\n")
            print(f"-> Hash cracked! The orginal word is: {cracked_password}")
        else:
            print("\nPassword not found in the wordlist.")

        end_time = time.time()
        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        # Format the elapsed time as hours:minutes:seconds
        elapsed_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        print("\n-----------------------------------------------")
        print("Elapsed time:", elapsed_time_formatted)
        print("Code Speed:", speed, "words per second")
        print("-----------------------------------------------")
#####################################################################################################
#####################################################################################################
#####################################################################################################
