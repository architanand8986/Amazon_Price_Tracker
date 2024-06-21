import matplotlib.pyplot as plt
import numpy as np

# don't obstruct while loading the graph else the main thread would come out of the main loop
# objective of file is for data visualisation
# the user would be given access to graphical information after 3 trackings

def check(date):
    i=0
    
    for d in date:
        if(d[0]=="d"):
            break
        else:
            
            i+=1
    
    return i
    
    
    
async def plot(dict,curr="₹"):
    
    nd=[]
    npr=[]
    
    for i in dict:
        
        nd.append(i['date'])
        i['price']=i['price'].replace(",","")
        npr.append(float(i['price']))
                
    fig=plt.figure()
    fig,ax=plt.subplots()
    
    
    avg=np.mean(npr)
    median=np.median(npr)
    
    
    line1=ax.plot(nd, npr,"g-o",
            label="Price",
            linewidth="2")
    
    line2=ax.axhline(y=avg,
            label="Average",
            color="red",
            linewidth="2",
            linestyle=':')
    
    line3=ax.axhline(y=median,
            label="Median",
            color="orange",
            linewidth="2",
            linestyle="dashed"
            )
    
    ax.set_title("Price Activity")
    ax.set_xlabel("Date:(DD/MM/YYYY)")
    ax.set_ylabel(f"Price:({curr})")
    ax.tick_params(axis='x', labelsize=8+(7-len(dict)))
    
    plt.legend(["Price","Mean_Price","Median_Price"],loc="upper right")
   
    plt.show()
    
   
     
    
    
   


if __name__=="__main__":
    l1=["0","3","4"]
    l2=["5","6","8"]
 
    plot(l1,l2,"$")