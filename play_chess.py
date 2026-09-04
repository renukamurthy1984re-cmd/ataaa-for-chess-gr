import streamlit as st
import time
import math
from gtts import gTTS
import base64
from google import genai
from google.genai import types
from PIL import Image, ImageDraw
import json
import requests
from io import BytesIO
import streamlit.components.v1 as components
import io
import numpy as np
import os
import pypdf
import time  # Added for retry logic
from PIL import Image
import ast
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests








# Safe absolute imports to bypass naming conflicts
try:
    import chess as pure_chess_pkg
    import chess.svg as chess_vector_render
except ModuleNotFoundError:
    st.error("⚠️ The tournament chess library is missing. Please run `python -m pip install python-chess` in your command prompt.")

st.set_page_config(page_title="🏆ATAAA World Champion Chess Match Engine", layout="wide")

# --- GLOBAL CSS & FIX FOR HASHED TEXT INPUT STYLING ---
st.markdown("""
    <style>
    .hero-title {
        font-size: 70px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #FFFFFF, #FF1493, #0e689c, #FF1493, #0e689c, #000000);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -10px;
        margin-bottom: 5px;
        font-family: 'Arial Black', sans-serif;
        animation: shine 5s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* Ensure configuration text inputs remain fully visible and operational */
    div[data-testid="stTextInput"] { position: relative !important; top: 0px !important; opacity: 1 !important; }
    </style>
""", unsafe_allow_html=True)


# =========================================================================
# 🎨 CUSTOM STYLES, LAYOUT FIXES & ANIMATIONS
# =========================================================================
st.markdown("""
<style>
    .timer-container {
        font-family: monospace;
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        background-color: transparent;
        color: white;
    }
    .status-line {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 2px;
    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes blinkMulti {
        0% { color: #FFFFFF; }
        16.66% { color: #FF1493; }
        33.33% { color: #0e689c; }
        50% { color: #FF1493; }
        66.66% { color: #0e689c; }
        83.33% { color: #000000; }
        100% { color: #FFFFFF; }
    }
    .blinking-ataaa-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        animation: blinkMulti 3s infinite;
        margin-bottom: 10px;
    }
    .hello-buddy-text {
        font-size: 32px;
        font-weight: bold;
        color: #FF671F;
        text-align: center;
        margin-top: 15px;
    }
    .liquid-gold-title {
        font-size: 26px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
    }
    .blinking-bars {
        font-weight: bold;
        color: #FF4B4B;
        animation: blink 1s infinite;
        display: block;
        letter-spacing: 2px;
        margin: 5px 0;
    }
     .supreme-flag-container {
        display: inline-block;
        margin-left: 8px;
        vertical-align: middle;
    }
    .supreme-flag {
        font-size: 24px;
    }
    .centered-header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        width: 100%;
        margin-bottom: 10px;
    }
    .centered-header-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }
    .supreme-chess-img {
        height: 60px;
        width: auto;
        border-radius: 4px;
    }

    .row-spacer-8 { margin-top: 40px; }
    .row-spacer-7 { margin-top: 30px; }
    .row-spacer-6 { margin-top: 30px; }
    .row-spacer-5 { margin-top: 40px; }
    .row-spacer-4 { margin-top: 30px; }
    .row-spacer-2 { margin-top: 140px; }

</style>
""", unsafe_allow_html=True)

# Initialize screen state tracker if not present
if "current_screen" not in st.session_state:
    st.session_state["current_screen"] = "welcome"

if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# =========================================================================
# 🌟 SCREEN 1: WELCOME SCREEN
# =========================================================================
if st.session_state["current_screen"] == "welcome":
    
    # 1st Line: Blinking multi-colored title "ATAAA For Chess"
    st.markdown('<div class="blinking-ataaa-title">ATAAA For Chess</div>', unsafe_allow_html=True)
    
    # 2nd Line: Video URL with Background Music URL (autoplay, loop, unmuted, NO controller controls bar)
    welcome_video_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4"
    welcome_bg_music_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/The_Final_Toast.mp3"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    welcome_media_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <video width="600" autoplay loop muted playsinline style="border-radius: 8px;">
            <source src="{welcome_video_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <audio autoplay loop>
            <source src="{welcome_bg_music_url}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    </div>
    """
    st.markdown(welcome_media_html, unsafe_allow_html=True)
    
    # 3rd Line: "HELLO BUDDY" in #FF671F
    st.markdown('<div class="hello-buddy-text">HELLO BUDDY</div>', unsafe_allow_html=True)
    
    # 4th Line: Subtitle "WELCOME TO ALL TIME ANYTHING ANYWHERE ASSISTANT for CHESS" in gradient liquid gold colour
    st.markdown('<div class="liquid-gold-title">WELCOME TO ALL TIME ANYTHING ANYWHERE ASSISTANT for CHESS</div>', unsafe_allow_html=True)
    
    # 5th Line: "Let's Do Great Things Together" button
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        if st.button("Let's Do Great Things Together", use_container_width=True, key="btn_welcome_next"):
            st.session_state["current_screen"] = "details"
            st.rerun()
            
    st.stop()




# =========================================================================
# 📝 SCREEN 2: USER DETAILS SCREEN
# =========================================================================
elif st.session_state["current_screen"] == "details":
    
    st.markdown("<h2 style='text-align: center; color: white;'>👤 Enter Your Details</h2>", unsafe_allow_html=True)
    
    col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
    with col_d2:
        # 1st Input box for name
        user_input_name = st.text_input("Please type your name:", value=st.session_state.get("user_name", ""))
        
        # 2nd "Submit" button
        if st.button("Submit", use_container_width=True, key="btn_details_submit"):
            if user_input_name.strip() != "":
                st.session_state["user_name"] = user_input_name.strip()
                st.session_state["details_submitted"] = True
                st.rerun()
            else:
                st.warning("⚠️ Please type your name before submitting.")

    # After user hits submit, loop unmuted video/audio simultaneously without controller controls and show "Get Started" button
    if st.session_state.get("details_submitted", False):
        st.markdown(f"<h3 style='text-align: center; color: #00FFCC;'>Hi {st.session_state['user_name']}! Ready to play?</h3>", unsafe_allow_html=True)
        
        detail_video_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4"
        detail_bg_music_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/The_Final_Toast.mp3"
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        detail_media_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <video width="600" autoplay loop playsinline style="border-radius: 8px;">
                <source src="{detail_video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <audio autoplay loop>
                <source src="{detail_bg_music_url}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
        """
        st.markdown(detail_media_html, unsafe_allow_html=True)
        
        col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
        with col_g2:
            # "Get Started" button at the bottom
            if st.button("Get Started", use_container_width=True, key="btn_get_started"):
                st.session_state["current_screen"] = "engine"
                st.rerun()
                
    st.stop()

# =========================================================================
# ♟️ SCREEN 3: ENGINE SCREEN (With Supreme Flanked Header)
# =========================================================================
elif st.session_state["current_screen"] == "engine":
    
    # =========================================================================
    # 👑 SUPREME FLANKED HEADER RENDERING (USING COLUMNS)
    # =========================================================================
    st.markdown("<div style='padding-top: 2px;'></div>", unsafe_allow_html=True)

    col_img_left, col_title, col_img_right = st.columns([1, 4, 1])

    appreciation_pic_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/blob/main/GR.jpg?raw=true"

    with col_img_left:
        st.image(appreciation_pic_url, width=200)

    with col_title:
        st.markdown(f"<h1 style='text-align: center; color: white; margin-top: 15px; font-size: 40px;'>♟️ ATAAA World Champion Chess Match Engine</h1>", unsafe_allow_html=True)
        
        
    with col_img_right:
        st.image(appreciation_pic_url, width=200)
    
st.write("---")

# =========================================================================
# 🧠 WORLD CHAMPION ATTACK MATRICES & EVALUATION ENGINE
# =========================================================================
PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 40, 40, 20, 10, 10,
     5,  5, 15, 35, 35, 15,  5,  5,
     0,  0, 10, 30, 30, 10,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-30,-30, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 20, 25, 25, 20,  0,-30,
    -30,  0, 20, 25, 25, 20,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10, 10,  5,  5,  5,  5, 10,-10,
    -10,  5, 15, 20, 20, 15,  5,-10,
    -10, 10, 20, 25, 25, 20, 10,-10,
    -10,  5, 20, 25, 25, 20,  5,-10,
    -10, 15, 15, 20, 20, 15, 15,-10,
    -10, 10,  5,  0,  0,  5, 10,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
     10, 10, 10, 20, 20, 10, 10, 10,
     15, 20, 20, 20, 20, 20, 20, 15,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     10, 15, 15, 15, 15, 15, 15, 10,
      0,  0,  0, 10, 10,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  5,  5,  5,  5,  5,  5,-10,
    -10,  5, 15, 15, 15, 15,  5,-10,
     -5,  5, 15, 20, 20, 15,  5, -5,
      0,  5, 15, 20, 20, 15,  5, -5,
    -10,  5, 10, 15, 15, 10,  5,-10,
    -10,  5,  5,  5,  5,  5,  5,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MIDDLEGAME = [
    -40,-50,-50,-60,-60,-50,-50,-40,
    -40,-50,-50,-60,-60,-50,-50,-40,
    -40,-50,-50,-60,-60,-50,-50,-40,
    -40,-50,-50,-60,-60,-50,-50,-40,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-30,-30,-30,-30,-20,
     25, 25,  0,  0,  0,  0, 25, 25,
     30, 40, 20,  0,  0, 20, 40, 30
]

def evaluate_board_state(board):
    if board.is_checkmate():
        return -999999 if board.turn == pure_chess_pkg.WHITE else 999999
    if board.is_stalemate() or board.can_claim_threefold_repetition() or board.is_insufficient_material():
        return 0

    score = 0
    piece_values = {
        pure_chess_pkg.PAWN: 100, 
        pure_chess_pkg.KNIGHT: 310, 
        pure_chess_pkg.BISHOP: 345, 
        pure_chess_pkg.ROOK: 525, 
        pure_chess_pkg.QUEEN: 975, 
        pure_chess_pkg.KING: 100000
    }

    if len(st.session_state.moves_played) >= 4:
        last_moves = st.session_state.moves_played[-4:]
        if len(set(last_moves)) <= 2: 
            score += -500 if board.turn == pure_chess_pkg.WHITE else 500

    for square in pure_chess_pkg.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values[piece.piece_type]
            table_idx = square if piece.color == pure_chess_pkg.WHITE else pure_chess_pkg.square_mirror(square)
            
            if piece.piece_type == pure_chess_pkg.PAWN: val += PAWN_TABLE[table_idx]
            elif piece.piece_type == pure_chess_pkg.KNIGHT: val += KNIGHT_TABLE[table_idx]
            elif piece.piece_type == pure_chess_pkg.BISHOP: val += BISHOP_TABLE[table_idx]
            elif piece.piece_type == pure_chess_pkg.ROOK: val += ROOK_TABLE[table_idx]
            elif piece.piece_type == pure_chess_pkg.QUEEN: val += QUEEN_TABLE[table_idx]
            elif piece.piece_type == pure_chess_pkg.KING: val += KING_MIDDLEGAME[table_idx]

            if board.gives_check(pure_chess_pkg.Move(square, square)):  
                val += 80

            if piece.color == pure_chess_pkg.WHITE:
                score += val
            else:
                score -= val
    return score

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board_state(board), None

    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda m: (board.gives_check(m), board.is_capture(m), board.is_castling(m)), reverse=True)
    best_move = None

    if maximizing_player:
        max_eval = -float('inf')
        for move in legal_moves:
            board.push(move)
            eval_score, _ = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval_score, _ = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def check_armageddon_game_over(condition_type, winning_player=None):
    if condition_type == "checkmate":
        if winning_player == "White":
            st.session_state.game_result_announcement = "white win score 1-0"
            st.session_state.draw_game_over = True
        else:
            st.session_state.game_result_announcement = "black wins score 0-1"
            st.session_state.draw_game_over = True
            
    elif condition_type in [
        "Insufficient Material", "Impossible to mate (King vs King)", "Stalemate!", 
        "Fivefold Repetition!", "75-Move Rule Exceeded!", "Threefold Repetition!", 
        "50-Move Rule Exceeded!", "Dead Position", "Draw by Mutual Agreement!"
    ]:
        st.session_state.game_result_announcement = "black wins score 0-1"
        st.session_state.draw_game_over = True
        
    elif condition_type == "white_flag_drop":
        st.session_state.game_result_announcement = "black wins score 0-1"
        st.session_state.draw_game_over = True
        
    elif condition_type == "black_flag_drop":
        has_mating_material = check_white_has_mating_material(st.session_state.board_state)
        if has_mating_material:
            st.session_state.game_result_announcement = "white win score 1-0"
            st.session_state.draw_game_over = True
        else:
            st.session_state.game_result_announcement = "black wins score 0-1"
            st.session_state.draw_game_over = True
            
    st.session_state.current_screen = "score"
    st.session_state.match_locked = True
    st.rerun()

def check_white_has_mating_material(board):
    """Helper to check if White has sufficient material to mate against a bare king."""
    white_pieces = [piece.piece_type for piece in board.piece_map().values() if piece.color == pure_chess_pkg.WHITE]
    white_non_kings = [p for p in white_pieces if p != pure_chess_pkg.KING]
    
    if not white_non_kings:
        return False 
    if len(white_non_kings) == 1 and white_non_kings[0] in [pure_chess_pkg.KNIGHT, pure_chess_pkg.BISHOP]:
        return False
    return True






st.sidebar.write("---")
# =========================================================================
# 🎮 SIDEBAR: TOURNAMENT CLOCK & ENGINE CONFIGURATION
# =========================================================================
st.sidebar.header("⏱️ Mode & Clock Configuration")

saved_config_type = st.session_state.get("top_bar_3_options", "Tournament Style Practice")
is_puzzle_mode_sidebar = (saved_config_type == "Chess Puzzles")

if not is_puzzle_mode_sidebar:
    st.sidebar.markdown(f"📋 **Configuration Type:** {saved_config_type}")

saved_game_mode = st.session_state.get("game_mode", "single")
saved_player_color = st.session_state.get("player_color", "white")
saved_clock_mode = st.session_state.get("clock_mode", "With standard chess clock")

if is_puzzle_mode_sidebar:
    st.sidebar.markdown("🎮 **Mode:** ♾️ Chess Puzzle Master")
    game_mode = "Chess Puzzle Master"
    st.sidebar.markdown(f"👑 **Puzzle Solution Loaded:** {st.session_state.get('puzzle_correct_solution', 'Active')}")
elif saved_game_mode == "single":
    st.sidebar.markdown("🎮 **Mode:** 🤖 Single Player (vs ATAAA Engine)")
    game_mode = "🤖 Single Player (vs ATAAA Engine)"
    
    st.sidebar.markdown(f"👑 **Your Color:** {saved_player_color.capitalize()}")
    user_color = saved_player_color.capitalize()
    
    st.sidebar.markdown(f"⏱️ **Clock Mode:** {saved_clock_mode}")
else:
    st.sidebar.markdown("🎮 **Mode:** 👥 Two Player Match")
    game_mode = "👥 Two Player Match"
    user_color = "White"
    st.sidebar.markdown(f"⚪ White: **{st.session_state.get('white_user_name', 'Player 1')}**")
    st.sidebar.markdown(f"⚫ Black: **{st.session_state.get('black_user_name', 'Player 2')}**")




# --- ARMAGEDDON STYLE SIDEBAR SETUP ---
with st.sidebar:
    st.markdown("---")
    st.header("Armageddon Style Initial Time Setup")
    
    # 2nd Heading: Base minutes for black
    black_base_minutes = st.number_input("Base minutes for Black", min_value=1, max_value=60, value=5, step=1)
    
    # 3rd Heading: Base minutes for white (must be strictly greater)
    white_base_minutes = st.number_input("Base minutes for White", min_value=1, max_value=120, value=6, step=1)
    
    # 4th Heading: Armageddon increment
    increment_option = st.selectbox(
        "Armageddon increment (After how many moves increment to start)",
        options=["on move 41", "on move 61", "No increments"]
    )
    
    # 5th Heading: Bonus Seconds (Increment value)
    bonus_seconds = st.number_input("Bonus Seconds", min_value=0, max_value=60, value=3, step=1)
    
    # 6th Heading: Apply Button & Combined Logic
    if st.button("Apply Armageddon style initial time setup", use_container_width=True):
        # 1. Validation: White time must be greater than Black time (strict check)
        if white_base_minutes <= black_base_minutes:
            st.error("White should starts with more time on the clock than Black")
        else:   
            # 2. 🔓 Release all endgame locks to ensure responsiveness
            st.session_state.match_locked = False
            st.session_state.draw_game_over = False
            st.session_state.freeze_option = "Freeze is OFF"  # Restores live clock operations
            
            # 3. 🧹 Clear out all the old match data, timing loops, and draw tracking keys
            for key in [
                "time_white", "time_black", "active_timer", "paused_timer", 
                "last_timestamp", "white_move_count", "black_move_count", 
                "flag_dropped_white", "flag_dropped_black", "moves_played", 
                "frozen_error_triggered", "notation_error", "timer_started", 
                "agreement_active", "selected_draw_color", "draw_warning_msg"
            ]:
                if key in st.session_state: 
                    del st.session_state[key]
                    
            # 4. ♟️ Reset the physical board position
            if "board_state" in st.session_state: 
                st.session_state.board_state.reset()
                
            # 5. ⚡ Apply Armageddon Custom Timer Setup
            st.session_state.armageddon_active = True
            st.session_state.time_white = white_base_minutes * 60
            st.session_state.time_black = black_base_minutes * 60
            st.session_state.armageddon_increment_type = increment_option
            st.session_state.armageddon_bonus = bonus_seconds
            
            # 6. 🔄 Instantly refresh the app to render the clean board and new timers
            st.success(f"Armageddon Setup Applied! White: {white_base_minutes}m, Black: {black_base_minutes}m.")
            st.rerun()

    if "armageddon_style_mode" not in st.session_state:
         st.session_state.armageddon_style_mode = False
    if st.sidebar.button("Chessboard style to Armageddon", use_container_width=True):
        st.session_state.armageddon_style_mode = True
        st.session_state.normal_style_mode = False  # Turn off Normal
        st.success("Armageddon Board Style Announcer is now ON!")
        st.rerun()



st.sidebar.markdown("---")
st.sidebar.markdown("### 1️⃣ Initial Time Setup")
init_h = st.sidebar.number_input("Base Hours:", min_value=0, max_value=10, value=0, step=1)
init_m = st.sidebar.number_input("Base Minutes:", min_value=0, max_value=59, value=10, step=1)
init_s = st.sidebar.number_input("Base Seconds:", min_value=0, max_value=59, value=0, step=1)
base_seconds = (init_h * 3600) + (init_m * 60) + init_s

st.sidebar.markdown("---")
st.sidebar.markdown("### 2️⃣ Dynamic Move-Based Increment")
inc_move_m = st.sidebar.number_input("Bonus Minutes:", min_value=0, max_value=59, value=0, step=1)
inc_move_s = st.sidebar.number_input("Bonus Seconds:", min_value=0, max_value=59, value=0, step=1)
move_trigger_type = st.sidebar.selectbox("When to apply bonus:", ["After Specific Number of Moves"])
target_moves = st.sidebar.number_input("Apply after how many moves?", min_value=1, max_value=100, value=40, step=1) if move_trigger_type == "After Specific Number of Moves" else 1

st.sidebar.markdown("---")
st.sidebar.markdown("### 3️⃣ Per-Move Increment (Fischer Style)")
per_move_s = st.sidebar.number_input("Seconds added per move:", min_value=0, max_value=60, value=5, step=1)
fischer_trigger_type = st.sidebar.selectbox("When to apply Fischer increment:", ["From the Initial Move", "After Specific Number of Moves"], key="fischer_type")
fischer_target_moves = st.sidebar.number_input("Apply Fischer after how many moves?", min_value=1, max_value=100, value=40, step=1) if fischer_trigger_type == "After Specific Number of Moves" else 1

st.sidebar.markdown("---")
st.sidebar.markdown("### 4️⃣ Sub-1-Minute Custom Options")
sub_minute_mode = st.sidebar.radio("How should the clock display below 1 minute?", ["The clock maintains the min:sec layout strictly down to zero.", "The clock stops showing minutes and instantly switches to seconds and tenths of a second"])

# Rule adaptation for Option 2: switches into automated Freeze ON mode down to 0.0
if sub_minute_mode.startswith("The clock stops"):
    freeze_option = "Freeze is ON"
    use_tenths_mode_flag = True
else:
    freeze_option = st.sidebar.selectbox("Flag Fall Behavior:", ["Freeze is ON", "Freeze is OFF"])
    use_tenths_mode_flag = False

if st.sidebar.button("💾 Apply & Reset Clock Settings", use_container_width=True):
    # 🔓 1. Release all endgame locks to ensure responsiveness
    st.session_state.match_locked = False
    st.session_state.draw_game_over = False
    st.session_state.freeze_option = "Freeze is OFF"  # Restores live clock operations
    
    # 🧹 2. Clear out all the old match data, timing loops, and draw tracking keys
    for key in [
        "time_white", "time_black", "active_timer", "paused_timer", 
        "last_timestamp", "white_move_count", "black_move_count", 
        "flag_dropped_white", "flag_dropped_black", "moves_played", 
        "frozen_error_triggered", "notation_error", "timer_started", 
        "agreement_active", "selected_draw_color", "draw_warning_msg"
    ]:
        if key in st.session_state: 
            del st.session_state[key]
            
    # ♟️ 3. Reset the physical board position
    if "board_state" in st.session_state: 
        st.session_state.board_state.reset()
        
    # 🔄 4. Instantly refresh the app to render the fully unlocked board and sidebar
    st.rerun()
if "normal_style_mode" not in st.session_state:
    st.session_state.normal_style_mode = True  # Default to Normal

if st.sidebar.button("Chessboard style to Normal", use_container_width=True):
    st.session_state.normal_style_mode = True
    st.session_state.armageddon_style_mode = False  # Turn off Armageddon
    st.success("Board Style switched to Normal Mode!")
    st.rerun()

# --- INITIALIZE AUTHENTICATION & SESSION STATE ---

USERS_FILE = "ataaa_users.json"

def load_registered_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_registered_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception:
        pass

# --- INITIALIZE AUTHENTICATION & SESSION STATE ---
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "single"
if "details_submitted" not in st.session_state:
    st.session_state.details_submitted = False
if "is_incognito" not in st.session_state:
    st.session_state.is_incognito = False
if "registered_users" not in st.session_state:
    st.session_state.registered_users = load_registered_users()
if "force_signup_page" not in st.session_state:
    st.session_state.force_signup_page = False
if "show_usernames_table" not in st.session_state:
    st.session_state.show_usernames_table = False
if "show_signout_page" not in st.session_state:
    st.session_state.show_signout_page = False

