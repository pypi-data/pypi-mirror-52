import os
def get_structure(name):
    result = []
    with open(os.path.dirname(os.path.realpath(__file__)) + '/structures/' + name + '.xyz') as myfile:
        arc = []
        for line in myfile.readlines():
            if line.strip() == 'X':
                result.append(arc)
                arc = []
            else:
                arc.append(line.strip())
        if arc:
            result.append(arc)
    return result