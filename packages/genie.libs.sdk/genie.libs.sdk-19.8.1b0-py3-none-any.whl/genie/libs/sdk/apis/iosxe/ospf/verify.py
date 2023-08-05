"""Common verification functions for OSPF"""

# Python
import logging

# pyATS
from ats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError
)
from genie.libs.sdk.libs.utils.normalize import GroupKeys

# OSPF
from genie.libs.sdk.apis.iosxe.ospf.get import (
    get_ospf_neighbors_in_state,
    get_ospf_neighbors,
)

log = logging.getLogger(__name__)


def verify_ospf_max_metric_configuration(
    device, ospf_process_id, metric_value, max_time=15, check_interval=5
):
    """Verify OSPF max-metric configuration

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process ID
            metric_value (`int`): Metric value to be configured
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result(`bool`): verify result
            state
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ip ospf max-metric")
        except SchemaEmptyParserError:
            pass

        if out:
            try:
                for area in out["vrf"]["default"]["address_family"]["ipv4"][
                    "instance"
                ][str(ospf_process_id)]["base_topology_mtid"]:
                    res = out["vrf"]["default"]["address_family"]["ipv4"][
                        "instance"
                    ][str(ospf_process_id)]["base_topology_mtid"][area][
                        "router_lsa_max_metric"
                    ][
                        True
                    ][
                        "condition"
                    ]
                    state = out["vrf"]["default"]["address_family"]["ipv4"][
                        "instance"
                    ][str(ospf_process_id)]["base_topology_mtid"][area][
                        "router_lsa_max_metric"
                    ][
                        True
                    ][
                        "state"
                    ]

                    if str(metric_value) in res:
                        return state
            except KeyError:
                pass
        timeout.sleep()
    return False


def verify_ospf_neighbor_state(device, state, max_time=15, check_interval=5):
    """Verify OSPF neighbor is state

        Args:
            device (`obj`): Device object
            state (`str`): State to check for neighbor
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False        
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ip ospf neighbor")
        except SchemaEmptyParserError:
            pass
        if out:
            try:
                for intf in out["interfaces"]:
                    for neighbor in out["interfaces"][intf]["neighbors"]:
                        if (
                            state
                            in out["interfaces"][intf]["neighbors"][neighbor][
                                "state"
                            ]
                        ):
                            return True
            except KeyError:
                pass
        timeout.sleep()

    return False


def is_ospf_shutdown(
    device, max_time=15, check_interval=5, interface=None
):
    """ Verifies ospf is shutdown by verifying there are
        no neighbors

        Args:
            device('obj'): device to use
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            interface ('str'): Interface name
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        neighbors = get_ospf_neighbors(device, interface)
        if not neighbors:
            return True

        log.info(
            "OSPF is not shutdown; neighbors {} are still enabled".format(
                neighbors
            )
        )

        timeout.sleep()

    return False


def verify_ospf_in_state(
    device,
    neighbors=None,
    state=None,
    max_time=15,
    check_interval=5,
    interface=None,
):

    """ Verifies ospf process is enabled by checking if neighbors exist.
        If a list of neighbors is passed it will also verify is those neighbors
        have reached state

        Args:
            device('obj'): device to use
            neighbors('list'): If specified, function will verify the neighbors
                               are listed.
            state('str'): If specified, function will verify the neighbors are in
                          state.
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if not neighbors:
            if state:
                neighbors = get_ospf_neighbors_in_state(
                    device=device,
                    state=state,
                    neighbor_interface=interface,
                )
            else:
                neighbors = get_ospf_neighbors(
                    device=device, neighbor_interface=interface
                )

            if neighbors:
                return True
            else:
                log.info("OSPF is not enabled; no neighbors are enabled.")
        else:
            neighbors_in_state = get_ospf_neighbors_in_state(
                device, state=state
            )
            if set(neighbors).issubset(neighbors_in_state):
                return True

            log.info(
                "OSPF is not enabled; neighbors {} are not enabled.".format(
                    neighbors
                )
            )

        timeout.sleep()

    return False


