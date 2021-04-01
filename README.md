# PlexOnDemand

PlexOnDemand is a SMS-based service for downloading movies to your local Plex server.

## Installation

Use [docker compose](https://docs.docker.com/compose/) to build and run PlexOnDemand.

```bash
docker-compose build  --no-cache # reinitialize qbittorent with no-cache flag
```

## Usage

```bash
docker-compose up 
```

### SMS Commands Available
`search` - Searches for a Movie Title and Prompts User if The Title is Correct and to Download  
`status` - Gets Status of All Torrent Downloads

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)