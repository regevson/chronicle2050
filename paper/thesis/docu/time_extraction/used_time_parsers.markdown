# Time-Parsers:

### SUTime
- time parser by harvard-nlp-package
- has some problems with times/durations:
  - The SETI Institute will not announce … within the next 20 years.
    - doesn't extract
  - Within the next 25 years the United States of America will no longer consist of 50 States
    - doesn't extract

### parsedatetime
- time parser used when SUTime is not working
  - The SETI Institute will not announce … within the next 20 years.
    - extracts: 2043-04-04
  - Within the next 25 years the United States of America will no longer consist of 50 States
    - extracts: 2048-04-04

