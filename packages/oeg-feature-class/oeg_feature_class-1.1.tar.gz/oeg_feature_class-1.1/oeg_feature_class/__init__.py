# coding: utf-8
"""
According http://www.iliassociation.org/documents/industry/POF%20specs%20V3_2%20January%202005.pdf
Газпром 2-2.3-919-2015
"""


class Error(Exception):
    """
    Feature Class exception
    """


class MagnetType:  # pylint: disable=too-few-public-methods,no-init
    """
    Magnet system types
    """
    MFL = 'MFL'  # lengthwise
    TFI = 'TFI'  # diametral
    CAL = 'CAL'  # caliper


class FeatureClass:  # pylint: disable=too-few-public-methods,no-init
    """
    class for given geometry parameters
    """
    AXGR = 'AXGR'  # Axial Grooving (продольная канавка)
    AXSL = 'AXSL'  # Axial Slotting (продольная щель)
    CIGR = 'CIGR'  # Circumferential Grooving (поперечная канавка)
    CISL = 'CISL'  # Circumferential Slotting (поперечная щель)
    GENE = 'GENE'  # General (обширный)
    PINH = 'PINH'  # Pinhole (язва)
    PITT = 'PITT'  # Pitting (каверна)


MIN_PERCENT = {  # пороги обнаружения в % от толщины стенки трубы

  MagnetType.MFL: {
    FeatureClass.GENE: 5,
    FeatureClass.PITT: 10,
    FeatureClass.PINH: 20,
    FeatureClass.AXGR: 20,
    FeatureClass.CIGR: 8,
    FeatureClass.CISL: 8,
  },

  MagnetType.TFI: {
    FeatureClass.GENE: 5,
    FeatureClass.PITT: 10,
    FeatureClass.PINH: 20,
    FeatureClass.CIGR: 20,
    FeatureClass.AXGR: 8,
    FeatureClass.AXSL: 8,
  },
}

LIMITS = {

  MagnetType.MFL: {

    FeatureClass.GENE: lambda thick, length, width, depth: (
      lim(length, 0, 30),  # точность по длине, мм -/+
      lim(width, 0, 30),  # точность по ширине, мм -/+
      lim_z(depth, thick, 0.1),  # точность по глубине, мм -/+
    ),

    FeatureClass.PITT: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, 0, 30), lim_z(depth, thick, 0.1),
    ),

    FeatureClass.PINH: lambda thick, length, width, depth: (
      lim(length, 0, 15), lim(width, thick, 30), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.AXGR: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, 0, 30), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.CIGR: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, thick, 30), lim_z(depth, thick, 0.15),
    ),

    FeatureClass.CISL: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, thick, 30), lim_z(depth, thick, 0.15),
    ),

  },

  MagnetType.TFI: {

    FeatureClass.GENE: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 30), lim_z(depth, thick, 0.1),
    ),

    FeatureClass.PITT: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.1),
    ),

    FeatureClass.PINH: lambda thick, length, width, depth: (
      lim(length, thick, 30), lim(width, 0, 15), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.CIGR: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.AXGR: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.15),
    ),

    FeatureClass.AXSL: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.15),
    ),

  },
}


def lim_z(depth, thick, val):
    """
    limits for depth
    """
    return (depth - val * thick, depth + val * thick)


def lim(size, thick, val):
    """
    limits for width/length
    """
    return (size - (thick + val), size + (thick + val))


def size_class(length, width, thick):
    """
    calculate feature class for given parameters
    """
    if not all([width, length, thick]):
        raise Error("Wrong FeatureClass params. l={} w={} t={}".format(length, width, thick))

    size1 = thick
    if size1 < 10:
        size1 = 10

    size3 = 3 * size1
    size6 = 6 * size1
    lwr = float(length) / float(width)

    if (width >= size3) and (length >= size3):
        ret = FeatureClass.GENE

    elif (
      (size6 > width >= size1) and
      (size6 > length >= size1) and
      (2.0 > lwr > 0.5)
    ) and not (width >= size3 <= length):
        ret = FeatureClass.PITT

    elif (size3 > width >= size1) and (lwr >= 2.0):
        ret = FeatureClass.AXGR

    elif (size3 > length >= size1) and (lwr <= 0.5):
        ret = FeatureClass.CIGR

    elif (size1 > width > 0) and (size1 > length > 0):
        ret = FeatureClass.PINH

    elif length >= size1 > width > 0:
        ret = FeatureClass.AXSL

    elif width >= size1 > length > 0:
        ret = FeatureClass.CISL

    else:
        raise Error("Wrong FeatureClass params. l={} w={} t={}".format(length, width, thick))

    return ret


def is_detectable(sizes, thick, magnet_type=MagnetType.MFL):
    """
    return True if defekt with given sizes on wallthick more than minimal percent
    """
    length, width, depth = sizes
    cls = size_class(length, width, thick)
    min_percent = MIN_PERCENT[magnet_type]
    if cls not in min_percent:
        return False

    if depth < 0:  # through hole
        depth = thick

    return int(round(depth * 100.0 / thick, 0)) >= min_percent[cls]


def is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL):
    """
    return tuple from 3 boolean items, that represent limits by length, width, depth
    """
    limits = LIMITS[magnet_type]
    cls = size_class(real[0], real[1], thick)
    if cls not in limits:
        raise Error("Defect with params {} has class '{}'. Not applicable for method '{}'".format(
          real, cls, magnet_type
        ))

    length, width, depth = calcked
    limits_length, limits_width, limits_depth = limits[cls](thick, *real)

    return (
      limits_length[0] <= length <= limits_length[1],
      limits_width[0] <= width <= limits_width[1],
      limits_depth[0] <= depth <= limits_depth[1],
    )
