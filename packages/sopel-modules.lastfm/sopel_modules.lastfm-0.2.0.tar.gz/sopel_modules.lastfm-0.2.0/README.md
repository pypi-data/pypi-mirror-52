# lastfm sopel plugin

[![pypi status](https://img.shields.io/pypi/v/sopel-modules.lastfm.svg)](https://pypi.org/project/sopel-modules.lastfm/)
[![Build Status](https://travis-ci.org/shanedabes-sopel/sopel-lastfm.svg?branch=master)](https://travis-ci.org/shanedabes-sopel/sopel-lastfm)
[![pyup status](https://pyup.io/repos/github/shanedonohoe/poku/shield.svg)](https://pyup.io/account/repos/github/shanedabes-sopel/sopel-lastfm/)

A sopel plugin that returns the user's last listened track

## Installation

Can be installed from the pip using:

    pip install sopel_modules.lastfm


## Testing

If you would like to make a contribution, be sure to run the included tests. Test requirements can be installed using:

    pip install -r requirements_dev.txt

run tests using:

    make test

and start up a test sopel instance with docker by using:

    docker-compose up -d
    docker attach weechat
