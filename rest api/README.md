Instructions
============

In whatever language you like, as simple or as complex as you like, write a small daemon that will:

* Start listening on a HTTP or HTTPS port

--------- put into the word/WORDNAME db

* Accept PUT requests to /word/WORDNAME, with the body of the request being a JSON hash specifying a single word

    { "word": "ONE_WORD" }
--- test add single word
--- test add nonstandard characters


 * Return a HTTP error code and JSON hash when the request is not one word in length:

    { "error": "PUT requests must be one word in length" }
---- add more than one words 

 * Store a running count of all words that have been sent to it

  * E.g. "word COUNT has been sent 5 times", "word ROFFLE has been sent 8 times", etc
---- on a per word basis

* Accept GET requests to /words/WORDNAME
 * Return the integer count of how many times that word has been PUT to the api in a JSON hash

    { "WORDNAME": INTEGER_COUNT }
--- 

* Accept GET requests to /words
 * Return a JSON hash listing the count of every word

    {
       "WORDNAME": INTEGER_COUNT,
       "WORDNAME2": INTEGER_COUNT,
       "WORDNAME3": INTEGER_COUNT
    }

