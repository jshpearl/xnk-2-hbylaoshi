import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Ôn Tập Từ Vựng Dệt May - Thiên Trang",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Nhúng CSS màu Pastel nhẹ nhàng và Script JavaScript phát âm tiếng Trung
st.markdown("""
<style>
    /* Font & Background tổng thể */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF2F6 100%);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Nút nghe phát âm */
    .audio-btn {
        background-color: #E0E7FF;
        color: #4338CA;
        border: none;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        transition: all 0.2s ease;
    }
    .audio-btn:hover {
        background-color: #C7D2FE;
        transform: scale(1.03);
    }

    /* Thẻ Flashcard lật 3D */
    .flashcard-wrapper {
        perspective: 1000px;
        margin: 15px auto;
        max-width: 580px;
        cursor: pointer;
    }
    .flashcard-toggle {
        display: none;
    }
    .flashcard-inner {
        position: relative;
        width: 100%;
        min-height: 320px;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
        border-radius: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    }
    .flashcard-toggle:checked + .flashcard-inner {
        transform: rotateY(180deg);
    }
    .flashcard-face {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 24px;
        padding: 30px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1.5px solid #E2E8F0;
    }
    .flashcard-front {
        align-items: center;
        text-align: center;
    }
    .flashcard-back {
        transform: rotateY(180deg);
        background: #FAF5FF;
        border-color: #E9D5FF;
    }
    .chinese-word {
        font-size: 48px;
        color: #1E293B;
        margin: 10px 0 5px 0;
        font-weight: 700;
    }
    .pinyin-word {
        font-size: 22px;
        color: #6366F1;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .colloc-item {
        background: #FFFFFF;
        padding: 6px 12px;
        border-radius: 10px;
        margin-bottom: 6px;
        font-size: 13.5px;
        color: #334155;
        border: 1px solid #E2E8F0;
    }
    .example-box {
        background: #F1F5F9;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 13px;
        color: #475569;
        margin-top: 10px;
    }

    /* Khung danh mục từ */
    .vocab-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }
</style>

<script>
// Hàm JavaScript kích hoạt giọng đọc chuẩn tiếng Trung (zh-CN) của trình duyệt
function speakText(text, event) {
    if (event) event.stopPropagation();
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        utterance.rate = 0.85; // Tốc độ đọc vừa phải cho học viên
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Trình duyệt không hỗ trợ Web Speech API.");
    }
}
</script>
""", unsafe_allow_html=True)

