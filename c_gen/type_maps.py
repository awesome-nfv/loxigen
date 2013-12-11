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

#
# Miscellaneous type information
#
# Define the map between sub-class types and wire values.  In each
# case, an array indexed by wire version gives a hash from identifier
# to wire value.
#

import c_gen.of_g_legacy as of_g
import sys
from generic_utils import *
import loxi_utils.loxi_utils as loxi_utils
import c_gen.loxi_utils_legacy as loxi_utils
import loxi_globals

invalid_type = "invalid_type"
invalid_value = "0xeeee"  # Note, as a string

################################################################
#
# Define type data for inheritance classes:
#   instructions, actions, queue properties and OXM
#
# Messages are not in this group; they're treated specially for now
#
# These are indexed by wire protocol number
#
################################################################

instruction_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict()
    }

instruction_id_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict()
    }

action_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(),
    }

action_id_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(),
    }

queue_prop_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict()
    }

bsn_vport_types = {
    # version 1.0
    of_g.VERSION_1_0:dict(
        q_in_q      = 0,
        ),
    # version 1.1
    of_g.VERSION_1_1:dict(
        q_in_q      = 0,
        ),
    # version 1.2
    of_g.VERSION_1_2:dict(
        q_in_q      = 0,
        ),
    # version 1.3
    of_g.VERSION_1_3:dict(
        q_in_q      = 0,
        )
    }

oxm_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(),
    }

hello_elem_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(),
    }

table_feature_prop_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(),
    }

meter_band_types = {
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(),
    }

# All inheritance data for non-messages
inheritance_data = dict(
    of_instruction = instruction_types,
    of_instruction_id = instruction_id_types,
    of_action = action_types,
    of_action_id = action_id_types,
    of_oxm = oxm_types,
    of_queue_prop = queue_prop_types,
    of_hello_elem = hello_elem_types,
    of_table_feature_prop = table_feature_prop_types,
    of_meter_band = meter_band_types,
    # BSN specific inheritance extensions
    of_bsn_vport = bsn_vport_types
    )

def class_is_virtual(cls):
    """
    Returns True if cls is a virtual class
    """
    if cls.find("header") > 0:
        return True
    if loxi_utils.class_is_list(cls):
        return True
    return loxi_globals.unified.class_by_name(cls).virtual

################################################################
#
# These are message types
#
################################################################

# The hardcoded message types are for inheritance parents
message_types = {
    # version 1.0
    of_g.VERSION_1_0:dict(
        error_msg               = 1,
        experimenter            = 4,
        flow_mod                = 14,
        stats_request           = 16,
        stats_reply             = 17,
        ),

    # version 1.1
    of_g.VERSION_1_1:dict(
        error_msg               = 1,
        experimenter            = 4,
        flow_mod                = 14,
        group_mod               = 15,
        stats_request           = 18,
        stats_reply             = 19,
        ),

    # version 1.2
    of_g.VERSION_1_2:dict(
        error_msg               = 1,
        experimenter            = 4,
        flow_mod                = 14,
        group_mod               = 15,
        stats_request           = 18,
        stats_reply             = 19,
        ),

    # version 1.3
    of_g.VERSION_1_3:dict(
        error_msg               = 1,
        experimenter            = 4,
        flow_mod                = 14,
        group_mod               = 15,
        stats_request           = 18,  # FIXME Multipart
        stats_reply             = 19,
        )
    }

################################################################
#
# These are other objects that have a notion of type but are
# not (yet) promoted to objects with inheritance
#
################################################################

stats_types = {
    # version 1.0
    of_g.VERSION_1_0:dict(
        desc = 0,
        flow = 1,
        aggregate = 2,
        table = 3,
        port = 4,
        queue = 5,
        experimenter = 0xffff
        ),

    # version 1.1
    of_g.VERSION_1_1:dict(
        desc = 0,
        flow = 1,
        aggregate = 2,
        table = 3,
        port = 4,
        queue = 5,
        group = 6,
        group_desc = 7,
        experimenter = 0xffff
        ),

    # version 1.2
        of_g.VERSION_1_2:dict(
        desc = 0,
        flow = 1,
        aggregate = 2,
        table = 3,
        port = 4,
        queue = 5,
        group = 6,
        group_desc = 7,
        group_features = 8,
        experimenter = 0xffff
        ),

    # version 1.3
        of_g.VERSION_1_3:dict(
        desc = 0,
        flow = 1,
        aggregate = 2,
        table = 3,
        port = 4,
        queue = 5,
        group = 6,
        group_desc = 7,
        group_features = 8,
        meter = 9,
        meter_config = 10,
        meter_features = 11,
        table_features = 12,
        port_desc = 13,
        experimenter = 0xffff,
        bsn_lacp = 0xffff,
        bsn_switch_pipeline = 0xffff,
        bsn_port_counter = 0xffff,
        bsn_vlan_counter = 0xffff
        )
    }

