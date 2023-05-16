import scrapy


class PersonalSpider(scrapy.Spider):
    name = "personal"

    def start_requests(self):
        keywords = ["productos+personales"]
        for keyword in keywords:
            yield scrapy.Request(
                url=f"https://www.amazon.com.mx/s?k={keyword}&page=1",
                callback=self.search_products,
                meta={"keyword": keyword, "page": 1},
            )

    def search_products(self, response):
        keyword = response.meta["keyword"]
        page = response.meta["page"]

        products = response.css(
            "div.s-result-item[data-component-type=s-search-result]"
        )
        for product in products:
            calificacion = product.css("span.s-underline-text ::text").get("")
            if not calificacion:
                calificacion = None
            promocion = product.css("span.a-badge-text")
            prime = product.css("i.a-icon-prime")
            precio = product.css("span.a-price span.a-offscreen ::text").get("")
            if not precio:
                precio = None
            cupon = product.css("span.s-coupon-unclipped")    
            envio = product.css("div.a-row span.a-color-base ::text").getall()
            yield {
                "nombre": product.css("a.a-link-normal span.a-text-normal ::text").get(""),
                "puntaje": product.css("span.a-icon-alt ::text").get(""),
                "calificaciones": calificacion,
                "promocion": True if promocion else False,
                "precio": precio,
                "cupon": True if cupon else False,
                "prime": True if prime else False,
                "envio": envio[-1] if envio else None
            }


        if page == 1:
            total_pages = response.xpath(
                "//*[contains(@class, 's-pagination-item') and not(contains(@class, 's-pagination-separator'))]/text()"
            ).getall()
            last_page = total_pages[-1]
            for page_number in range(2, int(last_page)):
                yield scrapy.Request(
                    url=f"https://www.amazon.com.mx/s?k={keyword}&page={page_number}",
                    callback=self.search_products,
                    meta={"keyword": keyword, "page": page_number},
                )
