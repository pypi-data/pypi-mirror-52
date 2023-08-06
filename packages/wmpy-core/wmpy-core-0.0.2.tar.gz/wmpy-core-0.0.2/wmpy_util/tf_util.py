#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : tf_util.py
@Desc    : tensorflow相关工具类
"""
import os
import tensorflow as tf
from wmpy_util.time_util import timer
from tensorflow.python.platform import gfile


def graph_summay(session, log_dir):
    writter = tf.summary.FileWriter(log_dir,
                                    session.graph)


@timer
def load_model_from_ckpt(ckpt_file=None):
    """
    从ckpt文件中加载tensorflow模型
    :param ckpt_file:
    :return:
    """
    if ckpt_file is None:
        return
    with tf.Graph().as_default() as graph:
        sess = tf.Session(graph=graph)
        meta_file_path = get_meta_path_from_ckpt(ckpt_file)
        save = tf.train.import_meta_graph(meta_file_path)
        save.restore(sess=sess, save_path=ckpt_file)
    print("Load model from CKPT successed!")
    return sess


# @timer
def load_model_from_pb(pb_file=None, config=None):
    """
    从pb文件中恢复模型文件
    目前来说从pb内加载的模型不能再训练
    :param pb_file:
    :return: 返回session, input, output三元组
    """
    if pb_file is None:
        return
    with tf.gfile.FastGFile(pb_file, 'rb') as fp:
        graph_def = tf.GraphDef()
        fp_value = fp.read()
        graph_def.ParseFromString(fp_value)
        # 修复由于batchnorm层产生的加载问题
        graph_def = fix_graph_def_with_bn(graph_def)
        with tf.Graph().as_default() as graph:
            # 生成一个新的tensorflow Session
            new_sess = tf.Session(graph=graph, config=config)
            # 导入模型的图定义
            tf.import_graph_def(graph_def, name='')
            # print("Load model from pb_file succeed !")
        return new_sess


def load_model_from_hub(url, output_name=None, config=None):
    """
    从tensorflow-hub加载模型
    :param url: 模型地址
    :param output_name: 输出节点名称，如果为空则使用默认的输出节点
    :return:
    """
    import tensorflow_hub as hub
    module_spec = hub.load_module_spec(url)
    height, width = hub.get_expected_image_size(module_spec)
    channel = hub.get_num_image_channels(module_spec)
    with tf.Graph().as_default() as graph:
        input_tensor = tf.placeholder(tf.float32, [None, height, width, channel])
        module = hub.Module(module_spec)
        output_tensor = module(input_tensor)
        if output_name is not None:
            output_tensor = graph.get_tensor_by_name(output_name)
        session = tf.Session(graph=graph, config=config)
        # 初始化参数
        init = tf.global_variables_initializer()
        session.run(init)
    return session, input_tensor, output_tensor


def save_model_as_pb(session, output_node_name, pb_file_path):
    """
    将模型参数冻结为pb文件
    :param session:
    :param output_node_name:
    :param pb_file_path:
    :return:
    """
    if output_node_name is None:
        raise AttributeError("Output node name cannot be None!")
    if isinstance(output_node_name, list) or isinstance(output_node_name, tuple):
        output_node_name_list = output_node_name
    else:
        output_node_name_list = [output_node_name]
    filter_node_list = list()
    for node_name in output_node_name_list:
        filter_node_list.append(node_name.split(":")[0])
    graph_def = session.graph.as_graph_def()
    constant_graph = tf.graph_util.convert_variables_to_constants(session, graph_def, filter_node_list)
    with tf.gfile.FastGFile(pb_file_path, mode='wb') as f:
        f.write(constant_graph.SerializeToString())


def get_meta_path_from_ckpt(ckpt_path):
    """
    通过ckpt路径得到meta文件路径
    :param ckpt_path:
    :return:
    """
    # 分成 path/model_name   .ckpt-1000
    ckpt_prefix, _ = os.path.splitext(ckpt_path)
    # 第一种情况 model_name.ckpt.meta
    meta_file_path = ckpt_prefix + ".meta"
    if os.path.isfile(meta_file_path):
        return meta_file_path
    # 第二种情况 model_name.ckpt-???.meta
    meta_file_path = ckpt_path + ".meta"
    if os.path.isfile(meta_file_path):
        return meta_file_path
    dir_name = os.path.split(ckpt_path)[0]
    for file in os.listdir(dir_name):
        # 第三种情况 xxxxx.meta
        if file.endswith(".meta"):
            meta_file_path = os.path.join(dir_name, file)
            if os.path.isfile(meta_file_path):
                return meta_file_path


def fix_pbfile_with_bn(file, output_node_name):
    """
    修复pb模型文件
    :param file:
    :param output_node_name:
    :return:
    """
    file_list = []
    if os.path.isfile(file):
        dir_name, file_name = os.path.split(file)
        file_list.append(file_name)
    elif os.path.isdir(file):
        dir_name = file
        file_list = os.listdir(dir_name)
    else:
        raise ValueError("Param must be a file or dir: %s" % file)

    for file in file_list:
        if not file.endswith(".pb"):
            continue
        file_name, ext = os.path.splitext(file)
        file_path = os.path.join(dir_name, file)
        file_fix_path = os.path.join(dir_name, "%s_fix%s" % (file_name, ext))
        # pb
        graph_def = tf.GraphDef()
        with gfile.FastGFile(file_path, 'rb') as f:
            graph_def.ParseFromString(f.read())

        # for fixing the bug of batch norm
        graph_def = fix_graph_def_with_bn(graph_def)

        with tf.Graph().as_default():
            tf.import_graph_def(graph_def, name='')
            session = tf.Session()
            constant_graph = tf.graph_util.convert_variables_to_constants(session, graph_def, [output_node_name])
            with tf.gfile.FastGFile(file_fix_path, mode='wb') as f:
                f.write(constant_graph.SerializeToString())


def fix_graph_def_with_bn(graph_def):
    """
    修复带有batch_norm层的graph_def
    :param graph_def:
    :return:
    """
    # for fixing the bug of batch norm
    gd = graph_def
    for node in gd.node:
        # print(node.name, node.op)
        if node.op == 'RefSwitch':
            node.op = 'Switch'
            for index in range(len(node.input)):
                if 'moving_' in node.input[index]:
                    node.input[index] = node.input[index] + '/read'
        elif node.op == 'AssignSub':
            node.op = 'Sub'
            if 'use_locking' in node.attr: del node.attr['use_locking']
        elif node.op == 'AssignAdd':
            node.op = 'Add'
            if 'use_locking' in node.attr: del node.attr['use_locking']
    return gd


def get_input_output_from_graph(graph: tf.Graph):
    """
    假设网络包含一个输入，一个输出，以及可能有一个is_training标志位，并且所有的节点都在模型链路上
    思路：
        查找所有placeholder节点作为输入
        查找所有没有做过输入的节点，作为最终的输出节点
    TODO: 该方法目前无法适用于所有模型，有待改进
    :param graph:
    :return:
    """
    graph_def = graph.as_graph_def()
    placeholder_list = []
    node_set = set()
    input_set = set()
    for node in graph_def.node:
        if node.op.lower() == "placeholder":
            placeholder_list.append(node.name)
        name = node.name
        input_list = node.input
        node_set.add(name)
        for input_name in input_list:
            input_name = input_name.split(":")[0]
            input_name = input_name.replace("^", "")
            # for cl in check_list:
            #     if cl in input_name:
            #         print("input:", input_name, "  node:",cl)
            input_set.add(input_name)
    # print("node number:%d,  input node number:%d" % (len(node_set), len(input_set)))
    output_node = list()
    for name in node_set:
        if name not in input_set:
            output_node.append(name)
    if len(output_node) > 1:
        raise ValueError("Output tensor size larger than 1: %s" % str(output_node))
    output_tensor = graph.get_tensor_by_name(output_node[0] + ":0")
    input_tensor = None
    is_training = None
    for ph_name in placeholder_list:
        placeholder = graph.get_tensor_by_name(ph_name + ":0")
        shape = placeholder.shape
        # print("placeholder shape", shape)
        if shape.ndims is None or shape.ndims < 1:
            is_training = placeholder
        else:
            input_tensor = placeholder
    return input_tensor, output_tensor, is_training
