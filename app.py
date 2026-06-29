import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://recommendation-system-4jbu.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (Futuristic & Premium Cyberpunk Theme)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800;900&display=swap');

/* Main Streamlit App Overrides */
.stApp {
    background: radial-gradient(circle at 50% 50%, #0d0f22 0%, #05060a 100%) !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Block container adjustments */
.block-container { 
    padding-top: 1.5rem !important; 
    padding-bottom: 3rem !important; 
    max-width: 1400px !important; 
}

/* Titles and Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

/* Custom logo branding class */
.brand-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0, 240, 255, 0.25);
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
    text-align: center;
}

.brand-subtitle {
    color: #8b92b6;
    font-size: 0.95rem;
    letter-spacing: 0.5px;
    margin-bottom: 2rem;
    text-align: center;
}

/* Glassmorphic elements */
.movie-details-card {
    background: rgba(18, 22, 45, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(6, 182, 212, 0.2) !important;
    border-radius: 24px !important;
    padding: 28px !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5) !important;
    margin-bottom: 1.5rem;
    transition: border-color 0.3s ease;
}

.movie-details-card:hover {
    border-color: rgba(6, 182, 212, 0.4) !important;
}

/* Movie poster on details page */
.movie-details-poster {
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6) !important;
    transition: transform 0.4s ease !important;
}
.movie-details-poster:hover {
    transform: scale(1.01) translateY(-2px) !important;
}

/* Cinematic backdrop hero style */
.backdrop-hero {
    position: relative;
    height: 380px;
    border-radius: 24px;
    background-size: cover;
    background-position: center 25%;
    margin-bottom: 2rem;
    overflow: hidden;
    border: 1px solid rgba(6, 182, 212, 0.25);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
}
.backdrop-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, rgba(5, 6, 10, 0.1) 20%, rgba(5, 6, 10, 0.95) 100%);
}

/* Movie card column container styling */
.movie-grid-wrapper div[data-testid="column"] {
    background: rgba(18, 22, 40, 0.45) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.12) !important;
    border-radius: 18px !important;
    padding: 12px !important;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    margin-bottom: 1.5rem !important;
}

.movie-grid-wrapper div[data-testid="column"]:hover {
    transform: translateY(-8px) scale(1.03) !important;
    border-color: rgba(236, 72, 153, 0.6) !important;
    box-shadow: 0 12px 28px rgba(236, 72, 153, 0.25), 0 0 15px rgba(0, 240, 255, 0.25) !important;
}

.movie-grid-wrapper div[data-testid="column"] img {
    border-radius: 12px !important;
    transition: transform 0.3s ease !important;
}

.movie-grid-wrapper div[data-testid="column"]:hover img {
    transform: scale(1.02) !important;
}

/* Neon buttons for action details */
.movie-grid-wrapper div[data-testid="column"] button {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%) !important;
    color: #00f0ff !important;
    border: 1px solid rgba(6, 182, 212, 0.4) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-size: 0.78rem !important;
    margin-top: 10px !important;
    padding: 6px 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
}

.movie-grid-wrapper div[data-testid="column"] button:hover {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.55) 0%, rgba(236, 72, 153, 0.55) 100%) !important;
    color: #ffffff !important;
    border-color: rgba(236, 72, 153, 0.9) !important;
    box-shadow: 0 0 15px rgba(236, 72, 153, 0.45) !important;
    transform: translateY(-1px) !important;
}

/* Movie Titles */
.movie-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    margin-top: 10px !important;
    text-align: center !important;
    height: 2.4rem !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
    line-height: 1.2rem !important;
    transition: color 0.3s ease;
}

.movie-grid-wrapper div[data-testid="column"]:hover .movie-title {
    color: #ffffff !important;
}

/* Genre Badges */
.genre-badge {
    background: rgba(6, 182, 212, 0.12) !important;
    border: 1px solid rgba(6, 182, 212, 0.35) !important;
    color: #00f0ff !important;
    padding: 5px 14px !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    margin-right: 8px !important;
    margin-bottom: 8px !important;
    display: inline-block !important;
    font-family: 'Outfit', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    text-shadow: 0 0 8px rgba(6, 182, 212, 0.4) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}

/* Rating badge */
.rating-badge {
    background: rgba(236, 72, 153, 0.15) !important;
    border: 1px solid rgba(236, 72, 153, 0.45) !important;
    color: #ff007f !important;
    padding: 5px 14px !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    margin-right: 8px !important;
    display: inline-block !important;
    font-family: 'Outfit', sans-serif !important;
    text-shadow: 0 0 8px rgba(236, 72, 153, 0.4) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}