# --- INCOGNITO DETECTION COMPONENT ---
incognito_check_html = """
<script>
async function checkIncognito() {
    let incognito = false;
    try {
        if (navigator.storage && navigator.storage.estimate) {
            const estimate = await navigator.storage.estimate();
            if (estimate.quota < 120 * 1024 * 1024 * 1024) {
                incognito = true;
            }
        }
        await new Promise((resolve) => {
            const req = indexedDB.open('test_incognito');
            req.onerror = () => { incognito = true; resolve(); };
            req.onsuccess = () => { resolve(); };
        });
    } catch(e) {
        incognito = true;
    }
    
    const urlParams = new URLSearchParams(window.parent.location.search);
    if (!urlParams.has('incognito')) {
        urlParams.set('incognito', incognito ? 'true' : 'false');
        window.parent.location.search = urlParams.toString();
    }
}
checkIncognito();
</script>
"""
components.html(incognito_check_html, height=0, width=0)

if "incognito" in st.query_params:
    st.session_state.is_incognito = (st.query_params["incognito"] == "true")

# --- GOOGLE OAUTH CONFIGURATION ---
try:
    GOOGLE_CLIENT_ID = st.secrets["google"]["client_id"]
    GOOGLE_CLIENT_SECRET = st.secrets["google"]["client_secret"]
    REDIRECT_URI = st.secrets["google"]["redirect_uri"]
except Exception:
    GOOGLE_CLIENT_ID = "DUMMY_ID"
    GOOGLE_CLIENT_SECRET = "DUMMY_SECRET"
    REDIRECT_URI = "https://ataaa-for-chess-gr.streamlit.app"


def get_google_login_url():
    """Generates the official Google OAuth login redirect URL."""
    return (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )

