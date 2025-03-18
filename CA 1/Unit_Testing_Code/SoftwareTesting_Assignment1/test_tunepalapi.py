"""Unit tests for TunePalAPI."""

import unittest
from unittest.mock import patch
from tunepalapi import TunePalAPI, Song


class TestTunePalAPI(unittest.TestCase):
    """Unit test cases for TunePal API."""

    def setUp(self):
        """Initialize a test instance of TunePalAPI with test data."""
        self.api = TunePalAPI()
        self.api.songs = [
            Song("Song A", "Artist A", "2020"),
            Song("Song B", "Artist B", "2018"),
            Song("Song C", "Artist C", "2022"),
        ]
        self.api.page_size = 2
        self.api.current_page_index = 0

    def test_song_operations(self):
        """Test adding, preventing duplicates, and equality of songs."""
        # Test adding a song
        success = self.api.add_song("New Song", "New Artist", "2023")
        self.assertTrue(success)
        self.assertEqual(len(self.api.songs), 4)

        # Test preventing duplicate songs
        self.api.add_song("Song A", "Artist A", "2020")
        self.assertEqual(len(self.api.songs), 4)

        # Test song equality
        song1 = Song("Test Song", "Test Artist", "2021")
        song2 = Song("Test Song", "Test Artist", "2021")
        song3 = Song("Different Song", "Different Artist", "2021")
        self.assertTrue(song1 == song2)
        self.assertFalse(song1 == song3)
        self.assertFalse(song1 == "Not a Song")

    def test_pagination(self):
        """Test pagination methods: next_page, previous_page, and boundaries."""
        # Test next page
        self.api.next_page()
        self.assertEqual(self.api.current_page_index, 1)

        # Test previous page
        self.api.previous_page()
        self.assertEqual(self.api.current_page_index, 0)

        # Test previous page boundary
        self.api.previous_page()
        self.assertEqual(self.api.current_page_index, 0)

    def test_search(self):
        """Test search functionality."""
        # Test searching by title
        results = self.api.search("Song A")
        self.assertEqual(len(results), 1)

        # Test searching by artist
        results = self.api.search("Artist B")
        self.assertEqual(len(results), 1)

        # Test case-insensitive search
        results = self.api.search("song a")
        self.assertEqual(len(results), 1)

        # Test searching with special characters
        self.api.add_song("Song & Special", "Artist & Special", "2023")
        results = self.api.search("& Special")
        self.assertEqual(len(results), 1)

        # Test searching with an empty query
        results = self.api.search("")
        self.assertEqual(results, [])

        # Test searching for a non-existent song
        results = self.api.search("NonExistentSong")
        self.assertEqual(results, [])

    def test_get_songs_since(self):
        """Test filtering songs by release year."""
        # Test valid year
        results = self.api.get_songs_since("2019")
        self.assertEqual(len(results), 2)

        # Test invalid year input
        results = self.api.get_songs_since("invalid")
        self.assertEqual(results, [])

    def test_page_size(self):
        """Test setting and validating page size."""
        # Test setting a valid page size
        self.api.set_page_size(3)
        self.assertEqual(self.api.page_size, 3)

        # Test setting an invalid page size
        with self.assertRaises(ValueError):
            self.api.set_page_size(-1)

    @patch("os.path.exists", side_effect=lambda path: path != "songlist.csv")
    def test_file_not_found(self, _):
        """Test handling of missing songlist.csv file."""
        with self.assertRaises(FileNotFoundError):
            TunePalAPI(page_size=5)

    def test_repr_song(self):
        """Test the __repr__ method of the Song class."""
        song = Song("Test Song", "Test Artist", "2021")
        self.assertEqual(repr(song), "Song(Test Song, Test Artist, 2021)")

    def test_get_songs(self):
        """Test retrieving the current page of songs."""
        songs = self.api.get_songs()
        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0].title, "Song A")
        self.assertEqual(songs[1].title, "Song B")
