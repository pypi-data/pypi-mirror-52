# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
`compute.py`
Compute utilities.
"""

from slo_generator import utils

import logging
import time
import pprint
from collections import OrderedDict

LOGGER = logging.getLogger(__name__)

def compute(slo_config, error_budget_policy, timestamp=None, client=None,
            export=False):
    """Run pipeline to compute SLO, Error Budget and Burn Rate, and export the
    results (if exporters are specified in the SLO config).

    Args:
        slo_config (dict): SLO configuration.
        error_budget_policy (dict): Error Budget policy configuration.
        timestamp (int, optional): UNIX timestamp. Defaults to now.
        client (obj, optional): Existing metrics backend client.
        export (bool, optional): Enable / Disable export. Default: False.
    """
    if timestamp is None:
        timestamp = time.time()

    # Compute SLO, Error Budget, Burn rates and make report
    exporters = slo_config.get('exporters')
    reports = []
    for report in make_reports(
            slo_config,
            error_budget_policy,
            timestamp,
            client=client):
        reports.append(report)
        if exporters is not None and export is True:
            export(data, exporters)
    return reports

def export(data, exporters):
    """Export data using selected exporters.

    Args:
        data (dict): Data to export.
        exporters (list): List of exporter configurations.

    Returns:
        obj: Return values from exporters output.
    """
    LOGGER.debug("Exporters: %s" % pprint.pformat(exporters))
    LOGGER.debug("Data: %s" % pprint.pformat(data))
    results = []

    # Passing one exporter as a dict will work for convenience
    if isinstance(exporters, dict):
        exporters = [exporters]

    for config in exporters:
        LOGGER.debug("Exporter config: %s" % pprint.pformat(config))
        exporter_class = config.get('class')
        LOGGER.info("Exporting results to %s" % exporter_class)
        exporter = utils.get_exporter_cls(exporter_class)()
        ret = exporter.export(data, **config)
        results.append(ret)
        LOGGER.debug("Exporter return: %s" % pprint.pformat(ret))

def make_reports(slo_config, error_budget_policy, timestamp, client=None):
    """Run SLO reports for each step in the Error Budget config.

    Args:
        slo_config (dict): SLO configuration.
        error_budget_policy (dict): Error Budget policy.
        timestamp (int): UNIX timestamp.
        client (obj) (optional): Existing metrics backend client.

    Yields:
        list: List of SLO measurement results.
    """
    backend_config = slo_config.get('backend')
    backend_cls = backend_config.get('class')
    method = backend_config.get('method')
    backend = utils.get_backend_cls(backend_cls)(client=client)
    query = getattr(backend, method)

    # Loop through steps defined in error budget policy and make measurements
    for step in error_budget_policy:
        good_event_count, bad_event_count = query(
            timestamp=timestamp,
            window=step['measurement_window_seconds'],
            project_id=slo_config['backend']['project_id'],
            measurement=slo_config['backend']['measurement']
        )
        report = make_measurement(
            slo_config,
            step,
            good_event_count,
            bad_event_count,
            timestamp)
        yield report

def make_measurement(slo_config, step, good_event_count,
                     bad_event_count, timestamp):
    """Measure following metrics: SLI, SLO, Error Budget, Burn Rate.

    Args:
        slo_config (dict): SLO configuration.
        step (dict): Step config.
        good_event_count (int): Good events count.
        bad_event_count (int): Bad events count.
        timestamp (int): UNIX timestamp.

    Returns:
        dict: Report dictionary.
    """
    LOGGER.info(
        "Making SLO measurements for step '%s'",
        step['error_budget_policy_step_name'])
    if (good_event_count + bad_event_count) == 0:
        error = "No valid events for {}/{}/{}/{}".format(
            slo_config['service_name'],
            slo_config['feature_name'],
            slo_config['slo_name'],
            step['error_budget_policy_step_name'])
        LOGGER.error(error)
        return

    LOGGER.debug("Good event count: %s" % good_event_count)
    LOGGER.debug("Bad event count: %s" % bad_event_count)

    slo_target = float(slo_config['slo_target'])
    window = int(step['measurement_window_seconds'])
    alerting_burn_rate_threshold = int(step['alerting_burn_rate_threshold'])
    overburned_consequence_message = step['overburned_consequence_message']
    achieved_consequence_message = step['achieved_consequence_message']
    step_name = step['error_budget_policy_step_name']
    timestamp_human = utils.get_human_time(timestamp)

    # SLI
    sli = good_event_count / (good_event_count + bad_event_count)

    # SLO gap
    gap = sli - slo_target

    # Error budget
    error_budget_target = 1 - slo_target
    error_budget_target = 1 - slo_target
    error_budget_measurement = 1 - sli
    error_budget_remaining_minutes = window * gap / 60
    error_minutes = window * error_budget_measurement / 60
    error_budget_minutes = window * error_budget_target / 60

    # Burn rate
    # The burn rate is also the % of consumed error budget
    error_budget_burn_rate = error_budget_measurement / error_budget_target

    # Alert boolean on burn rate excessive speed
    alert = error_budget_burn_rate > alerting_burn_rate_threshold

    # Consequence message
    if alert:
        consequence_message = overburned_consequence_message
    elif error_budget_burn_rate <= 1:
        consequence_message = achieved_consequence_message
    else:
        consequence_message = (
            'Missed for this measurement window, but not enough to alert')

    # Build out result
    result = OrderedDict({
        'service_name': slo_config['service_name'],
        'feature_name': slo_config['feature_name'],
        'slo_name': slo_config['slo_name'],
        'slo_target': slo_config['slo_target'],
        'slo_description': slo_config['slo_description'],
        'error_budget_policy_step_name': step_name,
        'error_budget_remaining_minutes': error_budget_remaining_minutes,
        'error_budget_minutes': error_budget_minutes,
        'error_minutes': error_minutes,
        'error_budget_target': error_budget_target,
        'timestamp_human': timestamp_human,
        'timestamp': timestamp,
        # 'cadence': cadence,
        'consequence_message': consequence_message,
        'window': window,
        'bad_events_count': bad_event_count,
        'good_events_count': good_event_count,
        'sli_measurement': sli,
        'gap': gap,
        'error_budget_measurement': error_budget_measurement,
        'error_budget_burn_rate': error_budget_burn_rate,
        'alerting_burn_rate_threshold': alerting_burn_rate_threshold,
        'alert': alert
    })
    LOGGER.debug(pprint.pformat(result))
    return result
