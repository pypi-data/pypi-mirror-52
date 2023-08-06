
# Matcher-pcx-synomia

Extract themes from verbatims.


## Version 1.1.3
Release date: 2019-09-20


## Getting Started

pip install ...


## Prerequisites

* flashtext:
$ pip install flashtext


## Usage

* You would need a lexicon.txt with the following structure:
>> manque de place=><manque de place;place;-1<
>> personnel désagréable=><personnel désagréable;personnel;-1<
>> train direct=><train direct;train;1<

* Init matcher:
>> themes_matcher = matcher.ThemesMatcher('lexicon.txt')

* Extract themes from verbatims:
>> verbatims = ["","Le confort et la propreté","Rapidité (Train Direct), mais personnel désagréable","c'est catastrophique… retards chroniques, personnel désagréable","Le manque de place ds le tgv"]
>> matches = themes_matcher.match(verbatims)
>> print(matches)
[[], [], [['train direct', 'train', '1'], ['personnel désagréable', 'personnel', '-1']], [['personnel désagréable', 'personnel', '-1']], [['manque de place', 'place', '-1']]]



## Authors

* **Synomia**





