# Encryption machine
This repository contains a machine than can be used to encode, decode or hack texts given to it.
## Functional
	This machine is able to work only with caesar and vigenere cipher, and hack option for text is available only for caesar cipher.
## Encoding
	to encode text use this command:
	$ ./encryptor.py encode --cipher {caesar|vigenere} --key {<number>|<word>} [--input-file input.txt] [--output-file output.txt]
## Decoding
	to decode text use this:
	$ ./encryptor.py decode --cipher {caesar|vigenere} --key {<number>|<word>} [--input-file input.txt] [--output-file output.txt]
## Hacking
	First of all, to hack text you need to train a programm:
	$ ./encryptor.py train --text-file {input.txt} --model-file {model}
	where input file is a normal text, and a model file will contain statistics.
	This code uses frequency analysis to hack caesar cipher, that is why this training is 
	needed. After this, to hack text, use a command below:
	$ ./encryptor.py hack [--input-file input.txt] [--output-file output.txt] --model-file {model}
	This programm supports russian and english languages.

