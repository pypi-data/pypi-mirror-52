# Library for processing structured text into python object (dict or list) using templates.

## Using:
```shell script
text2py -t template.yml -i input.txt -o output.txt
```

```python
import text2py
parser = text2py.Parser(template)
output = parser.parse(input_file)
```

## Template format:

Scalar value:
```yaml
- regexp: 'Volume (?P<volume>\w+) Author (?P<author>\w+)'
  key: "{volume}"
  value: "{author}"
```
```python
{volume: author}
```
Dict value
```yaml
- regexp: 'Volume (?P<volume>\w+) Author (?P<author>\w+) Review (?P<review>)'
  key: "volumes.{volume}"
  values:
    - key: 'author'
      value: "{author}"
    - key: 'review'
      value: "{review}"
```
```python
{'volumes' {volume: {'author': author, 'review': review}}}
```

