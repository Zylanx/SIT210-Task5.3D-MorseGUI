from morse import MorseCode

assert MorseCode._generate_encoded_message("The quick brown fox jumped over the lazy dog") == \
       "-/..../. --.-/..-/../-.-./-.- -.../.-./---/.--/-. ..-./---/-..- .---/..-/--/.--././-.. ---/...-/./.-. -/..../. .-../.-/--../-.-- -../---/--."