/* Translucent Inputs & Selectboxes styling */
div[data-testid="stTextInput"] input {
    background-color: rgba(18, 22, 40, 0.7) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px 16px !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: rgba(236, 72, 153, 0.7) !important;
    box-shadow: 0 0 15px rgba(236, 72, 153, 0.25), inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] {
    background-color: rgba(18, 22, 40, 0.7) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"]:hover {
    border-color: rgba(6, 182, 212, 0.6) !important;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background: radial-gradient(circle at 100% 0%, #151930 0%, #080911 100%) !important;
    border-right: 1px solid rgba(6, 182, 212, 0.15) !important;
}

section[data-testid="stSidebar"] button {
    background: rgba(6, 182, 212, 0.08) !important;
    color: #00f0ff !important;
    border: 1px solid rgba(6, 182, 212, 0.25) !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}

section[data-testid="stSidebar"] button:hover {
    background: rgba(236, 72, 153, 0.18) !important;
    color: #ffffff !important;
    border-color: rgba(236, 72, 153, 0.5) !important;
    box-shadow: 0 0 10px rgba(236, 72, 153, 0.25) !important;
}

/* Custom styled horizontal rules */
hr {
    border-color: rgba(6, 182, 212, 0.2) !important;
    margin: 2rem 0 !important;
    box-shadow: 0 1px 2px rgba(6, 182, 212, 0.1);
}

/* Details page back button */
.back-btn-container button {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #a0a5c0 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.back-btn-container button:hover {
    border-color: rgba(6, 182, 212, 0.6) !important;
    color: #00f0ff !important;
    box-shadow: 0 0 8px rgba(6, 182, 212, 0.3) !important;
}

/* Placeholder for missing posters */
.no-poster-placeholder {
    height: 270px;
    background: rgba(255, 255, 255, 0.03);
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6b7280;
    font-size: 0.95rem;
    font-family: 'Outfit', sans-serif;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    st.markdown('<div class="movie-grid-wrapper">', unsafe_allow_html=True)
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown('<div class="no-poster-placeholder">🖼️ No Poster</div>', unsafe_allow_html=True)

                if st.button("View Details ⚡", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )
    st.markdown('</div>', unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            # might be {tmdb_id,title,poster_url}
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR (clean)
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### 🏠 Home Feed (only home)")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.markdown(
    """
    <div class="brand-logo">🎬 CINE-MATRIX</div>
    <div class="brand-subtitle">Quantum Movie Recommendation Engine</div>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title (keyword)", placeholder="Type: avenger, batman, love..."
    )

    st.divider()

    # SEARCH MODE (Autocomplete + word-match results)
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Dropdown
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        # map label -> id
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown("### Results")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    st.markdown(f"### 🏠 Home — {home_category.replace('_',' ').title()}")

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    a, b = st.columns([3, 1])
    with a:
        st.markdown("### 📄 Database Profile")
    with b:
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Back to Home"):
            goto_home()
        st.markdown('</div>', unsafe_allow_html=True)

    # Details (your FastAPI safe route)
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Large panoramic hero backdrop at the top
    if data.get("backdrop_url"):
        st.markdown(
            f"""
            <div class="backdrop-hero" style="background-image: url('{data["backdrop_url"]}');">
                <div class="backdrop-overlay"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.2], gap="large")

    with left:
        if data.get("poster_url"):
            st.markdown(
                f"""
                <img src="{data["poster_url"]}" class="movie-details-poster" style="width: 100%;" />
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="no-poster-placeholder">🖼️ No Poster</div>', unsafe_allow_html=True)

    with right:
        st.markdown("<div class='movie-details-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2>{data.get('title','')}</h2>", unsafe_allow_html=True)
        
        # Build badges / indicators
        release = data.get("release_date") or ""
        year = release[:4] if len(release) >= 4 else "N/A"
        
        badges_html = []
        if data.get("vote_average"):
            badges_html.append(f"<span class='rating-badge'>⭐ {data['vote_average']:.1f}/10</span>")
        badges_html.append(f"<span class='genre-badge'>📅 {year}</span>")
        
        for g in data.get("genres", []):
            badges_html.append(f"<span class='genre-badge'>{g['name']}</span>")
            
        badges_str = "".join(badges_html)
        st.markdown(f"<div style='margin: 1rem 0;'>{badges_str}</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 1.5rem 0 !important;'>", unsafe_allow_html=True)
        st.markdown("<h3>Overview</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='line-height: 1.6rem; color: #d1d5db; font-size: 1.05rem;'>{data.get('overview') or 'No overview available.'}</p>", 
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### ✅ Recommendations")

    # Recommendations (TF-IDF + Genre) via your bundle endpoint
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown("#### 🔎 Similar Movies (TF-IDF)")
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown("#### 🎭 More Like This (Genre)")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")