#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 12:49:58 2018

@author: bartosz
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import argparse
from tqdm import trange, tqdm
from time import perf_counter

class Polygons(object):
    def __init__(self, no_of_sides, len_of_tail, no_of_polygons, is_loop_closed, number_of_process=0):
        self.nos = no_of_sides
        self.nop = no_of_polygons
        self.lot = len_of_tail
        
        self.start_num = no_of_polygons * number_of_process
        
        self.vec_d      = np.zeros([self.nos-1, self.nop], order='F')  # diagonal lengths
        self.vec_theta  = np.zeros([self.nos-2, self.nop], order='F')  # dihedral angles
        self.loop_coors = np.zeros([3, self.nos, self.nop], order='F')
        self.tail_coors = np.zeros([3, self.lot, self.nop], order='F')
        self.lasso_coors = None

        self.passed = 0
        self.failed = 0

        #print(self.vec_d.strides)
        
        start = perf_counter()
        self.gen_diagonals()
        end = perf_counter()
        #print(end - start)
        
        self.calc_loop_vertices()
        if is_loop_closed == True:
            self.close_polygon()
        if self.lot > 0:
            self.gen_tail()
            self.join_loop_tail()
        if self.lot == 0:
            self.lasso_coors = self.loop_coors
        
        
    def join_loop_tail(self):
        self.lasso_coors = np.hstack([self.loop_coors, self.tail_coors])

    def close_polygon(self):
        self.loop_coors = np.concatenate((self.loop_coors[:,:,:], self.loop_coors[:,0,:].reshape(3,1,self.nop)), axis = 1)
    
    def gen_diagonals(self):
        #for p in trange(self.nop, desc = 'Losowanie przekątnych {:d}-kątów'.format(self.nos)):
        for p in range(self.nop):
            while 1:
                while 1:
                    s               = np.zeros(self.nos-1) # s[0] = 0 for numeration consistency with Canterella_2016
                    s[1:self.nos-2] = np.random.uniform(-1,1,self.nos-3)
                    s[self.nos-2]   = -np.sum(s)
                    if np.greater(np.abs(s[self.nos-2]), 1):
                        self.failed += 1
                    else:
                        break
                d = np.ones(self.nos-1)       # d[0] = 1 for numeration consistency with Canterella_2016 (also d[n-2] = 1)
                for i in range(1,self.nos-2): 
                    d[i] = d[i-1] + s[i]
                if np.any(np.less(d[:-1] + d[1:], 1)):
                    self.failed += 1
                else:
                    self.passed += 1
                    break
            theta = np.random.uniform(0,2*np.pi,self.nos-3)
            self.vec_d[:,p] = d
            self.vec_theta[1:,p] = theta # theta[0] = 0 for numeration consistency with Canterella_2016

    def calc_loop_vertices(self): # d1 = [x1, x2, x3]
        p0 = np.zeros([3,self.nop])
        p1 = np.vstack([np.ones([self.nop]).reshape([1,self.nop]), np.zeros([2,self.nop])])
        self.loop_coors[:,0,:] = p0
        self.loop_coors[:,1,:] = p1
        for i in range(2, self.nos):
            d2_len = self.vec_d[i-1,:]
            d1_len = self.vec_d[i-2,:]
            d1     = self.loop_coors[:,i-1,:]
            theta  = self.vec_theta[i-2,:]
            
            alpha, betha = self.rotate(d1)
            x   = (np.square(d1_len) - 1 + np.square(d2_len)) / (2 * d1_len)
            rho = np.sqrt(np.square(d2_len) - np.square(x))
            y   = rho * np.cos(theta)
            z   = rho * np.sin(theta)
            self.loop_coors[:,i,:] = self.unrotate([x,y,z],alpha,betha)
            #print(np.sum(np.square(self.loop_coors[:,i,:] - self.loop_coors[:,i-1,:])))
            #if i==3:
            #    self.tmp = np.zeros([3,4])
            #    self.tmp[:,0] = np.array(d1).flatten()
            #    self.tmp[:,1] = np.array([d1_len,0,0]).flatten()
            #    self.tmp[:,2] = np.array(self.loop_coors[:,i,:]).flatten()
            #    self.tmp[:,3] = np.array([x,y,z]).flatten()
            #    print(alpha/np.pi*180,betha/np.pi*180)


    def rotate(self,v): # rotate vector v = [x,y,z] -> w = [d,0,0] (d = length of v)
        x,y,z = v
        #       | 1     0           0      |      | cos(betha) -sin(betha) 0 |
        #   A = | 0 cos(alpha) -sin(alpha) |  B = | sin(betha)  cos(betha) 0 |
        #       | 0 sin(alpha)  cos(alpha) |      |     0           0      1 |
        alpha = np.arctan2(-z,y)
        #       |            x                |
        #  Av = | y cos(alpha) - z sin(alpha) |
        #       | y sin(alpha) + z cos(alpha) |
        # third component equal to zero gives condition on angle alpha that rotates v to the XY plane
        betha = np.arctan2( +z*np.sin(alpha) - y*np.cos(alpha), x )
        #       | x cos(betha) - sin(betha)[y cos(alpha) - z sin(alpha)] |
        # BAv = | z sin(betha) + cos(betha)[y cos(alpha) - z sin(alpha)] |
        #       |                         0                              |
        # second component equal to zero gives condition on angle betha that rotates Av to the x-axis
        return alpha, betha

    def unrotate(self,w,alpha,betha): # unrotates vector rotated by B(betha)A(alpha)
        w = np.array(w)
        alpha = np.array(alpha)
        betha = np.array(betha)
        # A(-alpha)B(-betha)
        try: zero = np.zeros(len(alpha))#; one = np.ones(len(alpha))
        except: zero = 0#; one = 1
        # TRANSPOSED, BUT DOESN'T LOOK LIKE (bracket order), transposition handled by np.einsum
        AB = np.array([[         np.cos(betha),               np.sin(betha),             zero      ],
                       [ -np.cos(alpha)*np.sin(betha),  np.cos(alpha)*np.cos(betha), np.sin(alpha) ],
                       [  np.sin(alpha)*np.sin(betha), -np.sin(alpha)*np.cos(betha), np.cos(alpha) ]])
        return np.einsum('ijk,jk->ik',AB,w)

    def gen_tail(self):
        fi    = np.random.uniform(0,2*np.pi,[self.lot, self.nop])
        theta = np.random.uniform(0,np.pi,[self.lot, self.nop])
        x = np.cos(fi) * np.sin(theta)
        y = np.sin(fi) * np.sin(theta)
        z = np.cos(theta)
        i = 0
        self.tail_coors[0,i,:] = x[i,:] + self.loop_coors[0,-1,:]
        self.tail_coors[1,i,:] = y[i,:] + self.loop_coors[1,-1,:]
        self.tail_coors[2,i,:] = z[i,:] + self.loop_coors[2,-1,:]
        for i in range(1,self.lot):
            self.tail_coors[0,i,:] = x[i,:] + self.tail_coors[0,i-1,:]
            self.tail_coors[1,i,:] = y[i,:] + self.tail_coors[1,i-1,:]
            self.tail_coors[2,i,:] = z[i,:] + self.tail_coors[2,i-1,:]


    def export_lasso_xyz(self, prefix, print_with_index, ll_format, tl_format):
        if tl_format==0:
            folder = 'l{:0{:d}d}/'.format(self.nos,ll_format)
        folder = 'l{:0{:d}d}_t{:0{:d}d}/'.format(self.nos,ll_format,self.lot,tl_format)
        try: os.mkdir(folder)
        except: pass
        if print_with_index:
            for polyg in range(self.nop):
                with open(folder + '/{}{:05d}.xyz'.format(prefix, polyg+self.start_num),'w') as f:        
                    for node in range(np.shape(self.lasso_coors)[1]):
                        f.write('{:2d} {:10f} {:10f} {:10f}\n'.format(node+1, self.lasso_coors[0, node, polyg], self.lasso_coors[1, node, polyg], self.lasso_coors[2, node, polyg] ))
        else:
            for polyg in range(self.nop):
                with open(folder + '/{}{:05d}.xyz'.format(prefix, polyg+self.start_num),'w') as f:
                    for node in range(np.shape(self.lasso_coors)[1]):
                        f.write('{:10f} {:10f} {:10f}\n'.format(self.lasso_coors[0, node, polyg], self.lasso_coors[1, node, polyg], self.lasso_coors[2, node, polyg] ))


    @staticmethod
    def gen_polygons(loop_len_vec, tail_len_vec, no_of_polygons, is_loop_closed, print_with_index, file_prefix, no_of_polygons_per_process=1):
        no_of_processes = int(no_of_polygons/no_of_polygons_per_process)
        ll_format = int(np.log10(max(loop_len_vec))+1)
        try:    tl_format = int(np.log10(max(tail_len_vec))+1)
        except: tl_format = 0
        for loop_len in loop_len_vec:
            for tail_len in tail_len_vec:
                for i in range(no_of_processes):                 
                    P = Polygons(loop_len, tail_len, no_of_polygons_per_process, is_loop_closed, i)
                    P.export_lasso_xyz(file_prefix, print_with_index, ll_format, tl_format)