common_flow_mod_types = dict(
    add = 0,
    modify = 1,
    modify_strict = 2,
    delete = 3,
    delete_strict = 4
    )

flow_mod_types = {
    # version 1.0
    of_g.VERSION_1_0:common_flow_mod_types,
    of_g.VERSION_1_1:common_flow_mod_types,
    of_g.VERSION_1_2:common_flow_mod_types,
    of_g.VERSION_1_3:common_flow_mod_types
    }

# These do not translate to objects (yet)
error_types = {
    # version 1.0
    of_g.VERSION_1_0:dict(
        hello_failed        = 0,
        bad_request         = 1,
        bad_action          = 2,
        flow_mod_failed     = 3,
        port_mod_failed     = 4,
        queue_op_failed     = 5
        ),

    # version 1.1
    of_g.VERSION_1_1:dict(
        hello_failed         = 0,
        bad_request          = 1,
        bad_action           = 2,
        bad_instruction      = 3,
        bad_match            = 4,
        flow_mod_failed      = 5,
        group_mod_failed     = 6,
        port_mod_failed      = 7,
        table_mod_failed     = 8,
        queue_op_failed      = 9,
        switch_config_failed = 10
        ),

    # version 1.2
    of_g.VERSION_1_2:dict(
        hello_failed         = 0,
        bad_request          = 1,
        bad_action           = 2,
        bad_instruction      = 3,
        bad_match            = 4,
        flow_mod_failed      = 5,
        group_mod_failed     = 6,
        port_mod_failed      = 7,
        table_mod_failed     = 8,
        queue_op_failed      = 9,
        switch_config_failed = 10,
        role_request_failed  = 11,
        experimenter = 0xffff
        ),

    # version 1.3
    of_g.VERSION_1_3:dict(
        hello_failed         = 0,
        bad_request          = 1,
        bad_action           = 2,
        bad_instruction      = 3,
        bad_match            = 4,
        flow_mod_failed      = 5,
        group_mod_failed     = 6,
        port_mod_failed      = 7,
        table_mod_failed     = 8,
        queue_op_failed      = 9,
        switch_config_failed = 10,
        role_request_failed  = 11,
        meter_mod_failed     = 12,
        table_features_failed= 13,
        experimenter = 0xffff
        )
    }

group_mod_types = {
    # version 1.0
    of_g.VERSION_1_0:dict(),

    # version 1.1
    of_g.VERSION_1_1:dict(
        add = 0,
        modify = 1,
        delete = 2
        ),

    # version 1.2
    of_g.VERSION_1_2:dict(
        add = 0,
        modify = 1,
        delete = 2
        ),

    # version 1.3
    of_g.VERSION_1_3:dict(
        add = 0,
        modify = 1,
        delete = 2
        )
    }

##
# These are the objects whose length is specified by an external
# reference, specifically another data member in the class.
#
#external_length_spec = {
#    ("of_packet_out", "actions", OF_VERSION_1_0) : "actions_len",
#    ("of_packet_out", "actions", OF_VERSION_1_1) : "actions_len",
#    ("of_packet_out", "actions", OF_VERSION_1_2) : "actions_len",
#    ("of_packet_out", "actions", OF_VERSION_1_3) : "actions_len"
#}


################################################################
#
# type_val is the primary data structure that maps an
# (class_name, version) pair to the wire data type value
#
################################################################

type_val = dict()
inheritance_map = dict()

