import requests 
  
# api-endpoint 
URL = "http://127.0.0.1:5000/lego"
  
# definfing a body for request
data = '{\n\t"request": "north"\n}' 
  
# sending post request
r = requests.request(method = 'post', url = URL, data = data) 
  
# extracting data in json format 
data = r.json() 

print(data)