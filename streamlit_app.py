import streamlit as st
from PIL import Image, ImageOps
import time
import random
import colorsys
import re

def generate_softer_colors(n):
    hue_step = 1.0 / n
    colors = []
    for i in range(n):
        hue = i * hue_step
        saturation = 0.3 + random.random() * 0.3  # 30-60% saturation 채도
        value = 0.8 + random.random() * 0.2  # 80-100% value 명도
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)   # 겹치지 않게
        colors.append(f"rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})")
    random.shuffle(colors)  # Shuffle to avoid predictable color order
    return colors


scinarios=[{"in1": "./asset/blank.png",
            "topk": [],
            "in2": "./asset/blank.png",
            "dbsim": [],
            "msg": ["메시지1", "메시지2"],
            },
            {"in1": "./new2_scinarios/bag_1.png",
            "topk": [{"score": 98.97, "class": "가방"},
                     {"score": 0.34, "class": "인라인"},
                     {"score": 0.12, "class": "소형안마기"},
                     {"score": 0.12, "class": "쌀통"},
                     {"score": 0.04, "class": "카페트"},],
            "in2": "./new2_scinarios/20240531_104548.png",
            "dbsim": [{"score": 89.49, "imgpath": "./new2_scinarios/bag_1.png"},
                      {"score": 83.01, "imgpath": "./new2_scinarios/20240612_195256.png"},
                      {"score": 80.27, "imgpath": "./new2_scinarios/가방9.png"},
                      {"score": 78.00, "imgpath": "./new2_scinarios/가방_111.png"},
                      {"score": 62.96, "imgpath": "./new2_scinarios/가방_124.png"},],
            "msg": ["메시지1", "메시지2"],
            },
            {"in1": "./new2_scinarios/fan_1.png",
            "topk": [{"score": 92.97, "class": "선풍기"},
                     {"score": 2.83, "class": "환풍기"},
                     {"score": 1.85, "class": "온풍기"},
                     {"score": 0.57, "class": "공기청정기"},
                     {"score": 0.44, "class": "스탠드에어컨"},],
            "in2": "./new2_scinarios/20240723_164136.png",
            "dbsim": [{"score": 87.79, "imgpath": "./new2_scinarios/fan_1.png"},
                      {"score": 76.93, "imgpath": "./new2_scinarios/선풍기19.png"},
                      {"score": 74.74, "imgpath": "./new2_scinarios/선풍기 4.png"},
                      {"score": 70.38, "imgpath": "./new2_scinarios/선풍기_13.png"},
                      {"score": 67.43, "imgpath": "./new2_scinarios/선풍기(대형) 19.png"},],
            "msg": ["메시지1", "메시지2"],
            }
            ]

map = {"가방":1, "선풍기":2, None:0}

st.set_page_config(layout="wide", page_title="HectoAX", initial_sidebar_state="collapsed")
st.logo(image="./asset/site-logo.jpg")
st.title('♻ AX CycleAI')


def main(idx=0):
    idx = 0
    scinario=scinarios[idx]


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
    # col1.image("./asset/폐기물 배출.png")
    ll.image(ImageOps.exif_transpose(Image.open(scinario["in1"])))

    for pred in scinario["topk"]:
        lr.json(pred)
        # lr.write(str(pred))


    # 수거 run
    rr.image(ImageOps.exif_transpose(Image.open(scinario["in2"])))
    # rr.image("./asset/폐기물 수거1.png")
    for i, search in enumerate(scinario["dbsim"]):
        if i==0:
            rl.image(ImageOps.exif_transpose(Image.open(search["imgpath"])), caption=search["score"])
            rll, rlr = rl.columns(2)
        elif i%2!=0:
            rll.image(ImageOps.exif_transpose(Image.open(search["imgpath"])), caption=search["score"])
        else:
            rlr.image(ImageOps.exif_transpose(Image.open(search["imgpath"])), caption=search["score"])


def adjust_height(image, set_aspect=None):
    if set_aspect == None:
        return image
    width, height = image.size
    pad = int((height/set_aspect-width)/2)
    image = image.convert('RGBA')
    new_image = ImageOps.expand(image, border=(pad,0,pad,10), fill=(0,0,0,0) )
    return new_image




