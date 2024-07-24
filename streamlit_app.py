import streamlit as st
from PIL import Image, ImageOps


scinarios=[{"in1": "./asset/blank.png",
            "topk": [],
            "in2": "./asset/blank.png",
            "dbsim": [],
            "msg": ["메시지1", "메시지2"],
            },
            {"in1": "./scinarios/bag_1.jpg",
            "topk": [{"score": 98.97, "class": "가방"},
                     {"score": 0.34, "class": "인라인"},
                     {"score": 0.12, "class": "소형안마기"},
                     {"score": 0.12, "class": "쌀통"},
                     {"score": 0.04, "class": "카페트"},],
            "in2": "./scinarios/20240531_104548.jpg",
            "dbsim": [{"score": 89.49, "imgpath": "./scinarios/bag_1.jpg"},
                      {"score": 83.01, "imgpath": "./scinarios/20240612_195256.jpg"},
                      {"score": 80.27, "imgpath": "./scinarios/가방9.jpg"},
                      {"score": 78.00, "imgpath": "./scinarios/가방_111.jpg"},
                      {"score": 62.96, "imgpath": "./scinarios/가방_124.jpeg"},],
            "msg": ["메시지1", "메시지2"],
            },
            {"in1": "./scinarios/fan_1.jpg",
            "topk": [{"score": 92.97, "class": "선풍기"},
                     {"score": 2.83, "class": "환풍기"},
                     {"score": 1.85, "class": "온풍기"},
                     {"score": 0.57, "class": "공기청정기"},
                     {"score": 0.44, "class": "스탠드에어컨"},],
            "in2": "./scinarios/20240723_164136.jpg",
            "dbsim": [{"score": 87.79, "imgpath": "./scinarios/fan_1.jpg"},
                      {"score": 76.93, "imgpath": "./scinarios/선풍기19.jpg"},
                      {"score": 74.74, "imgpath": "./scinarios/선풍기 4.jpg"},
                      {"score": 70.38, "imgpath": "./scinarios/선풍기_13.jpg"},
                      {"score": 67.43, "imgpath": "./scinarios/선풍기(대형) 19.jpg"},],
            "msg": ["메시지1", "메시지2"],
            }
            ]
idx = 1
scinario=scinarios[idx]

st.set_page_config(layout="wide", page_title="HectoAX", initial_sidebar_state="collapsed")

# UI
# st.write("## 폐기물 분류")
col1, rl, rr = st.columns([2, 1, 1])
ll, lr = col1.columns(2)
ll.write('### 배출')
lr.write("### ")
rl.write('### 수거')
rr.write("### ")
# ll, lr = col1.columns(2)
# rl, rr = col2.columns(2)

# 배출 run
col1.image("./asset/ex11.png")
ll.image(ImageOps.exif_transpose(Image.open(scinario["in1"])))

for pred in scinario["topk"]:
    lr.json(pred)
    # lr.write(str(pred))


# 수거 run
rr.image(ImageOps.exif_transpose(Image.open(scinario["in2"])))
for i, search in enumerate(scinario["dbsim"]):
    if i==0:
        rl.image(ImageOps.exif_transpose(Image.open(search["imgpath"])), caption=search["score"])
        rll, rlr = rl.columns(2)
    elif i%2!=0:
        rll.image(ImageOps.exif_transpose(Image.open(search["imgpath"])), caption=search["score"])
    else:
        rlr.image(ImageOps.exif_transpose(Image.open(search["imgpath"])), caption=search["score"])


