# tokendb
First write a token generator that creates a file with 10 million random tokens, one per line, each consisting of seven lowercase letters a-z. 

Then write a token reader that reads the file and stores the tokens in your DB. 

Naturally some tokens will occur more than once, so take care that these aren't duplicated in the DB, but do produce a list of all non-unique tokens and their frequencies. 

Find a clever way to do it efficiently in terms of network I/O, memory, and time and include documentation inline with your code or as txt file, describing your design decisions. 