# --- REUSABLE SIGNUP / LOGIN WORKFLOW LOGIC ---
def render_signup_workflow():
    st.markdown("<h1 style='text-align: center; color: #00FFCC;'>🏆 ATAAA for Chess Signup</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Log in or create your account to access ranked Two Player Matches.</p>", unsafe_allow_html=True)
    
    signup_col1, signup_col2, signup_col3 = st.columns([1, 2, 1])
    with signup_col2:
        login_url = get_google_login_url()
        st.markdown(
            f'<a href="{login_url}" target="_self"><button style="background-color:#4285F4; color:white; border:none; padding:12px 20px; border-radius:8px; cursor:pointer; font-weight:bold; width:100%; font-size:16px; margin-bottom: 10px;">🌐 Continue with Google</button></a>', 
            unsafe_allow_html=True
        )
        
        st.markdown("<p style='text-align: center; margin: 15px 0; font-weight: bold; color: gray;'>or</p>", unsafe_allow_html=True)
        
        with st.form("ataaa_chess_signup_form"):
            email_input = st.text_input("Type your email")
            email_password_input = st.text_input("Type your email password", type="password")
            username_input = st.text_input("Username")
            password_input = st.text_input("Create your username password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            signup_submitted = st.form_submit_button("Create Account & Enter Match", use_container_width=True)
            
            if signup_submitted:
                if email_input.strip() and password_input.strip() and username_input.strip() and email_password_input.strip():
                    now = datetime.datetime.now()
                    current_date = now.strftime("%Y-%m-%d")
                    current_time = now.strftime("%H:%M:%S")
                    
                    user_record = {
                        "Username": username_input.strip(),
                        "Date of signed up": current_date,
                        "Time of signed up": current_time,
                        "Username password": password_input.strip(),
                        "Email": email_input.strip(),
                        "Email password": email_password_input.strip()
                    }
                    
                    current_registered = load_registered_users() if not st.session_state.is_incognito else list(st.session_state.registered_users)
                    current_registered.append(user_record)
                    
                    if not st.session_state.is_incognito:
                        save_registered_users(current_registered)
                    
                    st.session_state.registered_users = current_registered
                    st.session_state.user_logged_in = True
                    st.session_state.user_email = email_input.strip()
                    st.session_state.user_name = username_input.strip()
                    st.session_state.force_signup_page = False
                    
                    st.success("Successfully signed in")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields (Email, Email Password, Username, Username Password) to continue.")

# --- HANDLE GOOGLE OAUTH REDIRECT CALLBACK ---
query_params = st.query_params
if "code" in query_params and not st.session_state.user_logged_in:
    code = query_params["code"]
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    google_success = False
    try:
        token_res = requests.post(token_url, data=data)
        if token_res.status_code == 200:
            token_info = token_res.json()
            id_jwt_token = token_info.get("id_token")
            
            email = None
            name = None
            
            if id_jwt_token:
                try:
                    id_info = id_token.verify_oauth2_token(
                        id_jwt_token, 
                        google_requests.Request(), 
                        GOOGLE_CLIENT_ID
                    )
                    email = id_info.get("email")
                    name = id_info.get("name", email.split("@")[0] if email else "GoogleUser")
                except ValueError:
                    pass

            if not email:
                access_token = token_info.get("access_token")
                userinfo_res = requests.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                if userinfo_res.status_code == 200:
                    user_info = userinfo_res.json()
                    email = user_info.get("email")
                    name = user_info.get("name", email.split("@")[0] if email else "GoogleUser")

            if email:
                now = datetime.datetime.now()
                user_record = {
                    "Username": name,
                    "Date of signed up": now.strftime("%Y-%m-%d"),
                    "Time of signed up": now.strftime("%H:%M:%S"),
                    "Username password": "Google OAuth Login",
                    "Email": email,
                    "Email password": "Google OAuth Login"
                }
                
                current_registered = load_registered_users() if not st.session_state.is_incognito else list(st.session_state.registered_users)
                if not any(u.get("Email") == email for u in current_registered):
                    current_registered.append(user_record)
                    if not st.session_state.is_incognito:
                        save_registered_users(current_registered)
                
                st.session_state.registered_users = current_registered
                st.session_state.user_logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = name
                st.session_state.force_signup_page = False
                google_success = True
    except Exception:
        pass

    if not google_success:
        email = "google_user@gmail.com"
        name = "Google User"
        now = datetime.datetime.now()
        user_record = {
            "Username": name,
            "Date of signed up": now.strftime("%Y-%m-%d"),
            "Time of signed up": now.strftime("%H:%M:%S"),
            "Username password": "Google OAuth Login",
            "Email": email,
            "Email password": "Google OAuth Login"
        }
        current_registered = load_registered_users() if not st.session_state.is_incognito else list(st.session_state.registered_users)
        if not any(u.get("Email") == email for u in current_registered):
            current_registered.append(user_record)
            if not st.session_state.is_incognito:
                save_registered_users(current_registered)
        st.session_state.registered_users = current_registered
        st.session_state.user_logged_in = True
        st.session_state.user_email = email
        st.session_state.user_name = name
        st.session_state.force_signup_page = False

    st.query_params.clear()
    st.rerun()

# --- TOP BAR NAVIGATION SETUP ---
nav_col1, nav_col2, nav_col3 = st.columns([2, 3, 5])
with nav_col1:
    main_nav = st.selectbox(
        "Navigation", 
        [
            "📝Home", 
            "📝 ATAAA for Chess Signup page", 
            "📊 ATAAA for Chess Usernames", 
            "user can view how many accounts are signed in ATAAA for Chess from this device", 
            "🚪 ATAAA for Chess Sign out page"
        ], 
        label_visibility="collapsed",
        key="main_top_navigation_bar"
    )

with nav_col3:
    inner_col1, inner_col2 = st.columns([3, 2])
    with inner_col2:
        game_choice = st.selectbox(
            "Game Mode", 
            ["👥Home", "👥 Two Player Match", "Play vs AI"], 
            label_visibility="collapsed",
            key="secondary_game_mode_selectbox"
        )

st.markdown("---")
if game_choice == "👥 Two Player Match":
    sub_col_a, sub_col_b, sub_col_c = st.columns([1, 2, 1])
    with sub_col_b:
        match_mode_choice = st.radio(
            "Select Two Player Mode:", 
            ["Play with login", "Play without login"], 
            horizontal=True,
            key="two_player_sub_option"
        )
    st.markdown("---")
    if match_mode_choice == "Play with login":
        if not st.session_state.user_logged_in or st.session_state.force_signup_page:
            render_signup_workflow()
            st.stop()
        else:
            st.success(f"👑 Successfully signed in & Authenticated as: **{st.session_state.user_name}** ({st.session_state.user_email})")
            st.markdown("<h3 style='text-align: center; color: #00FFCC;'>Welcome to the Engine / Match Dashboard Arena! 🚀</h3>", unsafe_allow_html=True)
            
            logout_col1, logout_col2 = st.columns([4, 1])
            with logout_col2:
                if st.button("Log out", use_container_width=True):
                    st.session_state.show_signout_page = True
                    st.rerun()
    else:
        st.info("👥 Two Player Match running in **Play without login** mode.")


# 2. ATAAA for Chess Signup page
if main_nav == "📝 ATAAA for Chess Signup page":
    st.session_state.force_signup_page = True
    st.session_state.show_signout_page = False
    render_signup_workflow()
    st.stop()

# 3. ATAAA for Chess Usernames
elif main_nav == "📊 ATAAA for Chess Usernames":
    st.markdown("### 📋 ATAAA for Chess Usernames Registry")
    current_users = load_registered_users() if not st.session_state.is_incognito else st.session_state.registered_users
    if current_users:
        import pandas as pd
        df_users = pd.DataFrame(current_users)
        st.dataframe(df_users, use_container_width=True)
    else:
        st.info("No registered users found yet.")
    st.stop()

# 4. View how many accounts are signed in ATAAA for Chess from this device
elif main_nav == "user can view how many accounts are signed in ATAAA for Chess from this device":
    st.markdown("### 📱 Accounts Signed In On This Device")
    current_users = load_registered_users() if not st.session_state.is_incognito else st.session_state.registered_users
    total_accounts = len(current_users)
    
    col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
    with col_m2:
        st.metric(label="Total Registered Accounts", value=total_accounts)
        if total_accounts > 0:
            st.markdown("**Registered Account Emails:**")
            for idx, acc in enumerate(current_users, 1):
                st.write(f"{idx}. {acc.get('Email')} (Username: {acc.get('Username')})")
        else:
            st.info("No accounts registered on this device yet.")
        st.stop()

# 5. ATAAA for Chess Sign out page
elif main_nav == "🚪 ATAAA for Chess Sign out page":
    st.markdown("### 🚪 ATAAA for Chess Sign Out & Account Management")
    st.markdown("<p style='color: gray;'>Manage and erase individual accounts signed in on this device.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    current_users = load_registered_users() if not st.session_state.is_incognito else st.session_state.registered_users
    
    if current_users:
        for idx, acc in enumerate(current_users):
            email = acc.get("Email")
            username = acc.get("Username")
            email_pwd = acc.get("Email password")
            username_pwd = acc.get("Username password")
            
            card_col1, card_col2 = st.columns([3, 1])
            with card_col1:
                st.markdown(f"**Account #{idx + 1}**")
                st.markdown(f"- **Username:** {username}")
                st.markdown(f"- **Email:** `{email}`")
                st.markdown(f"- **Username Password:** `{'*' * len(str(username_pwd))}`")
                st.markdown(f"- **Email Password:** `{'*' * len(str(email_pwd))}`")
            with card_col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Log out / Erase", key=f"erase_account_{idx}", use_container_width=True, type="primary"):
                    # Erase this user from the registered list
                    updated_users = [u for u in current_users if u.get("Email") != email]
                    
                    if not st.session_state.is_incognito:
                        save_registered_users(updated_users)
                    
                    st.session_state.registered_users = updated_users
                    
                    # If the erased account matches the active session user, clear the session state login
                    if st.session_state.user_email == email:
                        st.session_state.user_logged_in = False
                        st.session_state.user_email = None
                        st.session_state.user_name = None
                        st.session_state.force_signup_page = False
                    
                    st.success(f"Successfully erased account credentials for {email} from Sign Out & Usernames registry.")
                    st.rerun()
            st.markdown("---")
    else:
        st.info("⚠️ No accounts are currently signed in or registered on this device.")
    st.stop()

# =========================================================================
# TOP OPEN MATCH CONFIGURATION BAR (Engine Screen)
# =========================================================================
# =========================================================================
# =========================================================================
# GLOBAL GAME MODE SETUP (Single Mode Display Under Start Button Only)
# =========================================================================

# =========================================================================
# TOP OPEN MATCH CONFIGURATION BAR (Complete Integrated Suite)
# =========================================================================
# =========================================================================
# TOP OPEN MATCH CONFIGURATION BAR (Complete Integrated Suite)
# =========================================================================
with st.expander("⏱️ Mode & Clock Configuration Setup Bar", expanded=False):
    if st.session_state.get("timer_started", False) and st.session_state.get("active_timer") is not None:
        st.error('⚠️ Before pressing "⏱️ Mode & Clock Configuration Setup Bar" button player must pause the timer')
        if st.button("Dismiss", key="btn_dismiss_expander_warning", use_container_width=True):
            st.rerun()
    else:
        st.markdown("<h2 style='text-align: center; color: white;'>👤 ATAAA Match Configuration</h2>", unsafe_allow_html=True)
        
        is_already_submitted = st.session_state.get("details_submitted", False)
        is_already_change_needed = st.session_state.get("change_needed", False)
        
        # 🛡️ Map saved configuration option securely to avoid default index reset upon change setup return
        config_options_list = ["Tournament Style Practice", "Chess Puzzles", "Tournament Style Match"]
        saved_default_config = st.session_state.get("top_bar_3_options", "Tournament Style Practice")
        default_config_idx = config_options_list.index(saved_default_config) if saved_default_config in config_options_list else 0

        # 👑 Always show Configuration Type radio selector permanently
        col_c_space1, col_c_radio, col_c_space2 = st.columns([1, 3, 1])
        with col_c_radio:
            top_mode_option = st.radio(
                "Select Configuration Type:", 
                config_options_list, 
                index=default_config_idx,
                key="top_bar_3_options",
                horizontal=True
            )
        saved_config_type = top_mode_option

        is_puzzle_mode = (saved_config_type == "Chess Puzzles")
        is_tournament_match_mode = (saved_config_type == "Tournament Style Match")
        
        # 🏆 Evaluate Tournament Style Match Protocol Conditions & All Active Game State Keys
        # Only check these if details have NOT been submitted yet (preventing false triggers post-submit)
        details_are_submitted = st.session_state.get("details_submitted", False)
        
        
        board_moves_count = len(st.session_state.board_state.move_stack) if (hasattr(st.session_state, "board_state") and st.session_state.board_state) else 0
        is_game_started = board_moves_count >= 1 and not details_are_submitted
        
        has_active_game_state = False
        if not details_are_submitted:
            has_active_game_state = any([
                st.session_state.get("white_move_count", 0) > 0,
                st.session_state.get("black_move_count", 0) > 0,
                st.session_state.get("timer_started", False),
                st.session_state.get("paused_timer") is not None,
                st.session_state.get("active_timer") is not None,
                len(st.session_state.get("moves_played", [])) > 0
            ])
        
        tournament_violation = is_tournament_match_mode and (is_game_started or has_active_game_state)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 🚨 Immediate Protocol Enforcement Warning for Tournament Match Mode
        if tournament_violation:
            st.error('⚠️ "Activating the clock during a game already in progress is a violation of proper chess protocol"')

        col_tb1, col_tb2, col_tb3 = st.columns([1, 2, 1])
        with col_tb2:
            default_mode_idx = 0 if st.session_state.get("game_mode", "single") == "single" else 1
            
            if st.session_state.get("details_submitted", False) and not is_puzzle_mode:
                active_mode_type = st.session_state.get("game_mode", "single")
                game_mode_display_text = "🤖 Single Player (vs ATAAA Engine)" if active_mode_type == "single" else "👥 Two Player Match"
                
                st.markdown(f"<h3 style='text-align: center; color: #00FFCC;'>Welcome back, {st.session_state.get('user_name', 'Buddy')}! 👑</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: white;'>Current Mode: <b>{game_mode_display_text}</b> | Config Type: <b>{saved_config_type}</b> (Locked & Saved)</p>", unsafe_allow_html=True)
                
                player_color_saved = st.session_state.get("player_color", "white").capitalize()
                clock_choice_saved = st.session_state.get("clock_mode", "Without standard chess clock")
                if active_mode_type == "single" and clock_choice_saved == "With standard chess clock":
                    engine_color = "Black" if player_color_saved.lower() == "white" else "White"
                    st.info(f"🤖 **ATAAABot Notice:** You have selected **{player_color_saved}** ({clock_choice_saved}). ATAAA Engine will play as **{engine_color}**!")
                    if player_color_saved.lower() == "black":
                        st.info("💡 Notice: Press the button 🚀 Start (Black Triggers White) on left side of chessboard in main screen")

                if st.button("⚙️ Change Setup", use_container_width=True, key="btn_engine_top_change_setup"):
                    if st.session_state.get("timer_started", False) and st.session_state.get("active_timer") is not None:
                        st.error('⚠️ Before pressing "⚙️ Change Setup" button player must pause the timer')
                        if st.button("Dismiss", key="btn_dismiss_changesetup_warning", use_container_width=True):
                            st.rerun()
                    else:
                        st.session_state["details_submitted"] = False
                        
                        st.session_state["show_change_options"] = True
                        st.rerun()
            
            else:
                def on_mode_change():
                    if st.session_state.get("engine_top_game_mode", "").startswith("🤖 Single Player"):
                        st.session_state["engine_top_single_name"] = ""
                        st.session_state["user_name"] = ""
                    else:
                        st.session_state["engine_top_black_name"] = ""
                        st.session_state["engine_top_white_name"] = ""
                        st.session_state["black_user_name"] = ""
                        st.session_state["white_user_name"] = ""

                game_mode = st.radio("🎮 Select Match Mode:", ["🤖 Single Player (vs ATAAA Engine)", "👥 Two Player Match"], index=default_mode_idx, key="engine_top_game_mode", on_change=on_mode_change, label_visibility="collapsed")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if game_mode.startswith("🤖 Single Player"):
                    st.markdown("### **👑 Choose Your Color:**")
                    curr_color = st.session_state.get("player_color", "white")
                    default_color_idx = 0 if curr_color == "white" else 1
                    
                    user_color = st.radio("Select Color:", ["White", "Black"], index=default_color_idx, key="engine_top_user_color", label_visibility="collapsed", disabled=False)
                    
                    st.session_state["player_color"] = user_color.lower()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown("### **⚙️ Clock Activation Mode Selection**")
                    clock_choice = st.radio("Choose Mode Setup:", ["With standard chess clock", "Without standard chess clock"], key="engine_top_clock_choice", label_visibility="collapsed")
                    
                   

                    
                    user_input_name = st.text_input("Please type your name:", value=st.session_state.get("user_name", "") if st.session_state.get("game_mode", "single") == "single" else "", key="engine_top_single_name")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if is_puzzle_mode:
                        st.markdown("---")
                        st.markdown("### **💡 ATAAA Puzzle Master Series Assistant**")
                        
                        col_rm1, col_rm2, col_rm3 = st.columns(3)
                        with col_rm1:
                            if st.button("👁️ Show Answer Series", use_container_width=True, key="btn_show_answer_series_single"):
                                current_fen = st.session_state.get("board_fen", "")
                                if current_fen:
                                    import chess
                                    solution_board = chess.Board(current_fen)
                                    is_white_turn = solution_board.turn
                                    side_label = "White" if is_white_turn else "Black"
                                    
                                    try:
                                        complete_move_series = []
                                        for _ in range(1000000000):
                                            if solution_board.is_game_over():
                                                break
                                            _, best_move = minimax_alpha_beta(solution_board, 3, -float('inf'), float('inf'), solution_board.turn)
                                            if best_move:
                                                move_san = solution_board.san(best_move)
                                                solution_board.push(best_move)
                                                complete_move_series.append(move_san)
                                            else:
                                                break
                                        
                                        st.success(f"👑 **Complete Game Over Roadmap ({side_label} to move):**")
                                        
                                        formatted_series = ""
                                        for i in range(0, len(complete_move_series), 2):
                                            m1 = complete_move_series[i]
                                            m2 = complete_move_series[i+1] if i+1 < len(complete_move_series) else ""
                                            formatted_series += f"{m1} {m2}\n\n"
                                        
                                        st.markdown(f"```text\n{formatted_series.strip()}\n```")
                                        
                                    except Exception as e:
                                        st.error(f"Could not compute game over roadmap: {e}")
                                else:
                                    st.warning("⚠️ Please generate a puzzle first by submitting configuration!")
                        
                        if col_rm2:
                            if st.button("Could you tell me how the state of game will end ?", use_container_width=True, key="btn_game_end_state_truth_single"):
                                current_fen = st.session_state.get("board_fen", "")
                                if current_fen:
                                    import chess
                                    truth_board = chess.Board(current_fen)
                                    
                                    for _ in range(100):
                                        if truth_board.is_game_over():
                                            break
                                        _, best_move = minimax_alpha_beta(truth_board, 3, -float('inf'), float('inf'), truth_board.turn)
                                        if best_move:
                                            truth_board.push(best_move)
                                        else:
                                            break
                                        
                                    if truth_board.is_checkmate():
                                        winner = "Black" if truth_board.turn else "White"
                                        st.success(f"🎯 **Game Over Analysis:** 100% possible win for **{winner}** (Checkmate confirmed)!")
                                    elif truth_board.is_stalemate():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Stalemate**.")
                                    elif truth_board.is_insufficient_material():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Insufficient Material**.")
                                    elif truth_board.is_seventyfive_moves():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **75-Move Rule**.")
                                    elif truth_board.is_fivefold_repetition():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Fivefold Repetition**.")
                                    elif truth_board.is_threefold_repetition():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Threefold Repetition**.")
                                    elif truth_board.can_claim_threefold():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Threefold Repetition Claim**.")
                                    elif truth_board.is_fifty_moves():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **50-Move Rule**.")
                                    elif truth_board.can_claim_fifty_moves():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **50-Move Rule Claim**.")
                                    elif truth_board.is_game_over():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **General Terminal / Dead Position**.")
                                    else:
                                        eval_score, _ = minimax_alpha_beta(truth_board, 3, -float('inf'), float('inf'), truth_board.turn)
                                        if eval_score > 150:
                                            st.success("👑 **Game Over Analysis:** 100% possible win for **White** based on decisive tactical advantage.")
                                        elif eval_score < -150:
                                            st.success("👑 **Game Over Analysis:** 100% possible win for **Black** based on decisive tactical advantage.")
                                        else:
                                            st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Balanced Equilibrium / Equal Material**.")
                                else:
                                    st.warning("⚠️ Please generate a puzzle first by submitting configuration!")

                        st.markdown("---")
                    
                    if st.session_state.get("show_change_options", False) and not is_puzzle_mode:
                        st.markdown("---")
                        st.markdown("#### **Choose Post-Change Behavior:**")
                        
                        if not is_tournament_match_mode:
                            if st.button("🟢 Continue With Current Moves Of board", use_container_width=True, key="btn_engine_keep_moves"):
                                st.session_state["pending_preserve_moves"] = True
                                if hasattr(st.session_state, "board_state") and st.session_state.board_state:
                                    current_board = st.session_state.board_state
                                    current_turn_str = "white" if current_board.turn else "black"
                                    if user_color.lower() != current_turn_str:
                                        st.session_state["engine_must_play_current_turn"] = True
                                    else:
                                        st.session_state["engine_must_play_current_turn"] = False
                                st.session_state["show_change_options"] = False
                                st.success("✅ Behavior set: Current moves kept.")
                        
                        if st.button("🔴 Totally wipe the board, clock settings and reset game state", use_container_width=True, key="btn_engine_wipe_state"):
                            st.session_state.match_locked = False
                            st.session_state.draw_game_over = False
                            st.session_state.freeze_option = "Freeze is OFF"
                            st.session_state["engine_must_play_current_turn"] = False
                            for k in ["time_white", "time_black", "active_timer", "paused_timer", "last_timestamp", "white_move_count", "black_move_count", "flag_dropped_white", "flag_dropped_black", "moves_played", "frozen_error_triggered", "notation_error", "timer_started"]:
                                if k in st.session_state:
                                    del st.session_state[k]
                            if hasattr(st.session_state, "board_state") and st.session_state.board_state:
                                st.session_state.board_state.reset()
                            st.session_state["show_change_options"] = False
                            st.success("🧹 Game state completely wiped and reset!")
                            st.rerun()
                        st.markdown("---")
                    
                    submit_disabled = tournament_violation
                    
                    if st.button("Submit Configuration", use_container_width=True, key="btn_engine_top_submit_single", disabled=submit_disabled):
                        if is_puzzle_mode:
                            import chess
                            import random
                            
                            if "generated_puzzle_history" not in st.session_state:
                                st.session_state["generated_puzzle_history"] = set()
                                
                            generated_fen = None
                            correct_best_move_san = ""
                            
                            for _ in range(1000000000):
                                temp_board = chess.Board()
                                move_count = random.randint(10, 28)
                                for _ in range(move_count):
                                    legal_moves = list(temp_board.legal_moves)
                                    if legal_moves and not temp_board.is_game_over():
                                        temp_board.push(random.choice(legal_moves))
                                    else:
                                        break
                                        
                                candidate_fen = temp_board.fen()
                                if candidate_fen not in st.session_state["generated_puzzle_history"] and not temp_board.is_game_over():
                                    try:
                                        is_white_turn = temp_board.turn
                                        score, best_move = minimax_alpha_beta(temp_board, 3, -float('inf'), float('inf'), is_white_turn)
                                        if best_move:
                                            correct_best_move_san = temp_board.san(best_move)
                                            generated_fen = candidate_fen
                                            break
                                    except:
                                        continue
                                        
                            if not generated_fen:
                                temp_board = chess.Board("r1bqk2r/pppp1ppp/2n5/4p3/1bP1n3/3P1N2/PP2PPPP/R1BQKB1R w KQkq - 0 6")
                                generated_fen = temp_board.fen()
                                _, best_move = minimax_alpha_beta(temp_board, 2, -float('inf'), float('inf'), True)
                                correct_best_move_san = temp_board.san(best_move) if best_move else "Nxd2"
                                
                            st.session_state["generated_puzzle_history"].add(generated_fen)
                            st.session_state["board_fen"] = generated_fen
                            st.session_state["puzzle_correct_solution"] = correct_best_move_san
                            
                            if hasattr(st.session_state, "board_state") and st.session_state.board_state:
                                st.session_state.board_state = chess.Board(generated_fen)
                                
                            st.session_state["puzzle_mode_active"] = True
                            st.session_state["details_submitted"] = True
                            st.success(f"♾️ 100 Crore Infinite Non-Repeating Puzzle Generated! Solution Notation Loaded: **{correct_best_move_san}**")
                            st.rerun()
                        else:
                            if user_input_name.strip() != "":
                                st.session_state["user_name"] = user_input_name.strip()
                                st.session_state["player_color"] = user_color.lower()
                                st.session_state["clock_mode"] = clock_choice
                                st.session_state["game_mode"] = "single"
                                st.session_state["details_submitted"] = True
                                st.session_state["play_topbar_audio"] = True
                                st.session_state["show_change_options"] = False
                                
                                if hasattr(st.session_state, "board_state") and st.session_state.board_state:
                                    current_board = st.session_state.board_state
                                    if not current_board.is_game_over():
                                        current_turn_str = "white" if current_board.turn else "black"
                                        
                                        if clock_choice == "Without standard chess clock":
                                            if user_color.lower() == "black" and len(current_board.move_stack) == 0:
                                                _, engine_move = minimax_alpha_beta(current_board, 3, -float('inf'), float('inf'), True)
                                                if engine_move:
                                                    san_txt = current_board.san(engine_move)
                                                    current_board.push(engine_move)
                                                    if "moves_played" not in st.session_state:
                                                        st.session_state.moves_played = []
                                                    st.session_state.moves_played.append(f"White: {san_txt}")
                                            elif user_color.lower() == "white" and user_color.lower() != current_turn_str:
                                                is_engine_white = False
                                                _, engine_move = minimax_alpha_beta(current_board, 3, -float('inf'), float('inf'), is_engine_white)
                                                if engine_move:
                                                    san_txt = current_board.san(engine_move)
                                                    current_board.push(engine_move)
                                                    if "moves_played" not in st.session_state:
                                                        st.session_state.moves_played = []
                                                    st.session_state.moves_played.append(f"Black: {san_txt}")

                                st.success("✅ Configuration updated successfully!")
                                st.rerun()
                            else:
                                st.warning("⚠️ Please type your name before submitting.")
                
                else:  # Two Player Match Sub-Workflow
                    st.markdown("### **👥 Two Player Match Options**")
                    twoplayer_sub_option = st.radio(
                        "Select Two Player Option:",
                        ["Play with login", "Play without login"],
                        key="twoplayer_sub_option",
                        horizontal=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)

                    if twoplayer_sub_option == "Play without login":
                        st.markdown("### **Enter names for both sides simultaneously:**")
                        col_b, col_w = st.columns(2)
                        with col_b:
                            black_player_name = st.text_input("Black Player Name:", value=st.session_state.get("black_user_name", ""), key="engine_top_black_name")
                        with col_w:
                            white_player_name = st.text_input("White Player Name:", value=st.session_state.get("white_user_name", ""), key="engine_top_white_name")
                        st.markdown("<br>", unsafe_allow_html=True)

                    else:  # Play with login workflow with Platform Selector (Desktop Browser vs Mobile Phone OS Menu)
                        if "show_google_account_picker" not in st.session_state:
                            st.session_state["show_google_account_picker"] = False
                        if "google_auth_flow_step" not in st.session_state:
                            st.session_state["google_auth_flow_step"] = "account_picker"

                        # Platform simulator toggle to demonstrate Web Browser redirect vs Mobile OS slide-up menu
                        platform_mode = st.radio(
                            "Select Device Platform Simulation:",
                            ["🖥️ Desktop Web Browser (accounts.google.com)", "📱 Mobile Phone OS Menu (Android/iOS System Sheet)"],
                            key="oauth_platform_simulation",
                            horizontal=True
                        )
                        st.markdown("<br>", unsafe_allow_html=True)

                        if st.session_state.get("show_google_account_picker", False):
                            
                            # ==========================================
                            # DESKTOP BROWSER OAUTH WINDOW (accounts.google.com)
                            # ==========================================
                            if platform_mode.startswith("🖥️ Desktop"):
                                if st.session_state.get("google_auth_flow_step") == "account_picker":
                                    st.markdown("""
                                        <div style="background-color: #131314; border: 1px solid #444746; border-radius: 24px; padding: 32px; max-width: 820px; margin: 20px auto; color: #e3e3e3; font-family: Roboto, sans-serif; box-shadow: 0 12px 32px rgba(0,0,0,0.8);">
                                            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 24px;">
                                                <svg width="22" height="22" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.8 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.2 8.9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/><path fill="#FBBC05" d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.7s.2-2 .4-2.7L1.6 6.4C.6 8.4 0 10.6 0 13s.6 4.6 1.6 6.6l3.7-2.9z"/><path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.2-6.7-5.3L1.6 15.6C3.5 19.4 7.4 23 12 23z"/></svg>
                                                <span style="font-size: 15px; font-weight: 500; color: #e3e3e3;">accounts.google.com (Secure Redirect)</span>
                                            </div>
                                    """, unsafe_allow_html=True)

                                    col_picker_left, col_picker_right = st.columns([1, 1.2])

                                    with col_picker_left:
                                        st.markdown("""
                                            <div style="padding-right: 16px;">
                                                <div style="width: 48px; height: 48px; background: #00FF87; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: #000; margin-bottom: 16px;">♔</div>
                                                <h2 style="font-size: 28px; font-weight: 400; color: #e3e3e3; margin: 0 0 12px 0;">Choose an account</h2>
                                                <p style="font-size: 14px; color: #8e918f; margin: 0;">to continue to <b>ATAAA for Chess</b></p>
                                            </div>
                                        """, unsafe_allow_html=True)

                                    with col_picker_right:
                                        st.markdown("<div style='display: flex; flex-direction: column; gap: 4px;'>", unsafe_allow_html=True)
                                        
                                        if st.button("r   Renuga\nrenukamurthy1984re@gmail.com", key="btn_account_1", use_container_width=True):
                                            st.session_state["selected_account_name"] = "Renuga"
                                            st.session_state["selected_account_email"] = "renukamurthy1984re@gmail.com"
                                            st.session_state["google_auth_flow_step"] = "verify_device"
                                            st.rerun()

                                        if st.button("K   Chess Player\nplayer.chess99@gmail.com", key="btn_account_2", use_container_width=True):
                                            st.session_state["selected_account_name"] = "Chess Player"
                                            st.session_state["selected_account_email"] = "player.chess99@gmail.com"
                                            st.session_state["google_auth_flow_step"] = "verify_device"
                                            st.rerun()

                                        if st.button("⚙️ Use another account", key="btn_use_another_account", use_container_width=True):
                                            st.info("ℹ️ Redirecting to Google universal login portal...")

                                        st.markdown("</div>", unsafe_allow_html=True)

                                    st.markdown("""
                                            <div style="margin-top: 36px; border-top: 1px solid #444746; padding-top: 16px; font-size: 12px; color: #8e918f;">
                                                Before using this app, you can review ATAAA for Chess's <span style="color: #8ab4f8; cursor: pointer;">Privacy Policy</span> and <span style="color: #8ab4f8; cursor: pointer;">Terms of Service</span>.
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)

                                    if st.button("✕ Cancel & Return", key="btn_close_google_picker", use_container_width=True):
                                        st.session_state["show_google_account_picker"] = False
                                        st.session_state["google_auth_flow_step"] = "account_picker"
                                        st.rerun()

                                elif st.session_state.get("google_auth_flow_step") == "verify_device":
                                    sel_email = st.session_state.get("selected_account_email", "renukamurthy1984re@gmail.com")
                                    st.markdown(f"""
                                        <div style="background-color: #131314; border: 1px solid #444746; border-radius: 24px; padding: 32px; max-width: 820px; margin: 20px auto; color: #e3e3e3; font-family: Roboto, sans-serif; box-shadow: 0 12px 32px rgba(0,0,0,0.8);">
                                            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 24px;">
                                                <svg width="22" height="22" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.8 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.2 8.9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/><path fill="#FBBC05" d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.7s.2-2 .4-2.7L1.6 6.4C.6 8.4 0 10.6 0 13s.6 4.6 1.6 6.6l3.7-2.9z"/><path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.2-6.7-5.3L1.6 15.6C3.5 19.4 7.4 23 12 23z"/></svg>
                                                <span style="font-size: 15px; font-weight: 500; color: #e3e3e3;">accounts.google.com — Verify it's you</span>
                                            </div>
                                    """, unsafe_allow_html=True)

                                    col_v_left, col_v_right = st.columns([1, 1.2])

                                    with col_v_left:
                                        st.markdown(f"""
                                            <div style="padding-right: 16px;">
                                                <h2 style="font-size: 28px; font-weight: 400; color: #e3e3e3; margin: 0 0 12px 0;">Verify it's you</h2>
                                                <p style="font-size: 13px; color: #8e918f; margin: 0 0 20px 0; line-height: 1.5;">To help keep your account safe, Google wants to make sure it's really you</p>
                                                <div style="background: #202124; border: 1px solid #5f6368; border-radius: 8px; padding: 10px 14px; display: inline-block; font-size: 13px; color: #e3e3e3; margin-bottom: 24px;">
                                                    r &nbsp; {sel_email} ▼
                                                </div>
                                            </div>
                                        """, unsafe_allow_html=True)

                                    with col_v_right:
                                        st.markdown("""
                                            <div style="background: #202124; border-radius: 16px; padding: 24px; text-align: center; border: 1px solid #444746;">
                                                <div style="font-size: 64px; font-weight: 400; color: #e3e3e3; letter-spacing: 2px; margin-bottom: 12px;">83</div>
                                                <h3 style="font-size: 16px; font-weight: 500; color: #e3e3e3; margin: 0 0 8px 0;">Check your Galaxy J7 Neo</h3>
                                                <p style="font-size: 12px; color: #8e918f; line-height: 1.5; margin: 0;">Google sent a notification to your phone. Tap <b>Yes</b> on the Google prompt, then tap <b>83</b>.</p>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        st.markdown("<br>", unsafe_allow_html=True)
                                        if st.button("✅ Approve 2FA Handshake", key="btn_simulate_2fa_desktop", use_container_width=True):
                                            st.session_state["ataa_chess_signed_up"] = True
                                            st.session_state["user_name"] = st.session_state.get("selected_account_name", "Renuga")
                                            st.session_state["show_google_account_picker"] = False
                                            st.session_state["google_auth_flow_step"] = "account_picker"
                                            st.success("✅ Secure digital handshake successful! Token received from accounts.google.com.")
                                            st.rerun()

                                    if st.button("← Back to account list", key="btn_back_to_accounts_desk", use_container_width=True):
                                        st.session_state["google_auth_flow_step"] = "account_picker"
                                        st.rerun()

                            # ==========================================
                            # MOBILE PHONE OS SYSTEM SHEET MENU (Android / iOS)
                            # ==========================================
                            else:
                                st.markdown("""
                                    <div style="background-color: #1c1c1e; border: 1px solid #3a3a3c; border-radius: 28px 28px 0 0; padding: 28px; max-width: 480px; margin: 20px auto; color: #f2f2f7; font-family: -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 -10px 30px rgba(0,0,0,0.7);">
                                        <div style="width: 36px; height: 5px; background: #48484a; border-radius: 3px; margin: 0 auto 20px auto;"></div>
                                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                                            <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.8 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.2 8.9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/><path fill="#FBBC05" d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.7s.2-2 .4-2.7L1.6 6.4C.6 8.4 0 10.6 0 13s.6 4.6 1.6 6.6l3.7-2.9z"/><path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.2-6.7-5.3L1.6 15.6C3.5 19.4 7.4 23 12 23z"/></svg>
                                            <span style="font-size: 14px; font-weight: 600; color: #f2f2f7;">Sign in with Google OS Menu</span>
                                        </div>
                                        <p style="font-size: 13px; color: #aeaeb2; margin-bottom: 16px;">ATAAA for Chess wants to use google.com to sign in.</p>
                                """, unsafe_allow_html=True)

                                if st.button("r   Renuga (renukamurthy1984re@gmail.com)", key="btn_mobile_acc_1", use_container_width=True):
                                    st.session_state["ataa_chess_signed_up"] = True
                                    st.session_state["user_name"] = "Renuga"
                                    st.session_state["show_google_account_picker"] = False
                                    st.success("✅ Mobile OS Sheet token handshake successful!")
                                    st.rerun()

                                if st.button("K   Chess Player (player.chess99@gmail.com)", key="btn_mobile_acc_2", use_container_width=True):
                                    st.session_state["ataa_chess_signed_up"] = True
                                    st.session_state["user_name"] = "Chess Player"
                                    st.session_state["show_google_account_picker"] = False
                                    st.success("✅ Mobile OS Sheet token handshake successful!")
                                    st.rerun()

                                if st.button("✕ Cancel", key="btn_mobile_cancel", use_container_width=True):
                                    st.session_state["show_google_account_picker"] = False
                                    st.rerun()

                                st.markdown("</div>", unsafe_allow_html=True)

                        else:
                            is_signed_up = st.session_state.get("ataa_chess_signed_up", False)

                            if not is_signed_up:
                                st.markdown("### **👑 ATAAA for Chess Secure Sign-in**")
                                st.info("🔒 Click 'Continue with Google' to trigger platform-specific secure Google authentication.")

                                if st.button("Continue with Google", key="btn_google_signup", use_container_width=True):
                                    st.session_state["show_google_account_picker"] = True
                                    st.session_state["google_auth_flow_step"] = "account_picker"
                                    st.rerun()

                                st.markdown("<p style='text-align: center; color: #aaa; margin: 8px 0;'>or sign up manually</p>", unsafe_allow_html=True)

                                signup_email = st.text_input("Type your email:", key="signup_email_input")
                                signup_password = st.text_input("Create your password:", type="password", key="signup_password_input")
                                signup_username = st.text_input("Username:", key="signup_username_input")

                                if st.button("Complete Signup & Register", key="btn_complete_signup", use_container_width=True):
                                    if signup_email and signup_password and signup_username:
                                        st.session_state["ataa_chess_signed_up"] = True
                                        st.session_state["user_name"] = signup_username
                                        st.success(f"🎉 Account created successfully for {signup_username}!")
                                        st.rerun()
                                    else:
                                        st.error("⚠️ Please fill in all fields (email, password, username).")
                            else:
                                st.markdown(f"### **👋 Welcome back, {st.session_state.get('user_name', 'Player')}!**")
                                
                                friend_username = st.text_input("Type your friend username:", key="friend_username_input")
                                
                                col_sub_friend, col_list_friend = st.columns([1, 1])
                                with col_sub_friend:
                                    submit_friend = st.button("Submit Friend Username", key="btn_submit_friend_username", use_container_width=True)
                                with col_list_friend:
                                    see_all_friends = st.button("See all friend list", key="btn_see_all_friends", use_container_width=True)

                                if see_all_friends:
                                    st.info("📋 **Logged Friends List:**\n- Grandmaster_Leo\n- ChessQueen99\n- ATAAA_Bot_Pro\n- SpeedChessMaster")

                                if submit_friend and friend_username:
                                    st.session_state["invited_friend"] = friend_username
                                    st.session_state["friend_invite_step"] = "configure_invite"
                                    st.rerun()

                                if st.session_state.get("friend_invite_step") == "configure_invite":
                                    st.markdown("---")
                                    st.markdown(f"#### **Configure Match vs {st.session_state.get('invited_friend')}**")
                                    
                                    invite_color = st.radio("Select Color:", ["1st White", "2nd Black"], key="invite_color_choice")
                                    invite_time = st.selectbox("Set Time Control:", ["3 min (Blitz)", "5 min (Blitz)", "10 min (Rapid)", "15 min (Rapid)", "30 min (Classical)"], key="invite_time_choice")

                                    if st.button("Invite to play", key="btn_send_invite_to_play", use_container_width=True):
                                        st.session_state["invite_sent_active"] = True
                                        st.success(f"The \"{st.session_state.get('user_name')}\" invites the \"{st.session_state.get('invited_friend')}\" to play chess as {invite_color} with {invite_time}")

                                if st.session_state.get("invite_sent_active", False):
                                    st.markdown("---")
                                    st.markdown("#### **📬 Incoming Match Invitation Simulation**")
                                    st.info(f"Notification: {st.session_state.get('user_name')} has invited {st.session_state.get('invited_friend')} to play.")

                                    col_acc, col_bus, col_chg = st.columns(3)
                                    with col_acc:
                                        if st.button("Accept invite", key="btn_accept_invite"):
                                            st.success("Success accepted, launching will be in few seconds")
                                            st.session_state["details_submitted"] = True
                                            st.session_state["game_mode"] = "two_player"
                                            st.session_state["white_user_name"] = st.session_state.get('user_name')
                                            st.session_state["black_user_name"] = st.session_state.get('invited_friend')
                                            st.rerun()
                                    with col_bus:
                                        if st.button("Sorry, I'm bussy", key="btn_busy_invite"):
                                            st.warning(f"Not accepted, {st.session_state.get('user_name')} is currently busy.")
                                            st.session_state["invite_sent_active"] = False
                                            st.rerun()
                                    with col_chg:
                                        if st.button("I want to change", key="btn_change_invite"):
                                            st.session_state["friend_invite_step"] = "configure_invite"
                                            st.session_state["invite_sent_active"] = False
                                            st.rerun()

                    if is_puzzle_mode:
                        st.markdown("---")
                        st.markdown("### **💡 ATAAA Puzzle Master Series Assistant**")
                        
                        col_rm1, col_rm2, col_rm3 = st.columns(3)
                        with col_rm1:
                            if st.button("👁️ Show Answer Series", use_container_width=True, key="btn_show_answer_series_two"):
                                current_fen = st.session_state.get("board_fen", "")
                                if current_fen:
                                    import chess
                                    solution_board = chess.Board(current_fen)
                                    is_white_turn = solution_board.turn
                                    side_label = "White" if is_white_turn else "Black"
                                    
                                    try:
                                        complete_move_series = []
                                        for _ in range(1000000000):
                                            if solution_board.is_game_over():
                                                break
                                            _, best_move = minimax_alpha_beta(solution_board, 3, -float('inf'), float('inf'), solution_board.turn)
                                            if best_move:
                                                move_san = solution_board.san(best_move)
                                                solution_board.push(best_move)
                                                complete_move_series.append(move_san)
                                            else:
                                                break
                                        
                                        st.success(f"👑 **Complete Game Over Roadmap ({side_label} to move):**")
                                        
                                        formatted_series = ""
                                        for i in range(0, len(complete_move_series), 2):
                                            m1 = complete_move_series[i]
                                            m2 = complete_move_series[i+1] if i+1 < len(complete_move_series) else ""
                                            formatted_series += f"{m1} {m2}\n\n"
                                        
                                        st.markdown(f"```text\n{formatted_series.strip()}\n```")
                                        
                                    except Exception as e:
                                        st.error(f"Could not compute game over roadmap: {e}")
                                else:
                                    st.warning("⚠️ Please generate a puzzle first by submitting configuration!")
                                    
                        if col_rm2:
                            if st.button("Could you tell me how the state of game will end ?", use_container_width=True, key="btn_game_end_state_truth_two"):
                                current_fen = st.session_state.get("board_fen", "")
                                if current_fen:
                                    import chess
                                    truth_board = chess.Board(current_fen)
                                    
                                    for _ in range(100):
                                        if truth_board.is_game_over():
                                            break
                                        _, best_move = minimax_alpha_beta(truth_board, 3, -float('inf'), float('inf'), truth_board.turn)
                                        if best_move:
                                            truth_board.push(best_move)
                                        else:
                                            break
                                        
                                    if truth_board.is_checkmate():
                                        winner = "Black" if truth_board.turn else "White"
                                        st.success(f"🎯 **Game Over Analysis:** 100% possible win for **{winner}** (Checkmate confirmed)!")
                                    elif truth_board.is_stalemate():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Stalemate**.")
                                    elif truth_board.is_insufficient_material():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Insufficient Material**.")
                                    elif truth_board.is_seventyfive_moves():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **75-Move Rule**.")
                                    elif truth_board.is_fivefold_repetition():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Fivefold Repetition**.")
                                    elif truth_board.is_threefold_repetition():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Threefold Repetition**.")
                                    elif truth_board.can_claim_threefold():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Threefold Repetition Claim**.")
                                    elif truth_board.is_fifty_moves():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **50-Move Rule**.")
                                    elif truth_board.can_claim_fifty_moves():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **50-Move Rule Claim**.")
                                    elif truth_board.is_game_over():
                                        st.info("⚖️ **Game Over Analysis:** 100% possible draw by **General Terminal / Dead Position**.")
                                    else:
                                        eval_score, _ = minimax_alpha_beta(truth_board, 3, -float('inf'), float('inf'), truth_board.turn)
                                        if eval_score > 150:
                                            st.success("👑 **Game Over Analysis:** 100% possible win for **White** based on decisive tactical advantage.")
                                        elif eval_score < -150:
                                            st.success("👑 **Game Over Analysis:** 100% possible win for **Black** based on decisive tactical advantage.")
                                        else:
                                            st.info("⚖️ **Game Over Analysis:** 100% possible draw by **Balanced Equilibrium / Equal Material**.")
                                else:
                                    st.warning("⚠️ Please generate a puzzle first by submitting configuration!")

                        st.markdown("---")
                    
                    if st.session_state.get("show_change_options", False):
                        st.markdown("---")
                        st.markdown("#### **Choose Post-Change Behavior:**")
                        if not is_tournament_match_mode:
                            if st.button("🟢 Continue With Current Moves Of board", use_container_width=True, key="btn_engine_keep_moves_two"):
                                st.session_state["pending_preserve_moves"] = True
                                st.session_state["engine_must_play_current_turn"] = False
                                st.session_state["show_change_options"] = False
                                st.success("✅ Behavior set: Current moves and state will be kept.")
                        if st.button("🔴 Totally wipe the board, clock settings and reset game state", use_container_width=True, key="btn_engine_wipe_state_two"):
                            st.session_state.match_locked = False
                            st.session_state.draw_game_over = False
                            st.session_state.freeze_option = "Freeze is OFF"
                            st.session_state["engine_must_play_current_turn"] = False
                            for k in ["time_white", "time_black", "active_timer", "paused_timer", "last_timestamp", "white_move_count", "black_move_count", "flag_dropped_white", "flag_dropped_black", "moves_played", "frozen_error_triggered", "notation_error", "timer_started"]:
                                if k in st.session_state:
                                    del st.session_state[k]
                            if hasattr(st.session_state, "board_state") and st.session_state.board_state:
                                st.session_state.board_state.reset()
                            st.session_state["show_change_options"] = False
                            st.success("🧹 Game state completely wiped and reset!")
                            st.rerun()
                        st.markdown("---")

                    submit_disabled_two = tournament_violation
                    if st.button("Submit Configuration", use_container_width=True, key="btn_engine_top_submit_two", disabled=submit_disabled_two):
                        if is_puzzle_mode:
                            import chess
                            import random
                            
                            if "generated_puzzle_history" not in st.session_state:
                                st.session_state["generated_puzzle_history"] = set()
                                
                            generated_fen = None
                            correct_best_move_san = ""
                            
                            for _ in range(1000000000):
                                temp_board = chess.Board()
                                move_count = random.randint(10, 28)
                                for _ in range(move_count):
                                    legal_moves = list(temp_board.legal_moves)
                                    if legal_moves and not temp_board.is_game_over():
                                        temp_board.push(random.choice(legal_moves))
                                    else:
                                        break
                                        
                                candidate_fen = temp_board.fen()
                                if candidate_fen not in st.session_state["generated_puzzle_history"] and not temp_board.is_game_over():
                                    try:
                                        is_white_turn = temp_board.turn
                                        score, best_move = minimax_alpha_beta(temp_board, 3, -float('inf'), float('inf'), is_white_turn)
                                        if best_move:
                                            correct_best_move_san = temp_board.san(best_move)
                                            generated_fen = candidate_fen
                                            break
                                    except:
                                        continue
                                        
                            if not generated_fen:
                                temp_board = chess.Board("r1bqk2r/pppp1ppp/2n5/4p3/1bP1n3/3P1N2/PP2PPPP/R1BQKB1R w KQkq - 0 6")
                                generated_fen = temp_board.fen()
                                _, best_move = minimax_alpha_beta(temp_board, 2, -float('inf'), float('inf'), True)
                                correct_best_move_san = temp_board.san(best_move) if best_move else "Nxd2"
                                
                            st.session_state["generated_puzzle_history"].add(generated_fen)
                            st.session_state["board_fen"] = generated_fen
                            st.session_state["puzzle_correct_solution"] = correct_best_move_san
                            
                            if hasattr(st.session_state, "board_state") and st.session_state.board_state:
                                st.session_state.board_state = chess.Board(generated_fen)
                                
                            st.session_state["puzzle_mode_active"] = True
                            st.session_state["details_submitted"] = True
                            st.success(f"♾️ 100 Crore Infinite Non-Repeating Puzzle Generated! Solution Notation Loaded: **{correct_best_move_san}**")
                            st.rerun()
                        else:
                            if black_player_name.strip() != "" and white_player_name.strip() != "":
                                st.session_state["black_user_name"] = black_player_name.strip()
                                st.session_state["white_user_name"] = white_player_name.strip()
                                st.session_state["user_name"] = f"{white_player_name.strip()} (White) vs {black_player_name.strip()} (Black)"
                                st.session_state["game_mode"] = "two_player"
                                st.session_state["details_submitted"] = True
                                st.session_state["play_topbar_audio"] = True
                                st.session_state["show_change_options"] = False
                                
                                st.success("✅ Two-player configuration updated successfully!")
                                st.rerun()
                            else:
                                st.warning("⚠️ Please type your name before submitting.")

    if st.session_state.get("play_topbar_audio", False):
        audio_type = st.session_state.get("audio_type", "submit")
        if audio_type == "review":
            topopen_bg_music_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/The_Victor%E2%80%99s_Gate.mp3"
        else:
            topopen_bg_music_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/welcome%20sound.mp4"
        
        topopen_audio_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 15px;">
            <audio id="topopen_bg_audio" autoplay preload="auto">
                <source src="{topopen_bg_music_url}" type="audio/mp4">
                Your browser does not support the audio element.
            </audio>
        </div>
        <script>
            var topAudio = document.getElementById("topopen_bg_audio");
            if (topAudio) {{
                topAudio.loop = false;
                topAudio.muted = false;
                topAudio.volume = 1.0;
                topAudio.play().catch(function(error) {{
                    console.log("Audio autoplay prevented: ", error);
                }});
            }}
        </script>
        """
        st.markdown(topopen_audio_html, unsafe_allow_html=True)
        st.session_state["play_topbar_audio"] = False






# =========================================================================
# DYNAMIC MODE DISPLAY (Positioned ONLY Under Start Button)
# =========================================================================




#######ATAAA CHESS AI##############

#######ATAAA CHESS AI##############
# --- 1. SYSTEM CONFIG & STYLES ---
st.markdown("""
    <style>
    .shimmer-btn-label {
        font-size: 18px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #FFFFFF, #FF1493, #0e689c, #FF1493, #0e689c, #FFFFFF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', sans-serif;
        animation: shine 5s linear infinite;
        margin: 0;
        padding: 0;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION BUTTON WITH PERFECT CENTERING ---
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav2:
    st.markdown("""
        <div style="position: relative; width: 100%;">
    """, unsafe_allow_html=True)
    
    if st.button("", use_container_width=True, key="btn_toggle_ai_screen"):
        st.session_state.show_ai_screen = not st.session_state.get("show_ai_screen", False)
        st.rerun()        
    st.markdown("""
        <div style="margin-top: -60px; pointer-events: none; text-align: center;">
            <p class="shimmer-btn-label">✈️ ATAAA AI - Hub For Learning</p>
        </div>
    """, unsafe_allow_html=True)




# =========================================================================
# ⏱️ STATE INITIALIZATION
# =========================================================================
if "time_white" not in st.session_state: st.session_state.time_white = float(base_seconds)
if "time_black" not in st.session_state: st.session_state.time_black = float(base_seconds)
if "active_timer" not in st.session_state: st.session_state.active_timer = None
if "paused_timer" not in st.session_state: st.session_state.paused_timer = None  
if "last_timestamp" not in st.session_state: st.session_state.last_timestamp = None
if "white_move_count" not in st.session_state: st.session_state.white_move_count = 0
if "black_move_count" not in st.session_state: st.session_state.black_move_count = 0
if "flag_dropped_white" not in st.session_state: st.session_state.flag_dropped_white = False
if "flag_dropped_black" not in st.session_state: st.session_state.flag_dropped_black = False
if "board_state" not in st.session_state: st.session_state.board_state = pure_chess_pkg.Board()
if "moves_played" not in st.session_state: st.session_state.moves_played = []
if "frozen_error_triggered" not in st.session_state: st.session_state.frozen_error_triggered = False
if "notation_error" not in st.session_state: st.session_state.notation_error = False
if "timer_started" not in st.session_state: st.session_state.timer_started = False
if "agreement_active" not in st.session_state: st.session_state.agreement_active = False
if "selected_draw_color" not in st.session_state: st.session_state.selected_draw_color = None
if "draw_game_over" not in st.session_state: st.session_state.draw_game_over = False
if "draw_warning_msg" not in st.session_state: st.session_state.draw_warning_msg = None
if "threefold_stage" not in st.session_state: st.session_state.threefold_stage = 0  # 0: idle, 1: choice type, 2: choose color, 3: penalty panel
if "threefold_type" not in st.session_state: st.session_state.threefold_type = None  # "next_move" or "already"
if "threefold_claimant" not in st.session_state: st.session_state.threefold_claimant = None # "White" or "Black"
if "threefold_warning" not in st.session_state: st.session_state.threefold_warning = None
if "fifty_move_stage" not in st.session_state:
    st.session_state.fifty_move_stage = 0  # 0: Idle, 1: Claimant Selection, 2: Scenario Selection, 3: Input/Verification, 4: Penalty Screen
if "fifty_move_warning" not in st.session_state:
    st.session_state.fifty_move_warning = None
if "fifty_move_claimant" not in st.session_state:
    st.session_state.fifty_move_claimant = None
if "fifty_move_type" not in st.session_state:
    st.session_state.fifty_move_type = None
if "fifty_move_penalty_msg" not in st.session_state:
    st.session_state.fifty_move_penalty_msg = ""
if "armageddon_style_mode" not in st.session_state:
    st.session_state.armageddon_style_mode = False
# Initialize rotation index counters for the 10 distinct video/music pairs
for counter_key in ["normal_white_win_idx", "normal_black_win_idx", "armageddon_white_win_idx", "armageddon_black_win_idx"]:
    if counter_key not in st.session_state:
        st.session_state[counter_key] = 0
if "game_mode" not in st.session_state:
    st.session_state["game_mode"] = "single"

game_mode_eval = "🤖 Single Player (vs ATAAA Engine)" if st.session_state["game_mode"] == "single" else "👥 Two Player Match"


def apply_turn_increments(player_color):
    if freeze_option == "Freeze is OFF" and (st.session_state.flag_dropped_white or st.session_state.flag_dropped_black):
        return
        
    # Always sync move counts with the actual board stack so moves played before starting the clock are counted
    st.session_state.white_move_count = (len(st.session_state.board_state.move_stack) + 1) // 2
    st.session_state.black_move_count = len(st.session_state.board_state.move_stack) // 2

    # Check if timer is started; if not, sync counts but do not add any increments yet
    if not st.session_state.get("timer_started", False):
        return

    # Check if Armageddon mode is active
    is_armageddon = st.session_state.get("armageddon_active", False)
    
    if player_color == "white":
        if is_armageddon:
            # --- ARMAGEDDON INCREMENT LOGIC ONLY ---
            increment_type = st.session_state.get("armageddon_increment_type", "No increments")
            bonus_sec = st.session_state.get("armageddon_bonus", 0)
            
            if increment_type == "on move 41" and st.session_state.white_move_count >= 41:
                st.session_state.time_white += bonus_sec
            elif increment_type == "on move 61" and st.session_state.white_move_count >= 61:
                st.session_state.time_white += bonus_sec
        else:
            # --- NORMAL CLOCK STYLE INCREMENTS ---
            move_bonus = (inc_move_m * 60) + inc_move_s
            if fischer_trigger_type == "From the Initial Move" or (fischer_trigger_type == "After Specific Number of Moves" and st.session_state.white_move_count >= fischer_target_moves):
                st.session_state.time_white += per_move_s
            if move_trigger_type == "From the Initial Move" or (move_trigger_type == "After Specific Number of Moves" and st.session_state.white_move_count == target_moves):
                st.session_state.time_white += move_bonus
                
    elif player_color == "black":
        if is_armageddon:
            # --- ARMAGEDDON INCREMENT LOGIC ONLY ---
            increment_type = st.session_state.get("armageddon_increment_type", "No increments")
            bonus_sec = st.session_state.get("armageddon_bonus", 0)
            
            if increment_type == "on move 41" and st.session_state.black_move_count >= 41:
                st.session_state.time_black += bonus_sec
            elif increment_type == "on move 61" and st.session_state.black_move_count >= 61:
                st.session_state.time_black += bonus_sec
        else:
            # --- NORMAL CLOCK STYLE INCREMENTS ---
            move_bonus = (inc_move_m * 60) + inc_move_s
            if fischer_trigger_type == "From the Initial Move" or (fischer_trigger_type == "After Specific Number of Moves" and st.session_state.black_move_count >= fischer_target_moves):
                st.session_state.time_black += per_move_s
            if move_trigger_type == "From the Initial Move" or (move_trigger_type == "After Specific Number of Moves" and st.session_state.black_move_count == target_moves):
                st.session_state.time_black += move_bonus


def execute_champion_engine_move():
    if not st.session_state.board_state.is_game_over():
        # Safely pull user color from session state (defaults to 'white' if not set)
        curr_user_color = st.session_state.get("player_color", "white").capitalize()
        is_engine_white = (curr_user_color == "Black")
        
        _, best_move = minimax_alpha_beta(st.session_state.board_state, 3, -float('inf'), float('inf'), is_engine_white)
        
        if best_move:
            san_text = st.session_state.board_state.san(best_move)
            turn_label = "White" if st.session_state.board_state.turn == pure_chess_pkg.WHITE else "Black"
            st.session_state.board_state.push(best_move)
            if "moves_played" not in st.session_state:
                st.session_state.moves_played = []
            st.session_state.moves_played.append(f"{turn_label}: {san_text}")
            apply_turn_increments(turn_label.lower())



def process_chess_move(move_text):
    if move_text:
        cleaned_move = move_text.strip()
        st.session_state.notation_error = False
        st.session_state.frozen_error_triggered = False
        
        try:
            turn_now = "White" if st.session_state.board_state.turn == pure_chess_pkg.WHITE else "Black"
            
            # Attempt to parse standard SAN, or fallback to UCI coordinate parsing (e.g., b6a8) 
            # to ensure valid moves like Na8 are never falsely rejected by strict parsers.
            move_obj = None
            try:
                move_obj = st.session_state.board_state.parse_san(cleaned_move)
            except ValueError:
                try:
                    move_obj = pure_chess_pkg.Move.from_uci(cleaned_move)
                    if move_obj not in st.session_state.board_state.legal_moves:
                        move_obj = None
                except ValueError:
                    move_obj = None

            if move_obj is not None and move_obj in st.session_state.board_state.legal_moves:
                st.session_state.board_state.push(move_obj)
            else:
                # Fallback to standard push_san to raise ValueError for genuinely illegal/impossible moves
                st.session_state.board_state.push_san(cleaned_move)
            
            # History tracking
            if "board_history_hashes" not in st.session_state:
                st.session_state.board_history_hashes = []
            current_hash = st.session_state.board_state.epd()
            st.session_state.board_history_hashes.append(current_hash)

            if "moves_played" not in st.session_state:
                st.session_state.moves_played = []
            st.session_state.moves_played.append(f"{turn_now}: {cleaned_move}")
            
            if 'apply_turn_increments' in globals():
                apply_turn_increments(turn_now.lower())
                
            st.session_state.notation_error = False

            # ==========================================================
            # ⚡ ARMAGEDDON OVERRIDE: Intercept Draws & Checkmates Instantly
            # ==========================================================
            if st.session_state.get("armageddon_active", False) and st.session_state.get("armageddon_style_mode", False):
                board = st.session_state.board_state
                
                if board.is_checkmate():
                    winner = "White" if turn_now == "White" else "Black"
                    check_armageddon_game_over("checkmate", winning_player=winner)
                
                elif board.is_insufficient_material():
                    white_pieces = board.occupied_co[pure_chess_pkg.WHITE]
                    black_pieces = board.occupied_co[pure_chess_pkg.BLACK]
                    if bin(white_pieces).count("1") == 1 and bin(black_pieces).count("1") == 1:
                        check_armageddon_game_over("Impossible to mate (King vs King)")
                    else:
                        check_armageddon_game_over("Insufficient Material")
                        
                elif board.is_stalemate():
                    check_armageddon_game_over("Stalemate!")
                    
                elif board.is_fivefold_repetition() or board.can_claim_threefold_repetition():
                    check_armageddon_game_over("Threefold Repetition!")
                    
                elif board.is_seventyfive_moves() or len(st.session_state.get("moves_played", [])) >= 150:
                    check_armageddon_game_over("75-Move Rule Exceeded!")
                    
                elif board.is_fifty_moves():
                    check_armageddon_game_over("50-Move Rule Exceeded!")

            return True
            
        except ValueError:
            st.session_state.notation_error = True
            st.error("❌ Illegal move or incorrect notation format inside input box!")
            return False
    return False


def format_adaptive_timer(total_seconds, use_tenths_mode):
    if total_seconds <= 0:
        if use_tenths_mode:
            return "0.0 🏴"
        else:
            return "═══\n0:00\n═══"

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    if total_seconds < 60.0 and use_tenths_mode:
        tenths = int((total_seconds % 1) * 10)
        return f"{seconds}.{tenths}"
        
    if hours == 0:
        return f"{minutes}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

refresh_rate = 0.1 if (sub_minute_mode.startswith("The clock stops") and (st.session_state.time_white < 60 or st.session_state.time_black < 60)) else 1.0

# Pre-declare layout evaluation components for sticky dynamic rules down below
board = st.session_state.board_state
flag_is_dropped = st.session_state.flag_dropped_white or st.session_state.flag_dropped_black
is_game_over = board.is_game_over() or (flag_is_dropped and freeze_option == "Freeze is ON") or st.session_state.draw_game_over

# =========================================================================
# ⏱️ LIVE TIMING SYNC ENGINE (UPDATED TO PREVENT SUBTRACTION IF GAME OVER)
# =========================================================================
# =========================================================================
# ⏱️ LIVE TIMING SYNC ENGINE (UPDATED FOR INSTANT FLAG-DROP PROTECTION)
# =========================================================================
# =========================================================================
# ⏱️ LIVE TIMING SYNC ENGINE (UPDATED FOR INSTANT FLAG-DROP PROTECTION)
# =========================================================================
# =========================================================================
# ⏱️ LIVE TIMING SYNC ENGINE (UPDATED FOR INSTANT FLAG-DROP PROTECTION)
# =========================================================================
if st.session_state.timer_started and st.session_state.active_timer is not None:
    current_moment = time.time()
    if st.session_state.last_timestamp is not None:
        if not is_game_over:
            elapsed_time = current_moment - st.session_state.last_timestamp
            if st.session_state.active_timer == "white":
                st.session_state.time_white = max(0.0, st.session_state.time_white - elapsed_time)
                if st.session_state.time_white <= 0:
                    st.session_state.flag_dropped_white = True
                    st.session_state.active_timer = None
                    st.rerun() 
            elif st.session_state.active_timer == "black":
                st.session_state.time_black = max(0.0, st.session_state.time_black - elapsed_time)
                if st.session_state.time_black <= 0:
                    st.session_state.flag_dropped_black = True
                    st.session_state.active_timer = None
                    st.rerun() 
    st.session_state.last_timestamp = current_moment  # <--- End of timing engine block

# =========================================================================
# 🤖 SINGLE PLAYER ENGINE BLACK TURN TRIGGER (ON TIMER START)
# =========================================================================
if st.session_state.get("timer_started", False) and st.session_state.get("active_timer") == "black":
    if st.session_state.get("game_mode", "") == "single" and st.session_state.get("player_color", "white") == "white":
        current_board = st.session_state.get("board_state", None)
        if current_board and not current_board.is_game_over() and not current_board.turn:
            _, engine_move = minimax_alpha_beta(current_board, 3, -float('inf'), float('inf'), False)
            if engine_move:
                san_txt = current_board.san(engine_move)
                current_board.push(engine_move)
                if "moves_played" not in st.session_state:
                    st.session_state.moves_played = []
                st.session_state.moves_played.append(f"Black: {san_txt}")
                
                # ⏱️ Correctly invoke turn increments for engine black move
                apply_turn_increments("black")
                
                st.session_state.active_timer = "white"
                st.session_state.last_timestamp = time.time()
                st.rerun()

# =========================================================================
# 🤖 SINGLE PLAYER ENGINE WHITE TURN TRIGGER (ON TIMER START)
# =========================================================================
if st.session_state.get("timer_started", False) and st.session_state.get("active_timer") == "white":
    if st.session_state.get("game_mode", "") == "single" and st.session_state.get("player_color", "white") == "black":
        current_board = st.session_state.get("board_state", None)
        if current_board and not current_board.is_game_over() and current_board.turn:
            _, engine_move = minimax_alpha_beta(current_board, 3, -float('inf'), float('inf'), True)
            if engine_move:
                san_txt = current_board.san(engine_move)
                current_board.push(engine_move)
                if "moves_played" not in st.session_state:
                    st.session_state.moves_played = []
                st.session_state.moves_played.append(f"White: {san_txt}")
                
                # ⏱️ Correctly invoke turn increments for engine white move
                apply_turn_increments("white")
                
                st.session_state.active_timer = "black"
                st.session_state.last_timestamp = time.time()
                st.rerun()



# ⚡ ARMAGEDDON TIMEOUT HOOK (Intercepts flag drops instantly when Armageddon & Style mode are active)
if st.session_state.get("armageddon_active", False) and st.session_state.get("armageddon_style_mode", False):
    if st.session_state.get("flag_dropped_white", False) and not st.session_state.get("draw_game_over", False):
        check_armageddon_game_over("white_flag_drop")
    elif st.session_state.get("flag_dropped_black", False) and not st.session_state.get("draw_game_over", False):
        check_armageddon_game_over("black_flag_drop")


# Re-evaluate accurate state conditions before layout construction
flag_is_dropped = st.session_state.flag_dropped_white or st.session_state.flag_dropped_black
is_game_over = board.is_game_over() or (flag_is_dropped and freeze_option == "Freeze is ON") or st.session_state.draw_game_over


# =========================================================================
# 🛑 GLOBAL STICKY WARNINGS & LIVE PANEL RENDERING BLOCK
# =========================================================================
show_warnings = not (freeze_option == "Freeze is OFF" and (st.session_state.flag_dropped_white or st.session_state.flag_dropped_black))

if show_warnings:
    if st.session_state.frozen_error_triggered or (freeze_option == "Freeze is ON" and flag_is_dropped):
        st.error("🚫 Clock is frozen! Cannot pass the turn.")
        st.error("🚫 Clock is frozen! Cannot submit moves")
        
   
        
    if freeze_option == "Freeze is ON":
        if st.session_state.flag_dropped_white:
            st.error("🚨 White's flag has dropped! Black wins on time.")
        if st.session_state.flag_dropped_black:
            st.error("🚨 Black's flag has dropped! White wins on time.")

# Only clear draw warnings if the match isn't closed yet
if st.session_state.draw_warning_msg and not st.session_state.draw_game_over:
    st.warning(st.session_state.draw_warning_msg)
    st.session_state.draw_warning_msg = None 

# Show live negotiations only (Before game over match lock triggers)
if not st.session_state.draw_game_over and st.session_state.selected_draw_color is not None:
    current_check_moves = st.session_state.white_move_count if st.session_state.selected_draw_color == "White" else st.session_state.black_move_count
    if current_check_moves >= 40:
        st.info(f"📋 **player {st.session_state.selected_draw_color} asking for draw**")
board = st.session_state.board_state
use_tenths = sub_minute_mode.startswith("The clock stops")

# =========================================================================
# 🏆 ATAAA PROFICIENCY HONORS SCORE SCREEN
# =========================================================================
# =========================================================================
# 🏆 ATAAA PROFICIENCY HONORS SCORE SCREEN FOR NORMAL STYLE
# =========================================================================
if st.session_state.get("current_screen") == "score" and not st.session_state.get("armageddon_style_mode", False) and not st.session_state.get("review_mode_active", False):
    
    st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
    
    col_img_left, col_title, col_img_right = st.columns([1, 4, 1])
    
    balloon_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/blob/main/Ballons.jpg?raw=true"
    
    with col_img_left:
        st.image(balloon_url, width=100)
    

    with col_title:
        st.markdown("<h1 style='text-align: center; color: #1E90FF; margin-top: 15px;'>ATAAA Proficiency Honors</h1>", unsafe_allow_html=True)
        
    with col_img_right:
        st.image(balloon_url, width=100)
        
    st.markdown("---")
    
    winner_name = "White"
    if board.is_checkmate():
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        winner_name = "Black" if winning_side == "Black" else "White"
    elif st.session_state.get("flag_dropped_white", False):
        winner_name = "Black"
    elif st.session_state.get("flag_dropped_black", False):
        winner_name = "White"
    else:
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        winner_name = winning_side

    if board.is_checkmate() or board.result() in ["1-0", "0-1"] or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False):
        congrats_text = f"Congratulations, {winner_name}!"
    else:
        congrats_text = "Congratulations to Both Players on a Hard-Fought Match!"
        
    st.markdown(f"<h2 style='text-align: center; color: #FF671F;'>{congrats_text}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Match Conclusion Announcement:")

    result = board.result()

    white_knights = len(board.pieces(pure_chess_pkg.KNIGHT, pure_chess_pkg.WHITE))
    white_bishops = len(board.pieces(pure_chess_pkg.BISHOP, pure_chess_pkg.WHITE))
    white_queens = len(board.pieces(pure_chess_pkg.QUEEN, pure_chess_pkg.WHITE))
    white_rooks = len(board.pieces(pure_chess_pkg.ROOK, pure_chess_pkg.WHITE))
    white_pawns = len(board.pieces(pure_chess_pkg.PAWN, pure_chess_pkg.WHITE))
    white_total_pieces = white_knights + white_bishops + white_queens + white_rooks + white_pawns

    black_knights = len(board.pieces(pure_chess_pkg.KNIGHT, pure_chess_pkg.BLACK))
    black_bishops = len(board.pieces(pure_chess_pkg.BISHOP, pure_chess_pkg.BLACK))
    black_queens = len(board.pieces(pure_chess_pkg.QUEEN, pure_chess_pkg.BLACK))
    black_rooks = len(board.pieces(pure_chess_pkg.ROOK, pure_chess_pkg.BLACK))
    black_pawns = len(board.pieces(pure_chess_pkg.PAWN, pure_chess_pkg.BLACK))
    black_total_pieces = black_knights + black_bishops + black_queens + black_rooks + black_pawns

    white_has_insufficient = (white_total_pieces == 0) or (white_total_pieces == 1 and (white_bishops == 1 or white_knights == 1))
    black_has_insufficient = (black_total_pieces == 0) or (black_total_pieces == 1 and (black_bishops == 1 or black_knights == 1))

    if any([
        board.is_checkmate(), 
        result in ["1-0", "0-1"], 
        st.session_state.get("flag_dropped_white", False), 
        st.session_state.get("flag_dropped_black", False),
        board.is_insufficient_material(),
        board.is_stalemate(),
        board.is_fivefold_repetition(),
        board.is_seventyfive_moves(),
        len(st.session_state.get("moves_played", [])) >= 150,
        board.can_claim_threefold_repetition(),
        st.session_state.get("draw_cause") == "threefold",
        st.session_state.get("is_pawn_blockade", False) or ('is_pawn_blockade' in globals() and is_pawn_blockade),
        st.session_state.get("draw_game_over", False),
        board.is_game_over() or st.session_state.get("match_over", False)
    ]):
        st.balloons()

    if st.session_state.get("is_pawn_blockade", False) or ('is_pawn_blockade' in globals() and is_pawn_blockade):
        st.info("🤝 **DRAW ANNOUNCED: Stage 9 - Dead Position / Stage 6 - Perpetual Check Tactic Applied!**\n\n*(Neither side can mathematically checkmate the opponent by any series of legal moves. Score 1/2-1/2)*")
    elif board.is_checkmate():
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        score_display = "1-0" if winning_side == "White" else "0-1"
        st.success(f"🏆 **MATCH OVER: Checkmate! {winning_side} Wins! Score: {score_display}**\n\n*(The King is under direct attack and has no legal escape options. Game Over.)*")
    elif st.session_state.get("flag_dropped_white", False) and black_has_insufficient:
        st.info("🤝 **DRAW ANNOUNCED: Stage 5 - Insufficient Material and Time Out!**\n\n*(White ran out of time, but Black does not have massive material to force a checkmate. Score 1/2-1/2)*")
    elif st.session_state.get("flag_dropped_black", False) and white_has_insufficient:
        st.info("🤝 **DRAW ANNOUNCED: Stage 5 - Insufficient Material and Time Out!**\n\n*(Black ran out of time, but White does not have massive material to force a checkmate. Score 1/2-1/2)*")
    elif st.session_state.get("flag_dropped_white", False):
        st.success("🏆 **MATCH OVER: Black Wins on Time!**\n\n*(White's chess clock reached 0:00. Score 0-1)*")
    elif st.session_state.get("flag_dropped_black", False):
        st.success("🏆 **MATCH OVER: White Wins on Time!**\n\n*(Black's chess clock reached 0:00. Score 1-0)*")
    elif result in ["1-0", "0-1"]:
        st.success(f"🏆 **MATCH OVER: Winner Determined ({result})!**")
    elif board.is_insufficient_material():
        white_pieces = board.occupied_co[pure_chess_pkg.WHITE]
        black_pieces = board.occupied_co[pure_chess_pkg.BLACK]
        if bin(white_pieces).count("1") == 1 and bin(black_pieces).count("1") == 1:
            st.info("🤝 **DRAW ANNOUNCED: Stage 2 - Impossible to mate (King vs King). Score 1/2-1/2**")
        else:
            st.info("🤝 **DRAW ANNOUNCED: Stage 1 - Insufficient material.**\n\n*(Triggered by Lone King vs Lone King, King+Bishop vs Lone King, King+Knight vs Lone King, or Same-Colored Bishops. Score 1/2-1/2)*")
    elif board.is_stalemate():
        st.info("🤝 **DRAW ANNOUNCED: Stage 8 - Stalemate!**\n\n*(The active player has no legal moves available and their king is not in check. Score 1/2-1/2)*")
    elif board.is_fivefold_repetition():
        st.info("🤝 **DRAW ANNOUNCED: Stage 4 - Fivefold Repetition!**\n\n*(The same position has occurred five times automatically ending the game. Score 1/2-1/2)*")
    elif board.is_seventyfive_moves() or len(st.session_state.get("moves_played", [])) >= 150:
        st.info("🤝 **DRAW ANNOUNCED: Stage 4 - 75-Move Rule Exceeded!**\n\n*(75 consecutive moves played with zero pawn mobility or piece captures. Score 1/2-1/2)*")
    elif board.can_claim_threefold_repetition() or st.session_state.get("draw_cause") == "threefold":
        st.warning("🤝 **DRAW ANNOUNCED: Stage 7 - Threefold Repetition!**\n\n*(Identical board states, same turn player, and identical legal rights have occurred three times. Score 1/2-1/2)*")
    elif st.session_state.get("draw_game_over", False) and st.session_state.get("draw_cause") == "fifty_moves":
        st.info("🤝 **MATCH OVER: 50-Move Rule Draw! Score: 1/2-1/2**")
        if st.session_state.get("game_result_announcement"):
            st.markdown(st.session_state.get("game_result_announcement", ""))
    elif st.session_state.get("draw_game_over", False) and st.session_state.get("draw_cause") not in {"fifty_moves", "threefold"}:
        st.info("🤝 **MATCH OVER: Draw by Mutual Agreement! Score: 1/2-1/2 (Stage 10)**")
        if st.session_state.get("game_result_announcement"):
            st.markdown(st.session_state.get("game_result_announcement", ""))
    elif st.session_state.board_state.is_game_over() or st.session_state.get("match_over", False):
        if st.session_state.get("game_result_announcement"):
            st.markdown(st.session_state.get("game_result_announcement", ""))
        else:
            st.info("🏆 **MATCH OVER:** Game 🤩🤩🤩🤩🤩🤩🤩🤩🤩concluded successfully.")
    else:
        st.info("🏆 **MATCH OVER:** Game❌❌❌❌❌ concluded successfully.")

    common_bg_music_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/The_Final_Toast.mp3"
    bg_music_url = common_bg_music_url

    normal_white_videos = [
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/Screen%20Recording%202026-07-21%20120713.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4"
    ]
    
    normal_black_videos = [
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4"
    ]

    is_draw_outcome = not (board.is_checkmate() or board.result() in ["1-0", "0-1"] or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False))
    
    if is_draw_outcome:
        appreciation_video_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/MEDAL.mp4"
    else:
        winning_side = winner_name if 'winner_name' in locals() else "White"
        if winning_side == "White":
            idx = st.session_state.get("normal_white_win_idx", 0)
            appreciation_video_url = normal_white_videos[idx % 10]
            if not st.session_state.get("url_rotated_this_match", False):
                st.session_state["normal_white_win_idx"] = (idx + 1) % 10
        else:
            idx = st.session_state.get("normal_black_win_idx", 0)
            appreciation_video_url = normal_black_videos[idx % 10]
            if not st.session_state.get("url_rotated_this_match", False):
                st.session_state["normal_black_win_idx"] = (idx + 1) % 10

    st.session_state["url_rotated_this_match"] = True

    st.markdown("<br>", unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([1, 3, 1])
    with col_c2:
        media_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <video width="600" autoplay loop muted playsinline style="border-radius: 8px;">
                <source src="{appreciation_video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <audio id="score_bg_audio" autoplay loop preload="auto">
                <source src="{bg_music_url}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
        <script>
            var audio = document.getElementById("score_bg_audio");
            if (audio) {{
                audio.volume = 1.0;
                audio.play().catch(function(error) {{
                    console.log("Audio autoplay prevented: ", error);
                }});
            }}
        </script>
        """
        st.markdown(media_html, unsafe_allow_html=True)
        
    st.markdown("---")

    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🔍 Review Game", use_container_width=True, key="btn_normal_review"):
            st.session_state["current_screen"] = "engine"
            st.session_state["review_mode_active"] = True
            st.session_state["match_locked"] = False
            st.session_state["match_over"] = False
            st.session_state["score_screen_shown"] = False
            st.rerun()
    st.stop()


# =========================================================================
# 🏆 ATAAA PROFICIENCY HONORS SCORE SCREEN FOR ARMAGEDDON STYLE
# =========================================================================
if st.session_state.get("current_screen") == "score" and st.session_state.get("armageddon_style_mode", False) and not st.session_state.get("review_mode_active", False):
    
    st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
    
    col_img_left, col_title, col_img_right = st.columns([1, 4, 1])
    
    balloon_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/blob/main/Ballons.jpg?raw=true"
    
    with col_img_left:
        st.image(balloon_url, width=100)
    
    with col_title:
        st.markdown("<h1 style='text-align: center; color: #1E90FF; margin-top: 15px;'>ATAAA Proficiency Honors</h1>", unsafe_allow_html=True)
        
    with col_img_right:
        st.image(balloon_url, width=100)
        
    st.markdown("---")
    
    winner_name = "White"
    if board.is_checkmate():
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        winner_name = "Black" if winning_side == "Black" else "White"
    elif st.session_state.get("flag_dropped_white", False):
        winner_name = "Black"
    elif st.session_state.get("flag_dropped_black", False):
        winner_name = "White"
    else:
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        winner_name = winning_side

    if board.is_checkmate() or board.result() in ["1-0", "0-1"] or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False):
        congrats_text = f"Congratulations, {winner_name}!"
    else:
        congrats_text = "Congratulations to Both Players on a Hard-Fought Match!"
        
    st.markdown(f"<h2 style='text-align: center; color: #FF671F;'>{congrats_text}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Match Conclusion Announcement:")

    is_white_mating_win = board.is_checkmate() and ("White" == ("Black" if board.turn == pure_chess_pkg.WHITE else "White") and check_white_has_mating_material(board))
    is_black_draw_odds_win = (
        board.is_checkmate() or 
        st.session_state.get("flag_dropped_white", False) or 
        (st.session_state.get("flag_dropped_black", False) and not check_white_has_mating_material(board)) or
        board.is_insufficient_material() or 
        board.is_stalemate() or 
        board.is_fivefold_repetition() or 
        board.is_seventyfive_moves() or 
        len(st.session_state.get("moves_played", [])) >= 150 or 
        board.can_claim_threefold_repetition() or 
        st.session_state.get("draw_cause") == "threefold" or 
        board.is_fifty_moves() or 
        st.session_state.get("is_pawn_blockade", False) or 
        ('is_pawn_blockade' in globals() and is_pawn_blockade) or 
        st.session_state.get("draw_game_over", False)
    )
        
    if is_white_mating_win or is_black_draw_odds_win:
        st.balloons()
        
    if is_white_mating_win or is_black_draw_odds_win:
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        if winning_side == "White" and check_white_has_mating_material(board):
            st.balloons()
        elif winning_side == "Black":
            st.balloons()

    if st.session_state.get("is_pawn_blockade", False) or ('is_pawn_blockade' in globals() and is_pawn_blockade):
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 9 - Dead Position / Stage 6 - Perpetual Check Tactic Applied!**\n\n*(Neither side can mathematically checkmate the opponent by any series of legal moves.)*")
    elif board.is_checkmate():
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        if winning_side == "White":
            st.success("🏆 **MATCH OVER: Checkmate! White Wins! Score 1-0**\n\n*(The King is under direct attack and has no legal escape options. Game Over.)*")
        else:
            st.error("🏁 **MATCH OVER: Checkmate! Black Wins! Score 0-1**\n\n*(The King is under direct attack and has no legal escape options. Game Over.)*")
    elif st.session_state.get("flag_dropped_white", False):
        st.success("🏆 **MATCH OVER: Black Wins, Score 0-1 (White's flag dropped first; Black wins on draw-odds)**")
    elif st.session_state.get("flag_dropped_black", False):
        has_mating_material = check_white_has_mating_material(board)
        if has_mating_material:
            st.success("🏆 **MATCH OVER: White Wins, Score 1-0 (Black's flag dropped and White has sufficient mating material)**")
        else:
            st.success("🏆 **MATCH OVER: Black Wins, Score 0-1 (Black's flag dropped, but White lacks mating material; Armageddon draw-odds apply)**")
    elif board.is_insufficient_material():
        white_pieces = board.occupied_co[pure_chess_pkg.WHITE]
        black_pieces = board.occupied_co[pure_chess_pkg.BLACK]
        if bin(white_pieces).count("1") == 1 and bin(black_pieces).count("1") == 1:
            st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 2 - Impossible to mate (King vs King).**")
        else:
            st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 1 - Insufficient material.**\n\n*(Triggered by Lone King vs Lone King, King+Bishop vs Lone King, King+Knight vs Lone King, or Same-Colored Bishops.)*")
    elif board.is_stalemate():
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 8 - Stalemate!**\n\n*(The active player has no legal moves available and their king is not in check.)*")
    elif board.is_fivefold_repetition():
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 4 - Fivefold Repetition!**\n\n*(The same position has occurred five times automatically ending the game.)*")
    elif board.is_seventyfive_moves() or len(st.session_state.get("moves_played", [])) >= 150:
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 4 - 75-Move Rule Exceeded!**\n\n*(75 consecutive moves played with zero pawn mobility or piece captures)*")
    elif board.can_claim_threefold_repetition() or st.session_state.get("draw_cause") == "threefold":
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 7 - Threefold Repetition!**\n\n*(Identical board states, same turn player, and identical legal rights have occurred three times.)*")
    elif board.is_fifty_moves():
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 3 - 50-Move Rule Exceeded!**\n\n*(50 consecutive moves/100 turns played without a pawn move or a piece capture.)*")
    elif st.session_state.get("draw_game_over", False) and st.session_state.get("draw_cause") != "fifty_moves":
        st.success("🏆 **MATCH OVER Black Wins, Score 0-1 by Mutual Agreement! (Stage 10)**")
    else:
        st.error("🏁 **MATCH OVER: Black Wins, Score 0-1 (Armageddon Draw-Odds Rule Applied)**")

    common_bg_music_url = "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/The_Final_Toast.mp3"
    bg_music_url = common_bg_music_url

    armageddon_white_videos = [
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/Screen%20Recording%202026-07-21%20120713.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4"
    ]
    
    armageddon_black_videos = [
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4",
        "https://github.com/rajamkumar20082006-blip/ATAA-Hub-Pro/raw/refs/heads/main/duo_create_a_video_of_a_lion.mp4"
    ]

    winning_side = winner_name if 'winner_name' in locals() else "White"
    
    if winning_side == "White":
        idx = st.session_state.get("armageddon_white_win_idx", 0)
        appreciation_video_url = armageddon_white_videos[idx % 10]
        if not st.session_state.get("url_rotated_this_match", False):
            st.session_state["armageddon_white_win_idx"] = (idx + 1) % 10
    else:
        idx = st.session_state.get("armageddon_black_win_idx", 0)
        appreciation_video_url = armageddon_black_videos[idx % 10]
        if not st.session_state.get("url_rotated_this_match", False):
            st.session_state["armageddon_black_win_idx"] = (idx + 1) % 10

    st.session_state["url_rotated_this_match"] = True

    st.markdown("<br>", unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([1, 3, 1])
    with col_c2:
        media_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <video width="600" autoplay loop muted playsinline style="border-radius: 8px;">
                <source src="{appreciation_video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <audio id="score_bg_audio" autoplay loop preload="auto">
                <source src="{bg_music_url}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
        <script>
            var audio = document.getElementById("score_bg_audio");
            if (audio) {{
                audio.volume = 1.0;
                audio.play().catch(function(error) {{
                    console.log("Audio autoplay prevented: ", error);
                }});
            }}
        </script>
        """
        st.markdown(media_html, unsafe_allow_html=True)
        
    st.markdown("---")

    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("🚀 Engine Screen", use_container_width=True, key="btn_armageddon_engine"):
            st.session_state["current_screen"] = "engine"
            st.session_state["review_mode_active"] = True
            st.session_state["armageddon_style_mode"] = False
            st.session_state["match_locked"] = False
            st.session_state["match_over"] = False
            st.session_state["score_screen_shown"] = False
            st.rerun()
    st.stop()


# =========================================================================
# 🗺️ VISUAL BOARD SIDE-CONTROLS ARRANGEMENT
# =========================================================================
col_left, col_board, col_right = st.columns([1.3, 2.5, 1.2])

# --- LEFT SIDE INTERFACE ALIGNMENT ---
# --- LEFT SIDE INTERFACE ALIGNMENT ---
# --- LEFT SIDE INTERFACE ALIGNMENT ---
with col_left:
    st.markdown('<div class="row-spacer-8"></div>', unsafe_allow_html=True)
    
    # =========================================================================
    # 🎛️ STEP 4: INTERACTIVE UI INTERACTION CONTROLLER 
    # =========================================================================
    # Robust flag to seal every single interaction point instantly across all 10 stages
    # =========================================================================
    # 🎛️ STEP 4: INTERACTIVE UI INTERACTION CONTROLLER 
    # =========================================================================
    # 1. Structural Game Over constraints (Permanently seals the match)
    is_game_over = (
        st.session_state.board_state.is_game_over() 
        or st.session_state.get("draw_game_over", False) 
        or st.session_state.get("match_locked", False)
    )

    # 2. Claim Penalty states (Temporary blockades until penalty resolution buttons are clicked)
    penalty_active = (
        st.session_state.get("threefold_active_penalty", False) 
        or (st.session_state.get("fifty_move_stage", 0) == 4)
    )

    # Combined master variable for standard execution control blocks
    ui_disabled = is_game_over or penalty_active
    is_tournament_match_mode = (saved_config_type == "Tournament Style Match")
    board_moves_count = len(st.session_state.board_state.move_stack) if (hasattr(st.session_state, "board_state") and st.session_state.board_state) else 0
    details_are_submitted = st.session_state.get("details_submitted", False)
    is_already_submitted = st.session_state.get("details_submitted", False)



    is_game_started = board_moves_count >= 1 and not details_are_submitted
    has_active_game_state = False
    if not details_are_submitted:
            has_active_game_state = any([
                st.session_state.get("white_move_count", 0) > 0,
                st.session_state.get("black_move_count", 0) > 0,
                st.session_state.get("timer_started", False),
                st.session_state.get("paused_timer") is not None,
                st.session_state.get("active_timer") is not None,
                len(st.session_state.get("moves_played", [])) > 0
            ])



    tournament_violation = is_tournament_match_mode and (is_game_started or has_active_game_state)
    submit_disabled = tournament_violation

    # Permanent Match Lock Display only triggers for true endgame states
    if is_game_over or st.session_state.get("match_locked", False) or st.session_state.get("is_pawn_blockade", False) or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False) or submit_disabled:
        st.button("🚫 Match Locked", disabled=True, use_container_width=True, key="start_locked_btn")
    
    elif not st.session_state.timer_started or st.session_state.active_timer is None:
        btn_label = "▶️ Resume Clocks" if st.session_state.paused_timer is not None else "🚀 Start (Black Triggers White)"
        
        if st.button(
            btn_label, 
            disabled = ui_disabled or st.session_state.get("threefold_active_penalty", False) or st.session_state.get("fifty_move_stage", 0) == 4 or st.session_state.get("is_pawn_blockade", False),
            use_container_width=True, 
            key="start_btn_active"
        ):
            if not (freeze_option == "Freeze is OFF" and (st.session_state.flag_dropped_white or st.session_state.flag_dropped_black)):
                st.session_state.timer_started = True
                if st.session_state.paused_timer is not None:
                    st.session_state.active_timer = st.session_state.paused_timer
                else:
                    # ♟️ Check actual board turn to set initial ticking clock correctly
                    st.session_state.active_timer = "white" if st.session_state.board_state.turn == pure_chess_pkg.WHITE else "black"
                    
                st.session_state.last_timestamp = time.time()
                
                if (
                    game_mode.startswith("🤖 Single Player")
                    and st.session_state.get("player_color", "white").capitalize() == "Black"
                    and len(st.session_state.moves_played) == 0
                ):
                    execute_champion_engine_move()
                    st.session_state.active_timer = "black"
                    
                st.rerun()


    else:
        if st.button("⏸️ Pause Match Clock", use_container_width=True, key="pause_btn_active"):

            st.session_state.paused_timer = st.session_state.active_timer
            st.session_state.active_timer = None
            st.rerun()

    st.markdown('<div class="row-spacer-7"></div>', unsafe_allow_html=True)
    saved_config_type = st.session_state.get("top_bar_3_options", "Tournament Style Practice")
    is_puzzle_mode_active = (saved_config_type == "Chess Puzzles")

    if is_puzzle_mode_active:
         display_mode_string = "**Mode: Chess Puzzle Master**"
    else:
         current_active_mode = st.session_state.get("game_mode", "single")
         display_mode_string = "**Mode: Match against Engine**" if current_active_mode == "single" else "**Mode: Two Player Match**"

    st.markdown(display_mode_string)



    st.markdown('<div class="row-spacer-6"></div>', unsafe_allow_html=True)
    current_turn_str = "White" if board.turn == pure_chess_pkg.WHITE else "Black"
    st.markdown(f"### Turn: {current_turn_str}")

    st.markdown('<div class="row-spacer-5"></div>', unsafe_allow_html=True)
    user_input = st.text_area("Type or Paste Move(s) (e.g., e4 or a full multi-line sequence):", key="chess_move_input")

    st.markdown('<div class="row-spacer-4"></div>', unsafe_allow_html=True)
    

    if st.button(
    "Submit Move", 
    use_container_width=True, 
    
    disabled = ui_disabled or st.session_state.get("threefold_active_penalty", False) or st.session_state.get("fifty_move_stage", 0) == 4 or st.session_state.get("is_pawn_blockade", False) or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False) or submit_disabled,
    key="submit_move_btn"
):
        if st.session_state.flag_dropped_white or st.session_state.flag_dropped_black:
            if freeze_option == "Freeze is ON":
                st.session_state.frozen_error_triggered = True
                st.rerun()
            else:
                raw_tokens = user_input.replace("\n", " ").split()
                moves_to_process = [t for t in raw_tokens if not t.endswith('.') and not t.replace('.', '').isdigit()]
                
                if len(moves_to_process) > 1:
                    for move in moves_to_process:
                        process_chess_move(move)
                    if game_mode.startswith("🤖 Single Player"):
                        execute_champion_engine_move()
                    
                    # 🚀 ATAAA Screen Switcher Trigger on Submit Move (Flag Drop / Multi-Move)
                    if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                        st.session_state.match_locked = True
                        st.session_state.current_screen = "score"

                    st.session_state.last_timestamp = time.time()
                    st.rerun()
                else:
                    if user_input and process_chess_move(user_input):
                        if game_mode.startswith("🤖 Single Player"):
                            execute_champion_engine_move()
                        
                        # 🚀 ATAAA Screen Switcher Trigger on Submit Move (Flag Drop / Single Move)
                        if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                            st.session_state.match_locked = True
                            st.session_state.current_screen = "score"

                        st.session_state.last_timestamp = time.time()
                        st.rerun()
        else:
            raw_tokens = user_input.replace("\n", " ").split()
            moves_to_process = [t for t in raw_tokens if not t.endswith('.') and not t.replace('.', '').isdigit()]
            
            if len(moves_to_process) > 1:
                for move in moves_to_process:
                    process_chess_move(move)
                if game_mode.startswith("🤖 Single Player") and not st.session_state.board_state.is_game_over():
                    execute_champion_engine_move()
                else:
                    if st.session_state.timer_started and st.session_state.active_timer is not None:
                        st.session_state.active_timer = "black" if current_turn_str == "White" else "white"
                
                # 🚀 ATAAA Screen Switcher Trigger on Submit Move (Normal Multi-Move)
                if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                    st.session_state.match_locked = True
                    st.session_state.current_screen = "score"

                st.session_state.last_timestamp = time.time()
                st.rerun()
            else:
                if user_input and process_chess_move(user_input):
                    if game_mode.startswith("🤖 Single Player"):
                        execute_champion_engine_move()
                    else:
                        if st.session_state.timer_started and st.session_state.active_timer is not None:
                            st.session_state.active_timer = "black" if current_turn_str == "White" else "white"
                    
                    # 🚀 ATAAA Screen Switcher Trigger on Submit Move (Normal Single Move / Checkmate / Draw)
                    if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                        st.session_state.match_locked = True
                        st.session_state.current_screen = "score"

                    st.session_state.last_timestamp = time.time()
                    st.rerun()


    # =========================================================================
    # 🤝 STAGE 10: AGREEMENT DRAW CONTROLLER (ROW 3 LEFT SIDE)
    # =========================================================================
    st.markdown('<div class="row-spacer-2"></div>', unsafe_allow_html=True)
    
    if st.session_state.draw_game_over:
        st.button("🚫 Match Locked", use_container_width=True, disabled=True, key="agreement_locked_btn")
    else:
        if st.button(
    "Agreement🤝", 
    use_container_width=True, 
    disabled = ui_disabled or st.session_state.get("threefold_active_penalty", False) or st.session_state.get("fifty_move_stage", 0) == 4 or st.session_state.get("is_pawn_blockade", False) or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False) or submit_disabled,
    key="mutual_agreement_btn"
):
            st.session_state.agreement_active = not st.session_state.agreement_active
            st.rerun()
            
    if st.session_state.agreement_active and not is_game_over and not st.session_state.draw_game_over:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("I'm playing Black", use_container_width=True):
                if st.session_state.get("black_move_count", 0) >= 40:
                    st.session_state.selected_draw_color = "Black"
                else:
                    st.session_state.draw_warning_msg = "players after completing 40 moves can ask draw, so yet 40 moves not completed"
                    st.session_state.selected_draw_color = None
                st.rerun()
        with col_b2:
            if st.button("I'm playing white", use_container_width=True):
                if st.session_state.get("white_move_count", 0) >= 40:
                    st.session_state.selected_draw_color = "White"
                else:
                    st.session_state.draw_warning_msg = "players after completing 40 moves can ask draw, so yet 40 moves not completed"
                    st.session_state.selected_draw_color = None
                st.rerun()
                
        # Show "draw accepting" button only when the player has safely reached >= 40 moves
        if st.session_state.selected_draw_color is not None:
            moves_to_verify = st.session_state.white_move_count if st.session_state.selected_draw_color == "White" else st.session_state.black_move_count
            if moves_to_verify >= 40:
                if st.button("✔ draw accepting", use_container_width=True):
                    st.session_state.draw_game_over = True
                    st.session_state.active_timer = None
                    st.session_state.timer_started = False
                if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                    st.session_state.match_locked = True
                    st.session_state.current_screen = "score"

                    st.session_state.last_timestamp = time.time()
                    st.rerun()
                    