def is_interface_igp_sync_ospf_enabled(
    interface,
    vrf,
    address_family,
    instance,
    area_address,
    device,
    parsed_output=None,
    max_time=15,
    check_interval=5,
):
    """ Verifies if interface has LDP IGP sync enabled 
        from command 'show ip ospf mpls ldp interface'
        
        Args:
            parsed_output ('dict')  : Output from parser
            interface ('str')       : Interface being checked
            vrf      ('str')        : vrf name
            address_family ('str')  : Interface address family (ipv4 or ipv6)
            instance ('str')        : Instance number
            area_address ('str')    : Area address
            device                  : Device to be executed command
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Raises:
            Exception

        Returns
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if not parsed_output:
            try:
                parsed_output = device.parse("show ip ospf mpls ldp interface")
            except SchemaEmptyParserError as se:
                pass
        try:
            igp_sync = (
                parsed_output["vrf"]
                .get(vrf, {})
                .get("address_family", {})
                .get(address_family, {})
                .get("instance", {})
                .get(instance, {})
                .get("areas", {})
                .get(area_address, {})
                .get("interfaces", {})
                .get(interface, {})
                .get("mpls", {})
                .get("ldp", {})
                .get("igp_sync", False)
            )
            return igp_sync
        except Exception:
            log.error("Could not extract IGP sync information")
        parsed_output = None
        timeout.sleep()
    return False


def verify_sid_in_ospf(
    device,
    process_id=None,
    sid=None,
    code=None,
    ip_address=None,
    avoid_codes=None,
    prefix=None,
):
    """ Verifies if SID is found in ospf
        from command 'show ip ospf segment-routing sid-database'

        Args:
            device (`obj`): Device to be executed command
            process_id (`int`): Process Id to check in output
            sid (`int`): SID value
            code (`str`): Check for codes in output
                ex.) code = 'L'
            ip_address (`str`): IP address to check in output
            avoid_codes (`list`): List of codes to avoid
                ex.)
                    avoid_codes = ['L', 'C']
            prefix (`str`): IP address to check as prefix in output
                ex.) prefix = '10.66.12.12/32'
        Raises:
            None
        Returns
            True
            False

    """
    try:
        out = device.parse("show ip ospf segment-routing sid-database")
    except (SchemaEmptyParserError):
        return False
    sid_count = 0

    if not avoid_codes:
        avoid_codes = []

    try:
        """
        ex.) Ouput for reference for dictionary out["process_id"]
        {
            'process_id': {
                '65109': {
                    'router_id': '10.66.12.12',
                    'sids': {
                        'total_entries': 1,
                        1: {
                            'sid': 1,
                            'codes': 'L',
                            'prefix': '10.66.12.12/32',
                            'adv_rtr_id': '10.66.12.12',
                            'area_id': 10.49.0.0
                        }
                    }
                }
            }
        }
        """
        for p_id, sid_dict in out["process_id"].items():
            if process_id and p_id != process_id:
                continue
            values = sid_dict["sids"].values()
            for v in values:
                if isinstance(v, int):
                    continue
                if sid and ("sid" not in v or v["sid"] != sid):
                    continue
                if ip_address and (
                    "adv_rtr_id" not in v or v["adv_rtr_id"] != ip_address
                ):
                    continue
                if code and ("codes" not in v or v["codes"] != code):
                    continue
                if avoid_codes and (
                    "codes" in v and v["codes"] in avoid_codes
                ):
                    continue
                if prefix and ("prefix" not in v or v["prefix"] != prefix):
                    continue
                sid_count += 1

    except KeyError:
        pass

    return sid_count != 0

def is_type_10_opaque_area_link_states_originated(device, max_time=300, check_interval=30, expected_result=True):
    """ Verifies if Type 10 opaque area link states are originated
        from command 'show ip ospf database opaque-area self-originate'

        Args:
            device (`obj`): Device to be executed command
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_result ('bool'): Expected result
                set expected_result = False if method should fail
                set expected_result = True if method should pass (default value)
        Raises:
            None
        Returns
            True
            False

    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ip ospf database opaque-area self-originate')
        except (SchemaEmptyParserError):
            pass

        if out:
            reqs = R(
                [
                'vrf',
                '(?P<vrf>.*)',
                'address_family',
                '(?P<af>.*)',
                'instance',
                '(?P<instance>.*)',
                'areas',
                '(?P<areas>.*)',
                'database',
                'lsa_types',
                '(?P<lsa_types>.*)',
                'lsa_type',
                '(?P<lsa_type>.*)'
                ]
            )

            found = find([out], reqs, filter_=False, all_keys=True)

            if not found and not expected_result:
                return expected_result

            if found:
                key_list = GroupKeys.group_keys(
                    reqs=reqs.args, ret_num={}, source=found, all_keys=True
                )

                if (key_list.pop()['lsa_type'] == 10) == expected_result:
                    return expected_result

        timeout.sleep()

    return False


