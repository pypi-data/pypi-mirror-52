# Seperator  
### Usage Samples:  
  
```python3  
from seperator.lines import line  
  
line()  
line("Hello World")  
line("Hello World",width=80)  
line("Hello World",char='*')  
line("Hello World",color='red')  
line("Hello World",align=5)  
line("Hello World",align=-5)  
line("Hello World",margin=(5,5))  
```  
```
--------------------------------------------------------------------------------
- Hello World ------------------------------------------------------------------
- Hello World ------------------------------------                         
* Hello World ******************************************************************  
- Hello World ------------------------------------------------------------------
----- Hello World --------------------------------------------------------------
-------------------------------------------------------------- Hello World -----
-     Hello World     ----------------------------------------------------------
```


```
from seperator.lines import dateline  
# you cannot additional
# info but other parameters are same with line
dateline()
```