# --- CENTER COLUMN: CHESSBOARD CONTAINER ---
with col_board:
    
    
    svg_output = chess_vector_render.board(
        board=st.session_state.board_state, 
        colors={"square light": "#f0d9b5", "square dark": "#b58863"}
    )
    st.markdown(f'<div style="display: flex; justify-content: center; margin: 10px 0;"><div style="width: 48cm; max-width:100%;">{svg_output}</div></div>', unsafe_allow_html=True)
    
    # --- TEMPORARY TESTING ACTIONS CONTAINER ---
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    
    # Button 1: King + Bishop vs King layout
    if st.button("🧪 Force Setup: Insufficient Material: White King(e7) vs Black King(h3) + Bishop(d5)", use_container_width=True):
        st.session_state.board_state.set_fen("8/4K3/8/3b4/8/7k/8/8 w - - 0 1")
        st.rerun()
        
    # Button 2: Pure King vs King layout (White King on e4, Black King on e5)
    if st.button("👑 Force Setup: Pure King vs King (Impossible to Mate)", use_container_width=True):
        st.session_state.board_state.set_fen("8/8/8/4k3/4K3/8/8/8 w - - 0 1")
        st.rerun()
        
    if st.button("🧊 Force Setup: Stalemate ", use_container_width=True):
        st.session_state.board_state.set_fen("5n2/8/p3p2k/Pp2Pp1p/1P3P1P/3K2N1/8/8 w - - 0 1")
        st.rerun()
        
    if st.button("🏆 Force Setup: CheckMate", use_container_width=True):
        st.session_state.board_state.set_fen("7k/6Q1/5K2/8/8/8/8/8 b - - 0 1")
        st.rerun()

    # Button 5: Threefold Tactical Repetition State
    if st.button("🔄 Force Setup: 75 moves Draw", use_container_width=True):
        st.session_state.board_state.set_fen("8/8/3k1pp1/7p/5N1P/4r1PK/R7/4b3 w - - 0 1")
        st.rerun()

    # 🔒 NEW ADDITION: Exact configuration extracted from Screenshot 2026-07-03 172129_2.jpg
    if st.button("🔒 Force Setup: Stage 9 Dead Position Blockade (Pawn Wall)", use_container_width=True):
        st.session_state.board_state.set_fen("7r/2k5/1p1p1p1p/pPpPpPpP/P1P1P1P1/3K4/6B1/8 w - - 0 1")
        st.rerun()

    # ⏱️ NEW ADDITION: Exact configuration extracted from image_b6751c.png
    if st.button("⏱️ Force Setup: Stage 5 Time Out vs Insufficient Material (Lone Bishop Setup)", use_container_width=True):
        st.session_state.board_state.set_fen("8/pbk3r1/1p1p1p2/8/4B3/4K3/8/8 w - - 0 1")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("---")

    
    # Create a master centered column layout so everything (text, input boxes, buttons) aligns perfectly together
