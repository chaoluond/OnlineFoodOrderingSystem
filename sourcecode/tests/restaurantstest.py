import requests
s = requests.Session()
host='http://ec2-54-88-148-235.compute-1.amazonaws.com/'   #  replace by your host here
s.headers.update({'Accept': 'application/json'})

# Test /restaurants GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants')
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

# Test /restaurants POST method
r = s.post('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)



# Test /restaurants/{restID} GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID} PUT method
r = s.put('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID} DELETE method
r = s.delete('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)



# Test /restaurants/{restID}/menus GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())
# Test /restaurants/{restID}/menus POST method
r = s.post('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)



# Test /restaurants/{restID}/menus/{menuID} GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID}/menus/{menuID} PUT method
r = s.put('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID}/menus/{menuID} DELETE method
r = s.delete('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)




# Test /restaurants/{restID}/menus/{menuID}/categories GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())
# Test /restaurants/{restID}/menus/{menuID}/categories POST method
r = s.post('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)



# Test /restaurants/{restID}/menus/{menuID}/categories/{catID} POST method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID}/menus/{menuID}/categories/{catID} PUT method
r = s.put('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID}/menus/{menuID}/categories/{catID} DELETE method
r = s.delete('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)




# Test /restaurants/{restID}/menus/{menuID}/categories/{catID}/items GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2/items')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())
# Test /restaurants/{restID}/menus/{menuID}/categories/{catID}/items POST method
r = s.post('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2/items')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)




# Test /restaurants/{restID}/menus/{menuID}/categories/{catID}/items/{itemID} GET method
r = s.get('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2/items/1149')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID}/menus/{menuID}/categories/{catID}/items/{itemID} PUT method
r = s.put('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2/items/1149')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)
# Test /restaurants/{restID}/menus/{menuID}/categories/{catID}/items/{itemID} DELETE  method
r = s.delete('http://ec2-54-88-148-235.compute-1.amazonaws.com/restaurants/7009c6cc1083e4c6b3dd/menus/27/categories/2/items/1149')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)

