import sys


class EcuationMember:
    def __init__(self, value, category):
        self.value = value
        self.category = category


def get_coeff(equation_member, exponent):
    i = 0
    print(equation_member)
    coefficient = 0
    while i < len(equation_member) - 2:
        number_str = ''
        if equation_member[i] == 'X' and equation_member[i + 1] == '^' and equation_member[i + 2] == str(exponent):
            j = i - 4
            while equation_member[j] != '*' and equation_member[j] != '-' and equation_member[j] != '+' and \
                    equation_member[j] != '/' and j >= 0:
                number_str = number_str + equation_member[j]
                j -= 1
        number_str = '0' if number_str == '' else number_str
        print(number_str)
        coefficient = coefficient + float(number_str[::-1])
        i += 1

    return coefficient


def del_zeros(element):
    return str(element).strip('0').strip('.')


def validate(equation):
    if equation.find("=") < 0:
        print("Wrong equation. Missing equals '='")
        sys.exit(-1)
    return True


def get_degree(equation):
    position = equation.find("^")
    tmp_degree = 0
    degree_value = 0
    while position != -1:
        degree_position = position + 1
        degree_value = int(equation[degree_position])
        if degree_value > tmp_degree:
            tmp_degree = degree_value
        position = equation.find("^", degree_position)
    return tmp_degree


def supress_operators(elements):
    numbers = [elements[0]]
    counter = 0
    for value in elements:
        if value[0] == '+':
            numbers.append(elements[counter + 1])
        elif value[0] == '-':
            numbers.append((elements[counter + 1][0] * (-1), elements[counter + 1][1]))
        counter += 1
    return numbers


def add_category(elements):
    for i in range(3):
        values = [category for value, category in elements if category == i]
        if len(values) == 0:
            elements.append((0, i))


def print_reduced_equation(equation):
    text = ''
    for i in range(3):
        value = equation[i][0]
        if value != 0:
            if value > 0:
                if i == 0:
                    text += str(value) + " * X^" + str(i) + " "
                else:
                    text += "+ " + str(value) + " * X^" + str(i) + " "
            else:
                text += "- " + str(value * (-1)) + " * X^" + str(i) + " "
    if text == '':
        return "0 = 0\nSolution: Any real number is a solution!"
    text += "= 0"
    return text


def do_equal_to_zero(equation):
    elements_after_equal = []
    elements_before_equal = []
    equal = False
    value = 0
    for element in equation:
        if element[value] == '=':
            equal = True
        if equal and element[value] != '=':
            elements_after_equal.append(element)
        else:
            elements_before_equal.append(element)
    for i in range(2):
        before = [value for value, category in elements_before_equal if category == i]
        if len(before) > 1:
            print("Wrong equation.\nOnly one element of one degree is permitted on one side equation")

    numbers_before = supress_operators(elements_before_equal)
    add_category(numbers_before)
    numbers_after = supress_operators(elements_after_equal)
    add_category(numbers_after)

    reduced_equation = []
    for i in range(3):
        value_before = [value for value, category in numbers_before if category == i]
        value_after = [value for value, category in numbers_after if category == i]
        reduced_equation.append((value_before[0] - value_after[0], i))
    return reduced_equation


def get_equation_members(equation):
    values = equation.split(' ')
    elements_list = []
    counter = 0
    for element in values:
        if element == 'X^0' and values[counter - 1] == "*":
            elements_list.append((float(values[counter - 2]), 0))
        elif element == 'X^1' and values[counter - 1] == "*":
            elements_list.append((float(values[counter - 2]), 1))
        elif element == 'X^2' and values[counter - 1] == "*":
            elements_list.append((float(values[counter - 2]), 2))
        elif element == '=':
            elements_list.append((element, 'equal'))
        elif element == '*':
            pass
        elif element == '+':
            elements_list.append((element, 'plus'))
        elif element == '-':
            elements_list.append((element, 'minus'))
        else:
            try:
                float(element)
            except:
                print("Error found in: " + element)
                sys.exit(-1)
        counter += 1
    return elements_list


