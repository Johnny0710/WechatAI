from . import spider


def get_city_weather(city):
    get_weather = spider.GetCityWeather(city)
    weather = get_weather.get_page()
    if weather.get('status') == None:
        message = """{}天气
        今天是 {} 
        天气 : {} 
        温度 : {} 
        {} 
        {} 
        {} 
        {} 
        {} 
        """.format(
            weather.get('城市'),
            weather.get('日期'),
            weather.get('天气'),
            weather.get('温度'),
            weather.get('湿度'),
            weather.get('风向'),
            weather.get('紫外线'),
            weather.get('空气质量'),
            weather.get('PM'))
        return message
    else:
        return '不存在当前城市'