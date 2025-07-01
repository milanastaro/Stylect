import streamlit as st
from utils.trade_engine import (
    get_pending_trades,
    respond_to_trade,
    get_trade_history,
    get_trade_reputation,
    generate_dual_shipping_labels
)

def show():
    username = st.session_state.user_info.get("username")
    st.title("🔁 Trade Center")
    st.write("View and manage your fashion trades and swaps.")

    st.markdown("### 📬 Pending Trades")

    pending = get_pending_trades(username)
    if not pending:
        st.info("No pending trades.")
    else:
        for trade_id, trade in pending.items():
            st.markdown(f"**Trade ID:** `{trade_id}`")
            st.markdown(f"- From: `{trade['from']}`")
            st.markdown(f"- To: `{trade['to']}`")
            st.markdown(f"- You send: **{trade['item_from']['title']}**")
            st.markdown(f"- You receive: **{trade['item_to']['title']}**")
            st.image(trade["item_from"]["image"], width=150, caption="Their Item")
            st.image(trade["item_to"]["image"], width=150, caption="Your Item")

            if username == trade["to"]:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Accept Trade", key=f"accept_{trade_id}"):
                        respond_to_trade(trade_id, accept=True)
                        st.success("Trade accepted!")
                        st.rerun()
                with col2:
                    if st.button("❌ Reject Trade", key=f"reject_{trade_id}"):
                        respond_to_trade(trade_id, accept=False)
                        st.warning("Trade rejected.")
                        st.rerun()
            else:
                st.caption("Awaiting response from other user.")
            st.markdown("---")

    st.markdown("### 📜 Trade History")
    history = get_trade_history(username)
    if not history:
        st.info("No past trades yet.")
    else:
        for tid, trade in history.items():
            st.markdown(f"**Trade ID:** `{tid}` — *{trade['status'].capitalize()}*")
            st.markdown(f"- From: `{trade['from']}`")
            st.markdown(f"- To: `{trade['to']}`")
            st.markdown(f"- Sent: **{trade['item_from']['title']}**")
            st.markdown(f"- Received: **{trade['item_to']['title']}**")
            st.caption(f"Resolved at: {trade.get('resolved_at')}")
            if trade["status"] == "accepted":
                labels = generate_dual_shipping_labels(trade["item_from"], trade["item_to"])
                st.code(labels["from_label"])
                st.code(labels["to_label"])
            st.markdown("---")

    st.markdown("### 🏅 Your Trade Reputation")
    rep = get_trade_reputation(username)
    st.metric("Trades Successfully Completed", rep)

