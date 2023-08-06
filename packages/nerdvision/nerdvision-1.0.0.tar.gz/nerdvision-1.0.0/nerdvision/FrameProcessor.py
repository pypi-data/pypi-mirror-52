import logging
import os

from nerdvision.models.EventSnapshot import EventSnapshot, SnapshotFrame, Variable, VariableId

our_logger = logging.getLogger("nerdvision")


class FrameProcessor(object):
    default_max_depth = 5
    default_max_list_len = 10
    default_max_str_length = 1024
    default_max_vars = 1000

    def __init__(self, max_depth=default_max_depth, max_list_len=default_max_list_len, max_str_length=default_max_str_length,
                 max_vars=default_max_vars):
        self.max_depth = max_depth
        self.max_list_len = max_list_len
        self.max_str_length = max_str_length
        self.max_vars = max_vars
        self.event = EventSnapshot()
        self.watchers = []
        self.depth = -1
        self.v_id = 0
        self.variable_cache = {}
        self.process_back_frame_vars = True

    def add_watcher(self, watcher):
        self.watchers.append(watcher)

    def next_id(self):
        self.v_id = self.v_id + 1
        return self.v_id

    def process_frame(self, frame, process_vars=True):
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        basename = os.path.basename(filename)
        func_name = frame.f_code.co_name

        self.depth = self.depth + 1

        snapshot_frame = SnapshotFrame(basename, func_name, lineno, filename, self.depth)

        self.event.add_frame(snapshot_frame)

        var_depth = 0
        f_locals = frame.f_locals

        if process_vars:
            self.process_frame_variables(f_locals, snapshot_frame, var_depth)

        back_ = frame.f_back
        if back_ is not None:
            self.process_frame(back_, self.process_back_frame_vars)

    def process_frame_variables(self, f_locals, snapshot_frame, var_depth):
        if var_depth >= self.max_depth:
            return

        keys = f_locals.keys()

        for key_ in keys:
            val_ = f_locals[key_]
            type_ = type(val_)
            hash_ = str(id(val_))
            next_id = self.next_id()
            self.process_variable(hash_, key_, next_id, snapshot_frame, type_, val_, var_depth)

    def process_variable(self, hash_, key_, next_id, snapshot_frame, type_, val_, var_depth):
        if self.v_id > self.max_vars:
            our_logger.debug('Skipping var no: %d; key: %s;', self.v_id, key_)
            return

        try:
            if hash_ in self.variable_cache:
                cache_id = self.variable_cache[hash_]
                snapshot_frame.add_variable(VariableId(cache_id, key_))
            elif type_ is str:
                variable = Variable(next_id, str(key_), type_, self.truncate_string(val_), hash_)
                self.variable_cache[hash_] = next_id
                snapshot_frame.add_variable(variable)
            elif type_ is int or type_ is float or type_ is bool or type_.__name__ == 'long':
                variable = Variable(next_id, str(key_), type_, val_, hash_)
                self.variable_cache[hash_] = next_id
                snapshot_frame.add_variable(variable)
            elif type_.__name__ == 'unicode' or type_ is type or type_.__name__ == "module":
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                self.variable_cache[hash_] = next_id
                snapshot_frame.add_variable(variable)
            elif type_ is dict:
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                self.variable_cache[hash_] = next_id
                self.process_frame_variables(val_, variable, var_depth + 1)
                snapshot_frame.add_variable(variable)
            elif type_ is tuple or type_ is list or type_.__name__ == 'listiterator' or type_.__name__ == 'list_iterator':
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                self.variable_cache[hash_] = next_id
                self.process_frame_variables_set(val_, variable, var_depth + 1)
                snapshot_frame.add_variable(variable)
            elif val_ is None:
                variable = Variable(next_id, str(key_), type_, None, hash_)
                self.variable_cache[hash_] = next_id
                snapshot_frame.add_variable(variable)
            elif type_.__name__ == 'listreverseiterator' or type_.__name__ == 'list_reverseiterator':
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                self.variable_cache[hash_] = next_id
                self.process_frame_variables_iter(val_, variable, var_depth + 1)
                snapshot_frame.add_variable(variable)
            elif type_ is set or type_ is frozenset:
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                self.variable_cache[hash_] = next_id
                self.process_frame_variables_set(val_, variable, var_depth + 1)
                snapshot_frame.add_variable(variable)
            elif hasattr(val_, '__dict__'):
                dict__ = val_.__dict__
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                self.variable_cache[hash_] = next_id
                self.process_frame_variables(dict__, variable, var_depth + 1)
                snapshot_frame.add_variable(variable)
            else:
                our_logger.debug("Unknown type processed %s:%s", str(key_), type_)
                variable = Variable(next_id, str(key_), type_, self.truncate_string(str(val_)), hash_)
                snapshot_frame.add_variable(variable)
        except:
            our_logger.exception("Unable to process variable %s:%s", str(key_), type_)

    def process_frame_variables_iter(self, inc_val_, variable, var_depth):
        if var_depth >= self.max_depth:
            return

        end = VariableId(-1, 'end')
        val = next(inc_val_, end)
        total = 0
        while val is not end and total < self.max_list_len:
            val_ = val
            type_ = type(val_)
            hash_ = str(id(val_))
            next_id = self.next_id()
            self.process_variable(hash_, total, next_id, variable, type_, val_, var_depth)
            total = total + 1
            val = next(inc_val_, end)

    def process_frame_variables_set(self, inc_val_, variable, var_depth):
        if var_depth >= self.max_depth:
            return

        total = 0
        for val_ in inc_val_:
            type_ = type(val_)
            hash_ = str(id(val_))
            next_id = self.next_id()
            self.process_variable(hash_, total, next_id, variable, type_, val_, var_depth)
            total = total + 1
            if total == self.max_list_len:
                break

    def truncate_string(self, string):
        return string[:self.max_str_length]