# ==========================================
# 2. DỮ LIỆU TỔNG HỢP 30 TỪ VỰNG CHUẨN
# ==========================================
VOCAB_DATA = [
    # --- BÀI 1: GIỚI THIỆU CÔNG TY & QUY MÔ (20 TỪ) ---
    {"id": 1, "lesson": 1, "word": "公司", "pinyin": "gōngsī", "meaning": "công ty", "collocations": ["台资公司 (công ty Đài Loan)", "总公司 (công ty mẹ)", "分公司 (chi nhánh)"], "example": "我们是一家专业的纺织公司。(Chúng tôi là một công ty dệt may chuyên nghiệp.)"},
    {"id": 2, "lesson": 1, "word": "台资", "pinyin": "táizī", "meaning": "vốn Đài Loan", "collocations": ["台资企业 (doanh nghiệp Đài Loan)", "台资独资 (100% vốn Đài)"], "example": "我们公司是台资企业。(Công ty chúng tôi là doanh nghiệp có vốn Đài Loan.)"},
    {"id": 3, "lesson": 1, "word": "成立", "pinyin": "chénglì", "meaning": "thành lập", "collocations": ["成立于……年 (thành lập năm...)", "正式成立 (chính thức thành lập)"], "example": "我们公司成立于 2015 年。(Công ty chúng tôi được thành lập vào năm 2015.)"},
    {"id": 4, "lesson": 1, "word": "规模", "pinyin": "guīmó", "meaning": "quy mô", "collocations": ["企业规模 (quy mô doanh nghiệp)", "规模很大 (quy mô rất lớn)"], "example": "工厂规模很大。(Quy mô nhà xưởng rất lớn.)"},
    {"id": 5, "lesson": 1, "word": "员工", "pinyin": "yuángōng", "meaning": "nhân viên, công nhân", "collocations": ["公司员工 (nhân viên công ty)", "员工人数 (số lượng nhân viên)"], "example": "现有 500 名员工。(Hiện tại có 500 nhân viên.)"},
    {"id": 6, "lesson": 1, "word": "生产", "pinyin": "shēngchǎn", "meaning": "sản xuất", "collocations": ["生产面料 (sản xuất vải)", "投入生产 (đưa vào sản xuất)"], "example": "工厂专门生产针织面料。(Nhà máy chuyên sản xuất vải dệt kim.)"},
    {"id": 7, "lesson": 1, "word": "经营", "pinyin": "jīngyíng", "meaning": "kinh doanh", "collocations": ["主要经营 (chủ yếu kinh doanh)", "经营范围 (phạm vi kinh doanh)"], "example": "主要经营高档运动面料。(Chuyên kinh doanh vải thể thao cao cấp.)"},
    {"id": 8, "lesson": 1, "word": "业务", "pinyin": "yèwù", "meaning": "nghiệp vụ, kinh doanh", "collocations": ["进出口业务 (nghiệp vụ XNK)", "开展业务 (triển khai nghiệp vụ)"], "example": "我们负责纺织品进出口业务。(Chúng tôi phụ trách nghiệp vụ xuất nhập khẩu dệt may.)"},
    {"id": 9, "lesson": 1, "word": "产品", "pinyin": "chǎnpǐn", "meaning": "sản phẩm", "collocations": ["新产品 (sản phẩm mới)", "产品目录 (catalogue sản phẩm)"], "example": "请发一份产品目录给我。(Xin vui lòng gửi cho tôi một bản catalogue sản phẩm.)"},
    {"id": 10, "lesson": 1, "word": "主打", "pinyin": "zhǔdǎ", "meaning": "chủ lực, bán chạy", "collocations": ["主打产品 (sản phẩm chủ lực)", "主打面料 (vải chủ lực)"], "example": "这是我们工厂的主打产品。(Đây là dòng sản phẩm chủ lực của nhà máy chúng tôi.)"},
    {"id": 11, "lesson": 1, "word": "面料", "pinyin": "miànliào", "meaning": "vải", "collocations": ["针织面料 (vải dệt kim)", "运动面料 (vải thể thao)"], "example": "这款面料手感非常好。(Mẫu vải này sờ bề mặt rất êm tay.)"},
    {"id": 12, "lesson": 1, "word": "材质", "pinyin": "cáizhì", "meaning": "chất liệu", "collocations": ["面料材质 (chất liệu vải)", "环保材质 (chất liệu thân thiện MT)"], "example": "这款面料的材质是什么？(Chất liệu của mẫu vải này là gì?)"},
    {"id": 13, "lesson": 1, "word": "纯棉", "pinyin": "chúnmián", "meaning": "100% cotton", "collocations": ["纯棉布 (vải cotton)", "100% 纯棉 (100% cotton)"], "example": "它是 100% 纯棉的。(Nó là vải 100% cotton.)"},
    {"id": 14, "lesson": 1, "word": "规格", "pinyin": "guīgé", "meaning": "quy cách, thông số", "collocations": ["确认规格 (xác nhận quy cách)", "产品规格 (quy cách sản phẩm)"], "example": "我们需要确认具体的面料规格。(Chúng tôi cần xác nhận thông số kỹ thuật vải cụ thể.)"},
    {"id": 15, "lesson": 1, "word": "货号", "pinyin": "huòhào", "meaning": "mã hàng", "collocations": ["面料货号 (mã vải)", "查货号 (tra mã hàng)"], "example": "请问这款布的货号是多少？(Xin hỏi mã hàng của mẫu vải này là bao nhiêu?)"},
    {"id": 16, "lesson": 1, "word": "工厂", "pinyin": "gōngchǎng", "meaning": "nhà máy, nhà xưởng", "collocations": ["参观工厂 (thăm nhà máy)", "工厂地址 (địa chỉ xưởng)"], "example": "欢迎来到我们工厂参观！(Chào mừng các bạn đến tham quan nhà máy chúng tôi!)"},
    {"id": 17, "lesson": 1, "word": "车间", "pinyin": "chējiān", "meaning": "phân xưởng sản xuất", "collocations": ["生产车间 (phân xưởng sản xuất)", "织造车间 (xưởng dệt)"], "example": "欢迎来车间参观。(Hoan nghênh các bạn ghé thăm phân xưởng.)"},
    {"id": 18, "lesson": 1, "word": "产能", "pinyin": "chǎnnéng", "meaning": "công suất, năng lực sản xuất", "collocations": ["月产能 (công suất tháng)", "产能充足 (công suất dồi dào)"], "example": "工厂每个月的产能非常充足。(Công suất hàng tháng của nhà máy rất dồi dào.)"},
    {"id": 19, "lesson": 1, "word": "出口", "pinyin": "chūkǒu", "meaning": "xuất khẩu", "collocations": ["出口到欧美 (xuất sang Âu Mỹ)", "出口市场 (thị trường XK)"], "example": "产品主要出口到欧美。(Sản phẩm chủ yếu xuất khẩu sang Âu Mỹ.)"},
    {"id": 20, "lesson": 1, "word": "欢迎", "pinyin": "huānyíng", "meaning": "chào đón, hoan nghênh", "collocations": ["欢迎来访 (chào mừng đến thăm)", "欢迎来厂 (chào mừng tới xưởng)"], "example": "欢迎各位领导莅临指导！(Nhiệt liệt hoan nghênh các vị lãnh đạo tới thăm!)"},

    # --- BÀI 2: HỎI ĐƠN GIÁ, HÀNG SẴN & MOQ (10 TỪ) ---
    {"id": 21, "lesson": 2, "word": "经理", "pinyin": "jīnglǐ", "meaning": "giám đốc, quản lý", "collocations": ["陈经理 (Giám đốc Trần)", "李经理 (Giám đốc Lý)"], "example": "陈经理，您好！(Chào Giám đốc Trần!)"},
    {"id": 22, "lesson": 2, "word": "单价", "pinyin": "dānjià", "meaning": "đơn giá", "collocations": ["面料单价 (đơn giá vải)", "确认单价 (xác nhận đơn giá)"], "example": "这款布的单价是多少？(Đơn giá của mẫu vải này là bao nhiêu?)"},
    {"id": 23, "lesson": 2, "word": "多少钱", "pinyin": "duōshao qián", "meaning": "bao nhiêu tiền", "collocations": ["一米多少钱 (bao nhiêu tiền 1 mét)", "这个多少钱 (cái này bao nhiêu tiền)"], "example": "请问针织布一米多少钱？(Cho hỏi vải dệt kim một mét bao nhiêu tiền?)"},
    {"id": 24, "lesson": 2, "word": "米", "pinyin": "mǐ", "meaning": "mét (đo vải)", "collocations": ["两千米 (2.000 mét)", "要多少米 (cần bao nhiêu mét)"], "example": "我们先订两千米。(Chúng tôi đặt trước 2.000 mét.)"},
    {"id": 25, "lesson": 2, "word": "优惠", "pinyin": "yōuhuì", "meaning": "ưu đãi, bớt giá", "collocations": ["价格优惠 (ưu đãi về giá)", "优惠一点 (bớt chút giá)"], "example": "订单量大，价格能优惠一点吗？(Đơn hàng lớn, giá có thể ưu đãi thêm chút không?)"},
    {"id": 26, "lesson": 2, "word": "算", "pinyin": "suàn", "meaning": "tính giá cho, tính toán", "collocations": ["算你 13 块 (tính bạn 13 tệ)", "怎么算 (tính thế nào)"], "example": "订两千米，算你 13 块一米。(Đặt 2.000 mét thì tính bạn 13 tệ một mét.)"},
    {"id": 27, "lesson": 2, "word": "现货", "pinyin": "xiànhuò", "meaning": "hàng có sẵn trong kho", "collocations": ["有现货 (có hàng sẵn)", "现货充足 (hàng sẵn dồi dào)"], "example": "请问这款面料有现货吗？(Cho hỏi mẫu vải này có sẵn hàng không?)"},
    {"id": 28, "lesson": 2, "word": "定织", "pinyin": "dìngzhī", "meaning": "đặt dệt theo yêu cầu", "collocations": ["定织面料 (vải đặt dệt riêng)", "安排定织 (sắp xếp đặt dệt)"], "example": "如果没有现货，可以定织吗？(Nếu không có sẵn hàng thì có thể đặt dệt riêng không?)"},
    {"id": 29, "lesson": 2, "word": "定染", "pinyin": "dìngrǎn", "meaning": "đặt nhuộm màu riêng", "collocations": ["定染颜色 (đặt nhuộm màu sắc)", "定染起订量 (MOQ đặt nhuộm)"], "example": "这个颜色需要定染吗？(Tông màu này có cần phải đặt nhuộm riêng không?)"},
    {"id": 30, "lesson": 2, "word": "起订量", "pinyin": "qǐdìngliàng", "meaning": "lượng đặt tối thiểu (MOQ)", "collocations": ["最低起订量 (MOQ tối thiểu)", "现货起订量 (MOQ hàng sẵn)"], "example": "定织定染的最低起订量是多少？(MOQ tối thiểu của đặt dệt đặt nhuộm là bao nhiêu?)"}
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
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []
if "quiz_active_idx" not in st.session_state:
    st.session_state.quiz_active_idx = 0
if "quiz_answered_correctly" not in st.session_state:
    st.session_state.quiz_answered_correctly = False
if "quiz_error_msg" not in st.session_state:
    st.session_state.quiz_error_msg = ""
if "quiz_wrong_attempts" not in st.session_state:
    st.session_state.quiz_wrong_attempts = 0

HISTORY_FILE = "study_history.json"
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(entry):
    hist = load_history()
    hist.insert(0, entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

# ==========================================
# 4. THANH ĐIỀU HƯỚNG & PHẠM VI BÀI HỌC
# ==========================================
st.markdown("<h2 style='text-align:center; color:#1E3A8A; margin-bottom:5px;'>🌸 Ôn Tập Từ Vựng Dệt May</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748B; font-size:14px; margin-bottom:20px;'>Hệ thống Flashcard & Luyện phản xạ từ vựng dành riêng cho Thiên Trang</p>", unsafe_allow_html=True)

col_scope, col_mode = st.columns([1, 2])
with col_scope:
    scope_choice = st.selectbox(
        "📚 Chọn bài học:",
        ["Tất cả (Bài 1 & 2)", "Bài 1: Công ty & Năng lực xưởng", "Bài 2: Đơn giá, Hàng sẵn & MOQ"],
        index=0
    )
with col_mode:
    mode_choice = st.radio(
        "🎯 Chế độ luyện tập:",
        ["Thẻ từ", "Trắc nghiệm", "Nối từ", "Mục lục từ", "Lịch sử"],
        horizontal=True
    )

# Lọc danh sách từ theo bài học
if scope_choice == "Bài 1: Công ty & Năng lực xưởng":
    current_vocab = [w for w in VOCAB_DATA if w["lesson"] == 1]
elif scope_choice == "Bài 2: Đơn giá, Hàng sẵn & MOQ":
    current_vocab = [w for w in VOCAB_DATA if w["lesson"] == 2]
else:
    current_vocab = VOCAB_DATA

total_words = len(current_vocab)
scope_ids = {w["id"] for w in current_vocab}
learned_count = len(st.session_state.learned_ids.intersection(scope_ids))
failed_count = len(st.session_state.failed_ids.intersection(scope_ids))
pct = int((learned_count / total_words) * 100) if total_words > 0 else 0

st.markdown(f"""
<div style='background:#F8FAFC; padding:10px 16px; border-radius:12px; border:1px solid #E2E8F0; margin-bottom:15px; font-size:13.5px;'>
    📊 <b>Tiến độ:</b> Đã thuộc: <b style='color:#10B981;'>{learned_count}/{total_words}</b> ({pct}%) | Cần ôn lại: <b style='color:#EF4444;'>{failed_count}</b> từ
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. CÁC CHẾ ĐỘ LUYỆN TẬP
# ==========================================

# --- CHẾ ĐỘ 1: THẺ TỪ FLASHCARD ---
if mode_choice == "Thẻ từ":
    if st.session_state.card_idx >= total_words:
        st.session_state.card_idx = 0

    col_nav1, col_nav2 = st.columns([1, 3])
    with col_nav1:
        st.caption(f"Thẻ số: **{st.session_state.card_idx + 1} / {total_words}**")
    with col_nav2:
        if st.button("🎲 Xáo thẻ ngẫu nhiên", use_container_width=True):
            st.session_state.card_idx = random.randint(0, total_words - 1)
            st.rerun()

    cur_word = current_vocab[st.session_state.card_idx]
    colloc_html = "".join([f"<div class='colloc-item'>• {c}</div>" for c in cur_word["collocations"]])

    flashcard_html = f"""
    <div class="flashcard-wrapper">
        <label>
            <input type="checkbox" class="flashcard-toggle" id="card_{cur_word['id']}_{st.session_state.card_idx}">
            <div class="flashcard-inner">
                <!-- MẶT TRƯỚC -->
                <div class="flashcard-face flashcard-front">
                    <span style="background:#E0E7FF; color:#4338CA; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700;">BÀI {cur_word['lesson']} • TỪ #{cur_word['id']}</span>
                    <div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                        <div class="chinese-word">{cur_word['word']}</div>
                        <div class="pinyin-word">{cur_word['pinyin']}</div>
                        <button type="button" class="audio-btn" onclick="speakText('{cur_word['word']}', event)">
                            🔊 Nghe phát âm
                        </button>
                    </div>
                    <div style="color: #94A3B8; font-size: 13px;">👆 <b>Chạm thẻ để lật xem nghĩa</b></div>
                </div>
                <!-- MẶT SAU -->
                <div class="flashcard-face flashcard-back">
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <b style="font-size:24px; color:#1E293B;">{cur_word['word']}</b>
                                <span style="font-size:16px; color:#6366F1; margin-left:8px; font-weight:600;">{cur_word['pinyin']}</span>
                            </div>
                            <button type="button" class="audio-btn" onclick="speakText('{cur_word['word']}', event)">
                                🔊 Nghe
                            </button>
                        </div>
                        <div style="color:#059669; font-weight:700; font-size:18px; margin:8px 0 10px 0;">👉 {cur_word['meaning']}</div>
                        <div style="font-size:13px; font-weight:600; color:#475569; margin-bottom:4px;">Cụm từ thông dụng:</div>
                        {colloc_html}
                        <div class="example-box">💬 <b>Ví dụ:</b><br>{cur_word['example']}</div>
                    </div>
                    <div style="color: #94A3B8; font-size: 13px; text-align: center;">👆 <b>Chạm lại để lật về chữ Hán</b></div>
                </div>
            </div>
        </label>
    </div>
    """
    st.markdown(flashcard_html, unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("✓ Đã nhớ", type="primary", use_container_width=True):
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

# --- CHẾ ĐỘ 2: TRẮC NGHIỆM TỪNG CÂU ---
elif mode_choice == "Trắc nghiệm":
    st.markdown("##### ✍️ Trắc nghiệm phản xạ nghĩa của từ")
    
    if len(st.session_state.quiz_list) == 0 or st.button("🎲 Tạo bài trắc nghiệm mới (10 câu)"):
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
        st.session_state.quiz_answered_correctly = False
        st.session_state.quiz_error_msg = ""
        st.session_state.quiz_wrong_attempts = 0
        st.rerun()

    total_q = len(st.session_state.quiz_list)
    cur_q_idx = st.session_state.quiz_active_idx

    if cur_q_idx >= total_q:
        st.balloons()
        st.success(f"🎉 **Chúc mừng bạn đã hoàn thành xuất sắc toàn bộ {total_q} câu hỏi!**")
        if st.button("🔄 Luyện tập lại từ đầu", type="primary", use_container_width=True):
            st.session_state.quiz_list = []
            st.rerun()
    else:
        q_item = st.session_state.quiz_list[cur_q_idx]
        st.caption(f"Câu hỏi: **{cur_q_idx + 1} / {total_q}**")
        st.progress((cur_q_idx) / total_q)

        with st.container(border=True):
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="color:#1E3A8A; margin:0;">{q_item['word']} <span style="font-size:18px; color:#64748B; font-weight:normal;">({q_item['pinyin']})</span></h2>
                <button type="button" class="audio-btn" onclick="speakText('{q_item['word']}', event)">
                    🔊 Nghe
                </button>
            </div>
            <p style="color:#475569; margin-top:8px; font-size:15px;">👉 Từ trên có nghĩa tiếng Việt là gì?</p>
            """, unsafe_allow_html=True)

            selected_answer = st.radio("Chọn đáp án:", q_item["options"], key=f"quiz_radio_{cur_q_idx}")

            if not st.session_state.quiz_answered_correctly:
                if st.button("Kiểm tra kết quả", type="primary", use_container_width=True):
                    if selected_answer == q_item["correct"]:
                        st.session_state.quiz_answered_correctly = True
                        st.session_state.quiz_error_msg = ""
                        st.session_state.learned_ids.add(q_item["id"])
                        st.rerun()
                    else:
                        st.session_state.quiz_wrong_attempts += 1
                        st.session_state.quiz_error_msg = f"❌ Bạn chọn '{selected_answer}' chưa chính xác. Hãy chọn lại nhé!"
                        st.session_state.failed_ids.add(q_item["id"])
                        st.rerun()

            if st.session_state.quiz_error_msg:
                st.error(st.session_state.quiz_error_msg)

            if st.session_state.quiz_answered_correctly:
                st.success(f"✓ Chính xác! **{q_item['word']}** có nghĩa là: **{q_item['correct']}**")
                next_text = "➡️ Câu tiếp theo" if (cur_q_idx + 1 < total_q) else "🏁 Hoàn thành bài thi"
                if st.button(next_text, type="primary", use_container_width=True):
                    st.session_state.quiz_active_idx += 1
                    st.session_state.quiz_answered_correctly = False
                    st.rerun()

# --- CHẾ ĐỘ 3: NỐI TỪ PHẢN XẠ ---
elif mode_choice == "Nối từ":
    st.markdown("##### 🧩 Trò chơi Nối từ - Nghĩa phản xạ")
    if "match_sample" not in st.session_state or st.button("🎲 Đổi 5 cặp từ mới"):
        st.session_state.match_sample = random.sample(current_vocab, min(5, len(current_vocab)))
        words = [w["word"] for w in st.session_state.match_sample]
        meanings = [w["meaning"] for w in st.session_state.match_sample]
        random.shuffle(words)
        random.shuffle(meanings)
        st.session_state.m_words = words
        st.session_state.m_meanings = meanings
        st.rerun()

    user_match = {}
    with st.form("match_form"):
        for w_text in st.session_state.m_words:
            entry = next(item for item in st.session_state.match_sample if item["word"] == w_text)
            st.markdown(f"👉 Từ: <b style='font-size:18px; color:#1E3A8A;'>{w_text}</b> <i>({entry['pinyin']})</i>", unsafe_allow_html=True)
            user_match[w_text] = st.selectbox(
                f"Nghĩa của {w_text}:",
                ["-- Chọn nghĩa phù hợp --"] + st.session_state.m_meanings,
                key=f"match_box_{w_text}",
                label_visibility="collapsed"
            )
            st.write("")

        if st.form_submit_button("Kiểm tra kết quả ghép đôi", type="primary", use_container_width=True):
            score = 0
            for item in st.session_state.match_sample:
                if user_match.get(item["word"]) == item["meaning"]:
                    score += 1
                    st.session_state.learned_ids.add(item["id"])
                else:
                    st.session_state.failed_ids.add(item["id"])
            total_m = len(st.session_state.match_sample)
            st.success(f"Kết quả: Bạn đã ghép đúng **{score}/{total_m}** cặp từ!")

# --- CHẾ ĐỘ 4: MỤC LỤC TỪ VỰNG CHI TIẾT ---
elif mode_choice == "Mục lục từ":
    st.markdown("##### 📖 Tra cứu nhanh từ vựng dệt may")
    search_q = st.text_input("🔍 Tìm kiếm:", placeholder="Nhập Hán tự, Pinyin hoặc Tiếng Việt...")
    
    filtered = current_vocab
    if search_q:
        q = search_q.strip().lower()
        filtered = [w for w in current_vocab if q in w["word"].lower() or q in w["pinyin"].lower() or q in w["meaning"].lower()]

    st.caption(f"Tìm thấy **{len(filtered)}** từ vựng:")
    for w in filtered:
        collocs_str = "".join([f"<div class='colloc-item'>• {c}</div>" for c in w["collocations"]])
        card_html = f"""
        <div class="vocab-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:24px; font-weight:700; color:#1E293B;">{w['word']} <span style="font-size:16px; color:#6366F1; font-weight:600;">{w['pinyin']}</span></span>
                <button type="button" class="audio-btn" onclick="speakText('{w['word']}', event)">
                    🔊 Nghe
                </button>
            </div>
            <div style="color:#059669; font-weight:600; font-size:15px; margin:4px 0 8px 0;">👉 {w['meaning']}</div>
            {collocs_str}
            <div class="example-box">💬 {w['example']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# --- CHẾ ĐỘ 5: LỊCH SỬ ---
elif mode_choice == "Lịch sử":
    st.markdown("##### 📊 Bảng theo dõi tiến độ")
    st.info("Hệ thống tự động ghi nhớ các từ bạn đã đánh dấu **✓ Đã nhớ** hoặc **⚡ Chưa thuộc** trong phiên học hiện tại.")
    st.markdown(f"- Tổng số từ đã thuộc: **{len(st.session_state.learned_ids)}** từ")
    st.markdown(f"- Số từ cần ôn lại: **{len(st.session_state.failed_ids)}** từ")
    if st.button("Xóa tiến độ và ôn lại từ đầu"):
        st.session_state.learned_ids = set()
        st.session_state.failed_ids = set()
        st.rerun()
