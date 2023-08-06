"""
The graph class containing the methods to calculate the graph (and knot) polynomials.
Expected graph description is the (extended) EM code.

Pawel Dabrowski-Tumanski
p.dabrowski at cent.uw.edu.pl
12.11.2018

Docs:
https://realpython.com/documenting-python-code/#docstring-types

The type used here: Google


Support in PyCharm:
https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html
- change default reStructuredText to Google

Docs will be published in: https://readthedocs.org/

"""

import re
import itertools
from topoly.polynomial import laurent
from copy import deepcopy
from math import sqrt
from random import choice

########
# TODO
# 2) Implement Reidemeister III move;
# 2') Make the Reidemeister move return number of crossings reduced;
# 3) Add graph simplification by applying Reidemeister moves;
# 4) Clean all;
# 5) Make comments;
# 6) Add exceptions;


class Graph:
    """Class docstrings go here."""

    def __init__(self, code = '', loop_nr = 0):
        """
        Parameters
        ----------
        code: str
            xxxxx
        loop_nr: int
            xxxxx
        """

        self.vertices = []
        self.crossings = []
        self.arc_nr = 0
        self.arcs = set()
        self.max_arc = 0
        self.loop_nr = loop_nr
        self.double_edges = set()
        if code:
            for line in code.splitlines():
                if line[0] == 'X':
                    self.crossings.append([int(x) for x in re.findall(r'\d+', line)])
                    self.max_arc = max([self.max_arc] + self.crossings[-1])
                    self.arcs |= set(self.crossings[-1])
                elif line[0] == 'V':
                    self.vertices.append([int(x) for x in re.findall(r'\d+', line)])
                    self.max_arc = max([self.max_arc] + self.vertices[-1])
                    self.arcs |= set(self.vertices[-1])
                    for element in line.strip('V[]').split(','):
                        if len(element) > 1 and element[-1] == 'd':
                            self.double_edges.add(int(element[:-1]))
        self.arc_nr = len(list(self.arcs))

    ######## geting as string########
    def get_PDcode(self):
        """ Return results as string.

        Returns
        -------
        str
            results as string
        """

        res = ""
        for crossing in self.crossings:
            res+='X' + str(crossing) + '\n'
        for vertex in self.vertices:
            res+='V' + str(vertex) + '\n'
            for double in list(self.double_edges):
                res = res.replace(str(double),str(double)+'d')
        return res

    ######## getting ########
    def get_loop_nr(self):
        """Return loop number.

        Returns
        -------
        int
            loop number
        """

        return self.loop_nr


    def get_writhe(self, orientation = []):        # TODO include situations like (1,1,2,3)
        """

        Args:
            orientation: list

        Returns:

        """
        if not orientation:
            orientation = self.find_paths()
        writh = 0
        for crossing in self.crossings:
            for path in orientation:
                if crossing[0] in path:
                    path1 = path
                if crossing[1] in path:
                    path2 = path
            if path1[path1.index(crossing[2])-1] == crossing[0]:
                arc1 = 1
            elif path1[path1.index(crossing[0])-1] == crossing[2]:
                arc1 = -1
            if path2[path2.index(crossing[-1])-1] == crossing[1]:
                arc2 = 1
            elif path2[path2.index(crossing[1])-1] == crossing[-1]:
                arc2 = -1
            if arc1*arc2 == 1:
                writh -= 1
            elif arc1*arc2 == -1:
                writh += 1
        return writh


    def get_connected_components(self):
        # 0.1 case
        if len(self.crossings) == 0 and len(self.vertices) == 0:
            return [set()]
        connected = []
        # connected are 0-2 and 1-3
        for c in self.crossings:
            connected.append((c[0], c[2]))
            connected.append((c[1], c[-1]))
        # vertex connects edges
        for v in self.vertices:
            connected.append(tuple(v))
        return self.find_connections(connected)

    def get_edges(self):
        # 0.1 case
        if len(self.crossings) == 0 and len(self.vertices) == 0:
            return [set()]
        connected = []
        # connected are 0-2 and 1-3
        for c in self.crossings:
            connected.append((c[0], c[2]))
            connected.append((c[1], c[-1]))
        for v in self.vertices:
            for edge in v:
                connected.append(tuple([edge]))
        return self.find_connections(connected)


    def get_connected_components_number(self):
        return len(self.get_connected_components()) + self.loop_nr

    def get_betti_1(self):
        return self.arc_nr + self.get_connected_components_number() - len(self.vertices) - 2 * len(self.crossings)

    ######## Creating ########
    def create_disjoined_components(self):
        components = self.get_connected_components()
        for cross in self.crossings:
            k = 0
            while k < len(components):
                l = k + 1
                while l < len(components):
                    if cross[0] in components[k] and cross[1] in components[1]:
                        components[k] |= components[l]
                        components.pop(l)
                    l += 1
                k += 1
        subgraphs = ['' if len(element) != 0 else 'V' for element in components]
        for k in range(len(components)):
            for cross in self.crossings:
                if all(c in components[k] for c in cross):
                    subgraphs[k] += 'X' + str(cross) + '\n'
            for vertex in self.vertices:
                if len(vertex) > 0 and all(v in components[k] for v in vertex):
                    subgraphs[k] += 'V' + str(vertex) + '\n'
        # for k in range(len(components)):
        #     subgraphs[k] = Graph(subgraphs[k]).reduce_double_vertices()
        return subgraphs


    ######## Simplifications ########
    def is_loop(self):
        if all(len(v) == 2 for v in self.vertices) and len(self.get_connected_components()) == 1:
            return True
        return False

    def reduce_double_vertices(self):
        translate = {}
        for vertex in self.vertices:
            if len(vertex) == 2:
                if vertex[1] in translate.keys():
                    translate[vertex[0]] = translate[vertex[1]]
                elif vertex[0] in [translate[key] for key in translate.keys()]:
                    translate[vertex[1]] = vertex[0]
                elif vertex[0] in translate.keys():
                    translate[vertex[1]] = translate[vertex[0]]
                else:
                    translate[vertex[0]] = vertex[1]
        vertices = [v for v in self.vertices if (len(v) != 2 or v[0] == v[1])]
        # code = ''
        # if len(self.crossings) > 0:
        #     code += 'X' + '\nX'.join([str([translate.get(key, key) for key in cross]) for cross in self.crossings]) + '\n'
        # if vertices:
        #     code += 'V' + '\nV'.join([str([translate.get(key, key) for key in vertex]) for vertex in vertices]) + '\n'
        # if not code and len(self.vertices) != 0:
        #     code += 'V' + str([translate.get(key, key) for key in self.vertices[0]]) + '\n'
        n = len(self.vertices) - len(vertices)
        self.crossings = [[translate.get(key, key) for key in cross] for cross in self.crossings]
        self.vertices = [[translate.get(key, key) for key in vertex] for vertex in vertices]
        if not self.vertices and not self.crossings:
            self.vertices = [[0,0]]
        return n

    def simplify_easy(self, debug=False):
        n_red, n1_tot, n1_sign, n5_tot, n5_sign = 0, 0, 0, 0, 0
        n_red_old = -1
        self.reduce_double_vertices()
        while n_red != n_red_old:
            n_red_old = n_red
            n1, n2 = self.reidemeister1()
            n_red += n1
            n1_tot += n1
            n1_sign += n2
            n1 = self.reidemeister2(debug)
            n_red += n1
            n1_tot += n1
            # n1, n2 = self.reidemeister5(debug)
            # n_red += n1
            # n5_tot += n1
            # n5_sign += n2
        return n_red, n1_tot, n1_sign, n5_tot, n5_sign

    def simplify(self, n=100, debug=False):
        self.simplify_easy(debug)
        n_red = 0
        for k in range(n):
            n0 = 0
            newg = deepcopy(self)
            n1 = newg.reidemeister4()
            n0 += n1
            newg.reidemeister3()
            n1, n2, x, y, z = newg.simplify_easy()
            n0 += n1
            if n0 > 0:
                self.vertices = newg.vertices
                self.crossings = newg.crossings
                n_red += n0
        return n_red

    def reidemeister1(self, debug=False):
        """

        Args:
            g:

        Returns:

        """
        n_red, n_sign = 0, 0
        if len(self.crossings) == 1 and len(self.vertices) == 0:
            cross = self.crossings[0]
            if cross[0] == cross[1] or cross[2] == cross[3]:
                n_sign += 1
            if cross[1] == cross[2] or cross[0] == cross[3]:
                n_sign -= 1
            n_red += 1
            self.crossings = []
            self.vertices = [[0,0]]
            return n_red, n_sign

        translate = {}
        to_simplify = []
        for cross in self.crossings:
            if any(len(set([cross[k], cross[k - 1]])) < 2 for k in range(4)):
                for k in range(4):
                    if cross[k] == cross[k - 1]:
                        rev = ''
                        for key in translate.keys():
                            if translate[key] == cross[k - 2]:
                                rev = key
                        if cross[k - 2] in translate.keys():
                            translate[cross[k - 3]] = translate[cross[k - 2]]
                        elif cross[k - 3] in translate.keys():
                            translate[cross[k - 2]] = translate[cross[k - 3]]
                        elif rev:
                            translate[cross[k - 3]] = cross[k - 2]
                        else:
                            translate[cross[k - 2]] = cross[k - 3]
                        to_simplify.append(cross)

        code = [cross for cross in self.crossings if cross not in to_simplify]
        for cross in [c for c in self.crossings if c not in code]:
            if cross[0] == cross[1] or cross[2] == cross[3]:
                n_sign += 1
            if cross[1] == cross[2] or cross[0] == cross[3]:
                n_sign -= 1
            n_red += 1

        code = [[translate.get(key, key) for key in cross] for cross in code]
        vertices = [[translate.get(key, key) for key in vert] for vert in self.vertices]
        if not code and not vertices:
            vertices = [[0,0]]
        if debug:
            print "r1"
            print self.crossings
            print self.vertices
            print translate
            print "to_simplify: ", to_simplify
            print "code: ", code
            print "vertices: ", vertices

        self.crossings = code
        self.vertices = vertices
        return n_red, n_sign


    def reidemeister2(self, debug=False):
        to_simplify = []
        translate = {}
        for k in range(len(self.crossings)):
            c1 = self.crossings[k]
            if c1 in to_simplify:
                continue
            for l in range(k):
                c2 = self.crossings[l]
                if c2 in to_simplify:
                    continue
                sub1 = sorted([c1[0], c1[2], c2[0], c2[2]])
                sub2 = sorted([c1[1], c1[3], c2[1], c2[3]])
                if len(set(sub1)) < 4 and len(set(sub2)) < 4:
                    for i in range(4):
                        if sub1[i] == sub1[i - 1]:
                            rev = ''
                            for key in translate.keys():
                                if translate[key] == sub1[i - 2]:
                                    rev = key
                            if sub1[i - 2] in translate.keys():
                                translate[sub1[i - 3]] = translate[sub1[i - 2]]
                            elif sub1[i-3] in translate.keys():
                                translate[sub1[i - 2]] = translate[sub1[i - 3]]
                            elif rev:
                                translate[sub1[i - 3]] = sub1[i - 2]
                            else:
                                translate[sub1[i - 2]] = sub1[i - 3]
                        if sub2[i] == sub2[i - 1]:
                            rev = ''
                            for key in translate.keys():
                                if translate[key] == sub2[i - 2]:
                                    rev = key
                            if sub2[i - 2] in translate.keys():
                                translate[sub2[i - 3]] = translate[sub2[i - 2]]
                            elif sub2[i-3] in translate.keys():
                                translate[sub2[i - 2]] = translate[sub2[i - 3]]
                            elif rev:
                                translate[sub2[i - 3]] = sub2[i - 2]
                            else:
                                translate[sub2[i - 2]] = sub2[i - 3]
                    to_simplify.append(c1)
                    to_simplify.append(c2)
        code = [cross for cross in self.crossings if cross not in to_simplify]
        code = [[translate.get(key, key) for key in cross] for cross in code]
        n_red = len(self.crossings) - len(code)
        vertices = [[translate.get(key, key) for key in vert] for vert in self.vertices]
        if debug:
            print "r2"
            print self.crossings
            print self.vertices
            print translate
            print "to_simplify: ", to_simplify
            print "code: ", code
            print "vertices: ", vertices
            print '...'
        self.crossings = code
        self.vertices = vertices
        return n_red


    def reidemeister3(self,debug=False):
        triples = []
        # identifying triples of crossings
        for k in range(len(self.crossings)):
            c1 = self.crossings[k]
            for l in range(k):
                c2 = self.crossings[l]
                sub1 = sorted([c1[0], c1[2], c2[0], c2[2]])
                if len(set(sub1)) < 4:      # two consecutive crossings "under"
                    search = [[c1[1],c2[1]], [c1[3],c2[3]], [c2[1],c1[1]], [c2[3],c1[3]]]
                    for i in range(l):
                        c3 = self.crossings[i]
                        if any([element for element in search[k] if element in c3] == search[k] for k in range(4)):
                            nc1 = [c1[0], 0, c1[2], 0]
                            nc2 = [c2[0], 0, c2[2], 0]
                            nc3 = [0, 0, 0, 0]
                            if c3[0] in c1 and c3[3] in c2:
                                nc1[c1.index(c3[0])] = c3[1]
                                nc1[c1.index(c3[0]) - 2] = c3[3]
                                nc2[c2.index(c3[3])] = c3[2]
                                nc2[c2.index(c3[3]) - 2] = c3[0]
                                nc3[0] = c1[c1.index(c3[0])-2]
                                nc3[1] = c3[3]
                                nc3[2] = c3[0]
                                nc3[3] = c2[c2.index(c3[3])-2]
                            elif c3[0] in c2 and c3[3] in c1:
                                nc2[c2.index(c3[0])] = c3[1]
                                nc2[c2.index(c3[0]) - 2] = c3[3]
                                nc1[c1.index(c3[3])] = c3[2]
                                nc1[c1.index(c3[3]) - 2] = c3[0]
                                nc3[0] = c2[c2.index(c3[0])-2]
                                nc3[1] = c3[3]
                                nc3[2] = c3[0]
                                nc3[3] = c1[c1.index(c3[3])-2]
                            elif c3[2] in c1 and c3[1] in c2:
                                nc1[c1.index(c3[2])] = c3[3]
                                nc1[c1.index(c3[2]) - 2] = c3[1]
                                nc2[c2.index(c3[1])] = c3[0]
                                nc2[c2.index(c3[1]) - 2] = c3[2]
                                nc3[0] = c3[2]
                                nc3[1] = c2[c2.index(c3[1]) - 2]
                                nc3[2] = c1[c1.index(c3[2]) - 2]
                                nc3[3] = c3[1]
                            elif c3[2] in c2 and c3[1] in c1:
                                nc2[c2.index(c3[2])] = c3[3]
                                nc2[c2.index(c3[2]) - 2] = c3[1]
                                nc1[c1.index(c3[1])] = c3[0]
                                nc1[c1.index(c3[1]) - 2] = c3[2]
                                nc3[0] = c3[2]
                                nc3[1] = c1[c1.index(c3[1]) - 2]
                                nc3[2] = c2[c2.index(c3[2]) - 2]
                                nc3[3] = c3[1]
                            elif c3[0] in c2 and c3[1] in c1:
                                nc2[c2.index(c3[0])] = c3[3]
                                nc2[c2.index(c3[0]) - 2] = c3[1]
                                nc1[c1.index(c3[1])] = c3[2]
                                nc1[c1.index(c3[1]) - 2] = c3[0]
                                nc3[0] = c2[c2.index(c3[0])-2]
                                nc3[1] = c1[c1.index(c3[1])-2]
                                nc3[2] = c3[0]
                                nc3[3] = c3[1]
                            elif c3[0] in c1 and c3[1] in c2:
                                nc1[c1.index(c3[0])] = c3[3]
                                nc1[c1.index(c3[0]) - 2] = c3[1]
                                nc2[c2.index(c3[1])] = c3[2]
                                nc2[c2.index(c3[1]) - 2] = c3[0]
                                nc3[0] = c1[c1.index(c3[0])-2]
                                nc3[1] = c2[c2.index(c3[1])-2]
                                nc3[2] = c3[0]
                                nc3[3] = c3[1]
                            elif c3[2] in c2 and c3[3] in c1:
                                nc2[c2.index(c3[2])] = c3[1]
                                nc2[c2.index(c3[2]) - 2] = c3[3]
                                nc1[c1.index(c3[3])] = c3[0]
                                nc1[c1.index(c3[3]) - 2] = c3[2]
                                nc3[0] = c3[2]
                                nc3[1] = c3[3]
                                nc3[2] = c2[c2.index(c3[2]) - 2]
                                nc3[3] = c1[c1.index(c3[3]) - 2]
                            elif c3[2] in c1 and c3[3] in c2:
                                nc1[c1.index(c3[2])] = c3[1]
                                nc1[c1.index(c3[2]) - 2] = c3[3]
                                nc2[c2.index(c3[3])] = c3[0]
                                nc2[c2.index(c3[3]) - 2] = c3[2]
                                nc3[0] = c3[2]
                                nc3[1] = c3[3]
                                nc3[2] = c1[c1.index(c3[2]) - 2]
                                nc3[3] = c2[c2.index(c3[3]) - 2]
                            triples.append([[c1,c2,c3],[nc1,nc2,nc3]])
        if triples:
            to_simplify, additional = choice(triples)
            code = [cross for cross in self.crossings if cross not in to_simplify] + additional
        else:
            code = [cross for cross in self.crossings]
            to_simplify, additional = [], []
        if debug:
            print "r3"
            print self.crossings
            print self.vertices
            print "additional: ", additional
            print "to_simplify: ", to_simplify
            print "code: ", code
            print "triples: ", triples
        self.crossings = code
        return

    def reidemeister4(self, debug=False):
        if debug:
            print "r4"
            print self.crossings
            print self.vertices
        translate = {}
        to_simplify = []
        additional = []
        vert_to_trans = []
        found = False
        for vert in self.vertices:
            adjacent = []
            for cross in self.crossings:
                if len(set(vert+cross)) < len(set(vert)) + len(set(cross)):
                    adjacent.append(cross)
            if len(adjacent) not in [2,3]:
                continue
            if len(adjacent) == 3:
                sub_tri_bottom = [adjacent[0][0],adjacent[0][2],adjacent[1][0],adjacent[1][2],adjacent[2][0],adjacent[2][2]]
                if len(set(sub_tri_bottom)) == 4 and (set([adjacent[k][0] for k in range(3)]) == set(vert) or set([adjacent[k][2] for k in range(3)]) == set(vert)):   # three under:
                    to_simplify += adjacent
                    translate[adjacent[0][2]] = adjacent[0][0]
                    translate[adjacent[1][0]] = adjacent[0][0]
                    translate[adjacent[1][2]] = adjacent[0][0]
                    translate[adjacent[2][0]] = adjacent[0][0]
                    translate[adjacent[2][2]] = adjacent[0][0]
                    if adjacent[0][1] in vert:
                        translate[adjacent[0][3]] = vert[vert.index(adjacent[0][1])]
                        translate[adjacent[1][3]] = vert[vert.index(adjacent[1][1])]
                        translate[adjacent[2][3]] = vert[vert.index(adjacent[2][1])]
                    else:
                        translate[adjacent[0][1]] = vert[vert.index(adjacent[0][3])]
                        translate[adjacent[1][1]] = vert[vert.index(adjacent[1][3])]
                        translate[adjacent[2][1]] = vert[vert.index(adjacent[2][3])]
                    found = True
                    break
                sub_tri_top = [adjacent[0][1],adjacent[0][3],adjacent[1][1],adjacent[1][3],adjacent[2][1],adjacent[2][3]]
                if len(set(sub_tri_top)) == 4 and (set([adjacent[k][1] for k in range(3)]) == set(vert) or set([adjacent[k][3] for k in range(3)]) == set(vert)):   # three above:
                    to_simplify += adjacent
                    translate[adjacent[0][3]] = adjacent[0][1]
                    translate[adjacent[1][1]] = adjacent[0][1]
                    translate[adjacent[1][3]] = adjacent[0][1]
                    translate[adjacent[2][1]] = adjacent[0][1]
                    translate[adjacent[2][3]] = adjacent[0][1]
                    if adjacent[0][0] in vert:
                        translate[adjacent[0][2]] = vert[vert.index(adjacent[0][0])]
                    else:
                        translate[adjacent[0][0]] = vert[vert.index(adjacent[0][2])]
                    if adjacent[1][0] in vert:
                        translate[adjacent[1][2]] = vert[vert.index(adjacent[1][0])]
                    else:
                        translate[adjacent[1][0]] = vert[vert.index(adjacent[1][2])]
                    if adjacent[2][0] in vert:
                        translate[adjacent[2][2]] = vert[vert.index(adjacent[2][0])]
                    else:
                        translate[adjacent[2][0]] = vert[vert.index(adjacent[2][2])]
                    found = True
                    break
            if found:
                break
            for k in range(len(adjacent)):
                sub1 = [adjacent[k][0],adjacent[k][2],adjacent[k-1][0],adjacent[k-1][2]]
                if len(set(sub1)) < 4:      #two crossings below
                    to_simplify += [adjacent[k],adjacent[k-1]]
                    mis_vert = list(set(vert)-set([adjacent[k][1],adjacent[k][3],adjacent[k-1][1],adjacent[k-1][3]]))[0]
                    if adjacent[k][0] in adjacent[k-1]:
                        translate[mis_vert] = adjacent[k][0]
                        if adjacent[k][1] in vert:
                            translate[adjacent[k][3]] = adjacent[k][1]
                            translate[adjacent[k-1][3]] = adjacent[k-1][1]
                            nvert = [translate.get(key,key) for key in [adjacent[k-1][0],adjacent[k][0],adjacent[k][2],mis_vert]]
                            nvert[3] = mis_vert
                            additional.append(nvert)
                        else:
                            translate[adjacent[k][1]] = adjacent[k][3]
                            translate[adjacent[k-1][1]] = adjacent[k-1][3]
                            nvert = [translate.get(key,key) for key in [adjacent[k - 1][0], mis_vert, adjacent[k][2], adjacent[k][0]]]
                            nvert[1] = mis_vert
                            additional.append(nvert)
                    else:
                        translate[mis_vert] = adjacent[k-1][0]
                        if adjacent[k][1] in vert:
                            translate[adjacent[k][3]] = adjacent[k][1]
                            translate[adjacent[k-1][3]] = adjacent[k-1][1]
                            nvert = [translate.get(key,key) for key in [adjacent[k][0], adjacent[k - 1][0], adjacent[k - 1][2], mis_vert]]
                            nvert[3] = mis_vert
                            additional.append(nvert)
                        else:
                            translate[adjacent[k][1]] = adjacent[k][3]
                            translate[adjacent[k-1][1]] = adjacent[k-1][3]
                            nvert = [translate.get(key,key) for key in [adjacent[k][0], mis_vert, adjacent[k - 1][2], adjacent[k - 1][0]]]
                            nvert[1] = mis_vert
                            additional.append(nvert)
                    vert_to_trans.append(vert)
                    found = True
                    break
            if found:
                break
            for k in range(len(adjacent)):
                sub1 = [adjacent[k][1],adjacent[k][3],adjacent[k-1][1],adjacent[k-1][3]]
                if len(set(sub1)) < 4:      #two crossings above
                    to_simplify += [adjacent[k],adjacent[k-1]]
                    mis_vert = list(set(vert)-set([adjacent[k][0],adjacent[k][2],adjacent[k-1][0],adjacent[k-1][2]]))[0]
                    if adjacent[k][1] in adjacent[k-1]:
                        translate[mis_vert] = adjacent[k][1]
                        if adjacent[k][0] in vert:
                            translate[adjacent[k][2]] = adjacent[k][0]
                            translate[adjacent[k-1][2]] = adjacent[k-1][0]
                            nvert = [translate.get(key,key) for key in [mis_vert,adjacent[k-1][1],adjacent[k][1],adjacent[k][3]]]
                            nvert[0] = mis_vert
                            additional.append(nvert)
                        else:
                            translate[adjacent[k][0]] = adjacent[k][2]
                            translate[adjacent[k-1][0]] = adjacent[k-1][2]
                            nvert = [translate.get(key,key) for key in [adjacent[k][1],adjacent[k][3],mis_vert,adjacent[k-1][1]]]
                            nvert[2] = mis_vert
                            additional.append(nvert)
                    else:
                        translate[mis_vert] = adjacent[k-1][1]
                        if adjacent[k][0] in vert:
                            translate[adjacent[k][2]] = adjacent[k][0]
                            translate[adjacent[k-1][2]] = adjacent[k-1][0]
                            nvert = [translate.get(key,key) for key in [mis_vert,adjacent[k-1][3],adjacent[k][3],adjacent[k][1]]]
                            nvert[0] = mis_vert
                            additional.append(nvert)
                        else:
                            translate[adjacent[k][0]] = adjacent[k][2]
                            translate[adjacent[k-1][0]] = adjacent[k-1][2]
                            nvert = [translate.get(key,key) for key in [adjacent[k][3],adjacent[k][1],mis_vert,adjacent[k-1][3]]]
                            nvert[2] = mis_vert
                            additional.append(nvert)
                    vert_to_trans.append(vert)
                    found = True
                    break
            if found:
                break

        code = [cross for cross in self.crossings if cross not in to_simplify]
        code = [[translate.get(key, key) for key in cross] for cross in code] + additional
        vertices = [[translate.get(key, key) for key in v] for v in self.vertices if v not in vert_to_trans] + vert_to_trans

        if debug:
            print translate
            print "to_simplify: ", to_simplify
            print "additional: ", additional
            print "code: ", code

        self.vertices = vertices
        self.crossings = code
        return len(to_simplify)

    def reidemeister5(self, debug=False):
        """

        Args:
            g:

        Returns:

        """
        n_red, n_sign = 0, 0
        translate = {}
        to_simplify = []
        vert = set([y for x in self.vertices for y in x])
        for vertex in self.vertices:
            for cross in self.crossings:
                for k in range(4):
                    if cross[k] in vertex and cross[k-1] in vertex and vertex.index(cross[k-1])-vertex.index(cross[k]) == 1:
                        translate[cross[k - 2]] = cross[k]
                        translate[cross[k - 3]] = cross[k-1]
                        self.crossings = [[translate.get(key, key) for key in c] for c in self.crossings if c != cross]
                        self.vertices = [[translate.get(key, key) for key in vert] for vert in self.vertices if vert != vertex]
                        vertex[vertex.index(cross[k-1])], vertex[vertex.index(cross[k])] = vertex[vertex.index(cross[k])], vertex[vertex.index(cross[k-1])]
                        self.vertices.append([translate.get(key, key) for key in vertex])
                        n_red += 1
                        if k%2 == 0:
                            n_sign -= 1
                        else:
                            n_sign += 1
                        return n_red, n_sign
        return n_red, n_sign


    ######## Polynomial calculations ########
    def kauffman_bracket(self):
        poly = laurent()
        for state in itertools.product(range(-1,2,2), repeat=len(self.crossings)):
            if not state:
                poly_state = laurent(1)
            else:
                g = deepcopy(self)
                for k in state:
                    g = g.smooth_crossing(typ=k)
                # polynomial for a given state (sequence of smoothings)
                poly_state = laurent('A^' + str(sum(state)) + 'k^' + str(max(0,g.get_loop_nr()-1)))
                # substitution for k =(-A^2 -A^-2)
                poly_state = poly_state({"k":'(-A^2 - A^-2)'})
            poly += poly_state
        return poly

    def jones_polynomial(self):
        poly = self.kauffman_bracket()
        # print self.get_writhe()
        poly = poly * laurent('A^' + str(-3*self.get_writhe()))
        if self.get_writhe() % 2 == 1:
            poly = poly * laurent('-1')
        poly = poly({"A": 'q^0.25'})
        return poly


    def yamada_h_subgraph(self, n0):
        """ Subgraph xxxxx

        Parameters
        ----------
        n0 : int
            xxxxxxxx

        Returns
        -------
        list ???
            xxxxxx
        """

        mu = self.get_connected_components_number()
        beta = self.get_betti_1()
        n = n0 - len(self.get_edges())
        return laurent(str((-1)**n) + 'x^' + str(mu-n) + 'y^' + str(beta))


    def yamada_two_variable(self):
        if len(self.vertices) == 0 and len(self.crossings) == 0:
            return laurent(1)
        poly = laurent()
        edges = self.get_edges()
        n = len(edges)
        subsets = [range(n)]
        for m in range(n):
            for perm in itertools.combinations(range(n), m):
                subsets.append(list(set(perm)))
        for subset in subsets:
            tmp = set()
            for element in subset:
                tmp |= edges[element]
            code = ''
            for vertex in self.vertices:
                code += 'V['
                for edge in vertex:
                    if edge in tmp:
                        code += str(edge) + ','
                if code[-1] == ',':
                    code = code[:-1]
                code += ']\n'
            for cross in self.crossings:
                code += 'V['
                for edge in cross:
                    if edge in tmp:
                        code += str(edge) + ','
                if code[-1] == ',':
                    code = code[:-1]
                code += ']\n'
            g=Graph(code[:-1])
            poly += g.yamada_h_subgraph(n)
        return poly

    def yamada_polynomial(self, debug=False, level=0):
        com = '   '.join(['' for _ in range(level+1)]) + '|-> '
        if not self.vertices and not self.crossings:
            if debug:
                print com + "Got " + repr(self.get_PDcode()).strip() + "; No vertex, no crossing, returning 1"
            return laurent(1)
        if len(self.crossings) == 1 and len(self.vertices) == 0:
            if debug:
                print com + "Got " + repr(self.get_PDcode()).strip() + "; Only one crossing, no vertex - it's a circle; Returning A+1+A^-1"
            return laurent('A+1+A^-1')
        if len(self.crossings) == 0 and self.is_loop():
            if debug:
                print com + "Got " + repr(self.get_PDcode()).strip() + "; It's a circle; Returning A+1+A^-1"
            return laurent('A+1+A^-1')

        # split sum
        subgraphs = self.create_disjoined_components()
        if len(subgraphs) > 1:      # split sum
            if debug:
                print com + "Got " + repr(self.get_PDcode()).strip() + "; Number of components > 1; Obtained subgraphs: ", subgraphs
            res = laurent(1)
            for subgraph in subgraphs:
                graph_tmp = Graph(subgraph)
                x, y, n1_sign, n5_tot, n5_sign = graph_tmp.simplify_easy()
                code = graph_tmp.get_PDcode()
                if debug:
                    print com + 'A^' + str(2*n1_sign) + '*', repr(code)
                res *= laurent('A^' + str(2 * n1_sign)) * graph_tmp.yamada_polynomial(debug, level + 1)
            return res

        # bouquet of circles
        if len(self.vertices) == 1 and len(self.crossings) == 0:
            if debug:
                print com + "Got " + repr(self.get_PDcode()).strip() + "; A bouquet of " + str(len(set(self.vertices[0]))) + " circles; Returning ", laurent('-1') * laurent('-A-1-A^-1')**len(set(self.vertices[0]))
            return laurent('-1') * laurent('-A-1-A^-1')**len(set(self.vertices[0]))

        # crossing smoothings
        if len(self.crossings) > 0:
            if debug:
                print com + "Got " + repr(self.get_PDcode()).strip() + "; Reducing crossing ", self.crossings[0]
            res = laurent(0)
            # A smoothing
            code = deepcopy(self.crossings[1:])
            vertices = deepcopy(self.vertices)
            vertices.append([self.crossings[0][0], self.crossings[0][1]])
            vertices.append([self.crossings[0][2], self.crossings[0][3]])
            if len(code) > 0:
                code = "X" + '\nX'.join([str(cross) for cross in code]) + '\n'
            else:
                code = ''
            if len(vertices) > 0:
                code += 'V' + '\nV'.join(str(vert) for vert in vertices) + '\n'
            graph_tmp = Graph(code)
            x, y, n1_sign, n5_tot, n5_sign = graph_tmp.simplify_easy()
            code = graph_tmp.get_PDcode()
            if debug:
                print com + 'A^' + str(2*n1_sign+1) + '*', repr(code)
            res += laurent('A^' + str(2*n1_sign+1)) * graph_tmp.yamada_polynomial(debug, level + 1)

            # A^-1 smoothing
            code = deepcopy(self.crossings[1:])
            vertices = deepcopy(self.vertices)
            vertices.append([self.crossings[0][0], self.crossings[0][3]])
            vertices.append([self.crossings[0][1], self.crossings[0][2]])
            if len(code) > 0:
                code = "X" + '\nX'.join([str(cross) for cross in code]) + '\n'
            else:
                code = ''
            if len(vertices) > 0:
                code += 'V' + '\nV'.join(str(vert) for vert in vertices) + '\n'
            graph_tmp = Graph(code)
            x, y, n1_sign, n5_tot, n5_sign = graph_tmp.simplify_easy()
            code = graph_tmp.get_PDcode()
            if debug:
                print com + 'A^' + str(2 * n1_sign-1) + '*', repr(code)
            res += laurent('A^' + str(2*n1_sign-1)) * graph_tmp.yamada_polynomial(debug, level + 1)

            # vertex smoothing
            vertices = deepcopy(self.vertices) + [self.crossings[0]]
            code = 'V' + '\nV'.join(str(vert) for vert in vertices) + '\n'
            if len(self.crossings) > 1:
                code += "X" + '\nX'.join([str(cross) for cross in self.crossings[1:]])
            graph_tmp = Graph(code)
            x, y, n1_sign, n5_tot, n5_sign = graph_tmp.simplify_easy()
            code = graph_tmp.get_PDcode()
            if debug:
                print com + 'A^' + str(2 * n1_sign + n5_sign) + '*', repr(code)
            res += laurent('A^' + str(2*n1_sign + n5_sign)) * graph_tmp.yamada_polynomial(debug, level + 1)

            return res

        # edge reducing
        if len(self.vertices) > 1:
            for k in range(1,len(self.vertices)):
                for l in range(k):
                    common = [v for v in self.vertices[k] if v in self.vertices[l]]
                    if len(common) > 0:
                        if debug:
                            print com + "Got " + repr(self.get_PDcode()).strip() + "; Reducing non-loop edge: V"+str(self.vertices[k]) + '<-' + str(common[0]) + '->V' + str(self.vertices[l])
                        res = laurent(0)
                        # edge removal
                        vertices = deepcopy(self.vertices)
                        vertices[k].pop(vertices[k].index(common[0]))
                        vertices[l].pop(vertices[l].index(common[0]))
                        if len(self.crossings) > 0:
                            code = "X" + '\nX'.join([str(cross) for cross in self.crossings]) + '\n'
                        else:
                            code = ''
                        if len(vertices) > 0:
                            code += 'V' + '\nV'.join(str(vert) for vert in vertices) + '\n'
                        graph_tmp = Graph(code)
                        if len(graph_tmp.get_connected_components()) > len(self.get_connected_components()):
                            if debug:
                                print com + 'Cut edge. Returning 0.'
                            return laurent(0)
                        x, y, n1_sign, n5_tot, n5_sign = graph_tmp.simplify_easy()
                        code = graph_tmp.get_PDcode()
                        if debug:
                            print com + '*A^' + str(2 * n1_sign) + '*', repr(code)
                        res += laurent('A^' + str(2 * n1_sign)) * graph_tmp.yamada_polynomial(debug,level + 1)
                        # edge contraction
                        vertices = deepcopy(self.vertices)
                        vertices[k].pop(vertices[k].index(common[0]))
                        vertices[l].pop(vertices[l].index(common[0]))
                        vertices.append(vertices[k] + vertices[l])
                        vertices.pop(k)
                        vertices.pop(l)
                        code = 'V' + '\nV'.join(str(vert) for vert in vertices) + '\n'
                        if len(self.crossings) > 0:
                            code += "X" + '\nX'.join([str(cross) for cross in code]) + '\n'
                        graph_tmp = Graph(code)
                        x, y, n1_sign, n5_tot, n5_sign = graph_tmp.simplify_easy()
                        code = graph_tmp.get_PDcode()
                        if debug:
                            print com + '*A^' + str(2 * n1_sign) + '*', repr(code)
                        res += laurent('A^' + str(2 * n1_sign)) * graph_tmp.yamada_polynomial(debug, level + 1)

                        # if debug:
                        #     print repr(code)
                        return res
        return laurent(1)


    def yamada_polynomial_combinatorial(self):
        poly = laurent()
        for state in itertools.product(range(-1,2), repeat=len(self.crossings)):
            if not state:
                poly_state = self.yamada_two_variable()
                poly_state = poly_state({"x": -1, "y": '-A -2 -A^-1'})

            else:
                g = deepcopy(self)
                for k in state:
                    g = g.smooth_crossing(typ=k)
                # polynomial for a given state (sequence of smoothings)
                poly_tmp = g.yamada_two_variable()
                # including the free loops
                poly_factor = laurent('xy - 1')**max(0,g.get_loop_nr())
                poly_tmp *= poly_factor
                # substitution
                poly_tmp = poly_tmp({"x": -1, "y": '-A -2 -A^-1'})
                poly_state = laurent('A^' + str(sum(state))) * poly_tmp
            poly += poly_state
        return poly


    def aps_bracket(self):
        poly = laurent()
        for state in itertools.product(range(2), repeat=len(self.double_edges)):
            g = deepcopy(self)
            for k in state:
                g = g.smooth_double(typ=k)
            # polynomial for a given state (sequence of smoothings)
            poly_state = g.kauffman_bracket() * laurent('k^' + str(max(0,g.loop_nr-1)))
            nC = sum(state)
            nD = len(state) - nC
            poly_state = poly_state * laurent('C^' + str(nC) + 'D^' + str(nD))
            # substitution for k =(-A^2 -A^-2)
            poly_state = poly_state({"k": '(-A^2 - A^-2)'})
            poly += poly_state
        return poly

    def aps_ps(self):
        poly = self.aps_bracket()
        return poly({"C": 'S+A^2P+A^-2P', "D": 'P+A^2S+A^-2S'})

    def sirp(self):
        poly = self.aps_bracket()
        return poly({"C": 'tA^-2', "D": 't-tA^4'})

    def aps_weights(self):
        poly = self.aps_ps()
        weights = {}
        for t in poly.term:
            if 'S' in t.degree.keys():
                sdeg = t.degree['S']
            else:
                sdeg = 0
            if 'P' in t.degree.keys():
                pdeg = t.degree['P']
            else:
                pdeg = 0
            p_tmp = laurent('S^'+str(sdeg)+'P^'+str(pdeg))
            if str(p_tmp) not in weights.keys():
                weights[str(p_tmp)] = 0
            weights[str(p_tmp)] += float(t.coef**2)/self.aps_weight_norm(pdeg+sdeg)

        for key in weights.keys():
            weights[key] = sqrt(weights[key])
        print(weights)
        return weights

    def aps_weight_norm(self, n):
        p_tmp = laurent('1-k^2')**n
        s = 0
        for t in p_tmp({"k":'(-A^2 - A^-2)'}).term:
            s += t.coef**2
        return s


    def kauffman_boundary(self):
        # join parts of PD code into three arcs
        arcs = self.find_paths()

        # calculate the number of twists
        n = self.calculate_twists(arcs)

        # make graph paralelization
        ncrossings, narcs, joints = self.make_paralelization(arcs)

        # add twists. Obtain graph along with the intervals constituting compnents
        new_g, components = self.add_twists(n, arcs, narcs, ncrossings, joints)

        # extract link
        link0, link1, link2 = new_g.extract_double_links(components)

        return link0, link1, link2

    ######## smoothing ########
    def smooth_crossing(self, typ, ind=0):
        # smoothings denote the connection of edges. Which edge connect to which is saved in dictionary trans
        trans = {}
        code = ''
        loop_nr = self.loop_nr
        if typ == 1:
            pair = sorted(self.crossings[ind][:2])
            trans[pair[1]] = pair[0]
            pair = sorted(self.crossings[ind][2:4])
            if pair[1] not in trans.keys():
                trans[pair[1]] = pair[0]
            else:
                if pair[0] != trans[pair[1]]:
                    triple = sorted([pair[0], pair[1], trans[pair[1]]])
                    trans[triple[1]] = triple[0]
                    trans[triple[2]] = triple[0]
        if typ == -1:
            pair = sorted([self.crossings[ind][0], self.crossings[ind][3]])
            trans[pair[1]] = pair[0]
            pair = sorted(self.crossings[ind][1:3])
            if pair[1] not in trans.keys():
                trans[pair[1]] = pair[0]
            else:
                if pair[0] != trans[pair[1]]:
                    triple = sorted([pair[0], pair[1], trans[pair[1]]])
                    trans[triple[1]] = triple[0]
                    trans[triple[2]] = triple[0]
        # sometimes it is 5->3, 3->2, so to avoid:
        for key in trans.keys():
            if trans[key] in trans.keys():
                trans[key] = trans[trans[key]]
        for k in range(len(self.crossings)):
            if k == ind:
                if typ == 0:
                    code += 'V' + str(self.crossings[k]) + '\n'
                continue
            code_tmp = self.crossings[k]
            for j in range(len(code_tmp)):
                if code_tmp[j] in trans.keys():
                    code_tmp[j] = trans[code_tmp[j]]
            code += 'X' + str(code_tmp) + '\n'
        for k in range(len(self.vertices)):
            code_tmp = self.vertices[k]
            for j in range(len(code_tmp)):
                if code_tmp[j] in trans.keys():
                    code_tmp[j] = trans[code_tmp[j]]
            code += 'V' + str(code_tmp) + '\n'

        # two ways the crossing can result in a loop or pairs of loops
        for key in trans.keys():
            if trans[key] == key:
                loop_nr += 1
        if len(trans.keys()) == 1:
            loop_nr += 1
        return Graph(code, loop_nr)

    def smooth_double(self, typ, ind=0):
        trans = {}
        vertices = []
        indices = []
        code = ''
        loop_nr = self.loop_nr
        edge = list(self.double_edges)[ind]
        for vertex in self.vertices:
            if edge in vertex:
                vertices.append(vertex)
                indices.append(vertex.index(edge))
        # C-type smoothing
        if typ == 1:
            for vertex in vertices:
                pair = vertex
                pair.pop(vertex.index(edge))
                pair.sort()
                if pair[1] not in trans.keys():
                    trans[pair[1]] = pair[0]
                else:
                    if pair[0] != trans[pair[1]]:
                        triple = sorted([pair[0], pair[1], trans[pair[1]]])
                        trans[triple[1]] = triple[0]
                        trans[triple[2]] = triple[0]
        # D-type smoothing:
        if typ == 0:
            pair = sorted([vertices[0][indices[0]-1], vertices[1][(indices[1]+1)%3]])
            trans[pair[1]] = pair[0]
            pair = sorted([vertices[1][indices[1]-1], vertices[0][(indices[0]+1)%3]])
            if pair[1] not in trans.keys():
                trans[pair[1]] = pair[0]
            else:
                if pair[0] != trans[pair[1]]:
                    triple = sorted([pair[0], pair[1], trans[pair[1]]])
                    trans[triple[1]] = triple[0]
                    trans[triple[2]] = triple[0]
        for k in range(len(self.crossings)):
            code_tmp = str(self.crossings[k])
            # sometimes it is 3->2, 5->3, so that is why it is doubled
            for key in trans:                   # TODO Make it better
                code_tmp = code_tmp.replace(str(key), str(trans[key]))
            for key in trans:
                code_tmp = code_tmp.replace(str(key), str(trans[key]))
            code += 'X' + code_tmp + '\n'
        for vertex in self.vertices:
            if vertex in vertices:
                continue
            code_tmp = str(vertex)
            for key in trans:
                code_tmp = code_tmp.replace(str(key), str(trans[key]))
            for key in trans:
                code_tmp = code_tmp.replace(str(key), str(trans[key]))
            code += 'V' + code_tmp + '\n'

        # two ways the crossing can result in a loop or pairs of loops
        for key in trans.keys():
            if trans[key] == key:
                loop_nr += 1
        if len(trans.keys()) == 1:
            loop_nr += 1
        return Graph(code, loop_nr)

    ######## Graph manipulation ########
    def __reversed__(self):
        # reversing graph orientation
        code = ''
        for crossing in self.crossings:
            ncross = crossing[2:] + crossing[:2]
            code += 'X[' + ','.join([str(x) for x in ncross]) + ']\n'
        return Graph(code)

    def change_chirality(self):
        # reversing each crossin of the graph
        code = ''
        for crossing in self.crossings:
            code += 'X[' + str(crossing[-1]) + ',' + ','.join([str(x) for x in crossing[:-1]]) + ']\n'
        for vertex in self.vertices:
            code += 'V' + str(vertex) + '\n'
        return Graph(code)

    ######## General functions ########
    # merge lists with common elements
    def find_connections(self, array):
        out = []
        while len(array) > 0:
            first, rest = array[0], array[1:]
            first = set(first)
            lf = -1
            while len(first) > lf:
                lf = len(first)
                rest2 = []
                for r in rest:
                    if len(first.intersection(set(r))) > 0:
                        first |= set(r)
                    else:
                        rest2.append(r)
                rest = rest2
            out.append(first)
            array = rest
        return out

    def calculate_twists(self, arcs):
        # orient the arcs from first to second vertex
        for k in range(len(arcs)):
            if arcs[k][0] not in self.vertices[0]:
                arcs[k] = list(reversed(arcs[k]))
        # dictionary of signed sums of crossings
        w = {}
        for pair in [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]:
            w[pair] = 0
        # calculation of signed sums of crossings between arcs
        for cross in self.crossings:
            pair = []  # which arcs cross
            pairs = []  # what are the orientations in crossing
            for k in range(len(arcs)):
                arc = arcs[k]
                if cross[0] in arc:
                    pair.append(k)
                    if cross[2] == arc[arc.index(cross[0]) - 1]:
                        pairs.append(-1)
                    else:
                        pairs.append(1)
                if cross[1] in arc:
                    pair.append(k)
                    if cross[3] == arc[arc.index(cross[1]) - 1]:
                        pairs.append(-1)
                    else:
                        pairs.append(1)
            sign = -pairs[0] * pairs[1]
            w[tuple(sorted(pair))] += sign

        # calculate number of twists
        n = {}
        a0 = -2 * (w[(0, 0)] + w[(1, 1)] - w[(0, 1)])
        a1 = -2 * (w[(1, 1)] + w[(2, 2)] - w[(1, 2)])
        a2 = -2 * (w[(0, 0)] + w[(2, 2)] - w[(0, 2)])
        n[0] = (a0 + a2 - a1) / 2
        n[1] = (a0 + a1 - a2) / 2
        n[2] = (a1 + a2 - a0) / 2
        return n

    def make_paralelization(self, arcs):
        intervals = set()
        ncrossings = []
        for crossing in self.crossings:
            s1 = ['R', 'L']
            s2 = ['R', 'L']
            for arc in arcs:
                if crossing[0] in arc:
                    if arc.index(crossing[0]) > arc.index(crossing[2]):
                        s1 = list(reversed(s1))
                if crossing[1] in arc:
                    if arc.index(crossing[1]) > arc.index(crossing[3]):
                        s2 = list(reversed(s2))
            c = [str(x) for x in crossing]
            newcross = []
            newcross.append(','.join([c[0]+s1[0],c[1]+s2[1],c[0]+'-'+c[2]+s1[0],c[1]+'-'+c[3]+s2[1]]))
            newcross.append(','.join([c[0]+'-'+c[2]+s1[0],c[1]+s2[0],c[2]+s1[0],c[1]+'-'+c[3]+s2[0]]))
            newcross.append(','.join([c[0]+s1[1],c[1]+'-'+c[3]+s2[1],c[0]+'-'+c[2]+s1[1],c[3]+s2[1]]))
            newcross.append(','.join([c[0]+'-'+c[2]+s1[1],c[1]+'-'+c[3]+s2[0],c[2]+s1[1],c[3]+s2[0]]))
            ncrossings += newcross
            for cross in newcross:
                intervals |= set(cross.split(','))
        narcs = self.find_arcs_parallel(ncrossings)
        joints = []
        # outgoing vertex
        vert = self.vertices[0]
        for k in range(len(vert)):          # TODO recode this
            joints.append([str(vert[k]) + 'R0', str(vert[k - 1]) + 'L0'])
        # ingoing vertex
        vert = self.vertices[1]
        for k in range(len(vert)):
            joints.append([str(vert[k]) + 'L', str(vert[k - 1]) + 'R'])
        return ncrossings, narcs, joints

    def add_twists(self, n, arcs, narcs, crossings, joints):
        npaths = []
        code = ''
        replaces = []
        # adding twists to each arc (obtaining additional paths and crossings)
        for k in range(len(arcs)):
            paralels = []
            for arc in narcs:
                if str(arcs[k][0]) + 'L' in arc:
                    if str(arcs[k][0]) + 'L' == arc[0]:
                        paralels.append(arc)
                    else:
                        paralels.append(list(reversed(arc)))
                if str(arcs[k][0]) + 'R' in arc:
                    if str(arcs[k][0]) + 'R' == arc[0]:
                        paralels.append(arc)
                    else:
                        paralels.append(list(reversed(arc)))
            paths, ncrossings = self.add_twists_arc(n[k], paralels)
            npaths += paths
            crossings += ncrossings

        # joining paths
        paths = []
        trans = {}
        while npaths:
            paths.append(npaths.pop())
            while paths[-1][0] != paths[-1][-1]:
                end = paths[-1][-1]
                for pair in joints:
                    if end in pair:
                        nvert = pair[pair.index(end) - 1]
                        break
                trans[end] = nvert
                if nvert == paths[-1][0]:
                    break
                for path in npaths:
                    if nvert in path:
                        if nvert == path[0]:
                            paths[-1] = paths[-1][:-1] + path
                        else:
                            paths[-1] = paths[-1][:-1] + list(reversed(path))
                        npaths.pop(npaths.index(path))
            trans[paths[-1][-1]] = paths[-1][0]
            paths[-1] = paths[-1][:-1] + [paths[-1][0]]

        # updating the removed intervals in crossings
        for k in range(len(crossings)):
            cross = crossings[k].split(',')
            for key in trans.keys():
                if key in cross:
                    cross[cross.index(key)] = trans[key]
            crossings[k] = ','.join(cross)

        # translating the crossings using new interval numbering from paths
        # intervals are numbered as consecutive in the arcs, i.e. indices after list flatten
        intervals = [item for path in paths for item in path]
        for k in range(len(crossings)):
            cross = crossings[k].split(',')
            for interval in intervals:
                if interval in cross:
                    cross[cross.index(interval)] = 1+intervals.index(interval)
            code += 'X' + str(cross) + '\n'
        code = code[:-1]
        components = []
        length = 0
        for path in paths:
            components.append(range(1+length, 1+length+len(path)))
            length += len(path)
        return Graph(code), components

    def add_twists_arc(self, n, paralels):
        starting = paralels[0][0][:-1]
        crossings = []
        paths = [[starting+'L0'], [starting+'R0']]
        last = ['L', 'R']
        for k in range(abs(n)):
            if n > 0:
                cross = ','.join([starting+'R'+str(k), starting+'R'+str(k+1), starting+'L'+str(k+1), starting+'L'+str(k)])
                cross = cross.replace('R' + str(abs(n)), 'R').replace('L' + str(abs(n)), 'L')
            if n < 0:
                cross = ','.join([starting+'L'+str(k), starting+'R'+str(k), starting+'R'+str(k+1), starting+'L'+str(k+1)])
                cross = cross.replace('R' + str(abs(n)), 'R').replace('L' + str(abs(n)), 'L')
            crossings.append(cross)
            last = list(reversed(last))
            if k != abs(n) - 1:
                paths[0].append(starting + last[0] + str(k + 1))
                paths[1].append(starting + last[1] + str(k + 1))
        for path in paralels:
            if starting + last[0] in path:
                paths[0] += path
            if starting + last[1] in path:
                paths[1] += path
        return paths, crossings,

    def extract_double_links(self, components):
        codes = []
        pairs = [(0,1), (1,2), (0,2)]
        for k in range(len(pairs)):
            codes.append('')
            crossings_tmp = deepcopy(self.crossings)
            trans = []
            span = components[pairs[k][0]] + components[pairs[k][1]]
            codes.append('')
            j = 0
            while j < len(crossings_tmp):
                cross = crossings_tmp[j]
                if cross[0] not in span or cross[1] not in span:
                    crossings_tmp.pop(j)
                    j -= 1
                    trans.append([cross[0], cross[2]])
                    trans.append([cross[1], cross[3]])
                j += 1
            intervals = list(set([item for cross in crossings_tmp for item in cross]) & set([item for pair in trans for item in pair]))
            trans2 = {}
            while intervals:
                vert = intervals.pop()
                nvert = vert
                while nvert not in intervals:
                    for pair in trans:
                        if nvert in pair:
                            nvert = pair[pair.index(nvert)-1]
                            trans.pop(trans.index(pair))
                            break
                intervals.pop(intervals.index(nvert))
                trans2[vert] = nvert
            crossings_tmp = self.update_intervals(crossings_tmp, trans2)
            paths = self.find_paths(crossings_tmp)
            intervals = [item for path in paths for item in path]
            trans3 = {}
            for j in range(len(intervals)):
                trans3[intervals[j]] = j + 1
            crossings_tmp = self.update_intervals(crossings_tmp, trans3)
            for cross in crossings_tmp:
                codes[k] += 'X' + str(cross) + '\n'
        return Graph(codes[0]), Graph(codes[1]), Graph(codes[2])

    def find_arcs_parallel(self, crossings):
        arcs = []
        starting_set = set()
        for vertex in self.vertices:
            for v in vertex:
                starting_set |= {str(v)+'R', str(v)+'L'}
        starting_set = sorted(list(starting_set))
        while starting_set:
            old = starting_set.pop(0)
            arc = [old]
            found = True
            while found:
                found = False
                for cross in crossings:
                    c = cross.split(',')
                    if old in c:
                        new = c[c.index(old)-2]
                        if new in arc:
                            continue
                        arc.append(new)
                        old = new
                        found = True
                        break
            if list(reversed(arc)) not in arcs:
                arcs.append(arc)
        return arcs

    def update_intervals(self, crossings, trans):
        for k in range(len(crossings)):
            cross = crossings[k]
            for l in range(len(cross)):
                c = cross[l]
                if c in trans.keys():
                    cross[l] = trans[c]
            crossings[k] = cross
        return crossings

    def find_paths(self, crossings=[], vertices = []):
        if not crossings:
            crossings = self.crossings
        if not vertices:
            vertices = self.vertices
        pairs = []
        paths = []
        for cross in crossings:
            pairs.append([cross[0], cross[2]])
            pairs.append([cross[1], cross[3]])
        intervals = sorted(list(set([item for cross in crossings for item in cross]) | set([item for vert in vertices for item in vert])))
        while intervals:
            path = []
            nvert = intervals[0]
            while nvert in intervals:
                intervals.pop(intervals.index(nvert))
                path.append(nvert)
                for pair in pairs:
                    if nvert in pair:
                        nvert = pair[pair.index(nvert)-1]
                        pairs.pop(pairs.index(pair))
                        break
            paths.append(path)
        return paths