def loadinitpage():
    idx = 0
    scinario=scinarios[idx]
    cls = None


    # UI
    # st.write("## 폐기물 분류")
    # col1, rl, rr = st.columns([2, 1, 1])
    # ll, lr = col1.columns(2)
    col1, col2 = st.columns(2)
    col2.header("🗂️ 수거대상목록", divider=True)
    ll, lr = col1.columns(2)
    ll.header("🗑️ 배출", divider=True)
    lr.header("🛻 수거", divider=True)
    rl, rrl, rrr = col2.columns([2, 1, 1])


    # ll.write('### 배출')
    # lr.write('### 수거')
    # rl.write("### ")
    # rr.write("### ")

    option = ll.selectbox(
    "버리실 물건의 사진을 입력해주세요.",
    ("가방", "선풍기"),
    index=None,
    placeholder="버리실 물건의 사진을 입력해주세요.",
    label_visibility="collapsed"
    )
    idx=map[option]
    scinario=scinarios[idx]


    # 배출 run
    # col1.image("./asset/폐기물 배출.png")
    # if option !=None: ll.write("입력한 사진이 전시됩니다.")
    ll.image(adjust_height(ImageOps.exif_transpose(Image.open(scinario["in1"]))))
    if option !=None:
        cls = scinario["topk"][0]["class"]
    option1 = lr.selectbox(
    "확인할 물건의 사진을 입력해주세요.",
    (f"{cls} 1",),
    index=None,
    placeholder="확인할 물건의 사진을 입력해주세요.",
    label_visibility="collapsed"
    )

    if option !=None and option1 == None:
        with ll:
            with st.spinner('물건을 감지하는 중...'):
                time.sleep(2)
    if option !=None:
        cls = scinario["topk"][0]["class"]
        ll.success(f'**버리실 물건은 "{cls}" (으)로 감지되었습니다.**', icon="✅")
    
    # need to change to bar chart

    with ll:
        if option!=None:
            colors = generate_softer_colors(len(scinario["topk"]))
            for i, (topks, color) in enumerate(zip(scinario["topk"], colors)):
                rgb = [int(c) for c in color[4:-1].split(',')]
                lighter_color = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.6)"
                st.markdown(f"""
                <div class='keyword-item' style='animation-delay: {i*0.1}s;'>
                    <div class='keyword-text'>{topks["class"]}</div>
                    <div class='importance-bar'>
                        <div class='importance-fill' style='width: {topks["score"]}%; background: linear-gradient(to right, {color}, {lighter_color});'></div>
                    </div>
                    <div class='keyword-score'>{topks["score"]}</div>
                </div>
                """, unsafe_allow_html=True)


    # for pred in scinario["topk"]:
    #     lr.json(pred)
        # lr.write(str(pred))


    # 수거 run
    if option1 == None:
            scinario=scinarios[0]

    lr.image(adjust_height(ImageOps.exif_transpose(Image.open(scinario["in2"]))))


    if option !=None and option1 != None:
        with rl:
            with st.spinner('물건을 확인하는 중...'):
                time.sleep(2)
        

    for i, search in enumerate(scinario["dbsim"]):
        if i==0:
            rl.image(adjust_height(ImageOps.exif_transpose(Image.open(search["imgpath"]))))
            rl.metric(label="Similarity", value=f'{search["score"]} %', delta=f'{search["score"]-85:.2f} % : 일치', label_visibility="collapsed")
            # rrl, rrr = rr.columns(2)
        elif i%2!=0:
            rrl.image(adjust_height(ImageOps.exif_transpose(Image.open(search["imgpath"]))))
            rrl.metric(label="Similarity", value=f'{search["score"]} %', delta=f'{search["score"]-85:.2f} % : 불일치', label_visibility="collapsed")
        else:
            rrr.image(adjust_height(ImageOps.exif_transpose(Image.open(search["imgpath"]))))
            rrr.metric(label="Similarity", value=f'{search["score"]} %', delta=f'{search["score"]-85:.2f} % : 불일치', label_visibility="collapsed")

    if option !=None and option1 !=None: lr.info(f"**확인한 물건은 수거 대상 물품이 맞습니다.**", icon="⭕")
    # rl.image("./asset/폐기물 수거1.png")


    # Custom CSS and JS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f6;
        color: #1e1e1e;
    }
    .gradient-text {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        color: #4a4a4a;
        border-bottom: 2px solid #4ecdc4;
        padding-bottom: 0.5rem;
    }
    .text-content {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 60vh;
        overflow-y: auto;
    }
    .keyword {
        padding: 2px 4px;
        border-radius: 4px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .keyword:hover {
        filter: brightness(90%);
    }
    .keyword-item {
        display: flex;
        align-items: center;
        margin-bottom: -30px;
        animation: slideIn 0.5s ease-out forwards;
        opacity: 0;
    }
    .keyword-text {
        width: 120px;
        font-weight: bold;
        margin-right: 10px;
        font-size: 1.2em;
    }
    .importance-bar {
        flex-grow: 1;
        height: 20px;
        background-color: #E7DFCF;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
    }
    .importance-fill {
        height: 100%;
        animation: fillBar 1s ease-out;
    }
    .keyword-score {
        width: 80px;
        text-align: right;
        font-size: 1.8em;
        color: #666;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    @keyframes fillBar {
        from {
            width: 0%;
        }
    }
    </style>

    <script>
    function animateKeywords() {
        const keywords = document.querySelectorAll('.keyword-item');
        keywords.forEach((keyword, index) => {
            setTimeout(() => {
                keyword.style.opacity = 1;
                keyword.style.transform = 'translateX(0)';
            }, index * 100);
        });
    }

    // Call the animation function when the page loads
    document.addEventListener('DOMContentLoaded', animateKeywords);
    </script>
    """, unsafe_allow_html=True)


if __name__=="__main__":
    loadinitpage()