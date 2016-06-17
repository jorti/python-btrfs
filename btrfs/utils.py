# Copyright (C) 2016 Hans van Kranenburg <hans.van.kranenburg@mendix.com>
#
# This file is part of the python-btrfs module.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License v2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 021110-1307, USA.


from btrfs.ctree import (
    BLOCK_GROUP_DATA, BLOCK_GROUP_SYSTEM, BLOCK_GROUP_METADATA,
    SPACE_INFO_GLOBAL_RSV, BLOCK_GROUP_TYPE_MASK,
    BLOCK_GROUP_RAID0, BLOCK_GROUP_RAID1, BLOCK_GROUP_RAID5,
    BLOCK_GROUP_RAID6, BLOCK_GROUP_DUP, BLOCK_GROUP_RAID10,
    BLOCK_GROUP_PROFILE_MASK,
    EXTENT_FLAG_DATA, EXTENT_FLAG_TREE_BLOCK, BLOCK_FLAG_FULL_BACKREF,
)

_block_group_type_str_map = {
    BLOCK_GROUP_DATA: 'Data',
    BLOCK_GROUP_SYSTEM: 'System',
    BLOCK_GROUP_METADATA: 'Metadata',
    BLOCK_GROUP_DATA | BLOCK_GROUP_METADATA: 'Data+Metadata',
    SPACE_INFO_GLOBAL_RSV: 'GlobalReserve',
}


def block_group_type_str(flags):
    return _block_group_type_str_map.get(
        flags & (BLOCK_GROUP_TYPE_MASK | SPACE_INFO_GLOBAL_RSV),
        'unknown'
    )


_block_group_profile_str_map = {
    0: 'single',
    BLOCK_GROUP_RAID0: 'RAID0',
    BLOCK_GROUP_RAID1: 'RAID1',
    BLOCK_GROUP_RAID5: 'RAID5',
    BLOCK_GROUP_RAID6: 'RAID6',
    BLOCK_GROUP_DUP: 'DUP',
    BLOCK_GROUP_RAID10: 'RAID10',
}


def block_group_profile_str(flags):
    return _block_group_profile_str_map.get(
        flags & BLOCK_GROUP_PROFILE_MASK,
        'unknown'
    )


pretty_size_units = '_KMGTPE'


def pretty_size(size, unit=None, binary=True):
    if unit == '':
        return str(size)
    base = 1024 if binary else 1000
    if unit is None:
        if size == 0:
            unit = ''
            unit_offset = 0
            base = 1000
        else:
            unit_offset = 0
            tmp = size
            while tmp >= 1024 and unit_offset < len(pretty_size_units) - 1:
                unit_offset = unit_offset + 1
                tmp = tmp / 1024
            unit = pretty_size_units[unit_offset] if unit_offset > 0 else ''
    else:
        unit = unit.upper()
        unit_offset = pretty_size_units.index(unit)
        if unit == 'K' and base == 1000:
            unit = 'k'
    divide_by = base ** unit_offset
    if divide_by > 0:
        size = float(size) / divide_by
    return "{0:.2f}{1}{2}B".format(size, unit, 'i' if base == 1024 and unit != '' else '')


def block_group_flags_str(flags):
    ret = []
    if flags & BLOCK_GROUP_DATA:
        ret.append("DATA")
    if flags & BLOCK_GROUP_METADATA:
        ret.append("METADATA")
    if flags & BLOCK_GROUP_SYSTEM:
        ret.append("SYSTEM")
    if flags & BLOCK_GROUP_RAID0:
        ret.append("RAID0")
    if flags & BLOCK_GROUP_RAID1:
        ret.append("RAID1")
    if flags & BLOCK_GROUP_DUP:
        ret.append("DUP")
    if flags & BLOCK_GROUP_RAID10:
        ret.append("RAID10")
    if flags & BLOCK_GROUP_RAID5:
        ret.append("RAID5")
    if flags & BLOCK_GROUP_RAID6:
        ret.append("RAID6")
    return '|'.join(ret)


def extent_flags_str(flags):
    ret = []
    if flags & EXTENT_FLAG_DATA:
        ret.append("DATA")
    if flags & EXTENT_FLAG_TREE_BLOCK:
        ret.append("TREE_BLOCK")
    if flags & BLOCK_FLAG_FULL_BACKREF:
        ret.append("FULL_BACKREF")
    return '|'.join(ret)