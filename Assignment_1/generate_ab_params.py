def generate_cost_function_params(student_id1, student_id2=0):
    """
    This function is used to generate group-specific cost-function parameters for the Modelica assignment.
    Use it as follows in a Python interpreter:
    > import cost_param
    > cost_param.generate_cost_function_params("<student_id1>","<student_id2>")
    
    :param student_id1: string: Last four digits of the student ID of the first/only student in the group.
    :param student_id2: string: Last four digits of the student ID of the second student in the group.
    :return: Prints the parameters a and b to stdout
    """
    
    combo = (int(student_id2) + int(student_id1)) % 10000
    a = int(str(combo)[:2])
    b = combo % 100
    if a == 0 and b == 0:
        print('a=1, b=1')
    elif a == 0:
        print('a=' + str(b) + ', b=' + str(b))
    elif b == 0:
        print('a=' + str(a) + ', b=' + str(a))
    else:
        def compute_hcf(x, y):
            while y:
                x, y = y, x % y
            return x

        hcf = compute_hcf(a, b)
        print('a=' + str(a / hcf) + ', b=' + str(b / hcf))

if __name__ == "__main__":
    generate_cost_function_params("3082", "")
