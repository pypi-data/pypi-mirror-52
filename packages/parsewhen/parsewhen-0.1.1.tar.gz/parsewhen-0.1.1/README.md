# parsewhen

Parse when is a library for extracting and parsing date / time from regular English text.


![pipeline status](https://gitlab.com/sj1k/parsewhen/badges/release/pipeline.svg)
![coverage](https://gitlab.com/sj1k/parsewhen/badges/release/coverage.svg)


## Usage


```python
import parsewhen

print(list(parsewhen.parse('Some text, Tuesday next week, 10pm. And more text')))

# ['Some text, ', datetime.datetime(2019, 9, 17, 22, 0), '. And more text'] 
# 
# .parse collects and converts the parts it can, otherwise it yields the original words.


print(list(parsewhen.extract('Some text, Tuesday next week, 10pm. And more text')))

# [datetime.datetime(2019, 9, 17, 22, 0, 0, 0)]
#
# .extract by default will extract datetimes and timedeltas but not words.


parsewhen.replace('Some text, Tuesday next week, 10pm. And more text')

# 'Some text, 2019-09-17 22:00:00. And more text'
#
# .replace will replace the datetime and timedelta parts with stringified versions.
```


## Roadmap

This is a list of things it can currently parse and the ones I plan to support.


**Note:** Day and Month actually work but the short names do not.


- [ ] Date / Time
   - [x] Time `10pm / 01:30`
   - [x] Date `1st / 2nd / ...`
   - [ ] Day `Monday / Friday / Wed / ...`               
   - [ ] Month `January / October / Apr / ...`
   - [x] Year `2019 / 2001 / ...`
   - [x] Prefixes `Next Tuesday / Last week / Next Month`
   - [x] Tomorrow `Tomorrow / Yesterday / ...`
   - [ ] Timezone `+11 / GMT+0`

- [ ] Duration
   - [x] Years `1year / 7years`
   - [x] Hour `10hours / 1hour`
   - [x] Minutes `5minutes / 2min`
   - [x] Seconds `3seconds / 100sec`
   - [x] Days `3 days / two days / ...` 
   - [x] Ago `2 days ago / 5 hours ago`