def print_solved_equation(equation, reduced_equation, solutions, discriminant, degree):
    # Ecuation form ax^2 + bx + c = 0
    a = reduced_equation[2][0]
    b = reduced_equation[1][0]
    c = reduced_equation[0][0]

    print("Equation:")
    print("\t" + equation)
    print("Reduced equation:")
    print("\t" + print_reduced_equation(reduced_equation))

    if discriminant > 0:
        print('Discriminant is strictly positive')
    elif discriminant < 0:
        print('Discriminant is strictly negative')
    elif discriminant == 0:
        print('Discriminant is 0')
    if a == 0 and b == 0 and c != 0:
        print("Solution: There is not a solution!")
        print()

    if degree == 1:
        type = "c + bx = 0"
        print("Solution:")
        x1 = solutions[0]
        print("\tX = " + str(x1))
        print()
        print("STEPS:")
        print("\tWe have an equation of type: %s" % type)
        print("\t" + print_reduced_equation(reduced_equation))
        print("\t(" + str(b) + ")*X = " + str(-1 * c))
        print("\tX = " + str(-1 * c) + "/" + str(b))
        print("\tX = " + round_eq(-1 * c / b))
        print()
        print("Discriminant:\n   D = b^2 - 4ac")
        print('\tDiscriminant = (' + str(b) + ")^2 - 4*(" + str(a) + ")*(" + str(c) + ") = " + str(discriminant))
    elif degree == 2:
        type = "c + bx + ax^2 = 0"
        x1 = solutions[0]
        x2 = solutions[1]
        if x1 == x2:
            print("Solution:")
            print("X = " + str(x1))
        else:
            print("Solutions: ")
            print("X1 = " + str(x1))
            print("X2 = " + str(x2))
        print()
        print("STEPS:")
        print("\tWe have an equation of type: %s" % type)
        print("\t" + print_reduced_equation(reduced_equation))
        print()
        print("1) Found the discriminant:\n   D = b^2 - 4ac")
        print('\tDiscriminant = (' + str(b) + ")^2 - 4*(" + str(a) + ")*(" + str(c) + ") = " + str(discriminant))
        print()
        print("2) D > 0:\n   X[1,2] = (-b +- sqrt(b^2 - 4ac)) / 2a")
        print()
        print(
            "\tX1 = (-(" + str(b) + ") + sqrt((" + str(b) + ")^2 - 4*( " + str(a) + ")*(" + str(c) + "))) / (2*(" + str(
                a) + "))")
        print("\tX1 = (" + str(b * (-1)) + ") + sqrt(" + str(discriminant) + ")) / (2*(" + str(a) + "))")
        if discriminant < 0:
            print("\tX1 = (" + str(b * (-1)) + " + " + round_eq((discriminant ** 0.5).imag) + "i) / " + str(2 * a))
        else:
            print("\tX1 = (" + str(b * (-1)) + " + " + str(discriminant ** 0.5) + ") / " + str(2 * a))
            print("\tX1 = " + str(b * (-1) + discriminant ** 0.5) + " / " + str(2 * a))
        print("\tX1 = " + str(x1))
        print()
        print(
            "\tX2 = (-(" + str(b) + ") - sqrt((" + str(b) + ")^2 - 4*( " + str(a) + ")*(" + str(c) + "))) / (2*(" + str(
                a) + "))")
        print("\tX2 = (" + str(b * (-1)) + " - sqrt(" + str(discriminant) + ")) / (2*(" + str(a) + "))")
        if discriminant < 0:
            print("\tX2 = (" + str(b * (-1)) + " - " + round_eq((discriminant ** 0.5).real) + ") / " + str(2 * a))
        else:
            print("\tX2 = (" + str(b * (-1)) + " - " + str(discriminant ** 0.5) + ") / " + str(2 * a))
            print("\tX2 = " + str(b * (-1) - discriminant ** 0.5) + " / " + str(2 * a))
        print("\tX2 = " + str(x2))
        print()
    print("Polynomial degree: ", degree)


def solve(equation):
    degree = get_degree(equation)
    if degree > 2:
        print("Sorry. I can solve second degree equations only")
        return False
    equation_elements = get_equation_members(equation)
    reduced_equation = do_equal_to_zero(equation_elements)

    a = reduced_equation[2][0]
    b = reduced_equation[1][0]
    c = reduced_equation[0][0]

    discriminant = b ** 2 - 4 * a * c

    solutions = []
    if discriminant >= 0:
        if degree == 0:
            if c != 0:
                exit(-1)
            else:
                solutions.append(0)
        if degree == 1:
            x1 = (-1) * c / b
            solutions.append(x1)
        elif degree == 2:
            x1 = (b * (-1) + discriminant ** 0.5) / (2 * a)
            x2 = (b * (-1) - discriminant ** 0.5) / (2 * a)
            solutions.append(x1)
            solutions.append(x2)
    elif discriminant < 0:
            x1 = (b * (-1) + discriminant ** 0.5) / (2 * a)
            x1 = round_eq(x1.real) + " + (" + round_eq(x1.imag) + ")i"
            x2 = (b * (-1) - discriminant ** 0.5) / (2 * a)
            x2 = round_eq(x2.real) + " + (" + round_eq(x2.imag) + ")i"
            solutions.append(x1)
            solutions.append(x2)

    print_solved_equation(equation, reduced_equation, solutions, discriminant, degree)


def round_eq(value):
    return str(round(value, 2))


def main():
    if len(sys.argv) == 2:
        try:
            equation = sys.argv[1]
            if not validate(equation):
                return
            if not solve(equation):
                return
        except:
            print("Not valid equation...Please check it.")

    else:
        print(
            'Write an equation as an argument.\nUsage example: python3 computor.py "5 * X^0 + 4 * X^1 - 9.367 * X^2 = 1 * '
            'X^0 + 1 * X^2"')


if __name__ == '__main__':
    main()
