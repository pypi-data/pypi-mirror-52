import os
from multipledispatch import dispatch
from ..kitti_object_3d import KITTIObject3D, KITTIObjectClass


@dispatch(str)
def load_label_2(absolute_path):
    with open(absolute_path) as f:
        lines = f.read().splitlines()
    labels = []
    for l in lines:
        items = l.split()
        cls = items[0]
        truncated, occluded, alpha, x1, y1, x2, y2, h, w, l, x, y, z, ry = map(float, items[1:])
        label = KITTIObject3D(KITTIObjectClass[cls], truncated, occluded, alpha,
                              x1, y1, x2, y2, h, w, l, x, y, z, ry)
        labels.append(label)
    return labels


@dispatch(str, str)
def load_label_2(label_2_dir, imgid):
    absolute_path = os.path.join(label_2_dir, imgid + '.txt')
    return load_label_2(absolute_path)


@dispatch(str, int)
def load_label_2(label_2_dir, imgid):
    imgid = '%06d' % imgid
    return load_label_2(label_2_dir, imgid)


@dispatch(str, str, str)
def load_label_2(kitti_root, split, imgid):
    calib_dir = os.path.join(kitti_root, 'object', split, 'label_2')
    return load_label_2(calib_dir, imgid)


@dispatch(str, str, int)
def load_label_2(kitti_root, split, imgid):
    imgid = '%06d' % imgid
    return load_label_2(kitti_root, split, imgid)
