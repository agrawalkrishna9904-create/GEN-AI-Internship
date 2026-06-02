# Q1: 
# Write a Python program that:
# Accepts a paragraph from the user.
# Converts text to lowercase.
# Removes punctuation.# Counts:
# Total characters,# Total words,# Total vowels
# Displays the frequency of each word.

str=input("Write a paragraph:")
print("you entered the paragraph:",str)

#vowels
vowels="aeiou"
print("Lowercase string is :",str.lower())
vowel_count=0
for ch in str.lower():
    if ch in vowels:
        vowel_count+=1
print("Number of vowels are:",vowel_count)

#Lowercase conversion
print("Lowercase string is :",str.lower())

#Remove punctuation
import string
words_clean=''.join(char for char in str if char not in string.punctuation)
print("Text after removing Punctuation:", words_clean)

#word count
words=str.split()
str1=len(words)
print(words)
print(str1)

#Frequency
frequency={word: words.count(word)
           for word in words}
print(frequency)