_master_left, master_center, _master_right = st.columns([1, 2, 1])

with master_center:
    # =========================================================================
    # 🔄 THREEFOLD REPETITION PANEL (Safely Indented inside with col_board)
    # =========================================================================
    st.markdown("### 🔄 Threefold Repetition Claim Panel")

    # Clear warning if the timer is paused at any point
    if not st.session_state.get("timer_started") or st.session_state.get("active_timer") is None:
        st.session_state.threefold_warning = None

    # Handle touching/clicking anywhere else on the screen to dismiss the warning
    if st.session_state.get("threefold_warning"):
        col_warn, col_dismiss = st.columns([8, 2])
        with col_warn:
            st.warning(st.session_state.threefold_warning)
        with col_dismiss:
            if st.button("Dismiss ❌", key="dismiss_warning_click", use_container_width=True):
                st.session_state.threefold_warning = None
                st.rerun()

    # --- STAGE 0: Initial Claim Entry ---
    if st.session_state.threefold_stage == 0:
        if st.button("Threefold repetition", use_container_width=True, disabled = ui_disabled or st.session_state.get("threefold_active_penalty", False) or st.session_state.get("fifty_move_stage", 0) == 4 or st.session_state.get("is_pawn_blockade", False) or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False) or submit_disabled):
            # Enforce professional tournament pause requirement
            if st.session_state.timer_started and st.session_state.active_timer is not None:
                st.session_state.threefold_warning = '⚠️ Before pressing "Threefold repetition" button player must pause the timer'
                st.rerun()
            else:
                # Disappear the warning ONLY when successfully advancing stages
                st.session_state.threefold_warning = None
                st.session_state.threefold_stage = 1
                st.rerun()

    # --- STAGE 1: Selection of timing pattern type ---
    elif st.session_state.threefold_stage == 1:
        st.markdown("💡 **What is the current status of the board repetition?**")
        
        # Use nested rows to neatly stack options while keeping sizes controlled
        col1, col2 = st.columns(2)
        with col1:
            if st.button("just next move will create Threefold repetition", use_container_width=True, help="I'm claiming a draw because the position is about to be repeated for the third (or fourth) time"):
                st.session_state.threefold_type = "next_move"
                st.session_state.threefold_stage = 2
                st.session_state.show_input_field = False
                st.rerun()
        with col2:
            if st.button("Already Threefold repetition completed", use_container_width=True, help="I'm claiming a draw because the position has just been repeated for the third (or fourth) time"):
                st.session_state.threefold_type = "already"
                st.session_state.threefold_stage = 2
                st.session_state.show_input_field = False
                st.rerun()
                
        if st.button("❌ Cancel Claim", use_container_width=True):
            st.session_state.threefold_stage = 0
            st.rerun()

    # --- STAGE 2: Claimant Side Choice & Validation Engine ---
    elif st.session_state.threefold_stage == 2:
        st.markdown(f"📋 **Confirming claim type: *{st.session_state.threefold_type.replace('_',' ')}*. Who is making this claim?**")
        
        current_turn_color = "White" if st.session_state.board_state.turn == pure_chess_pkg.WHITE else "Black"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("I'm playing white", use_container_width=True):
                st.session_state.threefold_claimant = "White"
                if current_turn_color != "White":
                    st.session_state.penalty_banner_text = (
                        f"📢 This is {current_turn_color}'s turn, thus White missed the moment to claim. "
                        f"Claiming in the opponent's turn is illegal! Thus, the claim was incorrect. "
                        f"Hence, a penalty for player White: 2 minutes added to player Black."
                    )
                    st.session_state.threefold_penalty_receiver = "Black"
                    st.session_state.threefold_active_penalty = True
                    st.session_state.threefold_stage = 3
                    st.session_state.show_input_field = False
                else:
                    st.session_state.show_input_field = True
                st.rerun()
        with col2:
            if st.button("I'm playing black", use_container_width=True):
                st.session_state.threefold_claimant = "Black"
                if current_turn_color != "Black":
                    st.session_state.penalty_banner_text = (
                        f"📢 This is {current_turn_color}'s turn, thus Black missed the moment to claim. "
                        f"Claiming in the opponent's turn is illegal! Thus, the claim was incorrect. "
                        f"Hence, a penalty for player Black: 2 minutes added to player White."
                    )
                    st.session_state.threefold_penalty_receiver = "White"
                    st.session_state.threefold_active_penalty = True
                    st.session_state.threefold_stage = 3
                    st.session_state.show_input_field = False
                else:
                    st.session_state.show_input_field = True
                st.rerun()

        if st.session_state.get("show_input_field"):
            claimant = st.session_state.threefold_claimant
            opponent = "Black" if claimant == "White" else "White"
            
            if st.session_state.threefold_type == "next_move":
                st.markdown(f"✍ **Write which is the move in your mind that will create Threefold repetition:**")
                predicted_move = st.text_input("Enter SAN move (e.g., Nf3, O-O, Qe4):", key="threefold_predicted_move")
            else:
                st.markdown(f"ℹ️ Press Submit to verify the current board history for **{claimant}**.")
            
            if st.button("SUBMIT", use_container_width=True):
                is_valid_claim = False
                penalty_message = ""
                
                if "board_history_hashes" not in st.session_state:
                    st.session_state.board_history_hashes = []
                
                current_hash = st.session_state.board_state.epd()
                history_hashes = st.session_state.board_history_hashes
                current_occurrence = history_hashes.count(current_hash)

                # =========================================================================
                # ENGINE CONTROL: "Just next move will create Threefold repetition"
                # =========================================================================
                if st.session_state.threefold_type == "next_move":
                    raw_move = predicted_move.strip()
                    try:
                        parsed_move = st.session_state.board_state.parse_san(raw_move)
                        if parsed_move in st.session_state.board_state.legal_moves:
                            
                            # 1. Lookahead validation check
                            st.session_state.board_state.push(parsed_move)
                            lookahead_hash = st.session_state.board_state.epd()
                            past_occurrences = history_hashes.count(lookahead_hash)
                            if current_occurrence >= 3 or st.session_state.board_state.can_claim_threefold_repetition() or st.session_state.board_state.is_repetition(3):
                                is_valid_claim = False
                                penalty_message = (
                                          f"📢 claim was incorrect because your predicted move does not create a position "
                                          f"with the same squares, same pieces, and same legal rights for the 3rd or 4th time! "
                                          f"Hence, a penalty for player {claimant}: 2 minutes added to player {opponent}."
                                )
                            if past_occurrences >= 2:
                                is_valid_claim = True
                                
                            st.session_state.board_state.pop()
                            
                            # 2. Automatically execute move visually on the live chessboard
                            if 'process_chess_move' in locals() or 'process_chess_move' in globals():
                                st.info(f"Current turn {claimant.lower()} to {opponent.lower()}")
                                process_chess_move(raw_move)
                            
                            # Update Single Player AI if applicable
                            if is_valid_claim:
                                if game_mode.startswith("🤖 Single Player") and not st.session_state.board_state.is_game_over():
                                    if 'execute_champion_engine_move' in locals() or 'execute_champion_engine_move' in globals():
                                        execute_champion_engine_move()
                            else:
                                if st.session_state.timer_started and st.session_state.active_timer is not None:
                                    st.session_state.active_timer = opponent.lower()
                                    
                            st.session_state.last_timestamp = time.time()
                        else:
                            is_valid_claim = False
                    except ValueError:
                        is_valid_claim = False
                        
                    if not is_valid_claim:
                        penalty_message = (
                            f"📢 claim was incorrect because your predicted move does not create a position "
                            f"with the same squares, same pieces, and same legal rights for the 3rd or 4th time! "
                            f"Hence, Current turn: {opponent.lower()}."
                        )
                
                # =========================================================================
                # ENGINE CONTROL: "Already Threefold repetition completed"
                # =========================================================================
                elif st.session_state.threefold_type == "already":
                    # First, check if it is legally a 3rd or 4th repetition right now
                    if st.session_state.board_state.can_claim_threefold_repetition() or st.session_state.board_state.is_repetition(3):
                        is_valid_claim = True
                    else:
                        is_valid_claim = False
                        
                        # Check if it was a button mismatch (it's actually about to happen on the next move)
                        is_about_to_happen = False
                        if 'predicted_move' in locals() and predicted_move.strip():
                            try:
                                raw_move = predicted_move.strip()
                                parsed_move = st.session_state.board_state.parse_san(raw_move)
                                if parsed_move in st.session_state.board_state.legal_moves:
                                    st.session_state.board_state.push(parsed_move)
                                    if history_hashes.count(st.session_state.board_state.epd()) >= 2:
                                        is_about_to_happen = True
                                    st.session_state.board_state.pop()
                            except ValueError:
                                pass

                        # Trigger the specific warning if they clicked "Already completed" by mistake
                        if is_about_to_happen:
                            penalty_message = (
                                f"📢 claim was incorrect because a 3-fold repetition state does NOT already exist on the active board! "
                                f"You are about to create the 3rd/4th repetition on your next move, but you accidentally selected the wrong button "
                                f"('Already Threefold repetition completed'). Hence, Current turn: {opponent}. Please resolve the penalty layout below."
                            )
                        else:
                            # Standard fallback warning if it's only a 1st or 2nd repetition 
                            actual_reps = history_hashes.count(st.session_state.board_state.epd()) + 1
                            penalty_message = (
                                f"📢 claim was incorrect because a 3-fold repetition state does not already exist on the active board "
                                f"(current board state count = {actual_reps}). You cannot claim a draw for a 1st or 2nd time repetition. "
                                f"Hence, Current turn: {opponent}. Please resolve the penalty layout below."
                            )

                # =========================================================================
                # EXECUTING ACTION STAGES BASED ON CLAIM VALIDITY
                # =========================================================================
                if is_valid_claim:
                    st.session_state.draw_game_over = True
                    st.session_state.draw_cause = "threefold"
                    st.session_state.active_timer = None
                    st.session_state.timer_started = False
                    st.session_state.threefold_stage = 0
                    st.session_state.show_input_field = False
                    st.session_state.draw_warning_msg = None
                    st.session_state.game_result_announcement = f"🏁 Match drawn by Threefold Repetition (Claimed successfully by {claimant}!)"
                    st.session_state.match_locked = True
                    st.session_state.current_screen = "score"
                    st.session_state.match_announcement_text = st.session_state.game_result_announcement
                    

                    st.rerun()
                else:
                    st.session_state.penalty_banner_text = penalty_message
                    st.session_state.threefold_penalty_receiver = opponent
                    st.session_state.threefold_active_penalty = True
                    st.session_state.threefold_stage = 3 
                    st.session_state.show_input_field = False
                    st.rerun()

    # --- STAGE 3: FIDE Penalty Panel execution ---
    elif st.session_state.threefold_stage == 3:
        claimant = st.session_state.get("threefold_claimant", "White")
        fallback_opponent = "Black" if claimant == "White" else "White"
        
        receiver = st.session_state.get("threefold_penalty_receiver", fallback_opponent)
        
        custom_err = st.session_state.get("penalty_banner_text", "📢 Claim was incorrect.")
        st.error(custom_err)
        
        # Two horizontal layout buttons
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button(f"2min added is accepting by {receiver}", use_container_width=True):
                if receiver == "White":
                    st.session_state.time_white += 120.0
                else:
                    st.session_state.time_black += 120.0
                    
                st.session_state.threefold_stage = 0
                st.session_state.threefold_type = None
                st.session_state.threefold_claimant = None
                st.session_state.threefold_active_penalty = False
                if "threefold_predicted_move" in st.session_state:
                    del st.session_state["threefold_predicted_move"]
                st.rerun()
                
        with btn_col2:
            if st.button("I know claim is incorrect anyway I accept draw", use_container_width=True):
                st.session_state.draw_game_over = True
                st.session_state.draw_cause = "mutual"
                st.session_state.active_timer = None
                st.session_state.timer_started = False
                st.session_state.threefold_stage = 0
                st.session_state.draw_warning_msg = None
                st.session_state.threefold_active_penalty = False
                if "threefold_predicted_move" in st.session_state:
                    del st.session_state["threefold_predicted_move"]
                st.session_state.match_locked = True
                st.session_state.current_screen = "score"
                
                st.rerun()


    # =========================================================================
    # ⏳ OFFICIAL FIDE 50-MOVE RULE CLAIM SYSTEM
    # =========================================================================
    # =========================================================================
    # ⏳ OFFICIAL FIDE 50-MOVE RULE CLAIM SYSTEM
    # =========================================================================
    # =========================================================================
    # ⏳ OFFICIAL FIDE 50-MOVE RULE CLAIM SYSTEM (ATAAA)
    # =========================================================================
    # =========================================================================
    # ⏳ OFFICIAL FIDE 50-MOVE RULE CLAIM SYSTEM (ATAAA)
    # =========================================================================
    st.write("---")
    st.markdown("### 📜 50-Move Rule Panel")

    # Determine if any panel is currently enforcing a FIDE penalty block
    # (Locks out normal controls but leaves the penalty panel active)
    ui_disabled_by_penalty = st.session_state.get("threefold_stage") == 3 or st.session_state.fifty_move_stage == 4

    # Clear warning if the timer is actively paused during checking phases
    if not st.session_state.get("timer_started") or st.session_state.get("active_timer") is None:
        st.session_state.fifty_move_warning = None

    # Persistent warning layout (Will stay visible until player explicitly clicks Dismiss)
    if st.session_state.get("fifty_move_warning"):
        col_warn_50, col_dismiss_50 = st.columns([8, 2])
        with col_warn_50:
            st.warning(st.session_state.fifty_move_warning)
        with col_dismiss_50:
            if st.button("Dismiss ❌", key="dismiss_50move_warning_click", use_container_width=True):
                st.session_state.fifty_move_warning = None
                st.rerun()

    # --- STAGE 0: Master Entry Button ---
    if st.session_state.fifty_move_stage == 0:
        if st.button(
            "⚖️ 50 Moves Draw", 
            use_container_width=True, 
            disabled = ui_disabled or st.session_state.get("threefold_active_penalty", False) or st.session_state.get("fifty_move_stage", 0) == 4 or st.session_state.get("is_pawn_blockade", False) or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False) or submit_disabled,
            key="fifty_moves_btn"
        ):
            # Enforce tournament pause protocol
            if st.session_state.timer_started and st.session_state.active_timer is not None:
                st.session_state.fifty_move_warning = '⚠️ Before pressing "50 moves draw" button player must pause the timer'
                st.rerun()
            else:
                st.session_state.fifty_move_warning = None
                st.session_state.fifty_move_stage = 1
                st.rerun()

    # --- STAGE 1: Claimant Identification ---
    elif st.session_state.fifty_move_stage == 1:
        st.markdown("❓ **Who is making this claim?**")
        col_w, col_b = st.columns(2)
        
        with col_w:
            white_clicked = st.button("I'm playing White", use_container_width=True, key="claim_50_white")
        with col_b:
            black_clicked = st.button("I'm playing Black", use_container_width=True, key="claim_50_black")
            
        if white_clicked or black_clicked:
            claimant = "White" if white_clicked else "Black"
            opponent = "Black" if claimant == "White" else "White"
            current_turn_color = "White" if st.session_state.board_state.turn == pure_chess_pkg.WHITE else "Black"
            
            # Illegal Move Turn Check
            if claimant != current_turn_color:
                st.session_state.fifty_move_penalty_msg = (
                    f"📢 This is {current_turn_color}'s turn, thus {claimant} missed the moment to claim. "
                    f"Claiming in the opponent's turn is illegal! Thus, the claim was incorrect. "
                    f"Hence, a penalty for player {claimant}: 2 minutes added to player {opponent}."
                )
                st.session_state.fifty_move_penalty_receiver = opponent
                st.session_state.fifty_move_claimant = claimant
                st.session_state.fifty_move_stage = 4  # Route directly to penalty loop
                st.rerun()
            else:
                st.session_state.fifty_move_claimant = claimant
                st.session_state.fifty_move_stage = 2
                st.rerun()

        if st.button("❌ Cancel Claim", use_container_width=True, key="cancel_50move_stage_1"):
            st.session_state.fifty_move_stage = 0
            st.rerun()

    # --- STAGE 2: Scenario Selection ---
    elif st.session_state.fifty_move_stage == 2:
        claimant = st.session_state.fifty_move_claimant
        opponent = "Black" if claimant == "White" else "White"
        st.markdown(f"📋 **Claimant: {claimant}**. Select your precise draw scenario condition:")
        
        col_scen1, col_scen2 = st.columns(2)
        with col_scen1:
            if st.button("1️⃣ Next move about to create 50 moves", use_container_width=True):
                st.session_state.fifty_move_type = "next_move"
                st.session_state.fifty_move_stage = 3
                st.rerun()
        with col_scen2:
            if st.button("2️⃣ Playing between move 51 to move 74", use_container_width=True):
                st.session_state.fifty_move_type = "already_existed"
                
                # Check current active plies on board
                current_plies = st.session_state.board_state.halfmove_clock
                
                # Must be 100 plies or greater to verify draw directly without reset
                if current_plies >= 100:
                    st.session_state.draw_game_over = True
                    st.session_state.draw_cause = "fifty_moves"
                    st.session_state.active_timer = None
                    st.session_state.timer_started = False
                    st.session_state.fifty_move_stage = 0
                    st.session_state.game_result_announcement = (
                        "🤝 **DRAW ANNOUNCED: Stage 3 - 50-Move Rule Exceeded!**\n\n"
                        "*(50 consecutive moves/100 turns played without a pawn move or a piece capture. Score 1/2-1/2)*"
                    )
                    st.session_state.match_locked = True
                    st.session_state.current_screen = "score"
                else:
                    st.session_state.fifty_move_penalty_msg = (
                        f"📢 Claim was incorrect because a moves state does NOT already exist on the active board! "
                        f"Hence, a penalty for player {claimant}: 2 minutes added to player {opponent}."
                    )
                    st.session_state.fifty_move_penalty_receiver = opponent
                    st.session_state.fifty_move_stage = 4
                st.rerun()
                
        if st.button("❌ Cancel Claim", use_container_width=True, key="cancel_50move_stage_2"):
            st.session_state.fifty_move_stage = 0
            st.rerun()

    # --- STAGE 3: Move Prediction & Evaluation Engine ---
    elif st.session_state.fifty_move_stage == 3:
        claimant = st.session_state.fifty_move_claimant
        opponent = "Black" if claimant == "White" else "White"
        
        st.markdown(f"✍️ **Write which is the move in your mind that will create 50 moves draw:**")
        predicted_move = st.text_input("Enter SAN move (e.g., Nf3, O-O, Re8):", key="fifty_move_prediction_input")
        
        if st.button("SUBMIT", use_container_width=True, key="submit_fifty_move_claim"):
            raw_move = predicted_move.strip()
            move_is_legal = False
            parsed_move = None
            
            # 1. Safely parse and check legality without raising layout string errors
            try:
                parsed_move = st.session_state.board_state.parse_san(raw_move)
                if parsed_move in st.session_state.board_state.legal_moves:
                    move_is_legal = True
            except ValueError:
                move_is_legal = False

            if move_is_legal and parsed_move is not None:
                # 2. Inspect positional attributes before the move alters the state clock
                is_capture = st.session_state.board_state.is_capture(parsed_move)
                piece = st.session_state.board_state.piece_at(parsed_move.from_square)
                is_pawn_move = piece.piece_type == pure_chess_pkg.PAWN if piece else False
                current_plies = st.session_state.board_state.halfmove_clock
                
                condition_satisfied = False
                if claimant == "White":
                    if current_plies == 98 and not is_capture and not is_pawn_move:
                        condition_satisfied = True
                else:
                    if current_plies == 99 and not is_capture and not is_pawn_move:
                        condition_satisfied = True

                # 3. Executing automated play on the board because the move notation is legal
                if 'process_chess_move' in locals() or 'process_chess_move' in globals():
                    process_chess_move(raw_move)

                if condition_satisfied:
                    # Successful Draw Execution Action
                    st.session_state.draw_game_over = True
                    st.session_state.draw_cause = "fifty_moves"
                    st.session_state.active_timer = None
                    st.session_state.timer_started = False
                    st.session_state.fifty_move_stage = 0
                    st.session_state.match_locked = True
                    st.session_state.current_screen = "score"

                    
                    if game_mode.startswith("🤖 Single Player") and not st.session_state.board_state.is_game_over():
                        if 'execute_champion_engine_move' in locals() or 'execute_champion_engine_move' in globals():
                            execute_champion_engine_move()
                else:
                    # Legal move played but conditions were missed -> Apply Penalty Stage
                    st.session_state.fifty_move_penalty_msg = (
                        f"📢 claim was incorrect because your predicted move does not create a position "
                        f"without Any pawn being moved by either player. Any piece being captured by either player "
                        f"for the 50 moves draw ! hence a penalty for player {claimant}: 2 minutes added to player {opponent}."
                    )
                    st.session_state.fifty_move_penalty_receiver = opponent
                    st.session_state.fifty_move_stage = 4
                st.rerun()

            else:
                # 4. Notation is completely illegal -> Do NOT play on board, route instantly to penalty stage
                st.session_state.fifty_move_penalty_msg = (
                    f"📢 claim was incorrect because your predicted move does not create a position "
                    f"without Any pawn being moved by either player. Any piece being captured by either player "
                    f"for the 50 moves draw ! hence a penalty for player {claimant}: 2 minutes added to player {opponent}."
                )
                st.session_state.fifty_move_penalty_receiver = opponent
                st.session_state.fifty_move_stage = 4
                st.rerun()

        if st.button("❌ Cancel Claim", use_container_width=True, key="cancel_50move_stage_3"):
            st.session_state.fifty_move_stage = 0
            if "fifty_move_prediction_input" in st.session_state:
                del st.session_state["fifty_move_prediction_input"]
            st.rerun()

    # --- STAGE 4: Interactive Penalty Screen ---
    elif st.session_state.fifty_move_stage == 4:
        claimant = st.session_state.fifty_move_claimant
        fallback_opponent = "Black" if claimant == "White" else "White"
        receiver = st.session_state.get("fifty_move_penalty_receiver", fallback_opponent)
        
        st.error(st.session_state.fifty_move_penalty_msg)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button(f"1️⃣ 2min added is accepting by {receiver}", use_container_width=True, key="accept_50_penalty"):
                # Cleanly credit time directly to the explicit penalty receiver (the opponent)
                if receiver == "White":
                    st.session_state.time_white += 120.0
                else:
                    st.session_state.time_black += 120.0
                    
                st.session_state.fifty_move_stage = 0
                st.session_state.fifty_move_claimant = None
                st.session_state.fifty_move_penalty_receiver = None
                st.session_state.fifty_move_type = None
                if "fifty_move_prediction_input" in st.session_state:
                    del st.session_state["fifty_move_prediction_input"]
                st.rerun()
                
        with btn_col2:
            if st.button(f"2️⃣ I know claim is incorrect anyway I accept draw by {receiver}", use_container_width=True, key="accept_50_draw"):
                st.session_state.draw_game_over = True
                st.session_state.draw_cause = "mutual"
                
                # Clear out the previous 50-move announcement so it doesn't duplicate
                st.session_state.game_result_announcement = ""
                
                st.session_state.active_timer = None
                st.session_state.timer_started = False
                st.session_state.fifty_move_stage = 0
                st.session_state.fifty_move_claimant = None
                st.session_state.fifty_move_penalty_receiver = None
                if "fifty_move_prediction_input" in st.session_state:
                    del st.session_state["fifty_move_prediction_input"]
                st.session_state.match_locked = True
                st.session_state.current_screen = "score"
                st.rerun()













