"""Module for TunePalAPI and Song classes."""

from typing import List
import csv
import os


class Song:
    """Class representing a song with title, artist, and release year."""

    def __init__(self, title: str, artist: str, release_year: str):
        self.title = title
        self.artist = artist
        self.release_year = release_year

    def __eq__(self, other):
        """Equality check to prevent duplicate songs."""
        if isinstance(other, Song):
            return (
                self.title == other.title
                and self.artist == other.artist
                and self.release_year == other.release_year
            )
        return False

    def __repr__(self):
        return f"Song({self.title}, {self.artist}, {self.release_year})"


class TunePalAPI:
    """API for managing a music library, including searching, pagination, and filtering."""

    def __init__(self, page_size=5):
        """Initialize the API, load songs from CSV, and set pagination parameters."""
        self.songs: List[Song] = []
        self.page_size = max(1, page_size)
        self.current_page_index = 0

        if not os.path.exists("songlist.csv"):
            raise FileNotFoundError("Error: songlist.csv file not found. Please ensure it exists.")

        with open("songlist.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row.get("Song Clean", "Unknown Title")
                artist = row.get("ARTIST CLEAN", "Unknown Artist")
                release_year = row.get("Release Year", "Unknown Year")
                self.songs.append(Song(title, artist, release_year))

    def _build_song_window(self, song_list: List[Song]):
        """Returns a subset of songs for the current page based on page size."""
        first_index = self.current_page_index * self.page_size
        last_index = first_index + self.page_size
        return song_list[first_index:last_index]

    def add_song(self, title: str, artist: str, release_year: str):
        """Adds a new song to the list if it does not already exist."""
        new_song = Song(title, artist, release_year)
        if new_song in self.songs:
            return False
        self.songs.append(new_song)
        return True

    def get_songs(self):
        """Returns the current page of songs."""
        return self._build_song_window(self.songs)

    def next_page(self):
        """Moves to the next page if there are more songs available."""
        if (self.current_page_index + 1) * self.page_size < len(self.songs):
            self.current_page_index += 1

    def previous_page(self):
        """Moves to the previous page, preventing negative index values."""
        if self.current_page_index > 0:
            self.current_page_index -= 1
        else:
            self.current_page_index = 0  # Ensure index is not negative

    def set_page_size(self, page_size: int):
        """Sets the number of songs per page."""
        if page_size <= 0:
            raise ValueError("Page size must be a positive integer.")
        self.page_size = page_size

    def search(self, query: str):
        """Searches for songs matching the title or artist."""
        if not query.strip():
            return []
        hits = [
            song
            for song in self.songs
            if query.lower() in song.title.lower() or query.lower() in song.artist.lower()
        ]
        return self._build_song_window(hits)

    def get_songs_since(self, release_year: str):
        """Filters songs released after the specified year."""
        try:
            year = int(release_year)
            hits = [
                song
                for song in self.songs
                if song.release_year.isdigit() and int(song.release_year) > year
            ]
            return self._build_song_window(hits)
        except ValueError:
            # Explicitly handle invalid year input for test coverage
            return self._build_song_window([])
