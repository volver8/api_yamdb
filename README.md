# Api_yamdb

## Description
*This API implements a backend for a web application*

*API documentation:* [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

![](https://www.ibexa.co/var/site/storage/images/_aliases/ibexa_content_full/3/4/1/0/300143-1-eng-GB/d4255a27c1fa-AdobeStock_261705271_What-is-an-API.jpeg)

This API implements serialization and deserialization of data in models such as:
- Category
- Genre
- Title
- Review
- Comment
- User

## Requests
There are some examples of requests:
  -  Model Title

      - GET request: /api/v1/titles/
          ```
          {
            "count": 0,
            "next": "string",
            "previous": "string",
            "results": [
              {
                "id": 0,
                "name": "string",
                "year": 0,
                "rating": 0,
                "description": "string",
                "genre": [
                  {
                  "name": "string",
                  "slug": "^-$"
                  }
                ],
                "category": {
                  "name": "string",
                  "slug": "^-$"
                }
              }
            ]
          }
          ```
       
  -  JWT token

      - POST request: /api/v1/auth/token/

        - Request samples
        ```
        {
          "username": "^w\\Z",
          "confirmation_code": "string"
        }
        ```
        - Response samples
        ```
        {
          "token": "string"
        }
        ```

## Developers:

- Vladimir Rusakov
- Evgeny Kudryashov
- Evgeny Cherednichenko
