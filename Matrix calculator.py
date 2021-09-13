def double_matrix():
    matrix_a = []
    matrix_b = []
    while True:
        i = 0
        rows, cols = [int(x) for x in input("Enter size of first matrix: ").split()]
        print("Enter first matrix:")
        while i < int(rows):
            list_input = [float(x) for x in input().split()]
            matrix_a.append(list_input)
            i += 1
        if len(matrix_a) == rows:
            rows_2, cols_2 = [int(x) for x in input("Enter size of second matrix: ").split()]
            print("Enter second matrix:")
            i = 0           
            while i < int(rows_2):
                list_input_2 = [float(x) for x in input().split()]
                # check(rows, cols, rows_2, cols_2)
                matrix_b.append(list_input_2)
                i += 1        
            return matrix_a, matrix_b, rows, cols, rows_2, cols_2

def single_matrix():
    matrix_single = []
    while True:
        i = 0
        rows, cols = [int(x) for x in input('Enter size of matrix: ').split()]
        print('Enter matrix:')
        while i < rows:
            list_ = [float(x) for x in input().split()]
            matrix_single.append(list_)
            i += 1
        return matrix_single, rows, cols

def multiply():
    matrix_a, matrix_b, rows, cols, rows_2, cols_2 = double_matrix()
    transposed_matrix_b = [[matrix_b[n][i] for n in range(rows_2)] for i in range(cols_2)]
    print("The results is:")
    for element in matrix_a:
        lista = []
        for element_2 in transposed_matrix_b:
            list_multiply = sum([element[i] * element_2[i] for i in range(cols)])
            lista.append(str(list_multiply))
        print(' '.join(lista))

def multiply_const():
    matrix_single, rows, cols = single_matrix()
    const = float(input("Enter constant: "))
    matrix_output = [[matrix_single[i][j] * const for j in range(cols)] for i in range(rows)]
    print("The results is:")  
    for element in matrix_output:
        print(*element)

def add():
    matrix_a, matrix_b, rows, cols, rows_2, cols_2 = double_matrix()
    if len(matrix_a) == rows and len(matrix_b) == rows:
        print("The result is:")
        matrix_output = [[matrix_a[i][j] + matrix_b[i][j] for j in range(cols)] for i in range(rows)]
        for element in matrix_output:
            print(*element)

def transpose(choice):
    if choice == '1':
        matrix_single, rows, cols = single_matrix()
        transposed_matrix_single = [[matrix_single[n][i] for n in range(rows)] for i in range(cols)]
        print("The results is:")
        for element in transposed_matrix_single:
            print(*element)

    if choice == '2':
        matrix_single, rows, cols = single_matrix()
        transposed_matrix_single = [[matrix_single[-n][-i] for n in range(1,rows+1)] for i in range(1,cols+1)]
        print("The results is:")
        for element in transposed_matrix_single:
            print(*element)

    if choice == '3':
        matrix_single, rows, cols = single_matrix()
        transposed_matrix_single = [[matrix_single[n][-i] for i in range(1,rows+1)] for n in range(cols)]
        print("The results is:")
        for element in transposed_matrix_single:
            print(*element)

    if choice == '4':
        matrix_a, rows, cols = single_matrix()
        transposed_matrix_a = [[matrix_a[-n][i] for i in range(rows)] for n in range(1,cols+1)]
        print("The results is:")
        for element in transposed_matrix_a:
            print(*element)

