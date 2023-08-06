import sys
# from topoly import yamada

# curve = []
# for k in range(3):
#     arc = []
#     file_name = 'arc' + str(k+1)
#     with open(file_name, 'r') as myfile:
#         for line in myfile.readlines():
#             arc.append(line.strip().split()[1:])
#     curve.append(arc)

# print(yamada(curve, translate=True, debug=True))

from topoly_homfly import find_link_code_to_string
data_dir = sys.argv[1]
print(find_link_code_to_string([(data_dir + '/arc1').encode('utf-8'), (data_dir + '/arc2').encode('utf-8'), (data_dir + '/arc3').encode('utf-8')], yamada=True))