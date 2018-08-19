### 看一下今天最高气温 超过35度的 , 只有六个城市, 毕竟入秋了嘛


```db.getCollection('citys').find({"max_temperature":{'$gt':'35'}})```

```
/* 1 */
{
    "_id" : ObjectId("5b7938d2e1267a73482e090c"),
    "city" : "安康",
    "day_weather" : "晴 西风 <3级",
    "max_temperature" : "36",
    "night_weather" : "晴 东风 <3级",
    "min_temperature" : "25"
}

/* 2 */
{
    "_id" : ObjectId("5b7938d5e1267a73482e0915"),
    "city" : "南充",
    "day_weather" : "多云 无持续风向 <3级",
    "max_temperature" : "36",
    "night_weather" : "晴 无持续风向 <3级",
    "min_temperature" : "25"
}

/* 3 */
{
    "_id" : ObjectId("5b7938d5e1267a73482e0916"),
    "city" : "达州",
    "day_weather" : "多云 无持续风向 <3级",
    "max_temperature" : "37",
    "night_weather" : "多云 无持续风向 <3级",
    "min_temperature" : "25"
}

/* 4 */
{
    "_id" : ObjectId("5b7938d5e1267a73482e0917"),
    "city" : "遂宁",
    "day_weather" : "多云 无持续风向 <3级",
    "max_temperature" : "36",
    "night_weather" : "晴 无持续风向 <3级",
    "min_temperature" : "25"
}

/* 5 */
{
    "_id" : ObjectId("5b7938d5e1267a73482e0918"),
    "city" : "广安",
    "day_weather" : "多云 无持续风向 <3级",
    "max_temperature" : "36",
    "night_weather" : "晴 无持续风向 <3级",
    "min_temperature" : "25"
}

/* 6 */
{
    "_id" : ObjectId("5b7938d5e1267a73482e091c"),
    "city" : "内江",
    "day_weather" : "多云 无持续风向 <3级",
    "max_temperature" : "36",
    "night_weather" : "晴 无持续风向 <3级",
    "min_temperature" : "24"
}
```


### 再来看一下 报着有雨的城市   数据略多 只放城市名称

```
datas = citys.find({"day_weather":{'$regex':'雨'}})
data = [d['city'] for d in datas]


['北京', '海淀', '朝阳', '顺义', '怀柔', '通州', '昌平', '延庆', '丰台', '石景山', '大兴', '房山', '密云', '门头沟', '平谷', '东城', '西城', '武汉', '鄂州', '孝感', '黄冈', '黄石', '随州', '南宁', '崇左', '来宾', '梧州', '贺州', '玉林', '钦州', '北海', '防城港', '甘孜', '阿坝']
有34个之多呢
```

