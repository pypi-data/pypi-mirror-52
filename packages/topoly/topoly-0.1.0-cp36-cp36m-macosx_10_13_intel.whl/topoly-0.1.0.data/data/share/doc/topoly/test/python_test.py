from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

from topoly.graph import Graph
from topoly.PD_codes import PDcodes
from topoly.Gauss_codes import Gauss
from topoly.format_parser import em_pd, coordinates_em
from topoly.examples import get_structure
''' 
# tests for laurent:
poly_p = laurent("x^2y^-3 - y^-1")
poly_q = laurent("1+3y^-1")
poly_r = laurent("-2x^5y^2+1")
poly_s = laurent("1")
poly_t = laurent("A^3x^2y - 2y^-1 +2x +2A x + 5A^1x^2y - yx +A")
poly_w = laurent("A")

print poly_p({"y":2})
print poly_p({"x":'A+1'})
print poly_p({"x":'A+1','y':2})
'''

'''
# test for graph'''
coords = get_structure('t31')
for arc in coords:
    print arc
code = coordinates_em(coords, closed=False)
print 'EMCode:'
print code
print('---')
code = em_pd(code)
# code = 'V[1,14,15]\nV[6,15,7]\nX[1,7,2,8]\nX[8,2,9,3]\nX[11,3,12,4]\nX[4,10,5,11]\nX[5,13,6,14]\nX[9,13,10,12]'
g = Graph(code)
print 'PDCode:'
print((g.get_PDcode()))
print('---')
# g2 = g.smooth_crossing(typ=-1).smooth_crossing(typ=-1).smooth_crossing(typ=-1)
# g2.print_PDcode()
# print g2.get_loop_nr()
# print g.kauffman_bracket()
poly = g.yamada_polynomial()
# print poly
# print("Yamada:")
# print(poly.print_short())
print(poly.understand_output('Yamada'))
# link1, link2, link3 = g.kauffman_boundary()
# print 'LINK 1 (Jones):'
# # print (link1.get_PDcode())
# poly1 = link1.jones_polynomial()
# print poly1.print_short()
# print poly1.understand_output('Jones')
# print 'LINK 2 (Jones):'
# # print (link2.get_PDcode())
# poly2 = link2.jones_polynomial()
# print poly2.print_short()
# print poly2.understand_output('Jones')
# print 'LINK 3 (Jones):'
# # print (link3.get_PDcode())
# poly3 = link3.jones_polynomial()
# print poly3.print_short()
# print poly3.understand_output('Jones')
# print "reversed:"
# reversed(g).print_PDcode()
# print reversed(g).kauffman_bracket()
# print reversed(g).jones_polynomial()
# # g.change_chirality().print_PDcode()
# print "chirality"
# g.change_chirality().print_PDcode()
# print g.change_chirality().kauffman_bracket()
# print g.change_chirality().jones_polynomial()
# print "two variable"
# print g.yamada_two_variable()
# print "yamada"
# poly = g.yamada_polynomial()
# print poly
# print poly.print_short()
# print g.yamada_polynomial().print_short()
# g.change_chirality().print_PDcode()
# print g.aps_bracket()
# print g.aps_ps()
# print g.aps_weights()
# print g.sirp()

# print bool(poly1 == poly3)
