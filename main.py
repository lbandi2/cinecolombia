from page import Page

url_upcoming = "https://www.cinecolombia.com/bogota/pronto"
filename_upcoming = "cinecolombia_upcoming.html"
url_playing = "https://www.cinecolombia.com/bogota/cartelera"
filename_playing = "cinecolombia_playing.html"

def main():
    a = Page(url_upcoming, filename_upcoming)
    b = Page(url_playing, filename_playing)

main()