def generate_maps():
    for parent, versioned in inheritance_data.items():
        inheritance_map[parent] = set()
        for ver, subclasses in versioned.items():
            for subcls in subclasses:
                inheritance_map[parent].add(subcls)

    for version, classes in message_types.items():
        for cls in classes:
            name = "of_" + cls
            type_val[(name, version)] = classes[cls]

    for parent, versioned in inheritance_data.items():
        for version, subclasses in versioned.items():
            for subcls, value in subclasses.items():
                name = parent + "_" + subcls
                type_val[(name, version)] = value

    # Special case OF-1.2 match type
    type_val[("of_match_v3", of_g.VERSION_1_2)] = 1
    type_val[("of_match_v3", of_g.VERSION_1_3)] = 1

# Utility function
def dict_to_array(d, m_val, def_val=-1):
    """
    Given a dictionary, d, with each value a small integer,
    produce an array indexed by the integer whose value is the key.
    @param d The dictionary
    @param m_val Ignore values greater than m_val
    @param def_val The default value (for indices not in range of d)
    """

    # Get the max value in range for hash
    max_val = 0
    for key in d:
        if (d[key] > max_val) and (d[key] < m_val):
            max_val = d[key]
    ar = []
    for x in range(0, max_val + 1):
        ar.append(def_val)
    for key in d:
        if (d[key] < m_val):
            ar[d[key]] = key
    return ar

def type_array_len(version_indexed, max_val):
    """
    Given versioned information about a type, calculate how long
    the unified array should be.

    @param version_indexed A dict indexed by version. Each value is a
    dict indexed by a name and whose value is an integer
    @param max_val Ignore values greater than this for length calcs
    """
    # First, find the max length of all arrays
    arr_len = 0
    for version, val_dict in version_indexed.items():
        ar = dict_to_array(val_dict, max_val, invalid_type)
        if arr_len < len(ar):
            arr_len = len(ar)
    return arr_len

# FIXME:  Need to move update for multipart messages

stats_reply_list = [
    "of_aggregate_stats_reply",
    "of_desc_stats_reply",
    "of_experimenter_stats_reply",
    "of_flow_stats_reply",
    "of_group_stats_reply",
    "of_group_desc_stats_reply",
    "of_group_features_stats_reply",
    "of_meter_stats_reply",
    "of_meter_config_stats_reply",
    "of_meter_features_stats_reply",
    "of_port_stats_reply",
    "of_port_desc_stats_reply",
    "of_queue_stats_reply",
    "of_table_stats_reply",
    "of_table_features_stats_reply",
    "of_bsn_stats_reply",
    "of_bsn_lacp_stats_reply",
    "of_bsn_switch_pipeline_stats_reply",
    "of_bsn_port_counter_stats_reply",
    "of_bsn_vlan_counter_stats_reply",
]

stats_request_list = [
    "of_aggregate_stats_request",
    "of_desc_stats_request",
    "of_experimenter_stats_request",
    "of_flow_stats_request",
    "of_group_stats_request",
    "of_group_desc_stats_request",
    "of_group_features_stats_request",
    "of_meter_stats_request",
    "of_meter_config_stats_request",
    "of_meter_features_stats_request",
    "of_port_stats_request",
    "of_port_desc_stats_request",
    "of_queue_stats_request",
    "of_table_stats_request",
    "of_table_features_stats_request",
    "of_bsn_stats_request",
    "of_bsn_lacp_stats_request",
    "of_bsn_switch_pipeline_stats_request",
    "of_bsn_port_counter_stats_request",
    "of_bsn_vlan_counter_stats_request",
]

flow_mod_list = [
    "of_flow_add",
    "of_flow_modify",
    "of_flow_modify_strict",
    "of_flow_delete",
    "of_flow_delete_strict"
]

error_msg_list = [
    "of_hello_failed_error_msg",
    "of_bad_request_error_msg",
    "of_bad_action_error_msg",
    "of_bad_instruction_error_msg",
    "of_bad_match_error_msg",
    "of_flow_mod_failed_error_msg",
    "of_group_mod_failed_error_msg",
    "of_port_mod_failed_error_msg",
    "of_table_mod_failed_error_msg",
    "of_queue_op_failed_error_msg",
    "of_switch_config_failed_error_msg",
    "of_role_request_failed_error_msg",
    "of_meter_mod_failed_error_msg",
    "of_table_features_failed_error_msg",
    "of_experimenter_error_msg"
]