def verify_opaque_type_7_prefix_and_flags(
    device, vrf, address_family, instance, prefix, flags
):
    """ Verifies if SID is found in ospf
        from command 'show ip ospf segment-routing sid-database'

        Args:
            device (`obj`): Device to be executed command
            vrf (`str`): VRF name
            address_family (`str`): Address family
            instance (`str`): Instance value
                ex.) instance = '65109'
            prefix (`str`): IP address to check as prefix in output
                ex.) prefix = '10.66.12.12/32'
            flags (`str`): Flags to check in output
                ex.) flags = 'N-bit'
        Raises:
            None
        Returns
            True
            False

    """

    out = device.parse("show ip ospf database opaque-area self-originate")

    filter_dict = {}
    filter_dict.update({"flags": flags})
    filter_dict.update({"prefix": prefix})

    for k, v in filter_dict.items():
        reqs = R(
            [
                "vrf",
                vrf,
                "address_family",
                address_family,
                "instance",
                instance,
                "areas",
                "(?P<area>.*)",
                "database",
                "lsa_types",
                "(?P<lsa_types>.*)",
                "lsas",
                "(?P<lsas>7.*)",
                "ospfv2",
                "body",
                "opaque",
                "extended_prefix_tlvs",
                "(?P<extended_prefix_tlvs>.*)",
                k,
                v,
            ]
        )
        found = find([out], reqs, filter_=False, all_keys=True)

        if not found:
            return False

    return True


def verify_sid_is_advertised_in_ospf(
    device, router_id, vrf, address_family, instance, prefix, flags
):
    """ Verifies if SID is advertised in ospf
        from command 'show ip ospf database opaque-area adv-router {router_id}'

        Args:
            device (`obj`): Device to be executed command
            router_id (`str`): Router ID
            vrf (`str`): VRF name
            address_family (`str`): Address family
            instance (`str`): Instance value
                ex.) instance = '65109'
            prefix (`str`): IP address to check as prefix in output
                ex.) prefix = '10.66.12.12/32'
            flags (`str`): Flags to check in output
                ex.) flags = 'N-bit'
        Raises:
            None
        Returns
            True
            False

    """
    out = device.parse(
        "show ip ospf database opaque-area adv-router {router_id}".format(
            router_id=router_id
        )
    )

    filter_dict = {}
    filter_dict.update({"flags": flags})
    filter_dict.update({"prefix": prefix})

    for k, v in filter_dict.items():
        reqs = R(
            [
                "vrf",
                vrf,
                "address_family",
                address_family,
                "instance",
                instance,
                "areas",
                "(?P<area>.*)",
                "database",
                "lsa_types",
                "(?P<lsa_types>.*)",
                "lsas",
                "(?P<lsas>7.*)",
                "ospfv2",
                "body",
                "opaque",
                "extended_prefix_tlvs",
                "(?P<extended_prefix_tlvs>.*)",
                k,
                v,
            ]
        )
        found = find([out], reqs, filter_=False, all_keys=True)

        if not found:
            return False

    return True

