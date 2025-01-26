import plotly.graph_objects as go

# اطلاعات شهرها
cities = [
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
]

# ایجاد نقشه با Plotly
fig = go.Figure()

# تعریف رنگ‌های متفاوت بر اساس جمعیت
color_scale = ["#f94144", "#f3722c", "#f8961e", "#f9844a", "#43aa8b", "#577590"]

# افزودن نقاط شهرها
for city in cities:
    population_index = min(len(color_scale) - 1, city["pop"] // 2000000)  # تعیین رنگ بر اساس جمعیت
    fig.add_trace(go.Scattergeo(
        lon=[city["lon"]],
        lat=[city["lat"]],
        text=f"{city['name']}<br>جمعیت: {city['pop']:,}",
        marker=dict(
            size=city["pop"] / 50000,
            color=color_scale[population_index],
            line=dict(width=1, color="black")
        ),
        name=city["name"]
    ))

# تنظیمات نقشه
fig.update_geos(
    resolution=50,
    showcountries=True,
    countrycolor="darkgray",
    showcoastlines=True,
    coastlinecolor="lightblue",
    showland=True,
    landcolor="lightgray",
    projection=dict(type="mercator"),
    lataxis=dict(range=[25, 40]),  # محدوده عرض جغرافیایی
    lonaxis=dict(range=[44, 63])    # محدوده طول جغرافیایی
)

# اضافه کردن لگند توضیح رنگ‌ها
fig.update_layout(
    title_text="10 شهر پرجمعیت ایران (اندازه و رنگ متناسب با جمعیت)",
    geo=dict(
        domain=dict(x=[0, 1], y=[0, 1]),
        center=dict(lat=32, lon=53)
    ),
    legend=dict(title="راهنمای رنگ")
)

fig.show()
