# cinecolombia

This script basically scrapes www.cinecolombia.com for now playing and upcoming movies:

* Gets info for movies from OMDB API and TMDB API
* If movie title is not recognized, it runs a simple search on Google to retrieve the correct one and test it against one of the previous APIs
* If movie is correct and is not already on the DB, it stores the data on a local MySQL DB
* If movie is on presale, it displays that flag