group_mod_list = [
    "of_group_add",
    "of_group_modify",
    "of_group_delete",
]

def sub_class_map(base_type, version):
    """
    Returns an iterable object giving the instance nameys and subclass types
    for the base_type, version values
    """
    rv = []
    if base_type not in inheritance_map:
        return rv

    for instance in inheritance_map[base_type]:
        subcls = loxi_utils.instance_to_class(instance, base_type)
        if not loxi_utils.class_in_version(subcls, version):
            continue
        rv.append((instance, subcls))

    return rv

################################################################
#
# Extension related data and functions
#
################################################################

# Per OF Version, per experimenter, map exp msg type (subtype) to object IDs
# @fixme Generate defines for OF_<exp>_SUBTYPE_<msg> for the values below?
extension_message_subtype = {
    # version 1.0
    of_g.VERSION_1_0:dict(  # Version 1.0 extensions
        bsn = {   # BSN extensions; indexed by class name, value is subtype
            },
        nicira = {   # Nicira extensions, value is subtype
            },
        ),
    of_g.VERSION_1_1:dict(  # Version 1.0 extensions
        bsn = {   # BSN extensions; indexed by class name, value is subtype
            },
        ),
    of_g.VERSION_1_2:dict(  # Version 1.0 extensions
        bsn = {   # BSN extensions; indexed by class name, value is subtype
            },
        ),
    of_g.VERSION_1_3:dict(  # Version 1.0 extensions
        bsn = {   # BSN extensions; indexed by class name, value is subtype
            },
        ),
}

# Set to empty dict if no extension actions defined
# Per OF Version, per experimenter, map actions to subtype
extension_action_subtype = {
    # version 1.0
    of_g.VERSION_1_0:dict(  # Version 1.0 extensions
        bsn = {   # of_action_bsn_
            },
        nicira = {   # of_action_nicira_
            }
        ),
    of_g.VERSION_1_1:dict(  # Version 1.0 extensions
        bsn = {   # of_action_bsn_
            },
        nicira = {   # of_action_nicira_
            }
        ),
    of_g.VERSION_1_2:dict(  # Version 1.0 extensions
        bsn = {   # of_action_bsn_
            },
        nicira = {   # of_action_nicira_
            }
        ),
    of_g.VERSION_1_3:dict(  # Version 1.0 extensions
        bsn = {   # of_action_bsn_
            },
        nicira = {   # of_action_nicira_
            }
        ),
}

# Set to empty dict if no extension actions defined
# Per OF Version, per experimenter, map actions to subtype
extension_action_id_subtype = {
    # version 1.0
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(  # Version 1.3 extensions
        bsn = {   # of_action_bsn_
            },
        nicira = {   # of_action_nicira_
            }
        ),
}

# Set to empty dict if no extension instructions defined
extension_instruction_subtype = {
    # version 1.0
    of_g.VERSION_1_0:dict(),
    of_g.VERSION_1_1:dict(),
    of_g.VERSION_1_2:dict(),
    of_g.VERSION_1_3:dict(
        bsn = {   # of_instruction_bsn_
            },
        nicira = {   # of_instruction_nicira_
            }
        ),
}

# Set to empty dict if no extension instructions defined
extension_queue_prop_subtype = {}

# Set to empty dict if no extension instructions defined
extension_table_feature_prop_subtype = {}

extension_objects = [
    extension_message_subtype,
    extension_action_subtype,
    extension_action_id_subtype,
    extension_instruction_subtype,
    extension_queue_prop_subtype,
    extension_table_feature_prop_subtype
]

################################################################
# These are extension type generic (for messages, actions...)
################################################################

def extension_to_experimenter_name(cls):
    """
    Return the name of the experimenter if class is an
    extension, else None

    This is brute force; we search all extension data for a match
    """

    for ext_obj in extension_objects:
        for version, exp_list in ext_obj.items():
            for exp_name, classes in exp_list.items():
                if cls in classes:
                    return exp_name
    return None

def extension_to_experimenter_id(cls):
    """
    Return the ID of the experimenter if class is an
    extension, else None
    """
    exp_name = extension_to_experimenter_name(cls)
    if exp_name:
        return of_g.experimenter_name_to_id[exp_name]
    return None

