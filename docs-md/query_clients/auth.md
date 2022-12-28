Module nibiru.query_clients.auth
================================

Classes
-------

`AuthQueryClient(channel: grpc.Channel)`
:   AuthQueryClient allows to query the endpoints made available by the Nibiru Chain's auth module.

    ### Ancestors (in MRO)

    * nibiru.query_clients.util.QueryClient

    ### Methods

    `account(self, address: str) ‑> dict`
    :   Returns information of the given account

        Example Return Value::

        ```json
        {
          "address": "nibi1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
          "pub_key": null,
          "account_number": "17",
          "sequence": "0"
        }
        ```

        Args:
            address(str): the address of the account we want to get information

        Returns:
            dict: a dictionary containing information of the account

    `accounts(self) ‑> dict`
    :   Accounts returns all the existing accounts

        Example Return Value::

        ```json
        {
        "accounts": [
            {
              "address": "nibi1qqrg9ntgkavhxyn3zq0zmz85yp8vxgd9gm85pp",
              "pub_key": null,
              "account_number": "16246",
              "sequence": "0"
            },
            {
              "address": "nibi1qqrhxfwt6eu66v6mcdt7zc6xhqnw0w54u3rep3",
              "pub_key": null,
              "account_number": "6927",
              "sequence": "0"
            }
          ]
        }
        ```

        Returns:
            dict: a dictionary with information of all the existing accounts paginated
