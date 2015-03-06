#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

def graph2dot(nodes, edges, edge_label, file_name="test.dot"):
    file = open(file_name, 'w')
    strs = ['digraph{',
            'graph[rankdir=LR]',
            nodes2dot(nodes),
            edges2dot(edges, edge_label),
            '}']
    file.writelines(strs)
    file.close()

def nodes2dot(nodes):
    s = ""
    for node in nodes:
        s += '\n{}[label=\"{}\"];'.format(node, node)
    return s

def edges2dot(edges, edge_label):
    s = ""
    for i, edge in enumerate(edges):
        s += '\n{}->{}[label=\"{}\"];'.format(edge[0], edge[1], edge_label[i])
    return s

def make_graph(rulebook, file_name="test.dot"):
    print("making dot file for graphviz...")
    nodes = set()
    edges = []
    edge_label = []
    for rule in rulebook.rules:
        nodes.add(rule.state)
        nodes.add(rule.next_state)
        edges.append([rule.state, rule.next_state])
        edge_label.append(rule.character)
    graph2dot(nodes, edges, edge_label, file_name)

    print("generating png file...")
    cmd = "dot -Tpng -O {}".format(file_name)
    os.system(cmd)
    print("end.")
