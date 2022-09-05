import scrapy


class KhaadiSpider(scrapy.Spider):
    name = 'KHAADI'
    start_urls = ['https://pk.khaadi.com']

    def parse(self, response, **kwargs):

        categories_list = response.css('div.open-children-toggle + a::attr(href)').getall()
        yield from response.follow_all(categories_list, callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):

        sub_categories_list = response.css('div.menu-thumb-img a::attr(href)').getall()
        yield from response.follow_all(sub_categories_list, callback=self.parse_products)

    def parse_products(self, response):
        product_listing = response.css('div.product-item-photo a::attr(href)').getall()
        yield from response.follow_all(product_listing, callback=self.parse_items)

    def parse_items(self, response):

        yield {
            'name': response.css('span.base::text').get(),
            'description': response.css('.value[itemprop="description"]::text').get(),
            'sale_price': response.css('span[data-price-type=finalPrice]::attr(data-price-amount)').get(),
            'old_price': response.css('span[data-price-type=oldPrice]::attr(data-price-amount)').get(),
            'SKU': response.css('.value[itemprop="sku"]::text').get().split('_')[0],
            'outfit_details': self.fetch_details(response),
            'url': response.url
        }

    def fetch_details(self, response):

        outfit_info = {}
        for info in response.css("#Details div"):
            outfit_heading = info.css("strong::text").get()
            outfit_value = info.css("div::text").get()
            outfit_info[outfit_heading] = outfit_value

        return outfit_info
