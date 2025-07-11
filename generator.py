
# here all the value from the 0 to 200 will be stored in a memory. 
def creater(): 
    listValue = []; 
    i = 1; 

    while i <= 200:
        listValue.append(i)
        i += 1

    return listValue

print(creater())


# Here the value will be generated one by one and it will not store all the value in a memory.
# This is called generator function. 
# It will generate the value one by one and it will not store all the value in a memory.
# It will save memory and it will be faster than the creater function.
# It is also called lazy evaluation.
def generator_create(): 
    i = 1; 

    while i <= 200: 
        yield i; 
        i += 1; 


generator_value = generator_create(); 

print(next(generator_value));
print(next(generator_value));  