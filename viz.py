import json
import sys

import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv)==4:
    filename = sys.argv[1]
    obj1 = sys.argv[2]
    obj2 = sys.argv[3]
    print('2D plot')
    print('File:', filename, 'Obj1:', obj1, 'Obj2:', obj2)

    with open(filename) as f:
        content = f.readlines()
    content = [json.loads(x.strip()) for x in content][1:]
    obj1_v = []
    obj2_v = []

    for c in content:
        obj1_v.append(c['objective'][obj1])
        obj2_v.append(c['objective'][obj2])

    plt.scatter(obj1_v, obj2_v)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.xlabel(obj1)
    plt.ylabel(obj2)
    plt.show()

if len(sys.argv)==5:
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    filename = sys.argv[1]
    obj1 = sys.argv[2]
    obj2 = sys.argv[3]
    obj3 = sys.argv[4]
    print('2D plot')
    print('File:', filename, 'Obj1:', obj1, 'Obj2:', obj2, 'Obj3:', obj3)

    with open(filename) as f:
        content = f.readlines()
    content = [json.loads(x.strip()) for x in content][1:]
    obj1_v = []
    obj2_v = []
    obj3_v = []

    for c in content:
        obj1_v.append(c['objective'][obj1])
        obj2_v.append(c['objective'][obj2])
        obj3_v.append(c['objective'][obj3])

    ax.scatter3D(obj1_v, obj2_v, obj3_v)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.gca().invert_zaxis()

    ax.set_xlabel(obj1)
    ax.set_ylabel(obj2)
    ax.set_zlabel(obj3)

    plt.show()

if len(sys.argv)==6:
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    filename = sys.argv[1]
    obj1 = sys.argv[2]
    obj2 = sys.argv[3]
    obj3 = sys.argv[4]
    obj4 = sys.argv[5]
    print('2D plot')
    print('File:', filename, 'Obj1:', obj1, 'Obj2:', obj2, 'Obj3:', obj3, 'Obj4:', obj4)

    with open(filename) as f:
        content = f.readlines()
    content = [json.loads(x.strip()) for x in content][1:]
    obj1_v = []
    obj2_v = []
    obj3_v = []
    obj4_v = []

    for c in content:
        obj1_v.append(c['objective'][obj1])
        obj2_v.append(c['objective'][obj2])
        obj3_v.append(c['objective'][obj3])
        obj4_v.append(c['objective'][obj4])

    obj4_v_scl = np.array(obj4_v)
    obj4_v_scl = (obj4_v_scl - obj4_v_scl.min()) / (obj4_v_scl.max() - obj4_v_scl.min())
    obj4_v_scl = 15*obj4_v_scl + 3

    #print(obj4_v_scl)
    ax.scatter3D(obj1_v, obj2_v, obj3_v, c=obj4_v_scl)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.gca().invert_zaxis()

    ax.set_xlabel(obj1)
    ax.set_ylabel(obj2)
    ax.set_zlabel(obj3)

    plt.show()


