from unstdio.unstdio import Unstdio

with Unstdio() as unstdio:
    print("Hello World!")  # out to Unstdio instance
print(unstdio.stdout.get_value())  # out to system stdout