def menu_transpose():
    print("""\n1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")
    choice = input("Your choice: ")
    transpose(choice)

def determinant(matrix):   
    i=0
    list_of_matrixes = []
    dets = matrix[0]
    accumulate = 0
    for z in range(len(matrix)):
        list_ = [num for num in range(len(matrix))]
        del list_[z]
        inter_matrix = [[matrix[y][x] for x in list_] for y in range(len(matrix))]
        del inter_matrix[i]
        list_of_matrixes.append(inter_matrix)
    if len(matrix) == 1:
        return matrix[0][0]
    elif len(matrix) != 3: 
        for i in range(len(matrix)):
            value_det = dets[i] * determinant(list_of_matrixes[i])
            if i % 2 == 0:
                accumulate += value_det
            else:
                accumulate -= value_det
        return accumulate
    else:
        for i in range(len(list_of_matrixes)):
            value_smallest_matrix = dets[i] * (list_of_matrixes[i][0][0] * list_of_matrixes[i][1][1] - list_of_matrixes[i][0][1]*list_of_matrixes[i][1][0])
            if i % 2 == 0:
                accumulate += value_smallest_matrix
            else:
                accumulate -= value_smallest_matrix
        return accumulate

def determinant_inversed_matrix_len_more_than_3(matrix):
    i=0
    list_of_matrixes = []
    dets = matrix[0]
    accumulate = 0
    list_dets = []
    for w in range(len(matrix)):        
        list_2 = [num for num in range(len(matrix))]
        del list_2[w]        
        for z in range(len(matrix)):
            list_1 = [num for num in range(len(matrix))]
            del list_1[z]
            inter_matrix = [[matrix[y][x] for x in list_1] for y in list_2]
            list_of_matrixes.append(inter_matrix)  
    if len(matrix) != 3:
        for i in range(len(list_of_matrixes)):
            value_det = determinant_inversed_matrix_len_more_than_3(list_of_matrixes[i])
            list_dets.append(value_det)
    else:        
        for i in range(len(list_of_matrixes[0])+1):
            value_smallest_matrix = dets[i] * (list_of_matrixes[i][0][0] * list_of_matrixes[i][1][1] - list_of_matrixes[i][0][1]*list_of_matrixes[i][1][0])                               
            if i % 2 == 0:
                accumulate += value_smallest_matrix
            else:
                accumulate -= value_smallest_matrix
        return accumulate
    
    new_dets_list = [list_dets[i:i+len(matrix)] for i in range(0,len(list_dets),len(matrix))]
    power = [num for num in range(1, len(matrix)+1)]
    opposite_sign = []
    for p in power:
        for q in power:
            x = (-1) ** (p + q)
            z = x * new_dets_list[p-1][q-1]
            opposite_sign.append(z)
    new_dets_list = [opposite_sign[i:i+len(matrix)] for i in range(0,len(opposite_sign),len(matrix))]
    
    _1_det_ = 0
    for x in range(len(matrix)):
        y = matrix[0][x] * new_dets_list[0][x]
        _1_det_ += y
    
    final_result = [[round(new_dets_list[y][x] * 1/_1_det_,4) for x in range(len(new_dets_list))] for y in range(len(new_dets_list))]
    print("The results is:")
    for element in final_result:
        print(*element)

def determinant_inversed_matrix_len_less_than_3(matrix):   
    i=0
    list_of_matrixes = []
    list_dets = []
    for w in range(len(matrix)):        
        list_2 = [num for num in range(len(matrix))]
        del list_2[w]        
        for z in range(len(matrix)):
            list_1 = [num for num in range(len(matrix))]
            del list_1[z]
            inter_matrix = [[matrix[y][x] for x in list_1] for y in list_2]
            list_of_matrixes.append(inter_matrix)         
    for i in range(len(list_of_matrixes)):
        value_smallest_matrix = (list_of_matrixes[i][0][0] * list_of_matrixes[i][1][1] - list_of_matrixes[i][0][1]*list_of_matrixes[i][1][0])                               
        list_dets.append(value_smallest_matrix)
    new_dets_list = [list_dets[i:i+len(matrix)] for i in range(0,len(list_dets),len(matrix))]
    power = [num for num in range(1, len(matrix)+1)]
    opposite_sign = []
    for p in power:
        for q in power:
            x = (-1) ** (p + q)
            z = x * new_dets_list[p-1][q-1]
            opposite_sign.append(z)
    new_dets_list = [opposite_sign[i:i+len(matrix)] for i in range(0,len(opposite_sign),len(matrix))]    
    _1_det_ = 0
    for x in range(len(matrix)):
        y = matrix[0][x] * new_dets_list[0][x]
        _1_det_ += y    
    final_result = [[new_dets_list[y][x] * 1/_1_det_ for x in range(len(new_dets_list))] for y in range(len(new_dets_list))]
    print("The results is:")
    for element in final_result:
        print(*element)

def determinant_inversed_matrix(matrix_single, rows, cols):
    transposed_matrix_single = [[matrix_single[n][i] for n in range(rows)] for i in range(cols)]

    if len(transposed_matrix_single) > 3:
        determinant_inversed_matrix_len_more_than_3(transposed_matrix_single)
    elif len(transposed_matrix_single) == 3:
        determinant_inversed_matrix_len_less_than_3(transposed_matrix_single)
    else:
        print("This matrix doesn't have an inverse.")
   
def menu():
    print("""\n1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")
    choice = input("Your choice: ")
    return choice

def check(rows, cols, rows_2, cols_2):
    if rows != rows_2 and cols != cols_2:
        print("The operation cannot be performed.")
        quit()

def main():
    choice = menu()
    if choice == '1':
        add()
        main()
    elif choice == '2':
        multiply_const()
        main()
    elif choice == '3':
        multiply()
        main()
    elif choice == '4':
        menu_transpose()
        main()
    elif choice == '5':
        matrix_single, rows, cols = single_matrix()
        print(determinant(matrix_single))
        main()
    elif choice == '6':
        matrix_single, rows, cols = single_matrix()
        determinant_inversed_matrix(matrix_single, rows, cols)
        main()
    else:
        quit()
main()
