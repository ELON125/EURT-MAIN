a_file = open("sample.txt", "r")
list_of_lines = a_file.readlines()

for lines in a_file.readlines():
  lines.write('-')

for num in range(2,155):
  num1 = num +1
  insertNum = int(num)
  list_of_lines[insertNum] = f"Line{num1}\n"
  a_file = open("sample.txt", "w")
  a_file.writelines(list_of_lines)
  a_file.close()