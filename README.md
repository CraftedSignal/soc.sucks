# soc.sucks

Static site served by GitHub Pages. Edit `index.html` and the crawler files
directly; there is no build step.

Run `python3 -m unittest discover -s tests -v` with Python 3 and Node.js
installed. CI checks metadata against `CNAME`, local assets and navigation
targets, inline JavaScript syntax, structured data, and crawler discovery on
pull requests and pushes to `main`.
