#!/usr/bin/env python3
import time

""" 
Multiple lines string
"""
s = """
<html>
<body>
Hello World
</body>
</html>
"""

print(s)


x = "good"
while True:

  try:
    print(x)
  except:
    print("something is wrong")
    exit(1)
  
  x = "Good"
  print(x)
  
  time.sleep(2) 
  
exit(0)
