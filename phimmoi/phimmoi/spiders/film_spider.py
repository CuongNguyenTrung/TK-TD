import scrapy


class FilmSpider(scrapy.Spider):
    name = "films"
    start_urls = ['http://www.phimmoi.net/phim-le/']

    def parse(self, response):
       movies = response.css("li.movie-item")
       for movie in movies:

           for href in response.css("ul.pagination a::attr(href)"):
               yield response.follow(href, callback=self.parse)

           #vào link cụ thể của film
           for href in movie.css("a.block-wrapper::attr(href)"):
               yield response.follow(href, callback=self.parse_film)


    def parse_film(self, response):
        def remove_strip(string):
            if string is not None:
                return string.strip()

        def remove_strip_array(array_string):
            return [item.strip() for item in array_string]

        movie_info = response.css("div.movie-info")
        v_name = remove_strip(movie_info.css("a.title-1::text").get())
        e_name = remove_strip(movie_info.css("span.title-2::text").get())
        content = remove_strip(movie_info.css("#film-content p::text").get())
        director = remove_strip(movie_info.css("a.director::text").get())
        country = remove_strip(movie_info.css("a.country::text").get())
        link = remove_strip(response.urljoin(response.css("a.title-1::attr(href)").get()))
        year = remove_strip(movie_info.css("span.title-year::text").get())[1:-1]
        tags = remove_strip_array(movie_info.css("dd.dd-cat a::text").getall())
        # print(v_name, e_name, content, link, director, country, year, tags)
        yield {
            "v_name" : v_name,
            "e_name" : e_name,
            "content" : content,
            "year" : year,
            "director" : director,
            "country" : country,
            "tags" : tags,
            "link" : link,
        }