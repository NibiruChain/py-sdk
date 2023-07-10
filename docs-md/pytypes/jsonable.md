Module pysdk.pytypes.jsonable
=============================

Functions
---------


`dict_to_jsonable(d: Mapping[~KT, +VT_co]) ‑> pysdk.pytypes.jsonable.Jsonable`
:   Recursively calls to_jsonable on each element of the given map.


`to_iso(dt: datetime.datetime) ‑> str`
:


`to_jsonable(obj: Any) ‑> Any`
:

Classes
-------

`Jsonable()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * pysdk.tx.Transaction

    ### Methods

    `to_json_str(self) ‑> str`
    :

    `to_jsonable(self) ‑> Any`
    :   Returns a JSON-serializable Python representation