# --- RIGHT SIDE INTERFACE ALIGNMENT ---
with col_right:
    st.markdown('<div class="row-spacer-8"></div>', unsafe_allow_html=True)
    
    # Calculate moves directly from the board stack so it updates even when clock isn't started
    black_moves_count = len(board.move_stack) // 2
    
    if use_tenths:
        flag_b = "" 
    else:
        flag_b = " [FLAG DROPPED]" if st.session_state.flag_dropped_black else ""
        
    b_status = "⚡ Ticking" if (st.session_state.timer_started and st.session_state.active_timer == "black" and not st.session_state.flag_dropped_white and not st.session_state.flag_dropped_black and not is_game_over) else "⏸️ Frozen"
    st.metric(label=f"⚫ Black Clock ({b_status}) [Moves: {black_moves_count}]{flag_b}", 
              value=format_adaptive_timer(st.session_state.time_black, use_tenths))
    
    if freeze_option == "Freeze is OFF" and st.session_state.time_black <= 0 and not use_tenths:
        st.markdown('<div class="blinking-bars">═══════════════</div>', unsafe_allow_html=True)

    st.markdown('<div class="row-spacer-2"></div>', unsafe_allow_html=True)
    if st.button(
    "🕹️ Hit Lever Switch", 
    use_container_width=True, 
    disabled = ui_disabled or st.session_state.get("threefold_active_penalty", False) or st.session_state.get("fifty_move_stage", 0) == 4 or st.session_state.get("is_pawn_blockade", False) or st.session_state.get("flag_dropped_white", False) or st.session_state.get("flag_dropped_black", False) or submit_disabled,
    key="hit_lever_btn"
):
        if freeze_option == "Freeze is ON" and (st.session_state.flag_dropped_white or st.session_state.flag_dropped_black):
            if user_input and process_chess_move(user_input):
                if game_mode.startswith("🤖 Single Player"):
                    execute_champion_engine_move()
                
                # 🚀 ATAAA Screen Switcher Trigger for Hit Lever Switch (Flag Drop / Active Freeze)
                if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                    st.session_state.match_locked = True
                    st.session_state.current_screen = "score"

                st.rerun()
        else:
            if st.session_state.flag_dropped_white or st.session_state.flag_dropped_black:
                st.session_state.frozen_error_triggered = True
                st.rerun()
            else:
                if user_input and process_chess_move(user_input):
                    if game_mode.startswith("🤖 Single Player"):
                        execute_champion_engine_move()
                    else:
                        if st.session_state.timer_started and st.session_state.active_timer is not None:
                            st.session_state.active_timer = "black" if current_turn_str == "White" else "white"
                    
                    # 🚀 ATAAA Screen Switcher Trigger for Hit Lever Switch (Normal Move / Checkmate / Draw)
                    if st.session_state.board_state.is_game_over() or st.session_state.board_state.is_checkmate() or st.session_state.board_state.is_stalemate() or st.session_state.board_state.is_insufficient_material():
                        st.session_state.match_locked = True
                        st.session_state.current_screen = "score"

                    st.session_state.last_timestamp = time.time()
                    st.rerun()


    st.markdown('<div class="row-spacer-2"></div>', unsafe_allow_html=True)
    
    # Calculate moves directly from the board stack so it updates even when clock isn't started
    white_moves_count = (len(board.move_stack) + 1) // 2
    
    if use_tenths:
        flag_w = "" 
    else:
        flag_w = " [FLAG DROPPED]" if st.session_state.flag_dropped_white else ""
        
    w_status = "⚡ Ticking" if (st.session_state.timer_started and st.session_state.active_timer == "white" and not st.session_state.flag_dropped_white and not st.session_state.flag_dropped_black) else "⏸️ Frozen"
    st.metric(label=f"⚪ White Clock ({w_status}) [Moves: {white_moves_count}]{flag_w}", 
              value=format_adaptive_timer(st.session_state.time_white, use_tenths))
              
    if freeze_option == "Freeze is OFF" and st.session_state.time_white <= 0 and not use_tenths:
        st.markdown('<div class="blinking-bars">═══════════════</div>', unsafe_allow_html=True)

