from sklearn import datasets

def helloworld():
    iris = datasets.load_iris() # just testing that sklearn works
    print("sklearn installed and working correctly: hello, world!")