def verify_ospf_tilfa_in_state_in_ospf(
    device,
    interface,
    max_time=60,
    check_interval=10,
    process_id=None,
    state="enabled",
):
    """ Verify if TI-LFA is enabled in OSPF

        Args:
            device ('str'): Device object
            interface ('str'): Interface name
            process_id ('int'): Process id
            max_time (int): Maximum wait time in seconds checking an ouput
            check_interval (int): Wait time between iterations when looping

        Raises:
            None
        Returns:
            True
            False
    """

    if state not in ("enabled", "disabled"):
        log.error('Expected state must be either "enabled" or "disabled"')
        return False

    timeout = Timeout(max_time=max_time, interval=check_interval)
    ti_lfa_enabled = "no"
    while timeout.iterate():
        try:
            output = device.parse("show ip ospf fast-reroute ti-lfa")
        except SchemaEmptyParserError:
            if "disabled" == state:
                break
            log.info("Could not find any information about ti-lfa")
            timeout.sleep()
            continue

        if process_id:
            ti_lfa_enabled = (
                output["process_id"]
                .get(process_id, {})
                .get("ospf_object", {})
                .get(interface, {})
                .get("ti_lfa_enabled", "no")
            )
            if ti_lfa_enabled == "yes":
                log.info("TI-LFA is enabled in OSPF on process {process_id} "
                         "and interface {interface} on device {device}"\
                         .format(process_id=process_id, interface=interface, device=device.name))
                return True

        else:
            for process_id in output["process_id"]:
                for intf in output["process_id"][process_id][
                    "ospf_object"
                ].get(interface, {}):
                    ti_lfa_enabled = output["process_id"][process_id].get(
                        "ospf_object", {}
                    )[interface]["ti_lfa_enabled"]
                    if ti_lfa_enabled == "yes":
                        log.info("TI-LFA is enabled in OSPF on process {process_id} "
                                 "and interface {interface} on device {device}"\
                                 .format(process_id=process_id, interface=interface, device=device.name))
                        return True

        if "disabled" == state:
            break

        timeout.sleep()

    log.info("TI-LFA is not enabled in OSPF")
    return False

def is_ospf_tilfa_enabled_in_sr(
    device,
    area=None,
    interface=None,
    max_time=60,
    check_interval=10,
    process_id=None,
    output=None,
):
    """ Verify if TI-LFA is enabled in SR

    Args:
        device ('str'): Device object
        interface ('str'): Interface name
        process_id ('int'): Process id
        area ('str'): Ospf area
        neighbor_address ('str'): Neighbor address
        max_time (int): Maximum wait time in seconds checking an ouput
        check_interval (int): Wait time between iterations when looping
        output ('dict'): Parsed output of command 'show ip ospf segment-routing protected-adjacencies'
    Raises:
        None
    Returns:
        True/False
    """

    log.info("Checking if TI-LFA is enabled in SR")

    is_enabled = False

    if not output:
        try:
            output = device.parse(
                "show ip ospf segment-routing protected-adjacencies"
            )
        except SchemaEmptyParserError:
            log.info("TI-LFA is not enabled in SR")
            return False

    if area and process_id and interface:
        neighbors = (
            output["process_id"]
            .get(process_id, {})
            .get("areas", {})
            .get(area, {})
            .get("neighbors", {})
        )
        for neighbor in neighbors:
            is_enabled = neighbors[neighbor]["interface"].get(interface, False)
            if is_enabled:
                log.info(
                    "TI-LFA is enabled in SR for interface {interface}".format(
                        interface=interface
                    )
                )
                break

    elif process_id and area:
        is_enabled = (
            output["process_id"]
            .get(process_id, {})
            .get("areas", {})
            .get(area, False)
        )
        if is_enabled:
            log.info(
                "TI-LFA is enabled for process id {process_id} and area {area}".format(
                    process_id=process_id, area=area
                )
            )

    elif process_id:
        is_enabled = (
            output["process_id"].get(process_id, {}).get("areas", False)
        )
        if is_enabled:
            log.info(
                "TI-LFA is enabled for process id {process_id}".format(
                    process_id=process_id
                )
            )

    elif area:
        for process_id in output["process_id"]:
            is_enabled = output["process_id"][process_id]["areas"].get(
                area, False
            )
            if is_enabled:
                log.info("TI-LFA is enabled on area {area}".format(area=area))
                break

    elif interface:
        for process_id in output["process_id"]:
            for area in output["process_id"][process_id]["areas"]:
                for neighbor in output["process_id"][process_id]["areas"][
                    area
                ]["neighbors"]["neighbors"]:
                    for intf in output["process_id"][process_id]["areas"][
                        area
                    ]["neighbors"]["neighbors"][neighbor]["interface"]:
                        if intf == interface:
                            log.info(
                                "TI-LFA is enabled in SR for interface {interface}".format(
                                    interface=interface
                                )
                            )
                            log.info("TI-LFA is enabled in SR")
                            return True
    else:
        for process_id in output["process_id"]:
            for area in output["process_id"][process_id].get("areas", {}):
                log.info(
                    "TI-LFA is enabled in SR for process {process_id} and area {area}".format(
                        process_id=process_id, area=area
                    )
                )
                return True

    if is_enabled:
        log.info("TI-LFA is enabled in SR")
        return True

    log.info("TI-LFA is not enabled in SR")
    return False

