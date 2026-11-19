import streamlit as st
import random

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN PASTEL NỮ TÍNH DỊU MẮT
# ==========================================
st.set_page_config(
    page_title="Ôn Tập Từ Vựng - Thiên Trang",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Nhúng CSS tinh tế: Ẩn thanh header/menu góc phải, màu sắc dịu dàng không chói mắt
st.markdown("""
<style>
    /* ẨN TOÀN BỘ CỤM ICON, MENU & HEADER GÓC PHẢI TRÊN */
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    [data-testid="stHeader"] {display: none !important; height: 0 !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    /* Căn chỉnh khoảng cách đỉnh trang */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 950px !important;
    }

    /* Nền tổng thể: Gradient hồng sữa, kem ngà và tím phấn oải hương */
    .stApp {
        background: linear-gradient(145deg, #FFF9FA 0%, #FBF6FC 50%, #F7F5FA 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header chính */
    .app-title {
        text-align: center;
        color: #5C1E3F;
        font-size: 27px;
        font-weight: 700;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }
    .app-subtitle {
        text-align: center;
        color: #8C4368;
        font-size: 13.5px;
        margin-bottom: 22px;
    }

    /* Thẻ Flashcard lật 3D */
    .flashcard-wrapper {
        perspective: 1000px;
        margin: 15px auto;
        max-width: 560px;
        cursor: pointer;
    }
    .flashcard-toggle {
        display: none;
    }
    .flashcard-inner {
        position: relative;
        width: 100%;
        min-height: 330px;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
        border-radius: 26px;
        box-shadow: 0 10px 28px -4px rgba(173, 114, 142, 0.12);
    }
    .flashcard-toggle:checked + .flashcard-inner {
        transform: rotateY(180deg);
    }
    .flashcard-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 26px;
        padding: 30px 26px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1.5px solid #F3DAE4;
    }
    .flashcard-front {
        align-items: center;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF5F8 100%);
    }
    .flashcard-back {
        transform: rotateY(180deg);
        background: linear-gradient(180deg, #FDFBFE 0%, #F9F3F7 100%);
        border-color: #EBD3E0;
    }
    .badge-pill {
        background: #F8E7EE;
        color: #8C2E59;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }
    .chinese-word {
        font-size: 50px;
        color: #5C1E3F;
        margin: 10px 0 4px 0;
        font-weight: 700;
    }
    .pinyin-word {
        font-size: 23px;
        color: #9D4E84;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* Cụm từ và ví dụ có Pinyin */
    .colloc-item {
        background: #FFFFFF;
        padding: 6.5px 12px;
        border-radius: 11px;
        margin-bottom: 5px;
        font-size: 13px;
        color: #374151;
        border: 1px solid #F3DAE4;
        line-height: 1.4;
    }
    .example-box {
        background: #FFF5F8;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 12.5px;
        color: #5C1E3F;
        border: 1px solid #FCE4EC;
        margin-top: 8px;
        line-height: 1.5;
    }

    /* Thẻ Mục lục */
    .vocab-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 12px;
        border: 1px solid #F3DAE4;
        box-shadow: 0 4px 12px -2px rgba(173, 114, 142, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DỮ LIỆU TỔNG HỢP 30 TỪ VỰNG CHUẨN CÓ PINYIN ĐẦY ĐỦ
# ==========================================
VOCAB_DATA = [
    # --- BÀI 1: CÔNG TY & NĂNG LỰC NHÀ XƯỞNG (20 TỪ) ---
    {
        "id": 1, "lesson": 1, "word": "公司", "pinyin": "gōngsī", "meaning": "công ty",
        "collocations": [
            "台资公司 (táizī gōngsī) — công ty Đài Loan",
            "总公司 (zǒng gōngsī) — công ty mẹ",
            "分公司 (fēn gōngsī) — chi nhánh"
        ],
        "example": "我们是一家专业的纺织公司。<br><i>(Wǒmen shì yì jiā zhuānyè de fǎngxī gōngsī. — Chúng tôi là một công ty dệt may chuyên nghiệp.)</i>"
    },
    {
        "id": 2, "lesson": 1, "word": "台资", "pinyin": "táizī", "meaning": "vốn Đài Loan",
        "collocations": [
            "台资企业 (táizī qǐyè) — doanh nghiệp Đài Loan",
            "台资独资 (táizī dúzī) — 100% vốn Đài"
        ],
        "example": "我们公司是台资企业。<br><i>(Wǒmen gōngsī shì táizī qǐyè. — Công ty chúng tôi là doanh nghiệp có vốn Đài Loan.)</i>"
    },
    {
        "id": 3, "lesson": 1, "word": "成立", "pinyin": "chénglì", "meaning": "thành lập",
        "collocations": [
            "成立于……年 (chénglì yú... nián) — thành lập năm...",
            "正式成立 (zhèngshì chénglì) — chính thức thành lập"
        ],
        "example": "我们公司成立于 2015 年。<br><i>(Wǒmen gōngsī chénglì yú èr líng yī wǔ nián. — Công ty chúng tôi được thành lập năm 2015.)</i>"
    },
    {
        "id": 4, "lesson": 1, "word": "规模", "pinyin": "guīmó", "meaning": "quy mô",
        "collocations": [
            "企业规模 (qǐyè guīmó) — quy mô doanh nghiệp",
            "规模很大 (guīmó hěn dà) — quy mô rất lớn"
        ],
        "example": "工厂规模很大。<br><i>(Gōngchǎng guīmó hěn dà. — Quy mô nhà xưởng rất lớn.)</i>"
    },
    {
        "id": 5, "lesson": 1, "word": "员工", "pinyin": "yuángōng", "meaning": "nhân viên, công nhân",
        "collocations": [
            "公司员工 (gōngsī yuángōng) — nhân viên công ty",
            "员工人数 (yuángōng rénshù) — số lượng nhân viên"
        ],
        "example": "工厂规模很大，现有 500 名员工。<br><i>(Gōngchǎng guīmó hěn dà, xiàn yǒu wǔbǎi míng yuángōng. — Quy mô xưởng rất lớn, hiện có 500 nhân viên.)</i>"
    },
    {
        "id": 6, "lesson": 1, "word": "生产", "pinyin": "shēngchǎn", "meaning": "sản xuất",
        "collocations": [
            "生产面料 (shēngchǎn miànliào) — sản xuất vải",
            "投入生产 (tóurù shēngchǎn) — đưa vào sản xuất"
        ],
        "example": "工厂专门生产针织面料。<br><i>(Gōngchǎng zhuānmén shēngchǎn zhēnzhī miànliào. — Nhà máy chuyên sản xuất vải dệt kim.)</i>"
    },
    {
        "id": 7, "lesson": 1, "word": "经营", "pinyin": "jīngyíng", "meaning": "kinh doanh",
        "collocations": [
            "主要经营 (zhǔyào jīngyíng) — chủ yếu kinh doanh",
            "经营范围 (jīngyíng fànwéi) — phạm vi kinh doanh"
        ],
        "example": "主要经营高档运动面料。<br><i>(Zhǔyào jīngyíng gāodàng yùndòng miànliào. — Chuyên kinh doanh vải thể thao cao cấp.)</i>"
    },
    {
        "id": 8, "lesson": 1, "word": "业务", "pinyin": "yèwù", "meaning": "nghiệp vụ, kinh doanh",
        "collocations": [
            "进出口业务 (jìn-chūkǒu yèwù) — nghiệp vụ XNK",
            "开展业务 (kāizhǎn yèwù) — triển khai nghiệp vụ"
        ],
        "example": "我们负责纺织品进出口业务。<br><i>(Wǒmen fùzé fǎngxīpǐn jìn-chūkǒu yèwù. — Chúng tôi phụ trách nghiệp vụ xuất nhập khẩu dệt may.)</i>"
    },
    {
        "id": 9, "lesson": 1, "word": "产品", "pinyin": "chǎnpǐn", "meaning": "sản phẩm",
        "collocations": [
            "新产品 (xīn chǎnpǐn) — sản phẩm mới",
            "产品目录 (chǎnpǐn mùlù) — catalogue sản phẩm"
        ],
        "example": "请发一份产品目录给我。<br><i>(Qǐng fā yí fèn chǎnpǐn mùlù gěi wǒ. — Xin vui lòng gửi một bản catalogue sản phẩm cho tôi.)</i>"
    },
    {
        "id": 10, "lesson": 1, "word": "主打", "pinyin": "zhǔdǎ", "meaning": "chủ lực, bán chạy",
        "collocations": [
            "主打产品 (zhǔdǎ chǎnpǐn) — sản phẩm chủ lực",
            "主打面料 (zhǔdǎ miànliào) — vải chủ lực"
        ],
        "example": "这是我们工厂的主打产品。<br><i>(Zhè shì wǒmen gōngchǎng de zhǔdǎ chǎnpǐn. — Đây là sản phẩm chủ lực của xưởng chúng tôi.)</i>"
    },
    {
        "id": 11, "lesson": 1, "word": "面料", "pinyin": "miànliào", "meaning": "vải",
        "collocations": [
            "针织面料 (zhēnzhī miànliào) — vải dệt kim",
            "运动面料 (yùndòng miànliào) — vải thể thao"
        ],
        "example": "这款面料的手感非常好。<br><i>(Zhè kuǎn miànliào de shǒugǎn fēicháng hǎo. — Mẫu vải này sờ rất mềm mại.)</i>"
    },
    {
        "id": 12, "lesson": 1, "word": "材质", "pinyin": "cáizhì", "meaning": "chất liệu",
        "collocations": [
            "面料材质 (miànliào cáizhì) — chất liệu vải",
            "环保材质 (huánbǎo cáizhì) — chất liệu thân thiện môi trường"
        ],
        "example": "这款面料的材质是什么？它是 100% 纯棉的。<br><i>(Zhè kuǎn miànliào de cáizhì shì shénme? Tā shì bǎifēnzhī bǎi chúnmián de. — Chất liệu vải này là gì? Nó là 100% cotton.)</i>"
    },
    {
        "id": 13, "lesson": 1, "word": "纯棉", "pinyin": "chúnmián", "meaning": "100% cotton",
        "collocations": [
            "纯棉布 (chúnmiánbù) — vải cotton",
            "100% 纯棉 (bǎifēnzhī bǎi chúnmián) — 100% cotton"
        ],
        "example": "我们工厂主要生产纯棉面料。<br><i>(Wǒmen gōngchǎng zhǔyào shēngchǎn chúnmián miànliào. — Nhà máy chúng tôi chủ yếu sản xuất vải cotton.)</i>"
    },
    {
        "id": 14, "lesson": 1, "word": "规格", "pinyin": "guīgé", "meaning": "quy cách, thông số",
        "collocations": [
            "确认规格 (quèrèn guīgé) — xác nhận quy cách",
            "产品规格 (chǎnpǐn guīgé) — quy cách sản phẩm"
        ],
        "example": "我们需要确认具体的面料规格。<br><i>(Wǒmen xūyào quèrèn jùtǐ de miànliào guīgé. — Chúng tôi cần xác nhận thông số kỹ thuật vải cụ thể.)</i>"
    },
    {
        "id": 15, "lesson": 1, "word": "货号", "pinyin": "huòhào", "meaning": "mã hàng",
        "collocations": [
            "面料货号 (miànliào huòhào) — mã vải",
            "查货号 (chá huòhào) — tra mã hàng"
        ],
        "example": "请问这款布的货号是多少？<br><i>(Qǐngwèn zhè kuǎn bù de huòhào shì duōshao? — Xin hỏi mã hàng của mẫu vải này là bao nhiêu?)</i>"
    },
    {
        "id": 16, "lesson": 1, "word": "工厂", "pinyin": "gōngchǎng", "meaning": "nhà máy, nhà xưởng",
        "collocations": [
            "参观工厂 (cānguān gōngchǎng) — thăm nhà máy",
            "工厂地址 (gōngchǎng dìzhǐ) — địa chỉ xưởng"
        ],
        "example": "欢迎来到我们工厂参观！<br><i>(Huānyíng lái dào wǒmen gōngchǎng cānguān! — Chào mừng đến tham quan nhà máy chúng tôi!)</i>"
    },
    {
        "id": 17, "lesson": 1, "word": "车间", "pinyin": "chējiān", "meaning": "phân xưởng sản xuất",
        "collocations": [
            "生产车间 (shēngchǎn chējiān) — phân xưởng sản xuất",
            "织造车间 (zhīzào chējiān) — xưởng dệt"
        ],
        "example": "欢迎来车间参观。<br><i>(Huānyíng lái chējiān cānguān. — Hoan nghênh ghé thăm phân xưởng.)</i>"
    },
    {
        "id": 18, "lesson": 1, "word": "产能", "pinyin": "chǎnnéng", "meaning": "công suất",
        "collocations": [
            "月产能 (yuè chǎnnéng) — công suất tháng",
            "产能充足 (chǎnnéng chōngzú) — công suất dồi dào"
        ],
        "example": "工厂的月产能非常稳定。<br><i>(Gōngchǎng de yuè chǎnnéng fēicháng wěndìng. — Công suất hàng tháng của nhà máy rất ổn định.)</i>"
    },
    {
        "id": 19, "lesson": 1, "word": "出口", "pinyin": "chūkǒu", "meaning": "xuất khẩu",
        "collocations": [
            "出口到欧美 (chūkǒu dào Ōu-Měi) — xuất sang Âu Mỹ",
            "出口市场 (chūkǒu shìchǎng) — thị trường xuất khẩu"
        ],
        "example": "产品主要出口到欧美。<br><i>(Chǎnpǐn zhǔyào chūkǒu dào Ōu-Měi. — Sản phẩm chủ yếu xuất khẩu sang Âu Mỹ.)</i>"
    },
    {
        "id": 20, "lesson": 1, "word": "欢迎", "pinyin": "huānyíng", "meaning": "chào đón, hoan nghênh",
        "collocations": [
            "欢迎来访 (huānyíng láifǎng) — chào mừng đến thăm",
            "欢迎来厂 (huānyíng lái chǎng) — chào mừng tới xưởng"
        ],
        "example": "产品主要出口到欧美，欢迎来车间参观！<br><i>(Chǎnpǐn zhǔyào chūkǒu dào Ōu-Měi, huānyíng lái chējiān cānguān! — Sản phẩm chủ yếu xuất sang Âu Mỹ, hoan nghênh đến thăm phân xưởng!)</i>"
    },

    # --- BÀI 2: ĐƠN GIÁ, HÀNG SẴN & MOQ (10 TỪ) ---
    {
        "id": 21, "lesson": 2, "word": "经理", "pinyin": "jīnglǐ", "meaning": "giám đốc, quản lý",
        "collocations": [
            "陈经理 (Chén jīnglǐ) — Giám đốc Trần",
            "李经理 (Lǐ jīnglǐ) — Giám đốc Lý",
            "业务经理 (yèwù jīnglǐ) — Quản lý kinh doanh"
        ],
        "example": "陈经理，您好！<br><i>(Chén jīnglǐ, nín hǎo! — Chào Giám đốc Trần!)</i>"
    },
    {
        "id": 22, "lesson": 2, "word": "单价", "pinyin": "dānjià", "meaning": "đơn giá",
        "collocations": [
            "面料单价 (miànliào dānjià) — đơn giá vải",
            "最低单价 (zuìdī dānjià) — đơn giá thấp nhất",
            "确认单价 (quèrèn dānjià) — xác nhận đơn giá"
        ],
        "example": "这款布的单价是多少？<br><i>(Zhè kuǎn bù de dānjià shì duōshao? — Đơn giá của mẫu vải này là bao nhiêu?)</i>"
    },
    {
        "id": 23, "lesson": 2, "word": "多少钱", "pinyin": "duōshao qián", "meaning": "bao nhiêu tiền",
        "collocations": [
            "一米多少钱 (yì mǐ duōshao qián) — một mét bao nhiêu tiền",
            "多少钱一米 (duōshao qián yì mǐ) — bao nhiêu tiền một mét"
        ],
        "example": "请问这款针织布一米多少钱？<br><i>(Qǐngwèn zhè kuǎn zhēnzhībù yì mǐ duōshao qián? — Cho hỏi vải dệt kim này bao nhiêu tiền một mét?)</i>"
    },
    {
        "id": 24, "lesson": 2, "word": "米", "pinyin": "mǐ", "meaning": "mét (đơn vị đo vải)",
        "collocations": [
            "两千米 (liǎng qiān mǐ) — hai nghìn mét",
            "一千米 (yì qiān mǐ) — một nghìn mét"
        ],
        "example": "我们先订两千米。<br><i>(Wǒmen xiān dìng liǎng qiān mǐ. — Chúng tôi đặt trước 2.000 mét.)</i>"
    },
    {
        "id": 25, "lesson": 2, "word": "优惠", "pinyin": "yōuhuì", "meaning": "ưu đãi, bớt giá",
        "collocations": [
            "价格优惠 (jiàgé yōuhuì) — ưu đãi về giá",
            "优惠一点 (yōuhuì yìdiǎn) — ưu đãi thêm chút"
        ],
        "example": "订单量大，价格能优惠一点吗？<br><i>(Dìngdān liàng dà, jiàgé néng yōuhuì yìdiǎn ma? — Đơn hàng lớn, giá có thể ưu đãi thêm chút không?)</i>"
    },
    {
        "id": 26, "lesson": 2, "word": "算", "pinyin": "suàn", "meaning": "tính giá cho, tính toán",
        "collocations": [
            "算你 13 块 (suàn nǐ shísān kuài) — tính bạn 13 tệ",
            "怎么算 (zěnme suàn) — tính thế nào"
        ],
        "example": "订两千米，算你 13 块一米。<br><i>(Dìng liǎng qiān mǐ, suàn nǐ shísān kuài yì mǐ. — Đặt 2.000 mét tính bạn 13 tệ một mét nhé.)</i>"
    },
    {
        "id": 27, "lesson": 2, "word": "现货", "pinyin": "xiànhuò", "meaning": "hàng có sẵn trong kho",
        "collocations": [
            "有现货 (yǒu xiànhuò) — có sẵn hàng",
            "现货充足 (xiànhuò chōngzú) — hàng sẵn dồi dào",
            "查现货 (chá xiànhuò) — kiểm tra hàng sẵn"
        ],
        "example": "请问这款面料有现货吗？<br><i>(Qǐngwèn zhè kuǎn miànliào yǒu xiànhuò ma? — Cho hỏi mẫu vải này có sẵn hàng không?)</i>"
    },
    {
        "id": 28, "lesson": 2, "word": "定织", "pinyin": "dìngzhī", "meaning": "đặt dệt theo yêu cầu",
        "collocations": [
            "定织面料 (dìngzhī miànliào) — vải đặt dệt riêng",
            "安排定织 (ānpái dìngzhī) — sắp xếp đặt dệt"
        ],
        "example": "如果没有现货，可以定织吗？<br><i>(Rúguǒ méiyǒu xiànhuò, kěyǐ dìngzhī ma? — Nếu không có hàng sẵn, có thể đặt dệt riêng không?)</i>"
    },
    {
        "id": 29, "lesson": 2, "word": "定染", "pinyin": "dìngrǎn", "meaning": "đặt nhuộm màu riêng",
        "collocations": [
            "定染颜色 (dìngrǎn yánsè) — đặt nhuộm màu sắc",
            "定染起订量 (dìngrǎn qǐdìngliàng) — MOQ đặt nhuộm"
        ],
        "example": "这个粉红色需要定染吗？<br><i>(Zhè ge fěnhóngsè xūyào dìngrǎn ma? — Màu hồng phấn này có cần phải đặt nhuộm không?)</i>"
    },
    {
        "id": 30, "lesson": 2, "word": "起订量", "pinyin": "qǐdìngliàng", "meaning": "lượng đặt tối thiểu (MOQ)",
        "collocations": [
            "最低起订量 (zuìdī qǐdìngliàng) — MOQ tối thiểu",
            "现货起订量 (xiànhuò qǐdìngliàng) — MOQ hàng sẵn"
        ],
        "example": "定织定染的最低起订量是多少？<br><i>(Dìngzhī dìngrǎn de zuìdī qǐdìngliàng shì duōshao? — Lượng đặt tối thiểu khi đặt dệt hoặc đặt nhuộm là bao nhiêu?)</i>"
    }
]

# ==========================================
# 3. QUẢN LÝ SESSION STATE
# ==========================================
if "learned_ids" not in st.session_state:
    st.session_state.learned_ids = set()
if "failed_ids" not in st.session_state:
    st.session_state.failed_ids = set()
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0

# State cho Trắc nghiệm (1 nút Tiếp theo duy nhất)
if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []
if "quiz_active_idx" not in st.session_state:
    st.session_state.quiz_active_idx = 0
if "quiz_last_feedback" not in st.session_state:
    st.session_state.quiz_last_feedback = None

# State cho Nối từ 2 cột tương tác
if "match_cards_left" not in st.session_state:
    st.session_state.match_cards_left = []
if "match_cards_right" not in st.session_state:
    st.session_state.match_cards_right = []
if "matched_ids" not in st.session_state:
    st.session_state.matched_ids = set()
if "selected_left_id" not in st.session_state:
    st.session_state.selected_left_id = None
if "selected_right_id" not in st.session_state:
    st.session_state.selected_right_id = None
if "match_error_msg" not in st.session_state:
    st.session_state.match_error_msg = ""

# ==========================================
# 4. TIÊU ĐỀ & ĐIỀU HƯỚNG
# ==========================================
st.markdown("<div class='app-title'>🌸 Ôn Tập Từ Vựng - Thiên Trang</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Hệ thống Flashcard & Phản xạ từ vựng Tiếng Trung Dệt May (Bài 1 & Bài 2)</div>", unsafe_allow_html=True)

col_scope, col_mode = st.columns([1, 1.45])
with col_scope:
    scope_choice = st.selectbox(
        "📚 Chọn bài học:",
        ["Tất cả (Bài 1 & 2 - 30 từ)", "Bài 1: Công ty & Năng lực xưởng (20 từ)", "Bài 2: Đơn giá, Hàng sẵn & MOQ (10 từ)"],
        index=0
    )
with col_mode:
    mode_choice = st.radio(
        "🎯 Chế độ:",
        ["Thẻ Flashcard", "Trắc nghiệm", "Nối từ 2 cột", "Mục lục từ vựng", "Tiến độ"],
        horizontal=True
    )

# Lọc danh sách từ theo bài học
if "Bài 1" in scope_choice:
    current_vocab = [w for w in VOCAB_DATA if w["lesson"] == 1]
elif "Bài 2" in scope_choice:
    current_vocab = [w for w in VOCAB_DATA if w["lesson"] == 2]
else:
    current_vocab = VOCAB_DATA

total_words = len(current_vocab)
scope_ids = {w["id"] for w in current_vocab}
learned_count = len(st.session_state.learned_ids.intersection(scope_ids))
failed_count = len(st.session_state.failed_ids.intersection(scope_ids))
pct = int((learned_count / total_words) * 100) if total_words > 0 else 0

st.markdown(f"""
<div style='background:linear-gradient(90deg, #FDF5F8 0%, #F9F3F7 100%); padding:9px 18px; border-radius:15px; border:1px solid #F3DAE4; margin-bottom:16px; font-size:13.5px; color:#5C1E3F;'>
    ✨ <b>Tiến độ học tập:</b> Đã thuộc: <b>{learned_count}/{total_words}</b> ({pct}%) • Cần ôn lại: <b>{failed_count}</b> từ
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. CHI TIẾT CÁC CHẾ ĐỘ ÔN TẬP
# ==========================================

# --- 1. THẺ FLASHCARD ---
if mode_choice == "Thẻ Flashcard":
    if st.session_state.card_idx >= total_words:
        st.session_state.card_idx = 0

    col_nav1, col_nav2 = st.columns([2, 1])
    with col_nav1:
        st.caption(f"Thẻ số: **{st.session_state.card_idx + 1} / {total_words}**")
    with col_nav2:
        if st.button("🎲 Xáo ngẫu nhiên", use_container_width=True):
            st.session_state.card_idx = random.randint(0, total_words - 1)
            st.rerun()

    cur_word = current_vocab[st.session_state.card_idx]
    colloc_html = "".join([f"<div class='colloc-item'>🌸 {c}</div>" for c in cur_word["collocations"]])

    flashcard_html = f"""
    <div class="flashcard-wrapper">
        <label>
            <input type="checkbox" class="flashcard-toggle" id="card_{cur_word['id']}_{st.session_state.card_idx}">
            <div class="flashcard-inner">
                <!-- MẶT TRƯỚC -->
                <div class="flashcard-face flashcard-front">
                    <span class="badge-pill">BÀI {cur_word['lesson']} • TỪ #{cur_word['id']}</span>
                    <div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                        <div class="chinese-word">{cur_word['word']}</div>
                        <div class="pinyin-word">{cur_word['pinyin']}</div>
                    </div>
                    <div style="color: #8C4368; font-size: 13px; font-weight: 500;">👆 <b>Chạm thẻ để lật xem nghĩa & ví dụ</b></div>
                </div>
                <!-- MẶT SAU -->
                <div class="flashcard-face flashcard-back">
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:baseline;">
                            <div>
                                <span style="font-size:25px; color:#5C1E3F; font-weight:700;">{cur_word['word']}</span>
                                <span style="font-size:18px; color:#9D4E84; margin-left:8px; font-weight:700;">{cur_word['pinyin']}</span>
                            </div>
                            <span class="badge-pill">BÀI {cur_word['lesson']}</span>
                        </div>
                        <div style="color:#059669; font-weight:700; font-size:18px; margin:6px 0 10px 0;">👉 {cur_word['meaning']}</div>
                        <div style="font-size:12px; font-weight:700; color:#5C1E3F; margin-bottom:4px;">CỤM TỪ KẾT HỢP (KÈM PINYIN):</div>
                        {colloc_html}
                        <div class="example-box">💬 <b>Ví dụ:</b><br>{cur_word['example']}</div>
                    </div>
                    <div style="color: #8C4368; font-size: 12.5px; text-align: center; margin-top:6px;">👆 <b>Chạm lại để lật về chữ Hán</b></div>
                </div>
            </div>
        </label>
    </div>
    """
    st.markdown(flashcard_html, unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🌸 Đã nhớ", type="primary", use_container_width=True):
            st.session_state.learned_ids.add(cur_word["id"])
            st.session_state.failed_ids.discard(cur_word["id"])
            st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
            st.rerun()
    with b2:
        if st.button("⚡ Chưa thuộc", use_container_width=True):
            st.session_state.failed_ids.add(cur_word["id"])
            st.session_state.learned_ids.discard(cur_word["id"])
            st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
            st.rerun()
    with b3:
        if st.button("⏭️ Tiếp theo", use_container_width=True):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
            st.rerun()

# --- 2. TRẮC NGHIỆM (CHỈ CẦN NÚT TIẾP THEO) ---
elif mode_choice == "Trắc nghiệm":
    st.markdown("##### ✍️ Trắc nghiệm chọn nghĩa đúng của từ")
    
    if len(st.session_state.quiz_list) == 0 or st.button("🎲 Bắt đầu bài kiểm tra 10 câu mới"):
        sample_size = min(10, len(current_vocab))
        sampled = random.sample(current_vocab, sample_size)
        new_quiz = []
        for item in sampled:
            wrong_pool = [w["meaning"] for w in VOCAB_DATA if w["id"] != item["id"]]
            distractors = random.sample(wrong_pool, 3)
            options = distractors + [item["meaning"]]
            random.shuffle(options)
            new_quiz.append({
                "id": item["id"],
                "word": item["word"],
                "pinyin": item["pinyin"],
                "correct": item["meaning"],
                "options": options
            })
        st.session_state.quiz_list = new_quiz
        st.session_state.quiz_active_idx = 0
        st.session_state.quiz_last_feedback = None
        st.rerun()

    total_q = len(st.session_state.quiz_list)
    cur_q_idx = st.session_state.quiz_active_idx

    if cur_q_idx >= total_q:
        st.balloons()
        st.success(f"🎉 **Chúc mừng bạn đã hoàn thành trọn vẹn {total_q} câu hỏi trắc nghiệm!**")
        if st.button("🔄 Làm bài trắc nghiệm mới", type="primary", use_container_width=True):
            st.session_state.quiz_list = []
            st.rerun()
    else:
        q_item = st.session_state.quiz_list[cur_q_idx]
        st.caption(f"Câu hỏi: **{cur_q_idx + 1} / {total_q}**")
        st.progress((cur_q_idx) / total_q)

        # Hiển thị thông báo phản hồi của câu vừa trả lời (nếu có)
        if st.session_state.quiz_last_feedback:
            fb = st.session_state.quiz_last_feedback
            if fb["is_correct"]:
                st.markdown(f"<div style='background:#ECFDF5; border:1px solid #A7F3D0; color:#065F46; padding:10px 14px; border-radius:12px; margin-bottom:12px; font-size:14px;'>✓ <b>Chính xác!</b> Câu trước ({fb['word']}): <b>{fb['correct']}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#FEF2F2; border:1px solid #FECACA; color:#991B1B; padding:10px 14px; border-radius:12px; margin-bottom:12px; font-size:14px;'>❌ <b>Chưa chính xác!</b> Câu trước ({fb['word']}) nghĩa là: <b>{fb['correct']}</b> (Bạn đã chọn: <i>{fb['user_choice']}</i>)</div>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"""
            <h2 style="color:#5C1E3F; margin-bottom:2px;">{q_item['word']} <span style="font-size:20px; color:#9D4E84; font-weight:normal;">({q_item['pinyin']})</span></h2>
            <p style="color:#4B5563; font-size:14.5px; margin-bottom:14px;">👉 Hãy chọn nghĩa tiếng Việt phù hợp nhất:</p>
            """, unsafe_allow_html=True)

            selected_answer = st.radio("Chọn đáp án:", q_item["options"], key=f"quiz_radio_{cur_q_idx}")

            # Nút duy nhất: Bấm Tiếp theo là tự động kiểm tra và chuyển tiếp
            next_label = "Tiếp theo ➡️" if (cur_q_idx + 1 < total_q) else "🏁 Hoàn thành bài trắc nghiệm"
            if st.button(next_label, type="primary", use_container_width=True):
                is_correct = (selected_answer == q_item["correct"])
                if is_correct:
                    st.session_state.learned_ids.add(q_item["id"])
                    st.session_state.failed_ids.discard(q_item["id"])
                else:
                    st.session_state.failed_ids.add(q_item["id"])

                st.session_state.quiz_last_feedback = {
                    "word": q_item["word"],
                    "correct": q_item["correct"],
                    "user_choice": selected_answer,
                    "is_correct": is_correct
                }
                st.session_state.quiz_active_idx += 1
                st.rerun()

# --- 3. NỐI TỪ 2 CỘT TƯƠNG TÁC (CHỮ HÁN & NGHĨA) ---
elif mode_choice == "Nối từ 2 cột":
    st.markdown("##### 🧩 Trò chơi Nối từ 2 Cột (Chạm từ tiếng Trung ➔ Chạm nghĩa tiếng Việt)")
    st.caption("💡 Cách chơi: Bấm chọn 1 từ bên Cột Trái, sau đó bấm chọn nghĩa tương ứng bên Cột Phải. Nếu sai sẽ báo đỏ, nếu đúng sẽ đổi màu xanh và khóa lại!")

    # Khởi tạo 5 cặp từ mới nếu chưa có hoặc khi bấm đổi
    if len(st.session_state.match_cards_left) == 0 or st.button("🎲 Đổi 5 cặp từ mới"):
        sample_size = min(5, len(current_vocab))
        sampled = random.sample(current_vocab, sample_size)
        
        left_items = [{"id": s["id"], "word": s["word"], "pinyin": s["pinyin"]} for s in sampled]
        right_items = [{"id": s["id"], "meaning": s["meaning"]} for s in sampled]
        
        random.shuffle(left_items)
        random.shuffle(right_items)
        
        st.session_state.match_cards_left = left_items
        st.session_state.match_cards_right = right_items
        st.session_state.matched_ids = set()
        st.session_state.selected_left_id = None
        st.session_state.selected_right_id = None
        st.session_state.match_error_msg = ""
        st.rerun()

    # Kiểm tra nếu hoàn thành đủ 5 cặp
    if len(st.session_state.matched_ids) == len(st.session_state.match_cards_left) and len(st.session_state.match_cards_left) > 0:
        st.balloons()
        st.success("🎉 **Tuyệt vời! Bạn đã ghép chính xác toàn bộ các cặp từ!**")
        if st.button("🎲 Chơi tiếp 5 cặp khác", type="primary", use_container_width=True):
            st.session_state.match_cards_left = []
            st.rerun()
    else:
        if st.session_state.match_error_msg:
            st.markdown(f"<div style='background:#FEF2F2; color:#991B1B; border:1px solid #FECACA; padding:9px 15px; border-radius:12px; margin-bottom:14px; font-size:13.5px;'>{st.session_state.match_error_msg}</div>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        # CỘT TRÁI: CHỮ HÁN + PINYIN
        with col_left:
            st.markdown("<p style='font-weight:700; color:#5C1E3F; text-align:center; font-size:15px; margin-bottom:8px;'>🇨🇳 CỘT TỪ TIẾNG TRUNG</p>", unsafe_allow_html=True)
            for item in st.session_state.match_cards_left:
                item_id = item["id"]
                label_text = f"{item['word']}  ({item['pinyin']})"
                
                # Trạng thái ô
                if item_id in st.session_state.matched_ids:
                    st.button(f"✓ {label_text}", key=f"matched_l_{item_id}", disabled=True, use_container_width=True)
                else:
                    is_selected = (st.session_state.selected_left_id == item_id)
                    btn_type = "primary" if is_selected else "secondary"
                    btn_label = f"👉 {label_text}" if is_selected else label_text
                    
                    if st.button(btn_label, key=f"btn_l_{item_id}", type=btn_type, use_container_width=True):
                        st.session_state.selected_left_id = item_id
                        st.session_state.match_error_msg = ""
                        
                        # Nếu bên phải đã được chọn trước đó -> thực hiện so khớp
                        if st.session_state.selected_right_id is not None:
                            if st.session_state.selected_left_id == st.session_state.selected_right_id:
                                st.session_state.matched_ids.add(item_id)
                                st.session_state.learned_ids.add(item_id)
                                st.session_state.selected_left_id = None
                                st.session_state.selected_right_id = None
                            else:
                                st.session_state.match_error_msg = "❌ Cặp từ ghép chưa chính xác, hãy thử lại nhé!"
                                st.session_state.selected_left_id = None
                                st.session_state.selected_right_id = None
                        st.rerun()

        # CỘT PHẢI: NGHĨA TIẾNG VIỆT
        with col_right:
            st.markdown("<p style='font-weight:700; color:#5C1E3F; text-align:center; font-size:15px; margin-bottom:8px;'>🇻🇳 CỘT NGHĨA TIẾNG VIỆT</p>", unsafe_allow_html=True)
            for item in st.session_state.match_cards_right:
                item_id = item["id"]
                label_text = item["meaning"]
                
                # Trạng thái ô
                if item_id in st.session_state.matched_ids:
                    st.button(f"✓ {label_text}", key=f"matched_r_{item_id}", disabled=True, use_container_width=True)
                else:
                    is_selected = (st.session_state.selected_right_id == item_id)
                    btn_type = "primary" if is_selected else "secondary"
                    btn_label = f"👉 {label_text}" if is_selected else label_text
                    
                    if st.button(btn_label, key=f"btn_r_{item_id}", type=btn_type, use_container_width=True):
                        st.session_state.selected_right_id = item_id
                        st.session_state.match_error_msg = ""
                        
                        # Nếu bên trái đã được chọn trước đó -> thực hiện so khớp
                        if st.session_state.selected_left_id is not None:
                            if st.session_state.selected_left_id == st.session_state.selected_right_id:
                                st.session_state.matched_ids.add(item_id)
                                st.session_state.learned_ids.add(item_id)
                                st.session_state.selected_left_id = None
                                st.session_state.selected_right_id = None
                            else:
                                st.session_state.match_error_msg = "❌ Cặp từ ghép chưa chính xác, hãy thử lại nhé!"
                                st.session_state.selected_left_id = None
                                st.session_state.selected_right_id = None
                        st.rerun()

# --- 4. MỤC LỤC TỪ VỰNG CHI TIẾT (CÓ PINYIN ĐẦY ĐỦ) ---
elif mode_choice == "Mục lục từ vựng":
    st.markdown("##### 📖 Tra cứu nhanh từ vựng dệt may (Kèm Pinyin cụm & ví dụ)")
    search_q = st.text_input("🔍 Tìm kiếm từ vựng:", placeholder="Nhập Hán tự, Pinyin hoặc Tiếng Việt...")
    
    filtered = current_vocab
    if search_q:
        q = search_q.strip().lower()
        filtered = [w for w in current_vocab if q in w["word"].lower() or q in w["pinyin"].lower() or q in w["meaning"].lower()]

    st.caption(f"Hiển thị **{len(filtered)}** từ vựng:")
    for w in filtered:
        collocs_str = "".join([f"<div class='colloc-item'>🌸 {c}</div>" for c in w["collocations"]])
        card_html = f"""
        <div class="vocab-card">
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <span style="font-size:24px; font-weight:700; color:#5C1E3F;">{w['word']} <span style="font-size:16px; color:#9D4E84; font-weight:700;">{w['pinyin']}</span></span>
                <span class="badge-pill">BÀI {w['lesson']} • #{w['id']}</span>
            </div>
            <div style="color:#059669; font-weight:700; font-size:16px; margin:4px 0 8px 0;">👉 {w['meaning']}</div>
            <div style="font-size:12px; font-weight:700; color:#5C1E3F; margin-bottom:4px;">CỤM TỪ KẾT HỢP (KÈM PINYIN):</div>
            {collocs_str}
            <div class="example-box">💬 <b>Ví dụ:</b><br>{w['example']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# --- 5. TIẾN ĐỘ ---
elif mode_choice == "Tiến độ":
    st.markdown("##### 📊 Theo dõi tiến độ học tập")
    st.info("Hệ thống tự động ghi nhớ các từ bạn đã thuộc trong phiên học hiện tại.")
    st.markdown(f"- 🌸 Tổng số từ đã thuộc: **{len(st.session_state.learned_ids)}** từ")
    st.markdown(f"- ⚡ Số từ cần ôn lại: **{len(st.session_state.failed_ids)}** từ")
    if st.button("Xóa tiến độ và ôn lại từ đầu"):
        st.session_state.learned_ids = set()
        st.session_state.failed_ids = set()
        st.rerun()
