# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['nightcore']
install_requires = \
['click>=7.0,<8.0', 'pydub>=0.23.1,<0.24.0']

entry_points = \
{'console_scripts': ['nightcore = nightcore:cli']}

setup_kwargs = {
    'name': 'nightcore',
    'version': '0.5.4',
    'description': 'Easy CLI for modifying the speed and pitch of audio',
    'long_description': '# Nightcore: Python CLI for creating chipmunk audio 🐿\n\nA small and focused CLI for changing the pitch and speed of audio files.\n\nFFmpeg is required for audio operations. See [here](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up) for instructions on how to set it up!\n\n> I had the idea for this a long time ago, and wanted to make it to prove a point. This program is not intended for, nor should it be used for, copyright infringement and piracy. [**Nightcore is not, and has never been, fair use**](https://www.avvo.com/legal-answers/does-making-a--nightcore--version-of-a-song--speed-2438914.html).\n\n## Installation\n\nNightcore is on PyPI, so you can use `pip` to install it (although [pipx](https://pipxproject.github.io/pipx/) is recommended)\n\n```sh\npip install nightcore\n```\n\n## Usage\n\nThe CLI is easy to use, and behaves as you would expect.\n\n```sh\n# By default it will increase the pitch by 2 semitones.\n$ nightcore music.mp3 > out.mp3\n\n# Specify pitch increase/decrease\n$ nightcore music.mp3 +3 > out.mp3\n\n# The above command is equivalent to the following:\n$ nightcore music.mp3 +3 semitones > out.mp3\n\n# Supports other types of speed-change out of the box\n$ nightcore music.mp3 +3 tones > out.mp3\n\n# Speed up by a percentage (150 percent => 1.5x speed)\n$ nightcore music.mp3 150 percent > out.mp3\n\n# Slowing down the music works as expected, too\n$ nightcore music.mp3 -3 > out.mp3\n\n# The `--output <file>` option can be used instead of redirection\n$ nightcore music.mp3 --output out.mp3\n\n# Set the extension manually with `--format <fmt>`\n$ nightcore badly_named_file --format mp3 > out.mp3\n\n# By default, the output file is equalized to counteract a pitch increase\n# To disable the automatic equalization, pass the `--no-eq` flag\n$ nightcore music.mp3 --no-eq > out.mp3\n```\n',
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'url': 'https://github.com/SeparateRecords/nightcore',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
