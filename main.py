import dash 
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# داده‌های شهرها (شامل نام، مختصات جغرافیایی، و جمعیت)
cities = pd.DataFrame([
    {"name": "Tehran", "lat": 35.6892, "lon": 51.3890, "pop": 8693706},
    {"name": "Mashhad", "lat": 36.2605, "lon": 59.6168, "pop": 3001184},
    {"name": "Isfahan", "lat": 32.6539, "lon": 51.6660, "pop": 1961260},
    {"name": "Karaj", "lat": 35.8400, "lon": 50.9391, "pop": 1592492},
    {"name": "Shiraz", "lat": 29.5926, "lon": 52.5836, "pop": 1565572},
    {"name": "Tabriz", "lat": 38.0962, "lon": 46.2738, "pop": 1558693},
    {"name": "Qom", "lat": 34.6416, "lon": 50.8746, "pop": 1201158},
    {"name": "Ahvaz", "lat": 31.3183, "lon": 48.6706, "pop": 1184788},
    {"name": "Kermanshah", "lat": 34.3277, "lon": 47.0778, "pop": 952285},
    {"name": "Urmia", "lat": 37.5522, "lon": 45.0761, "pop": 736224}
])

# اپلیکیشن Dash
app = dash.Dash(__name__)

#داشبورد طراحی بخش رابط کاربری
app.layout = html.Div([

    #عنوان داشبورد
    html.H1("داشبورد تحلیل جمعیت شهر های ایران",style={"textAlign":"center"}),
    #بخش تعاملی نقشه
    dcc.Graph(
        id="map", #شناسه نقشه
        config={"scrollZoom":False}#زوم نقشه با اسکرول

    ),
    #اسلایدر برای فیلتر شهر ها و جمعیت
    html.Label("فیلتر بر اساس جمعیت:"),
    dcc.Slider(
        id="population-slider", #شناسه
        min=0, #مقدار کمینه
        max=cities["pop"].max(), #مقدار بیشینه
        step=1000000, #گام حرکت
        value=cities["pop"].max(), #مقدار پیش فرض
        marks={i: f"{i//1000000}M" for i in range(0,cities["pop"].max()+1,2000000)} #نمایش مقیاس روی اسلایدر

    ),
    #نمودار میلیه ای
    dcc.Graph(id="bar-chart") #نمودار مقایسه جمعیت
    
])

#تعریف کال بک ها برای بروزرسانی داشبورد

@app.callback(

    #خروجی ها:نقشه و نمودار میله ای
    [Output("map", "figure"),
    Output("bar-chart", "figure")],
    #ورودی :مقدار اسلایدر جمعیت
    [Input("population-slider", "value")]
)
def update_dashboard(population_threshold):
    """
    این تابع داده هارابر اساس مقدار اسلایدر فیلتر کرده و نقشه و نمودار میله ای را بروزرسانی میکند
    """
    if population_threshold is None:
        return {}, {}  # بازگرداندن نقشه و نمودار خالی در صورت مقدار نامعتبر

    #فیلتر کردن شهر ها بر اساس مقدار جمعیت امتخاب شده
    filtered_cities=cities[cities["pop"] <= population_threshold]
    # اطمینان از وجود داده‌های فیلترشده
    if filtered_cities.empty:
        # اگر داده‌ای باقی نماند، نمودارها را خالی نمایش بده
        return {}, {}
    #نقشه تعاملی
    map_fig=px.scatter_geo(
        filtered_cities, #داده های فیلتر شده
        lat="lat",lon="lon", #ستون های عرض و طول جغرافیای
        size="pop", #اندازه نقاط بر اساس جمعیت
        hover_name="name", #نمایش نام شهر ها هنگام هاور
        title="موقیعت شهرها",
        color="pop", #رنگ نقاط بر اساس جمعیت
        projection="mercator" #نوع نمایش نقشه
    )
    #افزودن خطوط مرزی کشور ها
    map_fig.update_geos(
        showcountries=True, #نمایش خظوظ مرزی کشور ها
        countrycolor="darkgray",
        showcoastlines=True, #نمایش خطوط ساحلی
        coastlinecolor="blue" # رنگ خطوط ساحلی
    )


    #نمودار میله ای برای مقایسه جمعیت شهر ها 
    bar_fig =px.bar(
        filtered_cities.sort_values("pop",ascending=False), #مرتب سازی شهر ها بر اساس جمعیت
        x="name" , y="pop", #محور های نمودار
        title="مقایسه جمعیت شهرها" ,
        labels={"name":"شهر","pop":"جمعیت"} #برچسب محورها

    )

    return map_fig, bar_fig

    
if __name__=="__main__":
    app.run_server(debug=True)