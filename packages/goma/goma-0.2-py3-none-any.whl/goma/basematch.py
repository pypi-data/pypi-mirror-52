# -*- coding: utf-8 -*-

# goma
# ----
# Generic object mapping algorithm.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.2, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/goma
# License:  Apache License 2.0 (see LICENSE file)


class BaseMatch(object):
    """ Base match class """

    def match(self, *args):
        """ return match results """
        pass  # functions are implemented in sub classes

    def _has_relation_operator(self, condition_str):
        return str(condition_str)[:1] in ['<', '>', '!', '=', '(', '[']

    def _apply_relation_match(self, match_value, detail_value):
        """ return relation match results """

        match_value = match_value.replace(' ', '')

        # if interval
        if match_value[:1] in ['[', '(']:
            rel_vals = [type(detail_value)(val) for val in match_value[1:-1].split(',')]
            rel_ops = [self._repl_relation_operator(op) for op in [match_value[0], match_value[-1]]]
            # fixme NO eval usage !!!
            cmd = 'detail_value ' + rel_ops[0] + ' rel_vals[0] and detail_value ' + rel_ops[1] + ' rel_vals[1]'
            # match_res = eval(cmd)
        # else
        else:
            if self._repl_relation_operator(match_value[:2]):
                rel_ops = match_value[:2]
                rel_val = type(detail_value)(match_value[2:])
            else:
                rel_ops = match_value[:1]
                rel_val = type(detail_value)(match_value[1:])

            # fixme NO eval usage !!!
            cmd = 'detail_value ' + rel_ops + ' rel_val'
            # match_res = eval(cmd)
        # return match_res
        raise NotImplementedError('Relation match will be fixed in future releases.')

    def _repl_relation_operator(self, relation_symbol):
        if relation_symbol == '[': return '>='
        if relation_symbol == '(': return '>'
        if relation_symbol == ']': return '<='
        if relation_symbol == ')': return '<'
        if relation_symbol in ['<=', '=<']: return '<='
        if relation_symbol in ['>=', '=>']: return '>='
        if relation_symbol == '==': return '=='
        if relation_symbol == '!=': return '!='
        return relation_symbol
