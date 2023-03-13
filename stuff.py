my_dict = dict()

my_dict["stuff"] = 1
my_dict["what"] = 7
my_dict["hell"] = -1

for k, v in sorted(my_dict.items(), key= lambda item: item[0]):
    print(k, v)
