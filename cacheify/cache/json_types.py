from typing import Union, List, Dict

JSONType = Union[
    None,                # JSON null
    bool,                # JSON boolean
    int,                 # JSON number (integer)
    float,               # JSON number (float)
    str,                 # JSON string
    List['JSONType'],    # JSON array (can be nested)
    Dict[str, 'JSONType'] # JSON object (with string keys)
]