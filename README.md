# emojidon

**emojidon** is a tool for synchronizing emojis on a [Mastodon] instance. 🚀 It’s pretty early days here, so maybe don’t bet your VC funded startup on this project just yet. 💸


## Example

[![asciicast](https://asciinema.org/a/621696.svg)](https://asciinema.org/a/621696)


## Features

This is currently a script which uploads all PNG and GIF images in a given directory to a specified Mastodon instance based on filename-to-slug matching.


## Roadmap

This thing could do so much! But it probably _should_ do only a bit more. Some tentative ideas:

- actual CLI
- packaged better (aka really at all)
- other sync options:
    - overwrite on server
    - delete from server when missing in directory
- validation:
    - notify if any non-PNG and non-GIF files are present
    - notify if any PNG or GIF files are too big or w/e
- cope better with capitalization than it probably does
- use Mastodon API instead of Selenium—requires it to actually exist, though 😢
- support non-Mastodon fediverse projects, e.g., [Pixelfed], [Takahē], [Letterbook]


## Installation and Use

1. Install dependencies with `poetry install`
2. Copy `.env.sample` to `.env` and fill it out
3. Run `poetry run python sync.py`


## Development

See Installation instructions above. No tests or anything else yet, sorry. Remove the headless option for easier debugging.


## Contributing

Maybe don’t until at least some of this is fleshed out a bit more?

But if you’re really keen on it, see ideas in Roadmap or [open an issue]—I’m not opposed to contributions! ❤️


## License

MIT, see `LICENSE` file.


[Mastodon]: https://joinmastodon.org/ "Mastodon - Decentralized social media"
[Pixelfed]: https://pixelfed.org/ "Pixelfed - Decentralized social media"
[Takahē]: https://jointakahe.org/ "Welcome | Takahē"
[Letterbook]: https://github.com/Letterbook/Letterbook "Letterbook/Letterbook: A Mastodon-compatible microblogging server, optimized to reduce administrative costs and burdens."
[open an issue]: https://github.com/nkantar/emojidon/issues/new "New Issue · nkantar/emojidon"