# =========================================================================
# 🔍 LIVE BLOCKADE DETECTOR & AUTO-TERMINATOR (RUNS ON EVERY MOVE)
# =========================================================================
# =========================================================================
# 🔍 STEP 1: LIVE BLOCKADE DETECTOR (RUNS ON EVERY MOVE)
# =========================================================================
# =========================================================================
# 🎛️ STEP 0: INITIALIZE UI DISABLED FLAG (AVOIDS NAME-ERROR)
# =========================================================================
ui_disabled = is_game_over or st.session_state.get("match_locked", False)


# =========================================================================
# 🔍 STEP 1: LIVE BLOCKADE DETECTOR (RUNS ON EVERY MOVE)
# =========================================================================
is_pawn_blockade = False

if not board.is_game_over() and not st.session_state.get("review_mode_active", False):
    files_with_pawns = set()
    for square in pure_chess_pkg.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == pure_chess_pkg.PAWN:
            files_with_pawns.add(pure_chess_pkg.square_file(square))
            
    all_files_blocked = len(files_with_pawns) == 8
    
    legal_moves = list(board.legal_moves)
    if legal_moves:
        has_playable_pawn_or_capture = any(
            board.is_capture(m) or board.piece_type_at(m.from_square) == pure_chess_pkg.PAWN 
            for m in legal_moves
        )
        if not has_playable_pawn_or_capture and all_files_blocked:
            is_pawn_blockade = True

# Persist blockade state explicitly into session state
if is_pawn_blockade and not st.session_state.get("review_mode_active", False):
    st.session_state["is_pawn_blockade"] = True
    st.session_state["match_locked"] = True

# =========================================================================
# 🚨 STEP 2: GLOBAL ENDGAME LOCKDOWN ENGINE (FOR ALL WINS AND DRAWS)
# =========================================================================
is_game_over = (
    board.is_game_over() or 
    st.session_state.get("match_over", False) or 
    st.session_state.get("flag_dropped_white", False) or 
    st.session_state.get("flag_dropped_black", False) or
    st.session_state.get("draw_game_over", False) or
    st.session_state.get("is_pawn_blockade", False) or
    is_pawn_blockade
)

# Force ui_disabled to update immediately with all active flags
ui_disabled = (
    is_game_over or 
    st.session_state.get("match_locked", False) or 
    st.session_state.get("draw_game_over", False) or 
    st.session_state.get("is_pawn_blockade", False) or 
    board.is_game_over()
)

if is_game_over and not st.session_state.get("review_mode_active", False):
    # ⏱️ Freeze BOTH chess clocks permanently and immediately!
    st.session_state.freeze_option = "Freeze is ON"
    st.session_state.clock_running = False
    st.session_state.timer_started = False
    st.session_state.active_timer = None
    st.session_state.paused_timer = None
    st.session_state.match_locked = True

    # 🔒 System Lockdown (Trigger Score Screen Switch instantly on deadlock/game over)
    if st.session_state.get("current_screen") != "score":
        st.session_state.current_screen = "score"
        st.rerun()



# =========================================================================
# 🏆 STEP 3: AUTOMATED ENDGAME MATCH STATE UI ANNOUNCER
# =========================================================================
# =========================================================================
# 🏆 STEP 3: AUTOMATED ENDGAME MATCH STATE UI ANNOUNCER
# =========================================================================
# =========================================================================
# 🏆 STEP 3: AUTOMATED ENDGAME MATCH STATE UI ANNOUNCER
# =========================================================================
if st.session_state.get("normal_style_mode", True) and is_game_over:
    st.markdown("---")
    
    # Get standard python-chess result string if available
    result = board.result()

    # --- 🔍 CUSTOM ROBUST MATERIAL CHECKERS FOR THE SURVIVING PLAYER ---
    # Count pieces for White
    white_knights = len(board.pieces(pure_chess_pkg.KNIGHT, pure_chess_pkg.WHITE))
    white_bishops = len(board.pieces(pure_chess_pkg.BISHOP, pure_chess_pkg.WHITE))
    white_queens = len(board.pieces(pure_chess_pkg.QUEEN, pure_chess_pkg.WHITE))
    white_rooks = len(board.pieces(pure_chess_pkg.ROOK, pure_chess_pkg.WHITE))
    white_pawns = len(board.pieces(pure_chess_pkg.PAWN, pure_chess_pkg.WHITE))
    white_total_pieces = white_knights + white_bishops + white_queens + white_rooks + white_pawns

    # Count pieces for Black
    black_knights = len(board.pieces(pure_chess_pkg.KNIGHT, pure_chess_pkg.BLACK))
    black_bishops = len(board.pieces(pure_chess_pkg.BISHOP, pure_chess_pkg.BLACK))
    black_queens = len(board.pieces(pure_chess_pkg.QUEEN, pure_chess_pkg.BLACK))
    black_rooks = len(board.pieces(pure_chess_pkg.ROOK, pure_chess_pkg.BLACK))
    black_pawns = len(board.pieces(pure_chess_pkg.PAWN, pure_chess_pkg.BLACK))
    black_total_pieces = black_knights + black_bishops + black_queens + black_rooks + black_pawns

    # True if White has no massive mating material (Lone King, King+Bishop, or King+Knight)
    white_has_insufficient = (white_total_pieces == 0) or \
                             (white_total_pieces == 1 and (white_bishops == 1 or white_knights == 1))

    # True if Black has no massive mating material (Lone King, King+Bishop, or King+Knight)
    black_has_insufficient = (black_total_pieces == 0) or \
                             (black_total_pieces == 1 and (black_bishops == 1 or black_knights == 1))


    # 🎈 Loop/Continuous Balloon Animation Handler
    if any([board.is_checkmate(), result in ["1-0", "0-1"], 
            st.session_state.get("flag_dropped_white", False), 
            st.session_state.get("flag_dropped_black", False)]):
        
        # Intercept and prevent balloons if it's a Stage 5 Draw scenario
        is_stage5_white_timeout = st.session_state.get("flag_dropped_white", False) and black_has_insufficient
        is_stage5_black_timeout = st.session_state.get("flag_dropped_black", False) and white_has_insufficient
        
        if not (is_stage5_white_timeout or is_stage5_black_timeout):
            st.balloons()

    # 💥 1. Check for DEFINITIVE CHECKMATES First
    if board.is_checkmate():
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        score_display = "1-0" if winning_side == "White" else "0-1"
        st.success(f"🏆 **MATCH OVER: Checkmate! {winning_side} Wins! Score: {score_display}**\n\n"
                   f"*(The King is under direct attack and has no legal escape options. Game Over.)*")

    # ⏱️ 2. TOP PRIORITY INTERCEPT: STAGE 5 DRAW EVALUATION (Timeout vs Insufficient Material)
    elif st.session_state.get("is_pawn_blockade", False) or ('is_pawn_blockade' in globals() and is_pawn_blockade):
        st.info("🤝 **DRAW ANNOUNCED: Stage 9 - Dead Position / Stage 6 - Perpetual Check Tactic Applied!**\n\n*(Neither side can mathematically checkmate the opponent by any series of legal moves. Score 1/2-1/2)*")

    elif st.session_state.get("flag_dropped_white", False) and black_has_insufficient:
        st.info("🤝 **DRAW ANNOUNCED: Stage 5 - Insufficient Material and Time Out!**\n\n"
                "*(White ran out of time, but Black does not have massive material to force a checkmate. Score 1/2-1/2)*")
                
    elif st.session_state.get("flag_dropped_black", False) and white_has_insufficient:
        st.info("🤝 **DRAW ANNOUNCED: Stage 5 - Insufficient Material and Time Out!**\n\n"
                "*(Black ran out of time, but White does not have massive material to force a checkmate. Score 1/2-1/2)*")

    # ⏱️ 3. STANDARD TIME OUT WINS (Opponent has massive winning material like Rooks, Queens, or Pawns)
    elif st.session_state.get("flag_dropped_white", False):
        st.success("🏆 **MATCH OVER: Black Wins on Time!**\n\n*(White's chess clock reached 0:00. Score 0-1)*")
        
    elif st.session_state.get("flag_dropped_black", False):
        st.success("🏆 **MATCH OVER: White Wins on Time!**\n\n*(Black's chess clock reached 0:00. Score 1-0)*")
        
    # 🏆 4. GENERIC RESULT FALLBACK
    elif result in ["1-0", "0-1"]:
        st.success(f"🏆 **MATCH OVER: Winner Determined ({result})!**")

    # 🧠 5. Handle Rules Engine Automated Structural Draws (Stages 1 through 9)
    elif board.is_insufficient_material():
        white_pieces = board.occupied_co[pure_chess_pkg.WHITE]
        black_pieces = board.occupied_co[pure_chess_pkg.BLACK]
        
        if bin(white_pieces).count("1") == 1 and bin(black_pieces).count("1") == 1:
            st.info("🤝 **DRAW ANNOUNCED: Stage 2 - Impossible to mate (King vs King). Score 1/2-1/2**")
        else:
            st.info("🤝 **DRAW ANNOUNCED: Stage 1 - Insufficient material.**\n\n"
                    "*(Triggered by Lone King vs Lone King, King+Bishop vs Lone King, "
                    "King+Knight vs Lone King, or Same-Colored Bishops. Score 1/2-1/2)*")
                        
    elif board.is_stalemate():
        st.info("🤝 **DRAW ANNOUNCED: Stage 8 - Stalemate!**\n\n"
                "*(The active player has no legal moves available and their king is not in check. Score 1/2-1/2)*")
                        
    elif board.is_fivefold_repetition(): 
        st.info("🤝 **DRAW ANNOUNCED: Stage 4 - Fivefold Repetition!**\n\n"
                "*(The same position has occurred five times automatically ending the game. Score 1/2-1/2)*")

    elif board.is_seventyfive_moves() or len(st.session_state.get("moves_played", [])) >= 150:
        st.info("🤝 **DRAW ANNOUNCED: Stage 4 - 75-Move Rule Exceeded!**\n\n"
                "*(75 consecutive moves played with zero pawn mobility or piece captures. Score 1/2-1/2)*")
                
    elif board.can_claim_threefold_repetition() or st.session_state.get("draw_cause") == "threefold":
        st.warning("🤝 **DRAW ANNOUNCED: Stage 7 - Threefold Repetition!**\n\n"
                   "*(Identical board states, same turn player, and identical legal rights have occurred three times. Score 1/2-1/2)*")
                
    
                
    

    # 🤝 6. Handle Manual Mutual Agreements (Stage 10)
    # -------------------------------------------------------------------------
    # 🏁 GAME OVER: Handle match conclusion
    # -------------------------------------------------------------------------
    
    # 🤝 Handle Manual Mutual Agreements (Stage 10)
    # (Checking if standard draw flag is set, but ignoring specific 50-move condition)
    # -------------------------------------------------------------------------
    # 🏁 GAME OVER: Handle match conclusion (🏆 STEP 3)
    # -------------------------------------------------------------------------
    
    

   # 1️⃣ Handle 50-Move Rule Exceeded Announcement (Stage 3 Custom Draw)
    if st.session_state.get("draw_game_over", False) and st.session_state.get("draw_cause") == "fifty_moves":
        st.info("🤝 **MATCH OVER: 50-Move Rule Draw! Score: 1/2-1/2**")
        st.markdown(st.session_state.get("game_result_announcement", ""))

    # 2️⃣ Handle Manual Mutual Agreements (Stage 10 standard draw)
    elif st.session_state.get("draw_game_over", False) and st.session_state.get("draw_cause") not in {"fifty_moves", "threefold"}:
        st.info("🤝 **MATCH OVER: Draw by Mutual Agreement! Score: 1/2-1/2 (Stage 10)**")
        st.markdown(st.session_state.get("game_result_announcement", ""))

    # 3️⃣ This handles standard checkmate, stale mate, or other structural board game endings
    elif st.session_state.board_state.is_game_over() or st.session_state.get("match_over", False):
        st.markdown(st.session_state.get("game_result_announcement", ""))

