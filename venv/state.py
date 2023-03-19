kmap_q0 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

kmap_q1 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

kmap_q2 = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

code = "10010"

idx = {'00': 0, '01': 1, '11': 2, '10': 3}

q0 = [0, 0, 0, 1, 2, 2, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0]
q1 = [0, 1, 1, 1, 2, 2, 1, 1, 0, 0, 1, 0, 2, 2, 0, 0]
q2 = [1, 1, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0]

inputs = ["000" + code[0],
          "001" + code[1],
          "010" + code[3],
          "011" + code[2],
          "100" + "0",
          "101" + "0",
          "110" + code[4],
          "111" + "0",
          "000" + str(int(not(int(code[0])))),
          "001" + str(int(not(int(code[1])))),
          "010" + str(int(not(int(code[3])))),
          "011" + str(int(not(int(code[2])))),
          "100" + "1",
          "101" + "1",
          "110" + str(int(not(int(code[4])))),
          "111" + "1"]

for var, q in zip(inputs, q0):
    col = idx[var[:2]]
    row = idx[var[2:]]
    kmap_q0[row][col] = q

for var, q in zip(inputs, q1):
    col = idx[var[:2]]
    row = idx[var[2:]]
    kmap_q1[row][col] = q

for var, q in zip(inputs, q2):
    col = idx[var[:2]]
    row = idx[var[2:]]
    kmap_q2[row][col] = q


for lst in kmap_q0:
    print(lst)

print("")

for lst in kmap_q1:
    print(lst)

print("")


for lst in kmap_q2:
    print(lst)