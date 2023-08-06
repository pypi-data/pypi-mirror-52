# fastutils

Collection of simple utils.

## Install

```
pip install fastutils
```

## Installed Utils

- aesutils
- dictutils
- hashutils
- listutils
- strutils
- funcutils

## Usage Example

```
from fastutils import strutils
assert strutils.split("a,b.c", [",", "."]) == ["a", "b", "c"]
```



## Release Notice

### v0.3.0 

- Add listutils.unique to remove duplicated elements from the list.
- Add listutils.replace to replace element value in thelist with new_value in collection of map.

### v0.2.0 2019.09.10

- Add functuils.get_inject_params to smartly choose parameters from candidates by determine with the function's signature.
- Add functuils.call_with_inject to smartly call the function by smartly choose parameters.

### v0.1.1 2019.08.27

- Add strutils.wholestrip function, use to remove all white spaces in text.
- Fix strutils.is_urlsafeb64_decodable, strutils.is_base64_decodable and strutils.is_unhexlifiable functions, that have problem to test text contains whitespaces.

### v0.1.0 2019.08.23

- Add simple utils about operations of aes, dict, hash, list and str.
