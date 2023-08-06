"""GWCelery application configuration.

This module defines configuration variables and default values, including both
:doc:`generic options for Celery <celery:userguide/configuration>` as well as
options that control the behavior of specific GWCelery :mod:`~gwcelery.tasks`.

To override the configuration, define the ``CELERY_CONFIG_MODULE`` environment
variable to the fully qualified name of any Python module that can be located
in :obj:`sys.path`, including any of the following presets:

 * :mod:`gwcelery.conf.development`
 * :mod:`gwcelery.conf.playground` (the default)
 * :mod:`gwcelery.conf.production`
 * :mod:`gwcelery.conf.test`
"""

import getpass
import os

# Celery application settings.

# Task tombstones expire after 5 minutes.
# Celery's default setting of 1 day could cause the Redis database to grow too
# large because we pass large byte strings as task arguments and return values.
result_expires = 300

# Use pickle serializer, because it supports byte values.
accept_content = ['json', 'pickle']
event_serializer = 'json'
result_serializer = 'pickle'
task_serializer = 'pickle'

# Task priority settings.
task_inherit_parent_priority = True
task_default_priority = 0
task_queue_max_priority = 1
priority_steps = list(range(task_queue_max_priority + 1))

# GWCelery-specific settings.

expose_to_public = False
"""Set to True if events meeting the public alert threshold really should be
exposed to the public."""

lvalert_host = 'lvalert-playground.cgca.uwm.edu'
"""LVAlert host."""

gracedb_host = 'gracedb-playground.ligo.org'
"""GraceDB host."""

voevent_broadcaster_address = ':5342'
"""The VOEvent broker will bind to this address to send GCNs.
This should be a string of the form `host:port`. If `host` is empty,
then listen on all available interfaces."""

voevent_broadcaster_whitelist = []
"""List of hosts from which the broker will accept connections.
If empty, then completely disable the broker's broadcast capability."""

voevent_receiver_address = '68.169.57.253:8099'
"""The VOEvent listener will connect to this address to receive GCNs. For
options, see `GCN's list of available VOEvent servers
<https://gcn.gsfc.nasa.gov/voevent.html#tc2>`_. If this is an empty string,
then completely disable the GCN listener."""

superevent_d_t_start = {'gstlal': 1.0,
                        'spiir': 1.0,
                        'pycbc': 1.0,
                        'mbtaonline': 1.0}
"""Pipeline based lower extent of superevent segments.
For cwb and lib this is decided from extra attributes."""

superevent_d_t_end = {'gstlal': 1.0,
                      'spiir': 1.0,
                      'pycbc': 1.0,
                      'mbtaonline': 1.0}
"""Pipeline based upper extent of superevent segments
For cwb and lib this is decided from extra attributes."""

superevent_query_d_t_start = 100.
"""Lower extent of superevents query"""

superevent_query_d_t_end = 100.
"""Upper extent of superevents query"""

superevent_default_d_t_start = 1.0
"""Default lower extent of superevent segments"""

superevent_default_d_t_end = 1.0
"""Default upper extent for superevent segments"""

superevent_far_threshold = 1 / 3600
"""Maximum false alarm rate to consider events superevents."""

preliminary_alert_far_threshold = {'cbc': 1 / (60 * 86400),
                                   'burst': 1 / (365 * 86400),
                                   'test': 1 / (30 * 86400)}
"""Group specific maximum false alarm rate to consider
sending preliminary alerts."""

preliminary_alert_trials_factor = dict(cbc=4.0, burst=3.0)
"""Trials factor corresponding to trigger categories. For CBC and Burst, trials
factor is the number of pipelines. CBC pipelines are gstlal, pycbc, mbtaonline
and spiir. Burst searches are cwb.allsky, cwb.bbh and cwb.imbh."""

orchestrator_timeout = 300.0
"""The orchestrator will wait this many seconds from the time of the
creation of a new superevent to the time that annotations begin, in order
to let the superevent manager's decision on the preferred event
stabilize."""

pe_timeout = orchestrator_timeout + 45.0
"""The orchestrator will wait this many seconds from the time of the
creation of a new superevent to the time that parameter estimation begins, in
case the preferred event is updated with high latency."""

check_vector_prepost = {'gstlal': [2, 2],
                        'spiir': [2, 2],
                        'pycbc': [2, 2],
                        'MBTAOnline': [2, 2],
                        'oLIB': [0.5, 0.5],
                        'LIB': [0.5, 0.5],
                        'CWB': [0.5, 0.5],
                        'HardwareInjection': [2, 2],
                        'Swift': [2, 2],
                        'Fermi': [2, 2],
                        'SNEWS': [10, 10]}
"""Seconds before and after the superevent start and end times which the DQ
vector check will include in its check. Pipeline dependent."""

