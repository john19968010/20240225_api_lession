class Animal:
    def __init__(self):
        self.legs = 4
        self.eyes = 2

    def eat(self):
        print("i am eating.")


class Dog(Animal):

    def __init__(self):
        super().__init__()
        self.tail = 1

    def eat(self):
        # super().eat()
        print("i am eating dog food.")

    def barking(self):
        print("WOW")


class GoldenRetriever(Dog):
    def __init__(self):
        super().__init__()
        self.hair = "golden"

    def eat(self):
        super(Dog, self).eat()
        print("i am eating golden retriever food.")

    def barking(self):
        print("WOW WOW")


if __name__ == "__main__":
    john = GoldenRetriever()
    john.eat()
    # print(f"hair: {john.hair}")
    # print(f"tail: {john.tail}")
    # print(f"legs: {john.legs}")
    # print(f"eyes: {john.eyes}")
