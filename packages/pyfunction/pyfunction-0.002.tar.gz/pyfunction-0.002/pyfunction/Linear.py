from math import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot




class Linear:
    def __init__(self,scale,user_enter):
      self.scale = scale
      self.user_enter = user_enter

      mylist = []
      a = (convert(self.scale)) 
     
      for i in range(a[1],a[0], -1):  
          mylist.append(i)
      function = self.user_enter

      global coord_x
      global coord_y
      global data
      coord_x = []
      coord_y = []
      data = []

	    
      word(mylist, function)      

