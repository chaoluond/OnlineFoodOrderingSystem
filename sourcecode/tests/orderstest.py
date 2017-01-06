import requests
s = requests.Session()
host='http://ec2-54-88-148-235.compute-1.amazonaws.com/'   #  replace by your host here
s.headers.update({'Accept': 'application/json'})
data = [1]
# Test /orders GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

# Test /orders PUT method
r = s.put('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders?userID=1')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)



# Test /orders/{orderID} GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders/1')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

# Test /orders/{orderID} DELETE method
r = s.delete('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders/1')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())


# Test /orders/{orderID}/orderitems/1 GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders/1/orderitmes/1')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

# Test /orders/{orderID}/orderitems/1 DELETE method
r = s.delete('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders/1/orderitmes/1')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

# Test /orders/{orderID}/orderitems/1 PUT method
r = s.put('http://ec2-54-88-148-235.compute-1.amazonaws.com/orders/1/orderitmes/1')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

