<h1 align="center">Hash Cracker</h1>
<p align="center">
    <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.7-green.svg">
  </a>
  <a href="https://github.com/yamenBayer/hash_cracker">
    <img src="https://img.shields.io/badge/Release-1.0-blue.svg">
  </a>
    <a href="https://github.com/yamenBayer/hash_cracker">
    <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-brightgreen.svg">
  </a>
</p>


<p align="center">
  Advanced hash Cracker/Decoder/Decryptor written in Python 3
</p>


## Disclaimer

THIS CRACKER WAS CREATED ONLY FOR WHITE HUCKERS TO HELP THEM TEST THE SYSTEMS AND ALGORITHMS, OR IT COULD INJECTED ON KEY TRANFERING SYSTEM.


THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

## Features
- Works on Windows/Linux/OSx etc which supports Python 3
- Advanced, Lightweight, Easy to use
- Based on Advanced-BruteForce Technique
- Shows total attempts made by Cracker
- Automatically Stops the Script When Correct Password is Found
- Includes two techniques, one with advanced brute force (generate advanced wordlist), and the other with given wordlist as txt

## Prerequisite
- [x] Python 3.X  

## How To Use
```bash
# Install dependencies 
$ pip install latest python 3.x

# Clone this repository
$ git clone https://github.com/yamenBayer/hash_cracker.git

# Go into the repository
$ cd hash_cracker

# Getting Help Menu
$ python hash_cracker.py --help

# Cracking MD5 Hash Without saving Result
$ python hash_cracker.py -ha <Hash> -c <no. of cores>
$ Note: no. of cores must be equal or lower than the available cores in your system.

# Cracking Example
$ python hash_cracker.py -ha c1a5298f939e87e8f962a5edfc206918 -c 6
```

### Note : Procedure for cracking is same in all OS, and the maximum time around half hour and maximum word length supported is 4


## Contributors:
All contributor's pull request will be accepted if their pull request is worthy for this repo.


## Contact 
yamen.warss@gmail.com
