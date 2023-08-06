from math import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot



def convert(string):
  li = list(string.split(" "))
  li.remove('x')
  li = list(map(int, li)) 
  return li


class Show:
    def __init__(self,plot1):

      self.plot1 = plot1
      plot1 == 'plot'
      plot1 = plt.show()
      


def coef_calc(x,y,function):
  delta = lambda alpha, alpha2 : alpha - alpha2
  result1 = (delta(x, x+1))
  x = x + 1
  y2 = eval(function)
  result2 = y - y2
  plt.xlabel("Coeficiente Angular = {}".format(result2/result1))

  
  
  
  for i,type in enumerate(data):
    f = coord_x[i]
    g = coord_y[i]
    plt.scatter(f, g, marker='s', color='blue')
    plt.text(f+0.1, g+0.1, type, fontsize=9)
    
   
#coord_x = []
#coord_y = []
#data = []

def word(mylist, function):
    try:
        plt.title(function)
        x = mylist[0]   
        y = eval(function)      
        output = x
        output2 = y
        output3 = x,y
        coord_x.append(output)
        coord_y.append(output2)
        data.append(output3)
        del mylist[0]
        return word(mylist, function)
    except:
       
        #print("Função Terminada")
        mylist.clear()
        
        coef_calc(x,y,function)
      
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

