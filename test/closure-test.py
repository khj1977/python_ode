def closure_test(x):
    y = 1
    foo = lambda z: z + y

    return foo
    

func = closure_test(2)
r = func(4)

print(r)