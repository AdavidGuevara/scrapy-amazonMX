# Scraping to amazonMx.

- Use the anti-bot scrapeops tool.
- to access the headers you can use a class middleware with the following functions:

    def process_request(self, request, spider):
          print(f"Request Header: {request.headers}")

     def process_response(self, request, response, spider):
          print(f"Response Header: {response.headers}")
          return response  

