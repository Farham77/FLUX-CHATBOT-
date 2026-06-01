import streamlit as st
from groq import Groq
import os
from products import products_d
from dotenv import load_dotenv
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
    </style>
""", unsafe_allow_html=True)

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)


st.markdown("<h1 style='text-align: center;'>Flux ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Neutrino's Official Support Assistant</p>", unsafe_allow_html=True)

system_msg = {"role":"system","content": "You are Flux, the official customer support assistant for Neutrino — a premium Pakistani streetwear brand built on clean aesthetics, minimal design, and urban culture. Your job is to help customers with product information, stock availability, sizing, orders, shipping, and policies. You represent the Neutrino brand. Be warm, confident, and professional — helpful like a knowledgeable store associate, not robotic or corporate, but also never overly casual or using slang. BRAND IDENTITY: Brand Name: Neutrino. Vibe: Premium, minimal, urban, youth-focused Pakistani streetwear. Tone: Professional but approachable. Clear and helpful. Never stiff, never slangy. PRODUCT CATALOG & PRICES: Oversized Hoodie — PKR 3,500 | Colors: Black, White, Ash Grey | Sizes: S, M, L, XL. Graphic Tee — PKR 1,800 | Colors: White, Off-White, Black | Sizes: S, M, L, XL, XXL. Cargo Pants — PKR 4,200 | Colors: Olive, Black, Stone | Sizes: 28, 30, 32, 34, 36. Track Jacket — PKR 5,000 | Colors: Black, Navy | Sizes: S, M, L, XL. Neutrino Cap — PKR 1,200 | Colors: Black, White | One size fits all. CURRENT STOCK AVAILABILITY: Oversized Hoodie: Black (S, M available — L, XL sold out) | White (all sizes available) | Ash Grey (sold out). Graphic Tee: All colors and sizes available. Cargo Pants: Olive (28, 30, 32 available — 34, 36 sold out) | Black (all sizes available) | Stone (sold out). Track Jacket: Black (M, L available — S, XL sold out) | Navy (sold out). Neutrino Cap: Black (available) | White (available). SHIPPING POLICY: Flat shipping fee PKR 200. Free shipping on orders above PKR 5,000. Delivery time 3 to 5 working days nationwide. No international shipping currently. RETURN & EXCHANGE POLICY: Returns accepted within 7 days of delivery. Item must be unused, unwashed, with original tags attached. No returns on sale or discounted items. Exchanges accepted within 14 days of delivery. Customer is responsible for return shipping cost. ORDER SUPPORT: You do not have access to live order tracking. For order status, direct customers to DM @neutrino.pk on Instagram or email support@neutrino.pk with their order ID. For any complaint or issue beyond your scope, direct them to the same channels politely. SIZING GUIDE: S — chest 34-36 inches. M — chest 37-39 inches. L — chest 40-42 inches. XL — chest 43-45 inches. XXL — chest 46-48 inches. Cargo Pants sizing refers to waist in inches. If between sizes: size up for Oversized Hoodie and Track Jacket, stay true to size for Cargo Pants. RULES: Never invent products, prices, or policies not listed above. If you don't know something, say so honestly and direct the customer to support@neutrino.pk or @neutrino.pk on Instagram. Never promise restocks. Do not discuss anything unrelated to Neutrino or customer support. If a customer is frustrated or rude, stay calm, acknowledge their concern, and focus on helping. Always close the conversation on a positive on-brand note. Never use slang, casual expressions, or informal language like yo, totally, awesome, no worries etc. If a customer asks to see a product, see pictures, or see what something looks like, respond with something like Sure, here is a look at our [product name]: or Here is what the [product name] looks like: — keep it short and natural. Never say you cannot show images. The product card will appear below your response automatically. Respond like a professional brand representative who is warm, clear, and genuinely helpful."}

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("###  👋 Hey there!")
    st.markdown("I'm **Flux**, Neutrino's official support assistant. Ask me anything about our products, sizing, orders, or shipping.")


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
        
        for keyword in msg.get("products",[]):
            p = products_d[keyword]
            with st.container(border=True):
               col1,col2 =  st.columns(2)
               with col1:
                st.image(p["image"])
               with col2:
                st.write(f"**{p['name']}**")
                st.write(f"Price: {p['price']}")
                st.write(f"Available Size: {','.join(p['available_sizes'])}")
                st.write(f"Colors: {','.join(p['colors'])}")
    


u_input = st.chat_input("How Can I help you!")

if u_input:
    st.chat_message("user").write(u_input)
    st.session_state.messages.append({"role":"user", 
                                      "content":u_input
                                      })
    for m in st.session_state.messages:
        clean_messages =[{"role":m["role"],"content":m["content"]}]
    msg_for_api = [system_msg]+clean_messages
    with st.chat_message("assistant"):
         try:
          response =   client.chat.completions.create(
              model = "llama-3.3-70b-versatile",
              messages=msg_for_api,
              stream=True
          )
          
          full_reply = st.write_stream(
            chunk.choices[0].delta.content or "" for chunk in response
          )
         
             
          
          mentioned = []
          for keyword in products_d:
              if keyword in full_reply.lower():
                   mentioned.append(keyword) 
                   p = products_d[keyword]
                   with st.container(border=True):
                      col1,col2 =  st.columns(2)
                      with col1:
                        st.image(p["image"])
                      with col2:
                       st.write(f"**{p['name']}**")
                       st.write(f"Price: {p['price']}")
                       st.write(f"Available Size: {','.join(p['available_sizes'])}")
                       st.write(f"Colors: {','.join(p['colors'])}")
         
          st.session_state.messages.append({"role":"assistant",
                                      "content":full_reply,
                                      "products":mentioned
                                      })
    


         except Exception as e:
             st.error("Flux is busy right now. Please try again in a few seconds.")
             
    

             
        
         
    