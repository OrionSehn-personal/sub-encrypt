from manim import *
from subsitution_encryption import *
from Substitution import *

class Substituion_Cipher(Scene):
    def construct(self):
        title = Title("Substitution Cipher")
        self.play(Write(title))
        # self.wait(1)
        # self.play(FadeOut(title))
        # self.wait(1)

        message = "Hey!"
        message_text = Text(message)
        self.play(Write(message_text))
        # self.wait(2)

        # self.play(message_text.animate.shift(DOWN))


        explain_text = "Encoding: Convert message to Binary"
        explain_text = Text(explain_text).scale(0.50).shift(UP*2)
        self.play(Write(explain_text))

        self.wait(2)


        # Convert message to binary


        binary_message = ""
        for char in message:
            binary_message += bin(ord(char))[2:].zfill(8)
        
        binary_message_text = Text(binary_message).scale(0.5)  

        self.play(Transform(message_text, binary_message_text))
        # self.play(Write(binary_message_text), run_time=2)


        explain_text2 = "Encoding: Apply Fibbionacci Substitution, as Cipher to bit string"
        explain_text2 = Text(explain_text2).scale(0.50).shift(UP*2)
        self.play(Transform(explain_text, explain_text2))

        #draw 2x2 matrix
        matrix = Matrix([["a", "ab"], ["b", "a"]])
        matrix.scale(0.5)
        matrix.shift(UP)
        matrix.shift(LEFT*2)
        # self.play(Write(matrix))

        # Arrow to matrix

        # binary matrix
        binary_matrix = Matrix([["0", "01"], ["1", "0"]])
        binary_matrix.scale(0.5)
        binary_matrix.shift(UP)
        binary_matrix.shift(RIGHT*2)

        arrow = Arrow(start=matrix.get_center(), end=binary_matrix.get_center(), buff=1, stroke_width=2)

        matrix_group = VGroup(matrix, arrow, binary_matrix)

        self.play(Write(matrix_group), run_time=2)
        self.wait(2)

        fib_sub_binary = {"0": "01", "1": "0"}

        # apply substitution once

        one_sub = Substitution(fib_sub_binary, binary_message, 1)
        one_sub_text = Text(one_sub).scale(0.5 / 1.61)
        one_sub_text.shift(DOWN*0.5)
        self.play(Write(one_sub_text))

        # apply substitution twice
        two_sub = Substitution(fib_sub_binary, binary_message, 2)
        two_sub_text = Text(two_sub).scale(0.5 / (1.61**2))
        two_sub_text.shift(DOWN*1)
        self.play(Write(two_sub_text))


        # fade out matrix, and onesub, move up two_sub

        self.play(FadeOut(matrix_group), FadeOut(one_sub_text), FadeOut(message_text), two_sub_text.animate.shift(UP*1))
        
        #scale up two_sub
        self.play(two_sub_text.animate.scale(1.61))
        # two_sub_text.scale(1.61)
        
        # two_sub_text_markup = MarkupText(
        #     two_sub,
        #     color=WHITE,
        #     font_size=DEFAULT_FONT_SIZE

        # )
        # two_sub_text_markup.scale(two_sub_text.get_width() / two_sub_text_markup.get_width())

        # # self.play(Transform(two_sub_text, two_sub_text_markup), runtime=0)
        # self.play(FadeOut(two_sub_text), Write(two_sub_text_markup), runtime=0)
        # self.play(Write(two_sub_text_markup), runtime=0)

        # perform reverse subsitution
        explain_text3 = "Decoding: Perform reverse substitution"
        explain_text3 = Text(explain_text3).scale(0.50).shift(UP*2)
        self.play(Transform(explain_text, explain_text3))
        self.wait(1)
    

        # draw reverse matrix
        reverse_matrix = Matrix([["01", "0"], ["0", "1"]])
        reverse_matrix.scale(0.7)
        reverse_matrix.shift(UP)
        self.play(Write(reverse_matrix))
        self.wait(1)

        # two_sub_md = MarkupText(two_sub)

        crop_two_sub = two_sub[0:-40] + "..."
        #underline all 01's in the two_sub text
        two_sub_underline_text = MarkupText(
            crop_two_sub.replace("01", " <span underline='single' underline_color='white'>01</span> ")[1:],
            color=WHITE,
            font_size=DEFAULT_FONT_SIZE,
        )
        two_sub_underline_text.scale(0.3)
        two_sub_underline_text.shift(LEFT*1.50, DOWN*0.5)

        self.play(Write(two_sub_underline_text))

        self.wait(1)
        # apply reverse substitution once
        two_sub_reverse = reverse_substitution(fib_sub_binary, two_sub, 1)
        two_sub_reverse_text = Text(two_sub_reverse).scale(0.5 / (1.61 ** 0))
        two_sub_reverse_text.shift(DOWN*1)
        self.play(Write(two_sub_reverse_text))
        self.wait(1)


        # perform reverse substitution
        explain_text4 = "Decoding: Perform reverse substitution again"
        explain_text4 = Text(explain_text4).scale(0.50).shift(UP*2)
        self.play(Transform(explain_text, explain_text4))

        self.wait(1)

        # apply reverse substitution twice
        one_sub_reverse = reverse_substitution(fib_sub_binary, one_sub, 1)
        one_sub_reverse_text = Text(one_sub_reverse).scale(0.5 / (1.61**-1))
        one_sub_reverse_text.shift(DOWN*1.75)
        self.play(Write(one_sub_reverse_text))

        self.wait(2)

        # clear previous text
        self.play(FadeOut(two_sub_underline_text), FadeOut(two_sub_reverse_text), FadeOut(two_sub_text), one_sub_reverse_text.animate.shift(UP*1.75), FadeOut(reverse_matrix))

        #convert to ascii
        explain_text5 = "Decoding: Convert binary to ascii"
        explain_text5 = Text(explain_text5).scale(0.50).shift(UP*2)
        self.play(Transform(explain_text, explain_text5))

        #convert to

        convert_from_binary = "".join([chr(int(one_sub_reverse[i:i+8], 2)) for i in range(0, len(one_sub_reverse), 8)])
        ascii_text = Text(convert_from_binary).scale(0.5 / (1.61**-2)).shift(DOWN*2)
        self.play(Write(ascii_text))




        # self.play(Write(text))
        self.wait(2)


        self.play(FadeOut(explain_text), FadeOut(ascii_text), FadeOut(one_sub_reverse_text))
        self.wait(1)

        future_title = Title("Future Ideas")
        self.play(Transform(title, future_title))
        self.wait(1)

        future_text1 = Text("Define substitution on each character, then use subsitution as private key").scale(0.5).shift(UP*2.5)
        self.play(Write(future_text1))
        self.wait(1)

        future_matrix = Matrix([["a", "c"], ["b", "i"], ["c", "n"], ["d", "o"], ["...", "..."], ["z", "a"]]).scale(0.8)
        # future_matrix.shift()
        self.play(Write(future_matrix))
        self.wait(1)

        vary_text = Text("Vary the substitution matrix, to encode text").scale(0.5).shift(DOWN*2.5)
        self.play(Write(vary_text))
        self.wait(1)

        future_matrix2 = Matrix([["a", "b"], ["b", "c"], ["c", "i"], ["d", "x"], ["...", "..."], ["z", "p"]]).scale(0.8)
        self.play(Transform(future_matrix, future_matrix2))
        self.wait(1)

        future_matrix3 = Matrix([["a", "x"], ["b", "p"], ["c", "m"], ["d", "q"], ["...", "..."], ["z", "z"]]).scale(0.8)
        self.play(Transform(future_matrix, future_matrix3))
        self.wait(1)

        self.play(FadeOut(vary_text))

        future_matrix4 = Matrix([["a", "xi"], ["b", "pip"], ["c", "ain"], ["d", "q"], ["...", "..."], ["z", "zo"]]).scale(0.8)
        qustion_text = Text("When can we define a reverse substitution in a unique way?").scale(0.5).shift(DOWN*2.5)
        self.play(Transform(future_matrix, future_matrix4), Write(qustion_text))
        self.wait(2)

        question_text2 = Text("Can we use ciphers with longer subsitutions?").scale(0.5).shift(DOWN*3)
        self.play(Write(question_text2))
        self.wait(1)

        future_matrix5 = Matrix([["a", "xiop"], ["b", "pas"], ["c", "blue"], ["d", "a"], ["...", "..."], ["z", "ingp"]]).scale(0.8)
        self.play(Transform(future_matrix, future_matrix5))
        self.wait(2)
        
        self.play(FadeOut(future_matrix), FadeOut(qustion_text), FadeOut(question_text2), FadeOut(title), FadeOut(future_text1))
        self.wait(1)


        











