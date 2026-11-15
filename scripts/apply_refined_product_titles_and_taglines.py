import re

with open('src/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Exact mapping for INITIAL_ITEMS
items_data = [
    {
        "code": "air-rhizome:air-afn-1",
        "brand": "ALTINOR",
        "name": "コードレスDCサーキュレーター",
        "tagline": "部屋干し時間が3倍速乾！<br />コードレスで家中どこでも涼しい"
    },
    {
        "code": "milicute-himawari:x06-1",
        "brand": "mili cute",
        "name": "卓上超音波USB加湿器",
        "tagline": "冬の乾燥やウイルスを撃退！<br />7色LEDでデスクを潤す静音ミスト"
    },
    {
        "code": "fithome:kjjs-demipro",
        "brand": "FitHome",
        "name": "超音波メガネ時計洗浄機",
        "tagline": "水だけで皮脂汚れをごっそり！<br />隙間の黒ずみまでピカピカに洗浄"
    },
    {
        "code": "irisplaza-r:287573",
        "brand": "山善(YAMAZEN)",
        "name": "温度調節スリム電気ケトル",
        "tagline": "1℃刻みで朝1分スピード沸騰！<br />ドリップも白湯も極上の一杯に"
    },
    {
        "code": "irisplaza-r:274252",
        "brand": "BRUNO",
        "name": "コンパクトホットプレート",
        "tagline": "A4サイズで煮る焼くを1台で！<br />狭いキッチンでも自炊が楽しくなる"
    },
    {
        "code": "e-kurashi:10000001",
        "brand": "ROOMMATE",
        "name": "お弁当箱型小型炊飯器",
        "tagline": "最短14分で炊きたてご飯！<br />茶碗1杯分をそのまま食べられる"
    },
    {
        "code": "dasimon:ennice-w13",
        "brand": "DASIMON",
        "name": "MagSafe磁気吸着バッテリー",
        "tagline": "背面にピタッと貼るだけ急速充電！<br />薄型軽量で操作の邪魔にならない"
    },
    {
        "code": "aquilaria:mjta1",
        "brand": "Aquilaria",
        "name": "AndroidTV小型プロジェクター",
        "tagline": "手のひらサイズで天井が大画面に！<br />YouTubeやネトフリが直で見放題"
    },
    {
        "code": "catmart:sd-2603ss1",
        "brand": "SEAdragon",
        "name": "4WAY強力ハンディクリーナー",
        "tagline": "超軽量320gで机も車内も一網打尽！<br />エアダスター機能でキーボードも清掃"
    },
    {
        "code": "hitidear:m118",
        "brand": "Hitidear",
        "name": "ノズル差し込み小型布団乾燥機",
        "tagline": "ホースを挿すだけで冷え布団が即天国！<br />靴乾燥アタッチメントで雨の日も安心"
    },
    {
        "code": "auc-risecreation:y0530",
        "brand": "atRise",
        "name": "強力6枚刃コードレス毛玉取り器",
        "tagline": "お気に入りの服が新品に蘇る！<br />生地を傷めず高速で毛玉をごっそり"
    }
]

for it in items_data:
    code = it["code"]
    brand = it["brand"]
    name = it["name"]
    tagline = it["tagline"]
    
    # regex replace within the object block for this itemCode
    # find block starting with "itemCode": "code"
    pattern = rf'("itemCode":\s*"{re.escape(code)}",\s*"title":\s*")[^"]*(".*?"tagline":\s*")[^"]*(")'
    
    def repl(m):
        return f'{m.group(1)}{brand} | {name}{m.group(2)}{tagline}{m.group(3)}'
    
    content = re.sub(pattern, repl, content, flags=re.DOTALL)

with open('src/data.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("src/data.js updated with clean 2-part brand/name and 2-line fixed taglines!")
