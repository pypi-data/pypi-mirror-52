import random


class GMX(object):

    def __init__(self, subject):
        self.subject = [str(x) for x in subject]

    def play(self, rounds):
        goal_index = random.randint(0, len(self.subject) - 1)
        num_guesses = 0

        while num_guesses < rounds:
            selection = input("Your guess: ")
            selection_index = self.subject.index(selection)

            if selection_index < goal_index:
                print("Too low.")
            elif selection_index > goal_index:
                print("Too high.")
            else:
                break

            num_guesses += 1

        if selection_index == goal_index:
            print("You got it!")
        else:
            print("You've lost!")



