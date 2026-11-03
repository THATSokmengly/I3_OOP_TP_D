print("Exercise : A ")
print("\n")
rectangle_height = 6
rectangle_width = 25

for i in range (rectangle_height):
    if i == 0 or i == rectangle_height-1:
        print("*" * rectangle_width)
    else :
        print("*" + " " * (rectangle_width-2) + "*")

    
    