### YouTube Data
YouTube Data provides comprehensive YouTube video metadata scraping. Results are returned in a dictionary containing likes, dislikes, views published dates and more.

Website: [youtubedata.io](https://www.youtubedata.io)

### Usage
##### Positional Arguments
Usage is simple, the first method is to not pass any keyword arguments. In this case, the function will determine whether a channel code was passed. 

*Channel Codes begin with UC. For example, Ariana Grande's channel code is UC9CoOnJkIBMdeijd9qYoT_g*.

If a channel code was passed, YouTube Data will proceed straight to the scraping algorithm and extract the desired data. Otherwise, a step is added to find the channel that best matches the entered argument.

```python
from youtubedata import youtubedata 
```

```python
ariana_grande = youtubedata.get("UC9CoOnJkIBMdeijd9qYoT_g")
```

```python
ariana_grande = youtubedata.get("Ariana Grande")
```

##### Keyword Arguments
The second method is to explicity pass the keyword arguments *channel_code* and *best_match*. This way YouTube Data does not have to guess which is being provided.

```python
ariana_grande = youtubedata.get(channel_code = "UC9CoOnJkIBMdeijd9qYoT_g")
```

```python
ariana_grande = youtubedata.get(best_match = "Ariana Grande")
```

### Progress
Progress is indicated through percentage complete print statements. The algorithm works by first identifying all "playlists" associated to the channel and then extracting all video URLs in each playlist and then deduplicating any repeated URLs.