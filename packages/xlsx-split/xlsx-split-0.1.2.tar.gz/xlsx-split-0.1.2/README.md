# xlsx-split

Create new file for every row in excel sheet, with support of header and footer replication. 

## Install

    pip install xlsx-split

## Installed Commands

- xlsx-split

## Command Helps

```
    E:\xlsx-split>xlsx-split --help
    Usage: xlsx-split [OPTIONS] WORKBOOK

    Options:
    -h, --header TEXT            Header row number list.
    -f, --footer TEXT            Footer row number list.
    -c, --cols TEXT              Column number list.
    -r, --rows TEXT              Content row number list.
    -t, --test TEXT              Conditions that a good row must matchs. Format
                                like COL_LETTER:REGEX, e.g. A:\d+ means the
                                value of A column must be an Integer.
    -s, --sheet TEXT             Sheet name. Default to Current Active Sheet
    -w, --workspace TEXT         Where new files saved. Default to
                                "{FILENAME_ROOT}"
    -p, --filename-pattern TEXT  Default to
                                "{FILENAME_ROOT}-{ROW}.{FILENAME_EXT}"
    --help                       Show this message and exit.
```

## Notice

- header/footer/rows obeys ROWS-RULE.
- cols obeys COLS-RULE.
- test obeys TEST-RULE。
- filename-pattern obeys FILENAME-RULE。

### ROWS-RULE

- 1         == [1]
- 1,2,3     == [1,2,3]
- 1-3       == [1,2,3]
- 1-3,5     == [1,2,3,5]
- 3-        == [3,4,5,6....] # From the third row to the sheet.max_rows

### COLS-RULE

- A         == [1]
- A,B,C     == [1,2,3]
- A-C       == [1,2,3]
- A-C,E     == [1,2,3,5]
- C-        == [3,4,5,6....] # From column C to the sheet.max_cols

### TEST-RULE

- Can provide multiple tests.
- The final result is the result of LOGIC AND of all tests result.
- Test format: Column:TestRegex, e.g. A:\d+ means the Column A must contain digits.


### FILENAME-RULE

- filename-pattern is a python string format template.
- Available variables
    - FILEPATH          Source file's full path, e.g. c:\a\b.xlsx
    - DIRNAME           Source file's direct folder path, e.g. c:\a
    - FILENAME          Source file's filename, e.g. b.xlsx
    - FILENAME_ROOT     Source file's filename without ext, e.g. b
    - FILENAME_EXT      Source file's file ext, e.g. .xlsx
    - ROW               Index of current row，如1,2,3...
    - A..Z,AA...        The value of the cell [ROW, COLUMN]. A or Z or ZZ is the column.

## Releases

### 0.1.2

- Fix parse_rows & parse_cols problem.
- Document changes.

### 0.1.1

- Document changes.

### 0.1.0

- First release