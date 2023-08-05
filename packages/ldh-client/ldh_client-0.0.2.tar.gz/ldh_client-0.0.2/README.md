# Liberty CLI

[project] | [code] | [tracker]

*Liberty CLI* is a user-facing command-line client for interacting
with a Liberty Deckplan Host (LDH).

## Installation

The preferred way to install Liberty CLI is with your package
manager. The recommended package name is `ldh_client`. For example:

    sudo apt install ldh-client # Debian-based (doesn't exist yet)

or

    pipx install ldh-client

## Usage

Get help
```bash
liberty --help
```

Add Librem One tunnel VPN to your Network-Manager connections:

```bash
liberty tunnel-setup
```

I will ask your Librem One username and password.

## Installation (from source)

If you'd prefer to run from source...

1. Install Python 3.x and pipenv. (See
   <https://docs.pipenv.org/install/> for a tutorial.)

2. Get source:

        git clone https://source.puri.sm/liberty/ldh_client.git

3. Install with pipenv:

        apt-get install libcairo2-dev libgirepository1.0-dev
        cd ldh_client
        pipenv install --dev -e .

## Usage (from source)

```bash
cd ldh_client
pipenv run liberty --help
```

## Sharing and contributions

Liberty CLI (LDH client)  
<https://source.puri.sm/liberty/ldh_client>  
Copyright 2018-2019 Purism SPC  
SPDX-License-Identifier: AGPL-3.0-or-later  

Shared under AGPL-3.0-or-later. We adhere to the Community Covenant
1.0 without modification, and certify origin per DCO 1.1 with a
signed-off-by line. Contributions under the same terms are welcome.

For details see:

* [COPYING.AGPL.md], full license text
* [CODE_OF_CONDUCT.md], full conduct text
* [CONTRIBUTING.DCO.md], full origin text

<!-- Links -->

[project]: https://source.puri.sm/liberty/ldh_client
[code]: https://source.puri.sm/liberty/ldh_client/tree/master
[tracker]: https://source.puri.sm/liberty/ldh_client/issues
[SETUP.md]: SETUP.md
[COPYING.AGPL.md]: COPYING.AGPL.md
[CODE_OF_CONDUCT.md]: CODE_OF_CONDUCT.md
[CONTRIBUTING.DCO.md]: CONTRIBUTING.DCO.md
[COPYING.md]: COPYING.md
[CONTRIBUTING.md]: CONTRIBUTING.md
