import requests 
  
def request(command):

# api-endpoint 
    URL = "http://192.168.43.218:5000/lego"
  
# definfing a body for request
    data = '{\n\t"request":"' + command + '"\n}' 
  
# sending post request
    r = requests.request(method = 'post', url = URL, data = data) 
  
# extracting data in json format 
    data = r.json() 

    print(data)
