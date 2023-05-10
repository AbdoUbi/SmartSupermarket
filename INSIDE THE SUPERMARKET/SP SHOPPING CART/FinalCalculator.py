import os

total = 0
file_path = "./INSIDE THE SUPERMARKET/SP SHOPPING CART/"

try:
    with open("./INSIDE THE SUPERMARKET/FinalTotalCost.txt", "w") as recript:
        recript.write("SHOPPING RECEIPT\n")
        for file in os.listdir(file_path):
            if file.endswith(".txt"):
                try:
                    with open(os.path.join(file_path, file), "r") as items:
                        for line in items:
                            line = line.strip().split(",")
                            try:
                                total += float(line[1])
                                recript.write("Item: " + line[0] + " - Price: " + line[1] + "\n")
                            except ValueError:
                                print("Invalid price value found in file: ", file)
                        recript.write("---------\n")
                        recript.write("Total: " + str(total) + "\n")
                        recript.write("Have a nice day")
                except IOError:
                    print("Error occurred while opening file: ", file)
except IOError:
    print("Error occurred while writing to FinalTotalCost.txt")