uses_gatedhoft = {'gstlal': True,
                  'spiir': True,
                  'pycbc': True,
                  'MBTAOnline': True,
                  'oLIB': False,
                  'LIB': False,
                  'CWB': True,
                  'HardwareInjection': False,
                  'Swift': False,
                  'Fermi': False,
                  'SNEWS': False}
"""Whether or not a pipeline uses gated h(t). Determines whether or not
the DMT-DQ_VECTOR will be analyzed for data quality."""

llhoft_glob = '/dev/shm/kafka/{detector}_O2/*.gwf'
"""File glob for playground low-latency h(t) frames. Currently points
to O2 replay data."""

llhoft_channels = {
    'H1:DMT-DQ_VECTOR': 'dmt_dq_vector_bits',
    'L1:DMT-DQ_VECTOR': 'dmt_dq_vector_bits',
    'H1:GDS-CALIB_STATE_VECTOR': 'ligo_state_vector_bits',
    'L1:GDS-CALIB_STATE_VECTOR': 'ligo_state_vector_bits',
    'V1:DQ_ANALYSIS_STATE_VECTOR': 'virgo_state_vector_bits'}
"""Low-latency h(t) state vector configuration. This is a dictionary consisting
of a channel and its bitmask, as defined in :mod:`gwcelery.tasks.detchar`."""

idq_channels = ['H1:IDQ-PGLITCH_OVL_32_2048',
                'L1:IDQ-PGLITCH_OVL_32_2048']
"""Low-latency iDQ p(glitch) channel names from O2 replay."""

idq_pglitch_thresh = 0.95
"""If P(Glitch) is above this threshold, and
:obj:`~gwcelery.conf.idq_veto` for the pipeline is true, DQV will be labeled
for the event.
"""

idq_veto = {'gstlal': False,
            'spiir': False,
            'pycbc': False,
            'MBTAOnline': False,
            'oLIB': False,
            'LIB': False,
            'CWB': False,
            'HardwareInjection': False,
            'Swift': False,
            'Fermi': False,
            'SNEWS': False}
"""If true for a pipeline, iDQ values above the threshold defined in
:obj:`~gwcelery.conf.idq_pglitch.thres` will cause DQV to be labeled.
Currently all False, pending iDQ review (should be done before O3).
"""

low_latency_frame_types = {'H1': 'H1_O2_llhoft',
                           'L1': 'L1_O2_llhoft',
                           'V1': 'V1_O2_llhoft'}
"""Types of low latency frames used in Parameter Estimation with LALInference
(see :mod:`gwcelery.tasks.lalinference`) and in cache creation for detchar
checks (see :mod:`gwcelery.tasks.detchar`).
"""

high_latency_frame_types = {'H1': None,
                            'L1': None,
                            'V1': None}
"""Types of high latency frames used in Parameter Estimation with LALInference
and in cache creation for detchar checks. They do not exist for O2Replay data.
(see :mod:`gwcelery.tasks.lalinference` and :mod:`gwcelery.tasks.detchar`)
"""

strain_channel_names = {'H1': 'H1:GDS-CALIB_STRAIN_O2Replay',
                        'L1': 'L1:GDS-CALIB_STRAIN_O2Replay',
                        'V1': 'V1:Hrec_hoft_16384Hz_O2Replay'}
"""Names of h(t) channels used in Parameter Estimation with LALInference (see
:mod:`gwcelery.tasks.lalinference`)"""

state_vector_channel_names = {'H1': 'H1:GDS-CALIB_STATE_VECTOR',
                              'L1': 'L1:GDS-CALIB_STATE_VECTOR',
                              'V1': 'V1:DQ_ANALYSIS_STATE_VECTOR'}
"""Names of state vector channels used in Parameter Estimation with
LALInference (see :mod:`gwcelery.tasks.lalinference`)"""

pe_threshold = 1.0 / (28 * 86400)
"""FAR threshold in Hz for Parameter Estimation. PE group now applies
1/(4 weeks) as a threshold. 86400 seconds = 1 day and 28 days = 4 weeks."""

pe_results_path = os.path.join(os.getenv('HOME'), 'public_html/online_pe')
"""Path to the results of Parameter Estimation (see
:mod:`gwcelery.tasks.lalinference`)"""

pe_results_url = ('https://ldas-jobs.ligo.caltech.edu/~{}/'
                  'online_pe/').format(getpass.getuser())
"""URL of page where all the results of Parameter Estimation are outputted
(see :mod:`gwcelery.tasks.lalinference`)"""

raven_coincidence_windows = {'GRB_CBC': [-5, 1],
                             'GRB_Burst': [-600, 60],
                             'SNEWS': [-10, 10]}
"""Time coincidence windows passed to ligo-raven. External events and
superevents of the appropriate type are considered to be coincident if
within time window of each other."""

mock_events_simulate_multiple_uploads = False
"""If True, then upload each mock event several times in rapid succession with
random jitter in order to simulate multiple pipeline uploads."""
