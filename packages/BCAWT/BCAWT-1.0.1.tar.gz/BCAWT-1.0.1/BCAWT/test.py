import glob

path = "/home/ali/python_pkg/BCAWT pkg/test"
print (f"{path}/*.txt")
text = [ i for i in glob.glob(f"{path}/*.txt")]

print (text)