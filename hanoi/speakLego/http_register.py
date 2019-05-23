import requests 

def register():

  
# api-endpoint 
    URL = "http://192.168.43.218:5000/lego/register"
  
# definfing a body for request
    data = '{\n\t"name": "user2"\n}' 
  
# sending post request
    r = requests.request(method = 'post', url = URL, data = data) 
  
# extracting data in json format 
    data = r.json() 

    print(data)