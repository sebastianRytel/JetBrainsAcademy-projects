def grid():
    marks = ['_']*9
    list_1 = [mark for mark in marks]
    list_2 = [list_1[y:y+3] for y in range(0,9,3)]
    return list_2

def choice():
    matrix = grid()
    counter = 1
    matrix_list = []
    while True:        
        coordinates = input("Enter coordinates: ").split()
        if coordinates[0].isalpha() or coordinates[1].isalpha():
            print("You should enter numbers!")
            continue
        coordinates_list = [int(number) for number in coordinates]       
        coordinate_1, coordinate_2 = coordinates_list[0], coordinates_list[1]
        if int(coordinates[0]) > 3 or int(coordinates[1]) > 3:
            print("Coordinates should be from 1 to 3!")
            continue
        if matrix[coordinate_1-1][coordinate_2-1] == "X" or matrix[coordinate_1-1][coordinate_2-1] == "O":
            print("This cell is occupied! Choose another one!")
            continue
        if counter % 2 != 0:
            matrix[coordinate_1-1][coordinate_2-1] = 'X'
        else:
            matrix[coordinate_1-1][coordinate_2-1] = 'O'
        matrix_list.clear()
        print(9 * '-')
        for element in matrix:            
            matrix_list.append(element)
            print('|', " ".join(element),'|')
        print(9 * '-')
        counter += 1
        row_list = [row for row in matrix_list]
        columns = [[matrix_list[i+0][0+y] for i in range(0,3)] for y in range(0,3)]
        for i in range(0,3):
            if '_' not in row_list[i]:
                if row_list[i][0] == row_list[i][1] == row_list[i][2]:
                    print(row_list[i][0], "wins")
                    quit()
            if '_' not in columns[i]:
                if columns[i][0] == columns[i][1] == columns[i][2]:
                    print(columns[i][0], "wins")
                    quit()
        if '_' not in row_list[0]:
            if row_list[0][0] == row_list[1][1] == row_list[2][2]:
                print(row_list[0][0], 'wins')
                quit()
            if row_list[0][2] == row_list[1][1] == row_list[2][0]:
                print(row_list[0][2], 'wins')
                quit()
        list_end = []
        for i in range(3):
            for element in matrix:
                if element[i] != "_":
                    list_end.append(element[i])
        if len(list_end) == 9:
            print("Draw")
            quit()
                        
def print_grid():
    print(9 * '-')
    list_2 = grid()
    for element in list_2:
        print('|', " ".join(element),'|')
    print(9 * '-')
    return list_2
def main():
    grid()
    print_grid()
    choice()
main()
