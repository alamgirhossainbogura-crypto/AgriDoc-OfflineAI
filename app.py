import streamlit as st
from llama_cpp import Llama

# ১. পেজ কনফিগারেশন এবং স্টাইলিং
st.set_page_config(page_title="AgriDoc-OfflineAI", page_icon="🌾", layout="wide")

# সিএসএস দিয়ে নিচের NB সতর্কবার্তা এবং বাটনগুলোর লুক প্রফেশনাল করা
st.markdown("""
    <style>
    .disclaimer-box {
        padding: 15px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        color: #856404;
        font-weight: bold;
        margin-top: 50px;
    }
    .main-title {
        text-align: center;
        color: #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# ২. ১০টি আফ্রিকান ফসলের কমপ্লিট অফলাইন নলেজ বেস
CROP_DATABASE = {
    "Cassava": {
        "guide": "Thrives in well-drained sandy loam soil with a pH of 5.5-6.5. Plant healthy stem cuttings (20-30cm long) at a 45-degree angle. Space plants 1m x 1m apart. Highly drought-resistant once established.",
        "disease": "Cassava Mosaic Disease (CMD). Transmitted by whiteflies (Bemisia tabaci) and infected cuttings. Causes yellow/green mosaic patterns on leaves, leaf distortion, and severe stunting of the plant.",
        "remedy": "Strictly plant disease-resistant varieties (e.g., TMS series). Uproot and burn infected plants immediately upon detection. Practice strict weed control to reduce whitefly habitats."
    },
    "Maize (Corn)": {
        "guide": "Requires deep, fertile, well-drained loamy soil rich in organic matter. Plant seeds 3-5 cm deep with 25 cm spacing within rows and 75 cm between rows. Requires heavy nitrogen input and constant watering during flowering.",
        "disease": "Fall Armyworm (FAW) Infestation. Caused by Spodoptera frugiperda larvae. The caterpillars burrow into the whorl, feeding on young leaves and destroying the growing core of the plant.",
        "remedy": "Practice early planting at the start of the rainy season. Handpick and destroy visible caterpillars. Apply organic Neem seed oil spray or intercrop with pest-repellent plants like Desmodium.",
        "treatment": "Early planting, handpick caterpillars, or use organic Neem oil spray locally."
    },
    "Yam": {
        "guide": "Demands deep, loose, fertile, and well-drained soils. Plant seed yams in large mounds or ridges spaced 1m apart. Requires strong staking (2-3m poles) shortly after sprouting to support climbing vines.",
        "disease": "Yam Anthracnose. A fungal infection caused by Colletotrichum gloeosporioides. Manifests as dark brown or black lesions along leaf veins and vines, leading to leaf drop and vine dieback.",
        "remedy": "Select clean, lesion-free seed yams for planting. Implement a strict 3-year crop rotation cycle. Clear fields of plant debris after harvest to reduce fungal spore survival."
    },
    "Sorghum": {
        "guide": "Highly adaptable to low-rainfall zones. Prepare a fine seedbed; sow seeds 2-3 cm deep in rows spaced 60-75 cm apart. Requires minimal fertilization compared to maize.",
        "disease": "Sorghum Ergot. Caused by Claviceps africana fungus. A sticky, sweet fluid (honeydew) oozes from infected flowers, which later transforms into hard, dark fungal masses (sclerotia).",
        "remedy": "Always use certified, clean seeds. Practice deep plowing after harvest to bury fungal residues. Rotate crops with non-cereal plants to break the pathogen lifecycle."
    },
    "Rice": {
        "guide": "Best suited for heavy clayey loam soils that retain water well. For lowland rice, maintain a shallow water depth of 5-10 cm throughout the early vegetative growth stages. Space seedlings 20 cm x 20 cm.",
        "disease": "Rice Blast. A destructive fungal disease caused by Magnaporthe oryzae. Produces diamond-shaped/spindle lesions on leaves with gray centers and rots the neck node, causing lodging.",
        "remedy": "Avoid excessive nitrogen fertilizers which encourage fungal growth. Use blast-resistant crop lines. Keep the fields properly flooded to suppress spore germination."
    },
    "Cowpea": {
        "guide": "Thrives in poor, sandy soils where other crops struggle. Acts as a nitrogen-fixing crop. Sow seeds directly at a depth of 2.5-5 cm after the peak heavy rains subside.",
        "disease": "Cowpea Aphid-borne Mosaic Virus (CABMV). Transmitted by aphids. Causes intense green/yellow leaf mottling, severe leaf curling, distortion, and significant pod reduction.",
        "remedy": "Control the vector aphids early using local soapy water sprays. Promptly rogue (uproot) and destroy infected plants. Plant dense rows early to prevent aphid landing."
    },
    "Millet": {
        "guide": "Extremely drought-tolerant. Sows directly in shallow, sandy soils of low fertility. Requires minimal soil preparation and very low rainfall to complete its lifecycle.",
        "disease": "Downy Mildew (Green Ear). Fungal infection where leaves turn chlorotic (yellow/white) with white downy growth underneath, and the grain spike converts into a twisted green leafy structure.",
        "remedy": "Uproot and bury infected plants before spores mature. Practice deep seed treatment and rotate fields with non-cereal crops every alternate year."
    },
    "Sweet Potato": {
        "guide": "Propagated via healthy vine cuttings (30cm long). Plant cuttings on raised soil ridges or mounds to allow optimal tuber expansion. Prefers loose, sandy loam structures.",
        "disease": "Sweet Potato Weevil. Caused by Cylas formicarius. Adult weevils and grubs tunnel through the vines and tubers, depositing waste that makes the potatoes bitter and toxic.",
        "remedy": "Use clean, weevil-free vine cuttings taken from the tips. High earthing-up of soil around the roots prevents adult weevils from accessing tubers. Practice strict crop rotation."
    },
    "Plantain": {
        "guide": "Requires deep, rich, organic, alluvial soils with excellent drainage. Apply heavy organic mulch around the base to retain moisture. Needs protection from strong winds.",
        "disease": "Black Sigatoka (Black Leaf Streak). Air-borne fungal disease causing dark necrotic streaks on leaves, leading to large dead leaf areas and reduced fruit weight.",
        "remedy": "De-leaf infected areas regularly to reduce spore load. Maintain wide spacing (2.5m x 2.5m) to ensure air circulation and reduce humidity within the canopy."
    },
    "Groundnut": {
        "guide": "Requires light, loose sandy loam soil so that the flower pegs can easily penetrate the ground to form pods. Sow in sunny areas with moderate, evenly distributed rainfall.",
        "disease": "Groundnut Rosette Disease. A viral complex spread by aphids. Causes severe plant stunting, leaf chlorosis, and a bushy appearance, preventing pod development.",
        "remedy": "Plant early in the season at a high seed density to form a closed canopy that deters aphids. Uproot infected clusters immediately upon spotting."
    }
}

# ৩. লোকাল অফলাইন এআই মডেল লোডার (মেমোরি সেভিং ক্যাশ সহ)
@st.cache_resource
def load_local_model():
    try:
        return Llama(
            model_path="./models/phi-3-mini-4k-instruct.Q4_K_M.gguf",
            n_ctx=2048,
            n_threads=4, # CPU Threads for standard i5/Ryzen 5
            verbose=False
        )
    except Exception as e:
        return None

llm = load_local_model()

# ৪. সেশন স্টেট হ্যান্ডলিং (পেজ নেভিগেশন ম্যানেজ করার জন্য)
if "current_page" not in os.__dict__ and "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def go_to_page(page_name):
    st.session_state.current_page = page_name

def render_disclaimer():
    st.markdown("""
        <div class="disclaimer-box">
            📌 NB: These guidelines are for primary understanding only. For final and accurate solutions, please consult a professional agricultural specialist or certified officer.
        </div>
    """, unsafe_allow_html=True)

# ৫. ইন্টারফেস আর্কিটেকচার লজিক

# --- হোম পেজ ইন্টারফেস ---
if st.session_state.current_page == "Home":
    st.markdown("<h1 class='main-title'>🌾 AgriDoc: On-Device Agricultural Suite</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>An Offline Expert System Optimized for Commodity Hardware</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        if st.button("🌱 1. Cultivation Guide", use_container_width=True):
            go_to_page("Cultivation")
    with col2:
        if st.button("⚠️ 2. Disease Diagnosis", use_container_width=True):
            go_to_page("Disease")
    with col3:
        if st.button("🛡️ 3. Remedy & Prevention", use_container_width=True):
            go_to_page("Remedy")
    with col4:
        if st.button("🤖 4. AgriDoc AI Assistant", use_container_width=True):
            go_to_page("AI_Assistant")
            
    render_disclaimer()

# --- ১ম ইন্টারফেস: চাষাবাদ পদ্ধতি ---
elif st.session_state.current_page == "Cultivation":
    if st.button("⬅️ Back to Main Menu"):
        go_to_page("Home")
        st.rerun()
        
    st.header("🌱 Interface 1: Cultivation Guide")
    st.write("Select a major African crop to view structured offline cultivation methodologies.")
    
    selected_crop = st.selectbox("Select Crop:", list(CROP_DATABASE.keys()))
    st.info(f"### {selected_crop} Production Guide:\n{CROP_DATABASE[selected_crop]['guide']}")
    
    render_disclaimer()

# --- ২য় ইন্টারফেস: রোগের কারণ ---
elif st.session_state.current_page == "Disease":
    if st.button("⬅️ Back to Main Menu"):
        go_to_page("Home")
        st.rerun()
        
    st.header("⚠️ Interface 2: Disease Diagnosis Matrix")
    st.write("Understand major crop infections, vectors, and why they occur.")
    
    selected_crop = st.selectbox("Select Crop:", list(CROP_DATABASE.keys()))
    st.warning(f"### Major Disease Threat for {selected_crop}:\n{CROP_DATABASE[selected_crop]['disease']}")
    
    render_disclaimer()

# --- ৩য় ইন্টারফেস: রোগের প্রতিকার ---
elif st.session_state.current_page == "Remedy":
    if st.button("⬅️ Back to Main Menu"):
        go_to_page("Home")
        st.rerun()
        
    st.header("🛡️ Interface 3: Remedy & Organic Prevention")
    st.write("Actionable, cost-effective, and offline mitigation guidelines to rescue crops.")
    
    selected_crop = st.selectbox("Select Crop:", list(CROP_DATABASE.keys()))
    st.success(f"### Actionable Remedy / Control Measures:\n{CROP_DATABASE[selected_crop]['remedy']}")
    
    render_disclaimer()

# --- ৪র্থ ইন্টারফেস: এআই অ্যাসিস্ট্যান্ট ---
elif st.session_state.current_page == "AI_Assistant":
    if st.button("⬅️ Back to Main Menu"):
        go_to_page("Home")
        st.rerun()
        
    st.header("🤖 Interface 4: AgriDoc Offline AI Assistant")
    st.write("Powered by an on-device Small Language Model (SLM) executing 100% locally on your CPU.")
    
    if llm is None:
        st.error("Model weights file not detected inside `./models/` folder. Please check your setup or download the GGUF model.")
    else:
        st.success("On-Device LLM Status: Ready (Phi-3-mini 4-bit Quantized)")
        
        target_crop = st.selectbox("Select Target Context Crop:", list(CROP_DATABASE.keys()))
        user_query = st.text_input(f"Ask anything about {target_crop} issues:", placeholder="e.g., Explain how to spot or manage its major disease?")
        
        if user_query:
            with st.spinner("Processing local inference (Allocating CPU Threads)..."):
                # রিয়েল-টাইম লোকাল RAG কনটেক্সট বিল্ডিং
                context = f"Crop: {target_crop}\nCultivation: {CROP_DATABASE[target_crop]['guide']}\nDisease: {CROP_DATABASE[target_crop]['disease']}\nRemedy: {CROP_DATABASE[target_crop]['remedy']}"
                
                system_prompt = (
                    "You are AgriDoc AI, an expert agricultural offline assistant. Use the provided context data to answer the user's question accurately. "
                    "Keep answers brief, bulleted, and localized. Do not hallucinate. If unknown, say you don't know."
                )
                
                prompt = f"<|system|>\n{system_prompt}\n<|user|>\nContext:\n{context}\n\nQuestion: {user_query}<|end|>\n<|assistant|>\n"
                
                # ইনফারেন্স প্যারামিটার অপ্টিমাইজেশন (থার্মাল ও র‍্যাম বাজেট কন্ট্রোল)
                output = llm(
                    prompt,
                    max_tokens=200,
                    temperature=0.1,
                    stop=["<|end|>"]
                )
                
                response_text = output['choices'][0]['text'].strip()
                st.chat_message("assistant").write(response_text)
                
    render_disclaimer()
