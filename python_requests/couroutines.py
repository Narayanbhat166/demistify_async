def fun():
    print("Hello, World!")
    yield
    print("Goodbye, World!")
    yield


fun_call = fun()
next(fun_call)
print("Awesome World!")
next(fun_call)
