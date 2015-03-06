#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

def graph2dot(nodes, edges, edge_label, edge_styles, file_name="test.dot"):
    file = open(file_name, 'w')
    strs = ['digraph{',
            'graph[rankdir=LR]',
            nodes2dot(nodes),
            edges2dot(edges, edge_label, edge_styles),
            '}']
    file.writelines(strs)
    file.close()

def nodes2dot(nodes):
    s = ""
    for node, shape in nodes.items():
        # print(shape, node)
        s += '\n{}[shape=\"{}\", label=\"{}\"];'.format(node, shape, node)
    return s

def edges2dot(edges, edge_label, edge_styles):
    s = ""
    for i, edge in enumerate(edges):
        s += '\n{}->{}[style=\"{}\", label=\"{}\"];'.format(edge[0], edge[1], edge_styles[i], edge_label[i])
    return s

def make_graph(fa, file_name="test.dot"):
    print("making dot file for graphviz...")
    rulebook = fa.rulebook
    accept_states = fa.accept_states
    nodes = {}
    edges = []
    edge_label = []
    edge_styles = []
    for rule in rulebook.rules:
        nodes[rule.state] = 'circle'
        nodes[rule.next_state] = 'circle'
        edges.append([rule.state, rule.next_state])
        edge_label.append(rule.character)
        if not rule.character:
            edge_styles.append('dotted')
        else:
            edge_styles.append('')
    for accept_state in accept_states:
        nodes[accept_state] = 'doublecircle'
    graph2dot(nodes, edges, edge_label, edge_styles, file_name)

    print("generating png file...")
    cmd = "dot -Tpng -O {}".format(file_name)
    os.system(cmd)
    print("end.")
