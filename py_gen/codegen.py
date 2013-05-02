# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

from collections import namedtuple
import struct
import of_g
import loxi_front_end.type_maps as type_maps
import loxi_utils.loxi_utils as utils
import util
import oftype

OFClass = namedtuple('OFClass', ['name', 'pyname', 'members', 'type_members',
                                 'min_length', 'is_fixed_length'])
Member = namedtuple('Member', ['name', 'oftype'])
LengthMember = namedtuple('LengthMember', ['name', 'oftype'])
FieldLengthMember = namedtuple('FieldLengthMember', ['name', 'oftype', 'field_name'])
TypeMember = namedtuple('TypeMember', ['name', 'oftype', 'value'])
PadMember = namedtuple('PadMember', ['length'])

# XXX move to frontend
field_length_members = {
    ('of_packet_out', 1, 'actions_len') : 'actions',
    ('of_packet_out', 2, 'actions_len') : 'actions',
    ('of_packet_out', 3, 'actions_len') : 'actions',
    ('of_packet_out', 4, 'actions_len') : 'actions',
}

def get_type_values(cls, version):
    """
    Returns a map from the name of the type member to its value.
    """
    type_values = {}

    # Primary wire type
    if utils.class_is_message(cls):
        type_values['version'] = 'const.OFP_VERSION'
        type_values['type'] = util.constant_for_value(version, "ofp_type", util.primary_wire_type(cls, version))
        if cls in type_maps.flow_mod_list:
            type_values['_command'] = util.constant_for_value(version, "ofp_flow_mod_command",
                                                              type_maps.flow_mod_types[version][cls[8:]])
        if cls in type_maps.stats_request_list:
            type_values['stats_type'] = util.constant_for_value(version, "ofp_stats_types",
                                                                type_maps.stats_types[version][cls[3:-14]])
        if cls in type_maps.stats_reply_list:
            type_values['stats_type'] = util.constant_for_value(version, "ofp_stats_types",
                                                                type_maps.stats_types[version][cls[3:-12]])
        if type_maps.message_is_extension(cls, version):
            type_values['experimenter'] = '%#x' % type_maps.extension_to_experimenter_id(cls)
            type_values['subtype'] = type_maps.extension_message_to_subtype(cls, version)
    elif utils.class_is_action(cls):
        type_values['type'] = util.constant_for_value(version, "ofp_action_type", util.primary_wire_type(cls, version))
        if type_maps.action_is_extension(cls, version):
            type_values['experimenter'] = '%#x' % type_maps.extension_to_experimenter_id(cls)
            type_values['subtype'] = type_maps.extension_action_to_subtype(cls, version)
    elif utils.class_is_queue_prop(cls):
        type_values['type'] = util.constant_for_value(version, "ofp_queue_properties", util.primary_wire_type(cls, version))
    elif utils.class_is_hello_elem(cls):
        type_values['type'] = util.constant_for_value(version, "ofp_hello_elem_type", util.primary_wire_type(cls, version))
    elif utils.class_is_oxm(cls):
        oxm_class = 0x8000
        oxm_type = util.primary_wire_type(cls, version)
        oxm_masked = cls.find('masked') != -1 and 1 or 0
        oxm_len = of_g.base_length[(cls, version)] - 4
        type_values['type_len'] = '%#x' % (oxm_class << 16 | oxm_type << 8 | \
                                           oxm_masked << 8 | oxm_len)
    elif cls == "of_match_v2":
        type_values['type'] = 0
    elif cls == "of_match_v3":
        type_values['type'] = 1

    return type_values

# Create intermediate representation
def build_ofclasses(version):
    blacklist = ["of_action", "of_action_header", "of_header", "of_queue_prop",
                 "of_queue_prop_header", "of_experimenter", "of_action_experimenter",
                 "of_oxm", "of_oxm_header", "of_oxm_experimenter_header",
                 "of_hello_elem", "of_hello_elem_header"]
    ofclasses = []
    for cls in of_g.standard_class_order:
        if version not in of_g.unified[cls] or cls in blacklist:
            continue
        unified_class = util.lookup_unified_class(cls, version)

        # Name for the generated Python class
        if utils.class_is_action(cls):
            pyname = cls[10:]
        elif utils.class_is_oxm(cls):
            pyname = cls[7:]
        else:
            pyname = cls[3:]

        type_values = get_type_values(cls, version)
        members = []
        type_members = []

        pad_count = 0

        for member in unified_class['members']:
            if member['name'] in ['length', 'len']:
                members.append(LengthMember(name=member['name'],
                                            oftype=oftype.OFType(member['m_type'], version)))
            elif (cls, version, member['name']) in field_length_members:
                field_name = field_length_members[(cls, version, member['name'])]
                members.append(FieldLengthMember(name=member['name'],
                                                 oftype=oftype.OFType(member['m_type'], version),
                                                 field_name=field_name))
            elif member['name'] in type_values:
                members.append(TypeMember(name=member['name'],
                                          oftype=oftype.OFType(member['m_type'], version),
                                          value=type_values[member['name']]))
                type_members.append(members[-1])
            elif member['name'].startswith("pad"):
                # HACK this should be moved to the frontend
                pad_oftype = oftype.OFType(member['m_type'], version)
                length = struct.calcsize("!" + pad_oftype._pack_fmt())
                if pad_oftype.is_array: length *= pad_oftype.array_length
                members.append(PadMember(length=length))
            else:
                members.append(Member(name=member['name'],
                                      oftype=oftype.OFType(member['m_type'], version)))

        ofclasses.append(
            OFClass(name=cls,
                    pyname=pyname,
                    members=members,
                    type_members=type_members,
                    min_length=of_g.base_length[(cls, version)],
                    is_fixed_length=(cls, version) in of_g.is_fixed_length))
    return ofclasses

def generate_init(out, name, version):
    util.render_template(out, 'init.py', version=version)

def generate_action(out, name, version):
    ofclasses = [x for x in build_ofclasses(version)
                 if utils.class_is_action(x.name)]
    util.render_template(out, 'action.py', ofclasses=ofclasses, version=version)

def generate_oxm(out, name, version):
    ofclasses = [x for x in build_ofclasses(version)
                 if utils.class_is_oxm(x.name)]
    util.render_template(out, 'oxm.py', ofclasses=ofclasses, version=version)

def generate_common(out, name, version):
    ofclasses = [x for x in build_ofclasses(version)
                 if not utils.class_is_message(x.name)
                    and not utils.class_is_action(x.name)
                    and not utils.class_is_oxm(x.name)
                    and not utils.class_is_list(x.name)]
    util.render_template(out, 'common.py', ofclasses=ofclasses, version=version)

def generate_const(out, name, version):
    groups = {}
    for (group, idents) in of_g.identifiers_by_group.items():
        items = []
        for ident in idents:
            info = of_g.identifiers[ident]
            if version in info["values_by_version"]:
                items.append((info["ofp_name"], info["values_by_version"][version]))
        if items:
            groups[group] = items
    util.render_template(out, 'const.py', version=version, groups=groups)

def generate_message(out, name, version):
    ofclasses = [x for x in build_ofclasses(version)
                 if utils.class_is_message(x.name)]
    util.render_template(out, 'message.py', ofclasses=ofclasses, version=version)

def generate_pp(out, name, version):
    util.render_template(out, 'pp.py')

def generate_util(out, name, version):
    util.render_template(out, 'util.py')
