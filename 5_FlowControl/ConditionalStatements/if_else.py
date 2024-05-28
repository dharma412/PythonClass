# Print the student results based on marks. write a code.
# when marks are eqal and less to 35 print failed
# if marks aremore than 35 and below 50 print passed with C grade
# 51 to 69 b grade
# 70 89 A grade
#90 to 100 A+
marks=389
if marks<100:
    if marks<35:
        print("I am failed")
    elif 50<=marks>=35:
        print("I am passed but C garde")
    elif 51<=marks>=69:
        print("I am passed but with B garde")
    elif 89<=marks>=70:
        print("I am passed but with A grade")
    elif 100<=marks>=90:
        print("I am passed with A+")
else:
    print("give propernumermarks below 100")