import base64

x = "Siała baba mak"
print(x)
y = base64.b64encode(bytes(x,"utf-8"))
print(y)
z  = str(base64.b64decode(y)).format("utf-8")
print(z)
