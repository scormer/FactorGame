import streamlit as st

def generate_grid(n):
    """Generate the grid numbers for the game."""
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def is_valid_move(previous, current, clicked):
    """Check if the current move is valid."""
    return (
        current not in clicked and
        (previous == 0 or current % previous == 0 or previous % current == 0)
    )

def check_no_moves(previous, clicked, grid_numbers):
    """Check if there are no moves left for the current player."""
    for row in grid_numbers:
        for number in row:
            if is_valid_move(previous, number, clicked):
                return False
    return True

# Initialize session state variables
if "clicked" not in st.session_state:
    st.session_state.clicked = {}
if "turn" not in st.session_state:
    st.session_state.turn = "User A"
if "previous" not in st.session_state:
    st.session_state.previous = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "colors" not in st.session_state:
    st.session_state.colors = {"User A": "#ffcccc", "User B": "#cce5ff"}  # Default colors
if "grid_size" not in st.session_state:
    st.session_state.grid_size = 10
if "history" not in st.session_state:
    st.session_state.history = []

# Allow user to choose colors
st.sidebar.title("Customize Colors")
st.session_state.colors["User A"] = st.sidebar.color_picker("Choose color for User A", st.session_state.colors["User A"])
st.session_state.colors["User B"] = st.sidebar.color_picker("Choose color for User B", st.session_state.colors["User B"])

# Allow user to choose grid size
st.session_state.grid_size = st.sidebar.slider("Grid Size", min_value=4, max_value=20, value=st.session_state.grid_size)

# Game configuration
n = st.session_state.grid_size
st.title("Factor Game")
st.markdown(
    f"**Rules:**\n\n"
    f"1. Two users take turns clicking on a {n}x{n} grid.\n"
    f"2. A valid move is clicking on a grid that is either a factor or multiple of the previously clicked grid.\n"
    f"3. The game ends if a user cannot make a valid move or makes an invalid move."
)

grid_numbers = generate_grid(n)

# Display the grid
def display_grid():
    for i, row in enumerate(grid_numbers):
        cols = st.columns(n)
        for j, number in enumerate(row):
            color = "white"
            if number in st.session_state.clicked:
                color = st.session_state.colors[st.session_state.clicked[number]]
                cols[j].markdown(
                    f"<div style='background-color:{color}; text-align:center; padding:10px; border:1px solid black; font-size:16px; font-weight:bold; width:50px; height:50px; display:flex; align-items:center; justify-content:center;'>{number}</div>",
                    unsafe_allow_html=True
                )
            else:
                cols[j].button(f"{number}", key=f"{i}-{j}", on_click=handle_click, args=(number,))

# Handle user click
def handle_click(number):
    if st.session_state.game_over:
        st.warning("Game over! Start a new game.")
        return

    # Always add the click to history, regardless of validity
    st.session_state.history.append((number, st.session_state.turn))

    if not is_valid_move(st.session_state.previous, number, st.session_state.clicked):
        st.session_state.game_over = True
        st.session_state.winner = (
            "User B" if st.session_state.turn == "User A" else "User A"
        )
        st.error(
            f"Invalid move by {st.session_state.turn}. "
            f"{st.session_state.winner} wins the game!"
        )
        return

    # Mark the grid as clicked
    st.session_state.clicked[number] = st.session_state.turn
    st.session_state.previous = number

    # Check if the next user has any valid moves
    next_turn = "User B" if st.session_state.turn == "User A" else "User A"
    if check_no_moves(number, st.session_state.clicked, grid_numbers):
        st.session_state.game_over = True
        st.session_state.winner = st.session_state.turn  # Current player wins if no valid moves for next player
        return

    # Switch turns
    st.session_state.turn = next_turn

# Display the game interface
st.markdown(f"<h2 style='text-align: center; color: {st.session_state.colors[st.session_state.turn]};'>{st.session_state.turn}'s Turn</h2>", unsafe_allow_html=True)
display_grid()

if st.session_state.game_over:
    st.markdown(f"<h3 style='text-align: center; color: green;'>Game Over! Winner: {st.session_state.winner}</h3>", unsafe_allow_html=True)

# Display click history
st.markdown("### Move History")
for move, user in st.session_state.history:
    st.markdown(
        f"<div style='background-color:{st.session_state.colors[user]}; text-align:center; padding:5px; font-size:14px; width:100px; margin-bottom:5px;'>{user}: {move}</div>",
        unsafe_allow_html=True
    )

# Reset the game
if st.button("Restart Game"):
    st.session_state.clicked = {}
    st.session_state.turn = "User A"
    st.session_state.previous = 0
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.history = []
    st.experimental_rerun()
