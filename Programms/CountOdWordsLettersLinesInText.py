def counter(str1):
    num_words=0
    num_lines=0
    num_charc=0
    num_space=0

    with open('Files/Files.txt', "r") as file:
         for line in file:
             num_lines=num_lines+1

             for letters in line:
                 if (letters!=' '):
                     print(letters)

