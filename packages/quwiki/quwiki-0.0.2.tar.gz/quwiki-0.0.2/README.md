# QuWiki

Configurable, extendable and minimalistic wiki for your team generated from multiple sources, e.g. Google Drive, Github and many more.

## Usage
1. Install:
```
pip3 install quwiki --user
```
2. Initialize configuration file:
```
quwiki init
```
3. Generate wiki:
```
quwiki generate
```

## Development
Install package in _editable_ mode:
```
pip3 install -Ue .
```
and run:
```
quwiki
```
or to test:
```
python3 -m unittest discover -s test -p '*_test.py'
```

## Deployment
`quwiki` generates static HTML files in `/dist` directory. 

You can configure CI/CD to make the static files available online.
Otherwise, to serve the files locally, you can simply run:
```
cd dist/
python3 -m http.server
```

Further, short instructions will be given on how to use different CI/CD providers.

### Now (by Zeit.co)
Related files: `now.json` and `build.sh`.

You can use the following command to store secret files:
```
now secret add quwiki-gdrive-tocken "$(cat secrets/token.pickle | base64)"
```
