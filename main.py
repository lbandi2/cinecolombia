#!/usr/bin/env python3

from page import Page

url_upcoming = "https://www.cinecolombia.com/bogota/pronto"
filename_upcoming = "cinecolombia_upcoming.html"
url_playing = "https://www.cinecolombia.com/bogota/cartelera"
filename_playing = "cinecolombia_playing.html"

def main():
    upcoming = Page(url_upcoming, filename_upcoming)
    playing = Page(url_playing, filename_playing)

main()
