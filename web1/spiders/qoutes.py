# -*- coding: utf-8 -*-
import scrapy


class QoutesSpider(scrapy.Spider):
    name = 'qoutes'
    allowed_domains = ['buymebeauty.co.uk']
    start_urls = ['https://www.buymebeauty.co.uk/']

    def parse(self, response):
        links = response.xpath('.//*[@class="menu"]/li/a/@href').extract()
        for link in links:
            if("product-category" in link):
                yield scrapy.Request(link, callback=self.parse_cat)

    def parse_cat(self, response):
        _len = len(response.xpath(".//*[@class='woocommerce-pagination']/ul/li"))
        page_link = response.xpath(".//*[@class='woocommerce-pagination']/ul/li/a/@href").extract()

        if(_len != 0):
            for i in range(_len):
                yield scrapy.Request(page_link[i], callback=self.parse_page)
        else:
            yield scrapy.Request(response.url, callback=self.parse_page)

    def parse_page(self, response):
        product_links = response.xpath('.//*[@class="products columns-2"]/li/*[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href').extract()
        for product_link in product_links:
            yield scrapy.Request(product_link, callback=self.parse_product)


    def parse_product(self, response):
        image = response.xpath('.//figure/div/a/@href').extract()
        product_name = response.xpath('.//*[@class="summary entry-summary"]/h1/text()').extract()
        price = response.xpath('.//*[@class="summary entry-summary"]/*[@class="price"]/ins/span/text()').extract()
        category = response.xpath('.//*[@class="summary entry-summary"]/*[@class="product_meta"]/span/a/text()').extract()
        description = response.xpath('.//*[@class="summary entry-summary"]/*[@class="woocommerce-product-details__short-description"]/p/text()').extract()

        yield {
            'image': image,
            'product_name': product_name,
            'price': price,
            'category': category,
            'description': description
        }