def is_ospf_sr_label_preferred(device, process_id, output=None, max_time=60, check_interval=10):
    """ Verify if SR label is preferred for a process id
        Args:
            device ('obj'): Device object
            process_id ('str'): Process if
        Returns:
            True: SR labels are preferred
            False: SR labels are not preferred
        Raises:
            None
    """

    log.info("Getting SR attributes")
    if not output:
        try:
            output = device.parse("show ip ospf segment-routing")
        except SchemaEmptyParserError:
            log.info("Could not find any SR attributes")

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        is_sr_label_prefered = (
            output["process_id"]
            .get(process_id, {})
            .get("sr_attributes", {})
            .get("sr_label_preferred", False)
        )

        if is_sr_label_prefered:
            log.info("SR labels are the preferred ones")
            return True        

        try:
            output = device.parse("show ip ospf segment-routing")
        except SchemaEmptyParserError:
            log.info("Could not find any SR attributes")
            timeout.sleep()
            continue
        
        log.info("SR labels are not the preferred ones")
        timeout.sleep()
    
    return is_sr_label_prefered

def verify_ospf_segment_routing_lb_srlb_base_and_range(
    device,
    process_id,
    router_id,
    expected_srlb_base=None,
    expected_srlb_range=None,
    max_time=30,
    check_interval=10,
):
    """ Verifies segment routing gb SRLB Base value

        Args:
            device ('obj'): Device to use
            process_id ('str'): Ospf process id
            router_id ('str'): Router entry to look under
            expected_srlb_base ('int'): Expected value for SRLB Base
            expected_srlb_range ('int'): Expected value for SRLB Range
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
             True/False

        Raises:
            None
    """
    log.info(
        "Verifying router {router} has SRLB Base value of {value} and SRLB Range value of {value2}".format(
            router=router_id,
            value=expected_srlb_base,
            value2=expected_srlb_range,
        )
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        srlb_base, srlb_range = device.api.get_ospf_segment_routing_lb_srlb_base_and_range(
            device=device, process_id=process_id, router_id=router_id
        )

        if not (expected_srlb_base and expected_srlb_base != srlb_base) or (
            expected_srlb_range and expected_srlb_range != srlb_range
        ):
            return True

        if expected_srlb_base and expected_srlb_base != srlb_base:
            log.info(
                "Router {router} has SRLB Base value of {value}. Expected value is {expected}".format(
                    router=router_id,
                    value=srlb_base,
                    expected=expected_srlb_base,
                )
            )
        if expected_srlb_range and expected_srlb_range != srlb_range:
            log.info(
                "Router {router} has SRLB Range value of {value}. Expected value is {expected}".format(
                    router=router_id,
                    value=srlb_range,
                    expected=expected_srlb_range,
                )
            )

        timeout.sleep()

    return False


def verify_ospf_segment_routing_gb_srgb_base_and_range(
    device,
    process_id,
    router_id,
    expected_srgb_base=None,
    expected_srgb_range=None,
    max_time=30,
    check_interval=10,
):
    """ Verifies segment routing gb SRGB Base value

        Args:
            device ('obj'): Device to use
            router_id ('str'): Router entry to look under
            expected_srgb_base ('int'): Expected value for SRGB Base
            expected_srgb_base ('int'): Expected value for SRGB Range
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
             True/False

        Raises:
            None
    """
    log.info(
        "Verifying router {router} has SRGB Base value of {value}".format(
            router=router_id, value=expected_srgb_base
        )
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        srgb_base, srgb_range = device.api.get_ospf_segment_routing_gb_srgb_base_and_range(
            device=device, process_id=process_id, router_id=router_id
        )

        if not (expected_srgb_base and expected_srgb_base != srgb_base) or (expected_srgb_range and expected_srgb_range != srgb_range):
            return True

        if expected_srgb_base and expected_srgb_base != srgb_base:
            log.info(
                "Router {router} has SRGB Base value of {value}. Expected value is {expected}".format(
                    router=router_id, value=srgb_base, expected=expected_srgb_base
                )
            )
        if expected_srgb_range and expected_srgb_range != srgb_range:
            log.info(
                "Router {router} has SRGB Range value of {value}. Expected value is {expected}".format(
                    router=router_id, value=srgb_range, expected=expected_srgb_range
                )
            )

        timeout.sleep()

    return False
