
# Count Even and Odd Numbers
# Take a list of numbers as input (comma-separated).
# Count how many are even and how many are odd.

numbers=input("Enter some random numbers separated by comma:")
num_list=numbers.split(',')
even_count=0
odd_count=0

for num in num_list:
    if int(num)%2==0:
        even_count +=1
    else:
        odd_count +=1
print("even count=",even_count)
print("odd count=",odd_count)

