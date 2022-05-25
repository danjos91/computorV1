import sys
import ctypes

equation = "5 * X^0 + 4 * X^1 - 9.367 * X^2 = 1 * X^0 + 1 * X^2"

class EcuationMember:
    def __init__(self, value, category):
        self.value = value
        self.category = category


class Complex:
    def __init__(self, realpart, imagpart):
        self.real = realpart
        self.imaginary = imagpart


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
    return degree_value


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


def print_equation(equation):
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
    text += "= 0"
    return text


def do_equal_to_zero(equation):
    elements_after_equal = []
    elements_before_equal = []
    equal = False
    value = 0
    category = 1
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
                print("Not valid equation...Please check it.")
                sys.exit(-1)
        counter += 1
    return elements_list


def solve_equation(reduced_form):
    # Ecuation form ax^2 + bx + c = 0
    a = reduced_form[2][0]
    b = reduced_form[1][0]
    c = reduced_form[0][0]
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        print('Discriminant is strictly positive')
        print("Solutions: ")
        x1 = (b * (-1) + discriminant ** 0.5) / (2 * a)
        print("X1 = " + str(x1))
        x2 = (b * (-1) - discriminant ** 0.5) / (2 * a)
        print("X2 = " + str(x2))
        print("STEPS:")
        print("\tWe have an equation of type: c + bx + ax^2 = 0")
        print("\t" + print_equation(reduced_form))
        print("1) Found the discriminant:\n   D = b^2 - 4ac")
        print('\tDiscriminant = (' + str(b) + ")^2 - 4*(" + str(a) + ")*(" + str(c) + ") = " + str(discriminant))
        print("2) If D > 0:\n   X[1,2] = (-b +/- sqrt(b^2 - 4ac)) / 2a")
        print("\tX1 = (-(" + str(b) + ") + sqrt((" + str(b) + ")^2 - 4*( " + str(a) + ")*(" + str(c) + "))) / (2*(" + str(a) + "))")
        print("\tX1 = (" + str(b * (-1)) + ") + sqrt(" + str(discriminant) + ")) / (2*(" + str(a) + "))")
        print("\tX1 = (" + str(b * (-1)) + " + " + str(discriminant ** 0.5) + ") / " + str(2*a))
        print("\tX1 = " + str(b * (-1) + discriminant ** 0.5) + " / " + str(2 * a))
        print("\tX1 = " + str(x1))
        print("\tX2 = (-(" + str(b) + ") - sqrt((" + str(b) + ")^2 - 4*( " + str(a) + ")*(" + str(c) + "))) / (2*(" + str(a) + "))")
        print("\tX2 = (" + str(b * (-1)) + " - sqrt(" + str(discriminant) + ")) / (2*(" + str(a) + "))")
        print("\tX2 = " + str(b * (-1) - discriminant ** 0.5) + " / " + str(2 * a))
        print("\tX2 = " + str(x2))

def solve(equation):
    degree = get_degree(equation)
    if degree > 2:
        print("I cant solve second degree equations only")
        return False
    equation_elements = get_equation_members(equation)
    reduced_equation = do_equal_to_zero(equation_elements)
    print(print_equation(reduced_equation))
    solve_equation(reduced_equation)
    print("Polynomial degree: ", degree)


def main():
    if len(sys.argv) == 2:
        equation = sys.argv[1]
        if not validate(equation):
            print("Not valid equation...Please check it.")
            return
        if not solve(equation):
            return
    else:
        print(
            'Write an equation as an argument.\nUsage example: python3 computor.py "5 * X^0 + 4 * X^1 - 9.367 * X^2 = 1 * '
            'X^0 + 1 * X^2"')


if __name__ == '__main__':
    main()
