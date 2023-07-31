from manim import *
from subsitution_encryption import *
from Substitution import *


class Substituion_Cipher(Scene):
    def construct(self):
        text = Text("Substitution Cipher", font="Arial", color=WHITE).scale(1.5)
        self.play(Write(text))
        self.wait(1)
        self.play(FadeOut(text))
        self.wait(1)


        initial_message = "Hello"
        initial_message_text = Text(initial_message, font="Arial", color=WHITE).scale(1.5)
        self.play(Write(initial_message_text))
        self.wait(1)

        binary_message = ""
        for char in initial_message:
            binary_message += bin(ord(char))[2:].zfill(8)
        binary_message_text = Text(binary_message, font="Arial", color=WHITE).scale(0.5)
        self.play(Transform(initial_message_text, binary_message_text))
        self.wait(1)

        #replace 0s and 1s with a and b
        binary_message = binary_message.replace("0", "a")
        binary_message = binary_message.replace("1", "b")
        binary_message_text = Text(binary_message, font="Arial", color=WHITE).scale(0.5)
        self.play(Transform(initial_message_text, binary_message_text))
        self.wait(1)

        #encrypt

        iterations = 3
        for i in range(iterations):
            binary_message = Substitution(standardSubs[0][1], binary_message, 1)
            binary_message_text = Text(binary_message, font="Arial", color=WHITE).scale(0.5/(1.61**i))
            self.play(Transform(initial_message_text, binary_message_text))
            self.wait(1)









        # fib = Substitution(standardSubs[0][1], "a", 5)
        # fib_text = Text(fib, font="Arial", color=WHITE).scale(1.5)
        # # print(f"standard substitution: {fib}")
        # self.play(Write(fib_text))
        # self.wait(1)

        # rev = reverse_substitution("none", fib, 1)
        # rev_text = Text(rev, font="Arial", color=WHITE).scale(1.5)
        # #transform into reversed substitution
        # self.play(Transform(fib_text, rev_text))

        # self.play(Write(text))


        # self.play(Write(fib))
        
