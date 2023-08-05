# Anime Web Scraper
Scrapes anime data from https://myanimelist.net/ .

## Anime Model Data
These are, as for now, the only available data.
- Title
- English Title
- Japanese Title
- Synonyms
- Synopsis
- Anime Type
- Episodes
- Genres
- Poster (link)
- Trailer (link)

## Installation
```
pip install pymalscraper
```

## Basic Usage
```python
from pymalscraper.scraper import MALScraper
scraper = MALScraper()
anime = scraper.get_anime("kimi no na wa.")

> anime.title
'Kimi no na wa.'
> anime.english_title
'Your Name.'
> anime.japanese_title
'君の名は。'
> anime.synonyms
''
> anime.synopsis
"Mitsuha Miyamizu, a high school girl, yearns to live the life of a boy in the bustling city of Tokyo—a dream that stands in stark contrast..."
> anime.animetype
'Movie'
> anime.episodes
'1'
> anime.genres
'Romance, Supernatural, School, Drama'
> anime.poster
'https://cdn.myanimelist.net/images/anime/5/87048.jpg'
> anime.trailer
'https://www.youtube.com/embed/3KR8_igDs1Y?enablejsapi=1&wmode=opaque&autoplay=1'

# To get the anime url    
> scraper.get_anime_url('kimi no na wa.')
'https://myanimelist.net/anime/32281/Kimi_no_Na_wa'
```
