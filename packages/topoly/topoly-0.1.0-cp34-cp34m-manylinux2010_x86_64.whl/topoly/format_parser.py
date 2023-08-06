"""
Format parser. Parses between coordinates, EM code, Gauss code and PD code.
Allows for curve simplification by KMT method, dynamic relaxation and Monte Carlo simplification.

Pawel Dabrowski-Tumanski
p.dabrowski at cent.uw.edu.pl
12.11.2018
"""

import re
import os
from Command import Command

def gauss_pd(code):
    code = [int(x) for x in code.split(',')]
    narcs = max(code)
    newcode = ''
    for k in range(1, narcs+1):
        vertex = [code.index(-k), code.index(k), code.index(-k)+1, code.index(k)+1]
        newcode += 'X[' + ','.join([str(x) for x in vertex]).replace('0',str(narcs)) + ']\n'
    return newcode

def gaussorient_pd(code):
    return

def coordinates_pd(coords):
    emcode = coordinates_em(coords)
    return em_pd(emcode)

def pd_gauss(code):
    return

def pd_gaussorient(code):
    return

def pd_coordinates(code):
    return

def coordinates_gauss(coords):
    emcode = coordinates_em(coords)
    return em_gauss(emcode)

def coordinates_gaussorient(coords):
    emcode = coordinates_em(coords)
    return em_gaussorient(emcode)

def gauss_coordinates(code):
    code = gauss_pd(code)
    return coordinates_pd(code)

def gaussorient_coordinates(code):
    code = gaussorient_pd(code)
    return coordinates_pd(code)

def gauss_gaussorient(code):
    return

def gaussorient_gauss(code):
    return

def em_gauss(code):
    return

def em_gaussorient(code):
    return

def em_pd(code):
    result = ''
    letters = 'abcd'
    intervals = []
    for cross in code.splitlines():
        if not cross:
            continue
        number, rest = re.sub('[-+V]',' ',cross, count=1).split()
        print cross
        typ = cross.strip(number)[0]
        code_tmp = []
        tmp = re.split(r'(\d+)',rest)[1:]
        for k in range(0, len(tmp),2):
            end = tmp[k]+tmp[k+1]
            if typ == 'V':
                start = number + 'V'
            else:
                start = number + letters[k/2]
            interval = sorted([start, end])
            if interval not in intervals:
                intervals.append(interval)
            code_tmp.append(str(intervals.index(interval)))
        if typ == '-':
            code_tmp = list(reversed(code_tmp))
        if typ == '+':
            code_tmp = [code_tmp[1],code_tmp[0],code_tmp[3],code_tmp[2]]
        print re.sub('[-+]','X',typ)+'['+','.join(code_tmp)+']'
        result += re.sub('[-+]','X',typ)+'['+','.join(code_tmp)+'];'
    return result

def em_coordinates(code):
    code = em_pd(code)
    return coordinates_pd(code)

def pd_em(code):
    return

def gauss_em(code):
    return

def gaussorient_em(code):
    return

def coordinates_em(coords, closed=False):
    commons = {}
    commons_num = []
    n = 1
    for arc in coords:
        if arc[0] not in commons.keys():
            commons[arc[0]] = str(n)
            commons_num.append(n)
        else:
            n -= 1
        n += len(arc) - 1
        if arc[-1] not in commons.keys():
            commons[arc[-1]] = str(n)
            commons_num.append(n)
        else:
            n -= 1
    n = 1
    args = ''
    for k in range(len(coords)):
        arc = coords[k]
        with open('arc' + str(k), 'w') as myfile:
            while n in commons_num:
                n += 1
            for atom in arc:
                if atom in commons.keys():
                    myfile.write(commons[atom] + ' ' + atom + '\n')
                else:
                    myfile.write(str(n) + ' ' + atom + '\n')
                    n += 1
        args += 'arc' + str(k) + ' '
    bin_name = os.path.dirname(os.path.realpath(__file__)) + '/../build/homflylink'
    comp = Command(bin_name + ' --input ' + args + '-y')
    comp.run(timeout=1000)
    with open('YCode.txt') as myfile:
        res_tmp = [x.strip() for x in myfile.readlines()]
    if closed:
        res = []
        translate = {}
        for cross in res_tmp:
            if cross[:2] == '1V':
                translate['2V'] = cross[2:]
            elif cross[:2] == '2V':
                translate['1V'] = cross[2:]
            elif cross:
                res.append(cross.replace('1V', translate['1V']).replace('2V', translate['2V']))
    else:
        res = res_tmp
    result = '\n'.join(res)
    return result