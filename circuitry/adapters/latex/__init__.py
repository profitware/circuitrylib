#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sergey Sobko'
__email__ = 'S.Sobko@profitware.ru'
__copyright__ = 'Copyright 2013, The Profitware Group'

from re import match

from circuitry.adapters import AbstractAdapter


class LatexTruthTableAdapter(AbstractAdapter):
    public_properties = ('latex_columns', 'latex_columns_names', 'latex_table')

    default_method = lambda self: \
        (r'\begin{tabular}{%(latex_columns)s}' +
         r'\\\hline\\%(latex_columns_names)s\\' +
         r'\hline\\%(latex_table)s\hline\\\end{tabular}') % \
        {'latex_columns': self.latex_columns,
         'latex_columns_names': self.latex_columns_names,
         'latex_table': self.latex_table}

    @property
    def latex_columns(self):
        return '|%s|' % '|'.join(['c' * len(self._device[_signals]) for _signals in self._device.truth_table_signals])

    @property
    def latex_columns_names(self):
        signals_list = list()
        for signals in self._device.truth_table_signals:
            for signal in self._device[signals]:
                signal_match = match(r'^([a-zA-Z]+)(\d+)', str(signal))
                if signal_match is not None:
                    signals_list.append(('$%s_{%s}$' % (signal_match.group(1), signal_match.group(2))).upper())
        return '&'.join(signals_list)

    @property
    def _truth_table(self):
        return self._device.truth_table

    def _latex_final_state_machine(self, current_signals_name, current_value):
        return '%s' % str(current_value)

    @property
    def latex_table(self):
        truth_table = self._truth_table
        truth_table_lines = list()
        for row in truth_table:
            row_list = list()
            for signals_column_number in range(0, len(self._device.truth_table_signals)):
                current_signals_name = self._device.truth_table_signals[signals_column_number]
                for current_value in row[signals_column_number]:
                    row_list.append(self._latex_final_state_machine(current_signals_name, current_value))
            truth_table_lines.append('&'.join(row_list))
        return ' \\\\\n'.join(truth_table_lines) + ' \\\\\n'