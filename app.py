import streamlit as st
import datetime
import urllib.parse
import requests

# Application Configuration
st.set_page_config(page_title="Sea-to-Sky Thanksgiving Dinners", page_icon="🦃", layout="wide")

# Replace this with the real email address where you want to receive orders!
YOUR_BUSINESS_EMAIL = "your-email@example.com" 

# Mock Database / State Initialization (for the on-screen dashboard)
if "orders" not in st.session_state:
    st.session_state.orders = []

# Application Title
st.title("🍂 Sea-to-Sky Thanksgiving Dinner Pre-Orders")
st.subheader("Reserve your gourmet festive feast for local kitchen pickup")

# Business Contact & Location Banner
pickup_address = "5-1257 Commercial Way, Squamish, BC"
encoded_address = urllib.parse.quote(pickup_address)
google_maps_url = f"https://google.com{encoded_address}"

col_banner1, col_banner2 = st.columns(2)
with col_banner1:
    st.info(f"📍 **Pickup Location:** {pickup_address} | 📞 **Questions?** Call/Text **604.657.6247**")
with col_banner2:
    st.link_button("🗺️ Open in Google Maps", google_maps_url, use_container_width=True)

# Split Layout for Customer Interface
col1, col2 = st.columns(2)

with col1:
    st.header("1. Build Your Feast")
    
    meal_size = st.radio(
        "Select your dinner package size:",
        ["Dinner for 2 ($75)", "Family Feast for 6 ($210)", "Gathering Pack for 10+ ($340)"],
        index=1
    )
    
    diet_pref = st.selectbox("Dietary Adjustments:", ["Traditional Whole Roast", "Gluten-Free Modified", "Vegan/Plant-Based Alternative"])
    
    st.markdown("**Optional Holiday Enhancements:**")
    add_wine = st.checkbox("Add Locally Sourced BC VQA Wine Pairing (+$30)")
    add_dessert = st.checkbox("Add Extra Artisanal Pumpkin Pie Platter (+$25)")

with col2:
    st.header("2. Pickup Details")
    
    customer_name = st.text_input("Full Name")
    customer_email = st.text_input("Your Email Address")
    customer_phone = st.text_input("Your Phone Number")
    
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
    if customer_name and customer_phone and customer_email:
        
        # Prepare data packet for the email form processing backend
        form_data = {
            "Customer Name": customer_name,
            "Customer Phone": customer_phone,
            "Customer Email": customer_email,
            "Package Size": meal_size,
            "Dietary Choice": diet_pref,
            "Pickup Date": pickup_date.strftime("%Y-%m-%d"),
            "Pickup Time": pickup_time,
            "Add Wine": "Yes" if add_wine else "No",
            "Add Dessert": "Yes" if add_dessert else "No",
            "_cc": customer_email, # Automatically sends a carbon copy to the customer!
            "_subject": f"🦃 New Thanksgiving Order from {customer_name}"
        }
        
        # Post request to dispatch the email instantly
        form_submit_url = f"https://formsubmit.co{YOUR_BUSINESS_EMAIL}"
        
        try:
            response = requests.post(form_submit_url, data=form_data)
            
            # Save locally for the temporary app session view
            order_details = {
                "id": len(st.session_state.orders) + 1,
                "name": customer_name,
                "phone": customer_phone,
                "email": customer_email,
                "package": meal_size,
                "style": diet_pref,
                "date": pickup_date.strftime("%Y-%m-%d"),
                "time": pickup_time,
                "wine": add_wine,
                "dessert": add_dessert
            }
            st.session_state.orders.append(order_details)
            st.success(f"🎉 Thank you, {customer_name}! Your reservation has been sent. Check your inbox ({customer_email}) for your confirmation receipt shortly!")
            
        except Exception as e:
            st.error("⚠️ There was an issue processing your reservation request. Please try again or contact support.")
    else:
        st.error("⚠️ Please completely fill out your Name, Email, and Phone Number before booking.")

# Kitchen Manifest View
with st.expander("🛠️ Kitchen Order Manifest Dashboard"):
    if st.session_state.orders:
        st.write("### Production & Pickup Schedule")
        st.dataframe(st.session_state.orders, hide_index=True)
    else:
        st.info("No orders placed yet. Open the link to start accepting local kitchen reservations.")
