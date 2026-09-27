import streamlit as st
import datetime
import urllib.parse

# Application Configuration
st.set_page_config(page_title="Sea-to-Sky Thanksgiving Dinners", page_icon="🦃", layout="wide")

# Mock Database / State Initialization
if "orders" not in st.session_state:
    st.session_state.orders = []

# Application Title
st.title("🍂 Sea-to-Sky Thanksgiving Dinner Pre-Orders")
st.subheader("Reserve your gourmet festive feast for local kitchen pickup")

# Business Contact & Location Banner
pickup_address = "5-1257 Commercial Way, Squamish, BC"
encoded_address = urllib.parse.quote(pickup_address)
google_maps_url = f"https://google.com{encoded_address}"

# FIX: Added '2' inside the brackets here so Streamlit knows to make 2 columns
col_banner1, col_banner2 = st.columns(2)
with col_banner1:
    st.info(f"📍 **Pickup Location:** {pickup_address} | 📞 **Questions?** Call/Text **604.657.6247**")
with col_banner2:
    st.link_button("🗺️ Open in Google Maps", google_maps_url, use_container_width=True)

# FIX: Added '2' inside the brackets here as well
col1, col2 = st.columns(2)

with col1:
    st.header("1. Build Your Feast")
    
    # Dinner Selection
    meal_size = st.radio(
        "Select your dinner package size:",
        ["Dinner for 2 ($75)", "Family Feast for 6 ($210)", "Gathering Pack for 10+ ($340)"],
        index=1
    )
    
    # Dietary Prefs
    diet_pref = st.selectbox("Dietary Adjustments:", ["Traditional Whole Roast", "Gluten-Free Modified", "Vegan/Plant-Based Alternative"])
    
    # Local Add-ons
    st.markdown("**Optional Holiday Enhancements:**")
    add_wine = st.checkbox("Add Locally Sourced BC VQA Wine Pairing (+$30)")
    add_dessert = st.checkbox("Add Extra Artisanal Pumpkin Pie Platter (+$25)")

with col2:
    st.header("2. Pickup Details")
    
    # Customer Info
    customer_name = st.text_input("Full Name")
    customer_phone = st.text_input("Your Phone Number")
    
    # Date Picker restricting window to Canadian Thanksgiving Long Weekend
    pickup_date = st.date_input(
        "Pickup Date:",
        value=datetime.date(2026, 10, 11),  # Thanksgiving long weekend
        min_value=datetime.date(2026, 10, 9),
        max_value=datetime.date(2026, 10, 12)
    )
    
    pickup_time = st.selectbox("Preferred Pickup Time Window:", ["11:00 AM - 1:00 PM", "1:00 PM - 3:00 PM", "3:00 PM - 5:00 PM"])

# Submit Action
st.markdown("---")
if st.button("Complete Pre-Order Reservation", type="primary"):
    if customer_name and customer_phone:
        order_details = {
            "id": len(st.session_state.orders) + 1,
            "name": customer_name,
            "phone": customer_phone,
            "package": meal_size,
            "style": diet_pref,
            "date": pickup_date.strftime("%Y-%m-%d"),
            "time": pickup_time,
            "wine": add_wine,
            "dessert": add_dessert
        }
        st.session_state.orders.append(order_details)
        st.success(f"🎉 Thank you, {customer_name}! Your reservation is locked in for pickup on {pickup_date} during the {pickup_time} window. See you at Commercial Way!")
    else:
        st.error("⚠️ Please fill out your name and phone number before completing your reservation.")

# Kitchen Manifest View
with st.expander("🛠️ Kitchen Order Manifest Dashboard"):
    if st.session_state.orders:
        st.write("### Production & Pickup Schedule")
        st.dataframe(st.session_state.orders, hide_index=True)
    else:
        st.info("No orders placed yet. Open the link to start accepting local kitchen reservations.")
