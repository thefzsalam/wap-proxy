#http://wotd.rocks/new_tab/getWotdFeed.php
# date,definition,doYouKnow,examples,pronounce,title,type
import requests
class Wotd:
    """ Get the word of the day from a web service """

    def get():
        """
            Returns {
                        title       : "The word"
                        type        : "Noun,verb,etc"
                        pronounce   : "how to pronounce"
                        definition  : "The definition"
                        examples    : "example usage"
                        doYouKnow   : "some facts like etymology"
                        date        : "date of wotd"
                    }
        """
        r = requests.get('http://wotd.rocks/new_tab/getWotdFeed.php')
        return r.json()[0]
