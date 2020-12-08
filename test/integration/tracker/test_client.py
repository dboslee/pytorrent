import unittest
from bittorrent import (
    tracker,
    models,
)


class TestTrackerClient(unittest.TestCase):

    def setUp(self):
        self.tracker_url = "https://torrent.ubuntu.com/announce"
        self.info_hash = b'_\xff\x0e\x1c\x8a\xc4\x14\x86\x03\x10\xbc\xc1\xcbv\xac(\xe9`\xef\xbe'
        self.client = tracker.Client(self.tracker_url)

    def test_get(self):
        tracker_announce = self.client.get(self.info_hash, compact=False)
        assert isinstance(tracker_announce, models.TrackerAnnounce)

    def test_get_compact(self):
        tracker_announce = self.client.get(self.info_hash, compact=False)
        assert isinstance(tracker_announce, models.TrackerAnnounce)
