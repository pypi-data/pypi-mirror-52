import numpy

class HelloWorld():

  def __init__(self, my_string = "hello world!"):
    self.__message_to_sent = my_string
    self.__getmessage__()

    
  def __getmessage__(self):
    return self.__message_to_sent
