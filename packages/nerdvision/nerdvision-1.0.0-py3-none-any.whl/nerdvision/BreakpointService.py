import logging
import os
import threading

import sys
from nerdvision import settings
from nerdvision.ContextUploadService import ContextUploadService
from nerdvision.FrameProcessor import FrameProcessor
from nerdvision.models.EventSnapshot import Watcher

our_logger = logging.getLogger("nerdvision")


class BreakpointService(object):

    def __init__(self, set_trace=True):
        self.breakpoints = {}
        self.var_id = 1
        self.context_service = ContextUploadService()
        self.session_id = None
        if set_trace:
            sys.settrace(self.trace_call)
            threading.settrace(self.trace_call)

    def trace_call(self, frame, event, arg):
        if len(self.breakpoints) == 0:
            return None

        lineno = frame.f_lineno
        filename = frame.f_code.co_filename

        breakpoints_for = self.breakpoints_for(filename)

        if settings.is_point_cut_debug_enabled():
            our_logger.debug("Found %s breakpoints for %s", len(breakpoints_for), filename)

        if event == "call" and len(breakpoints_for) == 0:
            return None

        if event == "line":
            bps_ff, bps_sf = self.find_match(breakpoints_for, lineno, frame)

            if len(bps_ff) > 0 or len(bps_sf) > 0:
                max_collection_size, max_string_length, max_variables, max_variable_depth = self.get_breakpoint_config(
                    bps_ff + bps_sf)

                processor = FrameProcessor(max_variable_depth, max_collection_size, max_string_length, max_variables)

                if len(bps_sf) > 0 and len(bps_ff) == 0:
                    processor.process_back_frame_vars = False

                processor.process_frame(frame)

                for bp in bps_ff:
                    self.process_watches(bp, frame, processor)
                    self.context_service.send_event(processor.event, bp, processor.watchers, self.session_id)

                if len(bps_ff) > 0:
                    for i, sf in enumerate(processor.event.stack_trace):
                        if i > 0:
                            sf.variables = []

                for bp in bps_sf:
                    self.process_watches(bp, frame, processor)
                    self.context_service.send_event(processor.event, bp, processor.watchers, self.session_id)

        return self.trace_call

    def next_id(self):
        self.var_id = self.var_id + 1
        return self.var_id

    def process_request(self, response, session_id):
        self.session_id = session_id
        our_logger.debug("Processing breakpoints %s", response)
        new_breakpoints = {}
        for _breakpoint in response.breakpoints:
            if _breakpoint.args['class'] in new_breakpoints:
                new_breakpoints[_breakpoint.args['class']].append(_breakpoint)
            else:
                new_breakpoints[_breakpoint.args['class']] = [_breakpoint]
        self.breakpoints = new_breakpoints
        our_logger.debug("New breakpoint configuration %s", self.breakpoints)

    def breakpoints_for(self, filename):
        basename = os.path.basename(filename)

        if settings.is_point_cut_debug_enabled():
            our_logger.debug("Searching for breakpoint for %s", basename)

        if basename in self.breakpoints:
            breakpoints_basename_ = self.breakpoints[basename]
            return breakpoints_basename_
        else:
            return []

    def find_match(self, breakpoints_for, lineno, frame):
        bps_ff = []
        bps_sf = []
        for bp in breakpoints_for:
            if bp.line_no == lineno:
                if bp.condition is not None and bp.condition != "" and self.condition_matches(bp, frame):
                    if bp.type == 'stack':
                        bps_ff.append(bp)
                    else:
                        bps_sf.append(bp)
                elif bp.condition is None or bp.condition == "":
                    if bp.type == 'stack':
                        bps_ff.append(bp)
                    else:
                        bps_sf.append(bp)
        return bps_ff, bps_sf

    def get_breakpoint_config(self, breakpoints):
        max_collection_size = -1
        max_string_length = -1
        max_variables = -1
        max_variable_depth = -1

        for bp in breakpoints:
            tmp_max_col_size = bp.args['MAX_COLLECTION_SIZE']
            tmp_max_string_length = bp.args['MAX_STRING_LENGTH']
            tmp_max_variables = bp.args['MAX_VARIABLES']
            tmp_max_var_depth = bp.args['MAX_VAR_DEPTH']

            max_collection_size = self.get_max_value(max_collection_size, tmp_max_col_size)
            max_string_length = self.get_max_value(max_string_length, tmp_max_string_length)
            max_variables = self.get_max_value(max_variables, tmp_max_variables)
            max_variable_depth = self.get_max_value(max_variable_depth, tmp_max_var_depth)

            if max_collection_size == -1:
                max_collection_size = FrameProcessor.default_max_list_len
            if max_string_length == -1:
                max_string_length = FrameProcessor.default_max_str_length
            if max_variables == -1:
                max_variables = FrameProcessor.default_max_vars
            if max_variable_depth == -1:
                max_variable_depth = FrameProcessor.default_max_depth

        return max_collection_size, max_string_length, max_variables, max_variable_depth

    @staticmethod
    def get_max_value(item, compare):
        if compare.isdigit():
            compare = int(compare)
            if compare > item:
                return compare
            else:
                return item
        return -1

    @staticmethod
    def condition_matches(bp, frame):
        our_logger.debug("Executing condition evaluation: %s", bp.condition)
        try:
            result = eval(bp.condition, None, frame.f_locals)
            our_logger.debug("Condition result: %s", result)
            if result:
                return True
            return False
        except Exception:
            our_logger.exception("Error evaluating condition %s", bp.condition)
            return False

    @staticmethod
    def process_watches(bp, frame, processor):
        watches = bp.named_watchers
        for watch in watches:
            watch_ = watches[watch]
            our_logger.debug("Evaluating watcher: %s -> %s", watch, watch_)
            if watch_ != "":
                try:
                    eval_result = eval(watch_, None, frame.f_locals)

                    type_ = type(eval_result)
                    hash_ = str(id(eval_result))
                    next_id = processor.next_id()

                    watcher = Watcher(watch, watch_)

                    processor.process_variable(hash_, watch, next_id, watcher, type_, eval_result, 0)
                    processor.add_watcher(watcher)
                except Exception:
                    our_logger.exception("Error evaluating watcher %s", watch_)
        return
