# Wikimedia-Commons-Vanity-Stats
A small python script to gather media requests for uploaded files by a single user. Useful if you'd like to know how many reqeusts your media files have had!

Full disclosure, I used LLM tools to help with the creation of this script. I am not a programmer by trade, only mildy dangerous with a hint of understanding of what I'm doing. :) 

# How does it work?
Thet script uses the MediaWiki and mediarequests APIs to generate a report that is saved as a .csv file. The script queries a users uploads and provides the name of the file, how many media requests that files has seen, and the upload date of the file. 

When you run the script it will prompt you for some informaiton. There are also some rather sane defaults. 

Here are the prompts. You can also customize these parameters to your liking.

```username``` (default: Ckoerner) - You can overwrite this in the script with your username.

```analytics_frequency``` (daily/monthly, default: daily) – The mediareqeusts API provides either daily or monthy statistics.

```start_date``` (YYYYMMDD, default: 20130122) – The default is my account creation date. An easter egg! :p

```end_date``` (YYYYMMDD, default: <current date>) – The defualt will be the current date.

```output_CSV``` (default: media_requests.csv) – What the resulting .csv file will be named. It is saved to your ~/ user directory.

```max_files_to_check``` (default: 10) – How many files to check before stopping. Uses the Mediawiki API pagination for reqeusts greater than 500. 

```num_threads``` (default: 5) – The script runs parallel reqeusts to speed things up. Setting this higher will increase performance load, potentially making your computer run slower while the script executes.

Note: By default the script will run through files in ascending order. Meaning the user's oldest uploads to the newest. You can change this by modfiying the ```"aidir": "ascending"``` parameter. 

## Installation

MacOS:

1. Download vanity.py to your computer.
2. Open Terminal and type in the following

(You'll need to specify the location of ```vanity.py``` in order for this to work. i.e. /Users/<username>/Downloads/vanity.py)

```sh
python3 vanity.py
```

## Usage example

The script is called ''vanity'' as it provides you with numbers that don't really mean much, but it might be nice to know. 

In all seriousness, this script may be helpful if you are working with a partner organization and would like to give them some indication of how frequently viewed their media files are. It may also be helpful if you are doing any sort of grant work, or other reporting work, where you need to indicate a measure of impact or visibility to the work you are doing.

## Development setup

It's a python script. Any text editor should be fine to muck with it. 

## Release History

* 0.0.1
    * Initial commit after working on the script locally for a bit.

## Meta

Chris Koerner – [@Bluesky](https://bsky.app/profile/clkoerner.com) – chris@clkoerner.com

Distributed under the Creative Commons Zero v1.0 Universal license. See ``LICENSE`` for more information.

[https://github.com/ckoerner/Wikimedia-Commons-Vanity-Stats/blob/main/LICENSE](https://github.com/ckoerner/Wikimedia-Commons-Vanity-Stats/blob/main/LICENSE)

## Contributing

1. Fork it (<https://github.com/ckoerner/Wikimedia-Commons-Vanity-Stats/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