def extension_to_experimenter_macro_name(cls):
    """
    Return the "macro name" of the ID of the experimenter if class is an
    extension, else None
    """
    exp_name = extension_to_experimenter_name(cls)
    if exp_name:
        return "OF_EXPERIMENTER_ID_" + exp_name.upper()
    return None

def extension_to_subtype(cls, version):
    """
    Generic across all extension objects, return subtype identifier
    """
    for ext_obj in extension_objects:
        for version, exp_list in ext_obj.items():
            for exp_name, classes in exp_list.items():
                if cls in classes:
                    return classes[cls]

def class_is_extension(cls, version):
    """
    Return True if class, version is recognized as an extension
    of any type (message, action....)

    Accepts of_g.OF_VERSION_ANY
    """

    for ext_obj in extension_objects:
        if cls_is_ext_obj(cls, version, ext_obj):
            return True

    return False

# Internal
def cls_is_ext_obj(cls, version, ext_obj):
    """
    @brief Return True if cls in an extension of type ext_obj
    @param cls The class to check
    @param version The version to check
    @param ext_obj The extension object dictionary (messages, actions...)

    Accepts of_g.VERSION_ANY
    """

    # Call with each version if "any" is passed
    if version == of_g.VERSION_ANY:
        for v in of_g.of_version_range:
            if cls_is_ext_obj(cls, v, ext_obj):
                return True
    else:   # Version specified
        if version in ext_obj:
            for exp, subtype_vals in ext_obj[version].items():
                if cls in subtype_vals:
                    return True

    return False

################################################################
# These are extension message specific
################################################################

def message_is_extension(cls, version):
    """
    Return True if cls, version is recognized as an  extension
    This is brute force, searching records for a match
    """
    return cls_is_ext_obj(cls, version, extension_message_subtype)

def extension_message_to_subtype(cls, version):
    """
    Return the subtype of the experimenter message if the class is an
    extension, else None
    """
    if version in extension_message_subtype:
        for exp, classes in extension_message_subtype[version].items():
            for ext_class, subtype in classes.items():
                if cls == ext_class:
                    return subtype
    return None

################################################################
# These are extension action specific
################################################################

def action_is_extension(cls, version):
    """
    Return True if cls, version is recognized as an action extension
    This is brute force, searching records for a match
    """
    return cls_is_ext_obj(cls, version, extension_action_subtype)

def extension_action_to_subtype(cls, version):
    """
    Return the ID of the action subtype (for its experimenteer)
    if class is an action extension, else None
    """
    if version in extension_action_subtype:
        for exp, classes in extension_action_subtype[version].items():
            if cls in classes:
                return classes[cls]

    return None

################################################################
# These are extension action specific
################################################################

def action_id_is_extension(cls, version):
    """
    Return True if cls, version is recognized as an action ID extension
    This is brute force, searching records for a match
    """
    if version not in [of_g.VERSION_1_3]: # Action IDs only 1.3
        return False
    return cls_is_ext_obj(cls, version, extension_action_id_subtype)

def extension_action_id_to_subtype(cls, version):
    """
    Return the ID of the action ID subtype (for its experimenteer)
    if class is an action ID extension, else None
    """
    if version in extension_action_id_subtype:
        for exp, classes in extension_action_id_subtype[version].items():
            if cls in classes:
                return classes[cls]

    return None

################################################################
# These are extension instruction specific
################################################################

def instruction_is_extension(cls, version):
    """
    Return True if cls, version is recognized as an instruction extension
    This is brute force, searching records for a match
    """
    return cls_is_ext_obj(cls, version, extension_instruction_subtype)

################################################################
# These are extension queue_prop specific
################################################################

def queue_prop_is_extension(cls, version):
    """
    Return True if cls, version is recognized as an instruction extension
    This is brute force, searching records for a match
    """
    return cls_is_ext_obj(cls, version, extension_queue_prop_subtype)

################################################################
# These are extension table_feature_prop specific
################################################################

def table_feature_prop_is_extension(cls, version):
    """
    Return True if cls, version is recognized as an instruction extension
    This is brute force, searching records for a match
    """
    return cls_is_ext_obj(cls, version,
                          extension_table_feature_prop_subtype)
