# file = open("hello.txt", "w")
# file = open("hello.txt", "r")
# file = open("hello.txt", "a")

# file.write("My name is Ahmad")
# print(file.read())
# file.write("\nI am learning file_handling")

# file.close()

# with open("hello.txt", "r") as file:
#     print(file.read())

with open("dolphine.jpg", "rb") as source:
    image_data = source.read()

with open("copy.jpg", "wb") as destination:
    destination.write(image_data)

print("Image copied")