"""
Performance counters library
"""
import json
import logging
import time
from collections import defaultdict
from operator import itemgetter

import numpy as np
from tabulate import tabulate

__version__ = '1.0.5'
__author__ = 'Elie Bursztein (code@elie.net)'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PerfCounters():
    """
    Manage a set of performance counters
    """
    TIMER_COUNTER = 1
    VALUE_COUNTER = 2

    SORT_BY_VALUE = 1
    SORT_BY_NAME = 0

    def __init__(self, prefix=None):
        """Init a new set of counters.

        Args
            prefix (str, optional): prefix automatically appended to counters.
        """
        self.counters = defaultdict(dict)
        self.laps = defaultdict(list)
        self.prefix = prefix

    def __len__(self):
        return len(self.counters)

    def lap(self, name):
        """Record a lap for a given counter

        Args:
            name (str): counter name.
        """
        prefixed_name = self._prefix_counter(name)
        if name not in self.counters:
            self.start(name)
        self.laps[prefixed_name].append(time.time())

    def get(self, name):
        """Return the value of a given counter

        Args:
            name (str): Counter name.

        Returns:
            (int): Counter value
        """

        name = self._prefix_counter(name)
        if name not in self.counters:
            return None
        data = self.counters[name]
        if data['type'] == self.TIMER_COUNTER:
            if 'stop' not in data:
                return time.time() - data['start']
            else:
                return data['stop'] - data['start']
        else:
            return data['value']

    def merge(self, counters):
        """Merge a set of counters generated elsewhere.

        Args:
            counters (PerfCounters): PerfCounters object
        """

        # need to do manual merge to check if there is a dup
        for name, data in counters.counters.items():
            if name in self.counters:
                raise ValueError('Duplicate counter name:', name)
            else:
                self.counters[name] = data

    def set(self, name, value=1):
        """Set a value counter to a given values. Create it if needed.

        Args:
            name (str): counter name.
            value (int, optional): Defaults to 1. Counter value.
        """

        name = self._prefix_counter(name)
        self.counters[name]['value'] = value
        self.counters[name]['type'] = self.VALUE_COUNTER

    def increment(self, name, value=1):
        """
        Increment a value counter by the given value.

        Args:
            name (str): Counter name. Counter will be created if needed.
            value (int, optional): Defaults to 1. Value to increment by.
        """

        name = self._prefix_counter(name)
        if name in self.counters:
            self.counters[name]['value'] += value
        else:
            self.set(name, value=value)

    def start(self, name, warning_deadline=0, log=False):
        """ Create a new time counter.

        Args:
            name (str): counter name.
            warning_deadline (int, optional): log a warning if the counter
            exceed deadline.
            log(Bool, optional): log an info entry that counter started.
        """
        name = self._prefix_counter(name)
        if name in self.counters:
            raise ValueError("Timing counter exist. Counter name:", name)
        else:
            self.counters[name] = {}
            self.counters[name]['start'] = time.time()
            self.counters[name]['type'] = self.TIMER_COUNTER

        if warning_deadline:
            self.counters[name]['warning_deadline'] = warning_deadline

        if log:
            logger.info("%s counter started", name)

    def stop(self, name, log=False):
        """ Stop a given time counter.

        Args:
            name (str): counter name.
            log (bool, optional): add info log entry with time elapsed.
        """
        name = self._prefix_counter(name)
        if name in self.counters:
            self.counters[name]['stop'] = time.time()
        else:
            error_msg = "counter '%s' stopped before being created" % name
            logger.error(error_msg)
            raise ValueError(error_msg)

        if log:
            delta = self.counters[name]['stop'] - self.counters[name]['start']
            logger.info("%s counter stopped - elapsed:%s" % (name, delta))

        if 'warning_deadline' in self.counters[name]:
            diff = self.counters[name]['stop'] - self.counters[name]['start']
            if diff > self.counters[name]['warning_deadline']:
                logger.warning("counter %s deadline exceeded. Operation took:\
                               %s secs. Deadline was: %s secs", name, diff,
                               self.counters[name]['warning_deadline'])

    def stop_all(self):
        """ Stop all time counters."""
        for name, data in self.counters.items():
            if self.counters[name]['type'] == self.TIMER_COUNTER:
                if 'stop' not in data:
                    self.stop(name)

    def to_json(self):
        """Return counters as json object"""
        counters = self._get_counter_lists()
        # FIXME add laps and don't use a list
        return json.dumps(counters)

    def to_html(self, sort_by=1, reverse=True):
        """Return counters as HTML tables

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        Returns:
            str: counters as HTML tables
        """
        tables = self._tabulate(table_format='html')
        html = ""
        for table_name, table in tables.items():
            html += "%s</br>%s</br>" % (table_name, table)
        return html

    def report(self, sort_by=1, reverse=True):
        """Print counters in stdout as nicely formated tables.

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        """
        tables = self._tabulate(sort_by=sort_by, reverse=reverse)
        for table_name, table in tables.items():
            print("-=[%s]=-\n" % table_name)
            print("%s\n" % table)

    def log(self, sort_by=1, reverse=True):
        """Write counters in the info log

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
        """
        counter_lists = self._get_counter_lists(sort_by, reverse)
        for cnt_type, cnts in counter_lists.items():
            logger.info("\n-=[%s]=-\n" % cnt_type)
            for cnt in cnts:
                logger.info("%s:%s\n" % (cnt[0], cnt[1]))

    def _tabulate(self, sort_by=1, reverse=True, table_format='grid'):
        """Format counters as ASCII tables.

        Args:
            sort_by (int, optional): Defaults to SORT_BY_VALUE. How to\
            sort counters.
            reverse (bool, optional): Defaults to False. Reverse sort order.
            table_format (str, optional): Defaults to grid. Tabulate table\
            format style to use.

        Returns:
            dict: time_counters, value_counters as ASCII tables.
        """

        tables = {}
        counter_lists = self._get_counter_lists(sort_by, reverse)

        for cnt_type, cnts in counter_lists.items():

            # add laps stats if they exist to timer counters
            if cnt_type == self.TIMER_COUNTER and len(self.laps):
                headers = ['name', 'value', 'laps']

            else:
                headers = ["name", "value"]

            tables[cnt_type] = tabulate(cnts, headers, tablefmt=table_format)

        return tables

    def _get_counter_lists(self, sort_by=1, reverse=True):
        """Get sorted counter lists.
        """
        counters = defaultdict(list)
        for name, data in self.counters.items():
            if self.counters[name]['type'] == self.TIMER_COUNTER:
                if 'stop' not in data:
                    delta = time.time() - data['start']
                else:
                    delta = data['stop'] - data['start']
                # FIXME: lap stats
                counters['Timing counters'].append([name, delta])
            else:
                counters['Value counters'].append([name, data['value']])

        for k, v in counters.items():
            counters[k] = sorted(v, key=itemgetter(sort_by), reverse=reverse)

        return counters

    def _prefix_counter(self, name):
        """Prefix counter if needed.

        Args:
            name (str): counter name.
        """

        if self.prefix:
            return "%s_%s" % (self.prefix, name)
        else:
            return name

    def _compute_lap_stats(self):
        "compute laps statistics"

        stats = {}

        for name, timings in self.laps.items():

            # getting initial time
            previous_time = self.counters[name]['start']

            # computing deltas
            deltas = []
            for timing in timings:
                deltas.append(timing - previous_time)
                previous_time = timing

            # stats
            s = {
                "min": np.min(deltas),
                "average": np.average(deltas),
                "median": np.median(deltas),
                "max": np.max(deltas),
                "stddev": np.std(deltas)
            }
            stats[name] = s
        return stats
