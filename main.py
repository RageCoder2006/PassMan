import functions

# logics

print("=================================PassMan=================================")
print(f'                             Welcome toPassMan                          ')

print("Do you have an existing account?(y/n) [if not, you'll be redirected to signup :)]  ")
ask = input(">>>")
ask = ask.lower()

if ask in functions.yes:
    functions.login()
    functions.app()

elif ask == "":
    functions.login()
    functions.app()

else:
    functions.signup()
    functions.login()
    functions.app()