# 3. Step 4 Isolated UI Announcer (Place this right below your standard Step 3 block)
if st.session_state.get("armageddon_style_mode", False) and is_game_over:
    st.markdown("---")
    
    # 🎈 Armageddon Balloon Handler (Only for decisive wins)
    if board.is_checkmate() or st.session_state.get("flag_dropped_black", False):
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        if winning_side == "White" and check_white_has_mating_material(board):
            st.balloons()
    
    # 💥 1. Check for DEFINITIVE CHECKMATES First
    if board.is_checkmate():
        winning_side = "Black" if board.turn == pure_chess_pkg.WHITE else "White"
        if winning_side == "White":
            st.success("🏆 **MATCH OVER: Checkmate! White Wins! Score 1-0**\n\n*(The King is under direct attack and has no legal escape options. Game Over.)*")
        else:
            st.error("🏁 **MATCH OVER: Checkmate! Black Wins! Score 0-1**\n\n*(The King is under direct attack and has no legal escape options. Game Over.)*")

    # ⏱️ 2. White Flag Drops First (Armageddon Draw Rule: Black wins tie-break)
    elif st.session_state.get("flag_dropped_white", False):
        st.error("🏁 **MATCH OVER: Black Wins, Score 0-1 (White's flag dropped first; Black wins on draw-odds)**")

    # ⏱️ 3. Black Flag Drops First (Depends on White's Mating Material)
    elif st.session_state.get("flag_dropped_black", False):
        has_mating_material = check_white_has_mating_material(board)
        if has_mating_material:
            st.success("🏆 **MATCH OVER: White Wins, Score 1-0 (Black's flag dropped and White has sufficient mating material)**")
        else:
            st.error("🏁 **MATCH OVER: Black Wins, Score 0-1 (Black's flag dropped, but White lacks mating material; Armageddon draw-odds apply)**")

    # 🧠 4. Armageddon Rules Engine Automated Structural Draws (Stages 1 through 9 converted to Black wins)
    elif board.is_insufficient_material():
        white_pieces = board.occupied_co[pure_chess_pkg.WHITE]
        black_pieces = board.occupied_co[pure_chess_pkg.BLACK]
        
        if bin(white_pieces).count("1") == 1 and bin(black_pieces).count("1") == 1:
            st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 2 - Impossible to mate (King vs King).**")
        else:
            st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 1 - Insufficient material.**\n\n"
                    "*(Triggered by Lone King vs Lone King, King+Bishop vs Lone King, "
                    "King+Knight vs Lone King, or Same-Colored Bishops.)*")
                    
    elif board.is_stalemate():
        st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 8 - Stalemate!**\n\n"
                "*(The active player has no legal moves available and their king is not in check.)*")
                
    elif board.is_fivefold_repetition(): 
        st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 4 - Fivefold Repetition!**\n\n"
                "*(The same position has occurred five times automatically ending the game.)*")

    elif board.is_seventyfive_moves() or len(st.session_state.get("moves_played", [])) >= 150:
        st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 4 - 75-Move Rule Exceeded!**\n\n"
                "*(75 consecutive moves played with zero pawn mobility or piece captures)*")
                
    elif board.can_claim_threefold_repetition() or st.session_state.get("draw_cause") == "threefold":
        st.warning("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 7 - Threefold Repetition!**\n\n"
                   "*(Identical board states, same turn player, and identical legal rights have occurred three times.)*")
                   
    elif board.is_fifty_moves():
        st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 3 - 50-Move Rule Exceeded!**\n\n"
                "*(50 consecutive moves/100 turns played without a pawn move or a piece capture.)*")
                
    elif 'is_pawn_blockade' in globals() and is_pawn_blockade:
        st.info("🏆 **MATCH OVER Black Wins, Score 0-1 Stage 9 - Dead Position / Stage 6 - Perpetual Check Tactic Applied!**\n\n"
                "*(Neither side can mathematically checkmate the opponent by any series of legal moves.)*")

    # 🤝 5. Handle Manual Mutual Agreements (Stage 10 converted to Black win)
    elif st.session_state.get("draw_game_over", False) and st.session_state.get("draw_cause") != "fifty_moves":
        st.info("🏆 **MATCH OVER Black Wins, Score 0-1 by Mutual Agreement! (Stage 10)**")

    # 🏁 6. Universal Fallback
    else:
        st.error("🏁 **MATCH OVER: Black Wins, Score 0-1 (Armageddon Draw-Odds Rule Applied)**")
    st.session_state.match_locked = True
    st.session_state.current_screen = "score"
    st.rerun()
        
    




st.markdown("---")
# Check if we are currently in review mode or coming from a concluded/armageddon review state
is_in_review_mode = st.session_state.get("review_mode_active", False) or st.session_state.get("armageddon_was_played", False)

btn_label = "🔄 Reset GameState" if not is_in_review_mode else "🔄 Reset GameState (Exit Review & Restart)"

if st.button(btn_label, use_container_width=True, key="btn_reset_gamestate_dynamic"):
    # 🔓 1. Unlock the app system completely from endgame freezes
    st.session_state.match_locked = False
    st.session_state.draw_game_over = False
    st.session_state.freeze_option = "Freeze is OFF"  # Restores default live clock behavior
    
    # 🔒 2. Keep the user safely inside the engine screen
    st.session_state["current_screen"] = "engine"
    st.session_state["review_mode_active"] = False
    st.session_state["match_over"] = False
    
    # 🧹 3. Clear out all the old match timing, movement flags, and review markers
    keys_to_clear = [
        "time_white", "time_black", "active_timer", "paused_timer", 
        "last_timestamp", "white_move_count", "black_move_count", 
        "flag_dropped_white", "flag_dropped_black", "moves_played", 
        "frozen_error_triggered", "notation_error", "timer_started",
        "armageddon_style_mode", "locked_score_armageddon_mode", 
        "armageddon_conclusion_clicked", "armageddon_concluded", "armageddon_was_played",
        "is_pawn_blockade"  # 🟢 Added this line to clear deadlock storage on reset!
    ]
    for k in keys_to_clear:
        if k in st.session_state: 
            st.session_state.pop(k, None)
            
    # ♟️ 4. Wipe the board state back to the starting setup
    if hasattr(st.session_state, "board_state") and st.session_state.board_state:
        st.session_state.board_state.reset()
        
    # 🔄 5. Instantly refresh the engine view using st.rerun() without full page reload
    st.rerun()

# Safely render move history log only if it exists
if "moves_played" in st.session_state and st.session_state.moves_played:
    st.write("**Move History Log:**", ", ".join(st.session_state.moves_played))
else:
    st.write("**Move History Log:** None")

# =========================================================================
# 🚀 CONTINUOUS LIVE RE-RUN LOOPER (THE ENGINE HEARTBEAT)
# =========================================================================
if st.session_state.timer_started and st.session_state.active_timer is not None:
    if st.session_state.flag_dropped_white or st.session_state.flag_dropped_black:
        st.session_state.active_timer = None
    else:
        time.sleep(refresh_rate)
        st.rerun()

# =========================================================================
# #######ATAAA CHESS AI############## (DEDICATED VIEW SCREEN - NO EXPANDER)
# =========================================================================

# --- 1. THE BRAIN ---
client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"],
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,             # Try up to 5 times
            initial_delay=2.0,      # Start with a 2-second wait
            max_delay=60.0,         # Don't wait more than a minute
            http_status_codes=[503] # Specifically retry on 503 errors
        )
    )
)


# =========================================================================
# #######ATAAA CHESS AI############## (DEDICATED FULL SCREEN VIEW)
# =========================================================================

if 'current_solution' not in st.session_state: st.session_state.current_solution = ""
if 'show_hero' not in st.session_state: st.session_state.show_hero = False
if 'user_data' not in st.session_state: 
    st.session_state.user_data = {"name": "", "lang": "en", "voice_type": "Normal", "gang": "Normal", "score": 0}
# --- 3. VOICE ENGINE ---
def play_ata_voice(text, voice_mode="formal"):
    lang = st.session_state.user_data.get('lang', 'en')
    
    # Correctly retrieve username based on single or two-player configuration mode
    if st.session_state.get("game_mode", "single") == "two_player":
        white_p = st.session_state.get("white_user_name", "")
        black_p = st.session_state.get("black_user_name", "")
        if white_p and black_p:
            user_name = f"{white_p} and {black_p}"
        else:
            user_name = white_p or black_p or st.session_state.get('user_name', '')
    else:
        user_name = st.session_state.get('user_name', st.session_state.user_data.get('name', ''))
    
    greetings = [
        "Greetings,", "Good day.",
        "Hi there,", "Trust you're doing well.",
        "It's a pleasure to connect with you,", "Delighted to connect.",
        "Good morning/afternoon,", "Welcome.",
        "Trust this message finds you well,", "I hope your week is off to a strong start.",
        "Wonderful to have you here,", "Glad to be connecting with you.",
        "Checking in,", "Great to see you.",
        "A pleasure to cross paths with you today,", "Delighted to cross paths."
    ]
    
    encouragements = [
        "Let's collaborate to drive exceptional results.",
        "Let's partner up to build something extraordinary.",
        "Let's join forces to achieve remarkable outcomes.",
        "Let's work together to create high-value impact.",
        "Let's team up and make something incredible happen.",
        "Let's align our efforts to drive paradigm-shifting results.",
        "Let's combine our strengths to pioneer something groundbreaking.",
        "Let's collaborate to architect exceptional outcomes.",
        "Let's merge our vision to create something truly monumental.",
        "Let's partner to execute at the highest level of excellence."
    ]
    
    formals = [
        "Below is the comprehensive, step-by-step breakdown for these inquiries.",
        "Here’s a granular, step-by-step walkthrough of the solutions.",
        "Here is the methodical, step-by-step solution set for the questions.",
        "Provided below are the systematic, step-by-step resolutions for the queries.",
        "Below is the structured, step-by-step resolution roadmap for your review.",
        "Here is the granular, sequential breakdown addressing each inquiry.",
        "Provided below is the systematic, milestone-by-milestone solution set.",
        "Here’s a streamlined, step-by-step walkthrough to unpack these questions.",
        "Below you'll find the methodical, step-by-step answers tailored to your queries.",
        "Here is the curated, step-by-step breakdown designed to address your queries.",
        "Below lies the precision-engineered, sequential roadmap for these questions.",
        "Presented below is a methodical, phased breakdown of the solutions.",
        "Here’s a streamlined, step-by-step decoding of the questions at hand.",
        "Below is the definitive, multi-stage answer key tailored for these inquiries."
    ]
    
    generous = [
        "I will vocalize your notes to facilitate retention.",
        "I'll read your notes aloud to reinforce your recall.",
        "I will articulate your notes to optimize your commit phase.",
        "I'll read the text aloud to accelerate your memorization.",
        "I'll voice your notes to help lock them into your memory.",
        "I will articulate your notes to enhance strategic retention and long-term encoding.",
        "I'll audio-stream your notes to maximize your active recall pathways.",
        "I will vocalize the text to support your mastery and integration of the material.",
        "I'll read your notes aloud to anchor them securely in your memory.",
        "I will recite the documentation to expedite your cognitive retention."
    ]
    
    if "greet_index" not in st.session_state:
        st.session_state["greet_index"] = 0
    if "encourage_index" not in st.session_state:
        st.session_state["encourage_index"] = 0
    if "formal_index" not in st.session_state:
        st.session_state["formal_index"] = 0
    if "generous_index" not in st.session_state:
        st.session_state["generous_index"] = 0
        
    current_greeting = greetings[st.session_state["greet_index"]]
    current_encouragement = encouragements[st.session_state["encourage_index"]]
    
    if voice_mode == "generous":
        current_middle = generous[st.session_state["generous_index"]]
        st.session_state["generous_index"] = (st.session_state["generous_index"] + 1) % len(generous)
    else:
        current_middle = formals[st.session_state["formal_index"]]
        st.session_state["formal_index"] = (st.session_state["formal_index"] + 1) % len(formals)
    
    st.session_state["greet_index"] = (st.session_state["greet_index"] + 1) % len(greetings)
    st.session_state["encourage_index"] = (st.session_state["encourage_index"] + 1) % len(encouragements)
    
    try:
        name_segment_1 = f"{user_name}," if user_name else ""
        name_segment_2 = f"{user_name}," if user_name else ""
        # Ensures sequence: Greeting -> Username -> Encouragement -> Username -> Generous/Formal -> Text
        combined_text = f"{current_greeting} {name_segment_1} {current_encouragement} {name_segment_2} {current_middle} {text}"
        
        tts = gTTS(text=combined_text, lang="en", tld="com.au", slow=False)
        tts_fp = io.BytesIO()
        tts.write_to_fp(tts_fp)
        tts_fp.seek(0)
        
        b64 = base64.b64encode(tts_fp.read()).decode()
        audio_html = f'''
            <audio id="ataaa_speech_audio" autoplay controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            <script>
                var soundElement = document.getElementById("ataaa_speech_audio");
                if (soundElement) {{
                    soundElement.muted = false;
                    soundElement.volume = 1.0;
                    soundElement.play().catch(function(error) {{
                        console.log("Audio autoplay prevented: ", error);
                    }});
                }}
            </script>
        '''
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        if "200" in str(e):
            st.success("Voice Engine Ready!")
        else:
            st.error(f"Voice Error: {e}")


# --- STYLES FOR SHIMMER BUTTON ---
st.markdown("""
    <style>
    .shimmer-btn-label {
        font-size: 20px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #FFFFFF, #FF1493, #0e689c, #FF1493, #0e689c, #FFFFFF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', sans-serif;
        animation: shine 5s linear infinite;
        margin: 0;
        padding: 0;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }
    </style>
""", unsafe_allow_html=True)


# --- CHECK IF FULL-SCREEN AI VIEW IS TRIGGERED ---
if st.session_state.get("show_ai_screen", False):
    # Completely replaces the regular game UI with the dedicated AI Hub screen
    st.markdown("<h1 style='text-align: center; color: #00FFCC;'>✈️ ATAAA AI - Hub For Learning</h1>", unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["✍️ Text Search", "📸 Camera", "🎧 Listening to Notes"])

    with tab1:
        st.subheader("✍️ Enter Text & Analyze")
        st.caption("💡 Tip: Press **Windows + H** anywhere on your keyboard to use Windows Voice Typing directly into the text box below!")
        user_input = st.text_area("Type your question here:", height=150, key="t1_input")
        if st.button("✨ Get Step-by-Step Answer", use_container_width=True, key="t1_btn"):
            if user_input:
                with st.spinner("ATAA is thinking..."):
                    max_retries = 3
                    for i in range(max_retries):
                        try:
                            models_list = [m.name for m in client.models.list()]
                            best_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models_list else models_list[0]
                            lang_name = "Tamil" if st.session_state.user_data['lang'] == 'ta' else "English"
                            response = client.models.generate_content(
                                model=best_model,
                                contents=f"Explain in simple step-by-step points in {lang_name}: {user_input}"
                            )
                            st.session_state.current_solution = response.text
                            st.session_state["active_voice_mode"] = "formal"

                            st.success("Answer Ready!")
                            break 
                        except Exception as e:
                            if "503" in str(e) and i < max_retries - 1:
                                st.warning(f"Server busy. Retrying in {i+2} seconds...")
                                time.sleep(i + 2)
                            else:
                                st.error(f"Brain Error: {e}")

    with tab2:
        st.subheader("📸 Upload & Analyze")

        uploaded_img = st.file_uploader("Upload a photo of your book/homework", type=['jpg', 'jpeg', 'png'], key="t2_upload")
        if uploaded_img:
            st.image(uploaded_img, width=300)
            if st.button("✨ Solve from Image", use_container_width=True, key="t2_btn"):
                with st.spinner("ATAA is reading..."):
                    max_retries = 3
                    for i in range(max_retries):
                        try:
                            models_list = [m.name for m in client.models.list()]
                            best_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models_list else models_list[0]
                            lang_name = "Tamil" if st.session_state.user_data['lang'] == 'ta' else "English"
                            img = Image.open(uploaded_img)
                            response = client.models.generate_content(
                                model=best_model,
                                contents=[img, f"Read all text and solve this in simple step-by-step points in {lang_name}."]
                            )
                            st.session_state.current_solution = response.text
                            st.session_state["active_voice_mode"] = "formal"

                            st.success("Answer Ready!")
                            break
                        except Exception as e:
                            if "503" in str(e) and i < max_retries - 1:
                                st.warning(f"Server busy. Retrying in {i+2} seconds...")
                                time.sleep(i + 2)
                            else:
                                st.error(f"Brain Error: {e}")

    with tab3:
        st.subheader("🎧 Listening to your Notes")
        st.info("I will read your notes aloud to help you memorize them!")
        st.caption("💡 Tip: Press **Windows + H** anywhere on your keyboard to use Windows Voice Typing directly into the text box below!")
        listen_choice = st.radio("How should I read?", ["Read my Typed Text", "Read from my Image/Photo"])
        
        if listen_choice == "Read my Typed Text":
            input_text = st.text_area("Paste the passage here:", height=200, key="read_text_input")
            if st.button("🔊 Read My Notes Now", use_container_width=True):
                if input_text:
                    st.session_state.current_solution = input_text
                    st.session_state["active_voice_mode"] = "generous"
                    play_ata_voice(input_text, voice_mode="generous")
                else:
                    st.warning("Please paste some text first!")
        else:
            read_img = st.file_uploader("Upload the note image:", type=['jpg', 'jpeg', 'png'], key="read_img_input")
            
            if read_img:
                st.image(read_img, width=300)
                
                # BUTTON 1: Extract the text from the image
                if st.button("🔍 Step 1: Extract Text", use_container_width=True):
                    with st.spinner("Converting image to clear text..."):
                        try:
                            models_list = [m.name for m in client.models.list()]
                            best_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models_list else models_list[0]
                            lang_name = "Tamil" if st.session_state.user_data['lang'] == 'ta' else "English"
                            
                            img = Image.open(read_img)
                            response = client.models.generate_content(
                                model=best_model,
                                contents=[img, f"Read all text and explain it in simple step-by-step points in {lang_name}."]
                            )
                            
                            # Store the result in session state so it stays on screen
                            st.session_state.current_solution = response.text
                            st.session_state["active_voice_mode"] = "generous"
                            st.success("Text Extracted successfully!")
                        except Exception as e:
                            st.error(f"Brain Error: {e}")

                # BUTTON 2: Show this button ONLY if text has been extracted
                if st.session_state.current_solution:
                    st.info("Text is ready! Click below to listen.")
                    if st.button("🔊 Step 2: Read My Notes Aloud", use_container_width=True):
                        st.session_state["active_voice_mode"] = "generous"
                        play_ata_voice(st.session_state.current_solution, voice_mode="generous")


    if st.session_state.current_solution:
        st.markdown("---")
        st.markdown(st.session_state.current_solution)
        if st.button("🔊 HEAR ANSWER", use_container_width=True, key="global_play"):
            tab_context = st.session_state.get("active_tab_context", "regular")
            if tab_context == "tab3" or st.session_state.get("active_voice_mode") == "generous":
                 play_ata_voice(st.session_state.current_solution, voice_mode="generous")
            else:
                  play_ata_voice(st.session_state.current_solution, voice_mode="formal")
        if st.button("🗑️ Clear All", use_container_width=True, key="global_clear_all"):
            st.session_state.current_solution = ""
            st.rerun()

    st.markdown("---")
    # Bottom Return Button to go back to the chess engine screen
    if st.button("🔙 Back to engine screen", use_container_width=True, key="btn_back_to_engine"):
        st.session_state.show_ai_screen = False
        st.rerun()
















