import os
import streamlit as st
import razorpay

# Initialize Razorpay Client (Use Streamlit Secrets or Environment Variables)
RAZORPAY_KEY_ID = st.secrets.get("RAZORPAY_KEY_ID", os.environ.get("RAZORPAY_KEY_ID"))
RAZORPAY_KEY_SECRET = st.secrets.get("RAZORPAY_KEY_SECRET", os.environ.get("RAZORPAY_KEY_SECRET"))

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

st.title("FinWise Subscription Gateway")

# Collect User Info
with st.form("subscription_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    submitted = st.form_submit_button("Proceed to Payment")

if submitted:
    if not name or not email or not phone:
        st.error("Please fill in all fields.")
    else:
        try:
            # Create Razorpay Payment Link directly on the server side
            payment_link = client.payment_link.create({
                "amount": 50000,  # ₹500.00 in paise
                "currency": "INR",
                "accept_partial": False,
                "description": "Premium Mutual Fund Subscription",
                "customer": {
                    "name": name,
                    "email": email,
                    "contact": phone
                },
                "notify": {
                    "sms": True,
                    "email": True
                },
                "callback_url": "https://your-streamlit-app.streamlit.app", # Your app URL
                "callback_method": "get"
            })
            
            st.success("Payment link generated successfully!")
            # Display direct payment button
            st.link_button("👉 Click Here to Pay ₹500", payment_link["short_url"], type="primary")

        except Exception as e:
            st.error(f"Error creating payment link: {str(e)}")