if __name__ == '__main__':

    desc = """
    #################################################################\n\
    #   Program creates random equilateral closed polygons (loops)  #\n\
    #   closed polygons with random walk tails (lassos).            #\n\
    #                                                               #\n\
    #   Algorithm for generating random equilateral polygons based  #\n\
    #   on J. Cantarella \"A fast direct sampling algorithm for      #\n\
    #   equilateral closed polygons\". If you use this program,      #\n\
    #   please, cite his article.                                   #\n\
    #                                                               #\n\
    #   If you want to generate lasso instead of a loop use -t.     #\n\
    #                                                               #\n\
    #   Output is stored in .xyz format (three columns: x y z).     #\n\
    #   For output changes check -x, -p, -i, -c.                    #\n\
    #                                                               #\n\
    #   Author:  Bartosz Ambroży Greń                               #\n\
    #   Contact: b.gren [at] cent.uw.edu.pl                         #\n\
    #   Version 1.0 from 28.11.2018                                 #\n\
    #################################################################\n"""

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('loop_len_vec',    type=int, nargs='+', metavar='loop_length', help='length(s) of loop(s) measured in number of vertices')
    parser.add_argument('-t', '--tlen',    type=int, nargs='+', dest='tail_len_vec', metavar='TAIL_LENGTH', default=0, help='length(s) of tail(s) measured in number of vertices')
    parser.add_argument('-n', '--num',     type=int, dest='no_of_polygons', metavar='#STRUCTURES', default=1, help='number of generated structures for every combination of inputed loop and tail lengths')
    parser.add_argument('-p', '--prefix',  dest='file_prefix', metavar='NAME', default='polyg', help='set output file prefix')
    parser.add_argument('-i', '--index',   action='store_true', dest='print_with_index', help='.xyz file will have 4 columns: index x y z')
    parser.add_argument('-c', '--closed',  action='store_true', dest='is_loop_closed', help='duplicates first vertice of a loop as a last: loop of size n will have n+1 vertices, where 1st and n+1 will be identical')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    #parser.add_argument('-d', '--divide',  type=int, dest='no_of_polygons_per_process', default=1, help='Since all operations are in memory, for big numbers of polygons memory can be insufficient. So you can divide process of generating polygons.')
    args = vars(parser.parse_args())
    
    Polygons.gen_polygons(**args)        
    
    
