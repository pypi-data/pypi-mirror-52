import logging

import requests
from nerdvision import settings

our_logger = logging.getLogger("nerdvision")


class ContextUploadService(object):
    def __init__(self):
        self.url = settings.get_context_url()
        self.api_key = settings.get_setting("api_key")

    def send_event(self, event_snapshot, bp, watches, session_id):
        try:
            our_logger.debug("Sending snapshot to %s", self.url)
            snapshot_as_dict = event_snapshot.as_dict()
            snapshot_as_dict['named_watches'] = [watcher.as_dict() for watcher in watches]
            snapshot_as_dict['breakpoint'] = self.bp_as_map(bp)

            our_logger.debug("Sending event snapshot for breakpoint %s", bp.breakpoint_id)

            if settings.is_context_debug_enabled():
                our_logger.debug(snapshot_as_dict)

            response = requests.post(url=self.url + "?breakpoint_id=" + bp.breakpoint_id + "&workspace_id=" + bp.workspace_id,
                                     auth=(session_id, self.api_key), json=snapshot_as_dict)
            json = response.json()
            our_logger.debug("Context response: %s", json)
            response.close()
        except Exception:
            our_logger.exception("Error while sending event snapshot %s", self.url)

    def bp_as_map(self, bp):
        return {
            'breakpoint_id': bp.breakpoint_id,
            'workspace_id': bp.workspace_id,
            'rel_path': bp.rel_path,
            'line_no': bp.line_no,
            'condition': bp.condition,
            'src_type': bp.src_type,
            'named_watches': dict(bp.named_watchers),
            'args': dict(bp.args)
        }
