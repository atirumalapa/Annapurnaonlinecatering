import streamlit as st
import pandas as pd
import sqlite3
from PIL import Image
# user data
conn = sqlite3.connect("data.db")
c = conn.cursor()
#Post data
conn1 = sqlite3.connect("data1.db")
c1 = conn1.cursor()
#Order data
conn3 = sqlite3.connect("data3.db")
c3 = conn3.cursor()
# User login function
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)')
def add_userdata(username,password):
	c.execute("INSERT INTO usertable(username,password) VALUES (?,?)",(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM usertable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def view_all_users():
	c.execute('SELECT * FROM usertable')
	data = c.fetchall()
	return data
def get_all_user_name():
	c.execute('SELECT DISTINCT username FROM usertable')
	data = c.fetchall()
	return data
# Add post function
# Datae = Date
def create_posttable():
	c1.execute('CREATE TABLE IF NOT EXISTS posttable(Datae DATE,post TEXT)')
def add_postdata(data,post):
	c1.execute('INSERT INTO posttable(data,post) VALUES (?,?)',(data,post))
	conn1.commit()
def view_all_post():
	c1.execute('SELECT * FROM posttable')
	data = c1.fetchall()
	return data
def delete_post_date(Datae):
	c1.execute('DELETE FROM posttable WHERE data="{}"'.format(Datae))
	conn1.commit()
def get_all_post_Date():
	c1.execute('SELECT DISTINCT data FROM posttable')
	data = c1.fetchall()
	return data
#templates for post
title_temp = """
<div style = 'padding:10px, margin:10px;'>
<img src = 'https://www.w3schools.com/howto/img_avatar.png' alt = 'Avatar' style = 'vertical-align: middle; float: left; width: 50px; height: 50px; border-radius:50%'>
<h4 style = 'text-align:left;'>{}</h4>
<p style = 'text-align:center;'>{}</p>
</div>
"""
# Website function
def main():
	st.title("Annapurna online catering")
	menu = ["Home", "Login", "Signup","Admin login"]
	choice  = st.sidebar.selectbox("Menu", menu)

	if choice == "Home":
		st.subheader("Home")
		st.write("హలో అమ్మ")
		st.write("ఈ క్యాటరింగ్ అమెరికాకు మాత్రమే")
	elif choice == "Login":
		st.subheader("Login Section")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password", type = "password")
		st.write("click the box to login")
		if st.sidebar.checkbox("Login"):
			#if password == "12345":
			create_usertable()
			result =login_user(username,password)
			if result:
				st.success(f"Logged In as {username}")
				viewer_task = st.selectbox("Menu and order",["Menu", "Order"])
				if viewer_task == "Menu":
					st.subheader("Todays Menu")
					result = view_all_post()
					for i in result:
						b_date = i[0]
						b_post = i[1]
						st.markdown(title_temp.format(b_date, b_post),unsafe_allow_html = True)
				elif viewer_task == "Order":
					st.write("If you want to order for any special occasions please tell us one week before.",
						 " And if you want anything on the menu order now.",
						" Please scan the QR code to place your now.")
					if st.button("click to order"):
						chat_image = Image.open('WIN_20220816_12_38_49_Pro.jpg')
						st.image(chat_image)
			else:
				st.warning("Incorrect username/password")

	elif choice == "Signup":
		st.subheader("Create New Account")

		new_user  = st.text_input("User Name")
		new_password = st.text_input("Password", type = "password")

		if st.button("Signup"):
			usernames = [i[0] for i in get_all_user_name()]
			if new_user in usernames:
				st.warning("This username alredy exist")
			else:
				create_usertable()
				add_userdata(new_user,new_password)
				st.success("You have successfully created a valid Account")
				st.info("Go to Login Menu to login")
	elif choice == "Admin login":
		st.subheader("Admin Login Section")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password", type = "password")
		if st.sidebar.checkbox("Login"):
			if password == "ADMIN":
				st.success(f"Logged In as {username}")

				task = st.selectbox("Task", ["Add post", "Delete Post", "View Orders", "Delete Orders", "Profiles"])
				if task == "Add post":
					create_posttable()
					st.subheader("Add your post")
					date = st.date_input("Date")
					post = st.text_area("Write here")
					
					if st.button("Add"):
						add_postdata(date,post)
						st.success("Post "+ post + " saved")

				elif task == "Delete Post":
					st.subheader("Delete post that is Yesterday")

					result = view_all_post()
					clean_db1 = pd.DataFrame(result, columns = ["Date", "Post"])
					st.dataframe(clean_db1)
					all_post = [i[0] for i in get_all_post_Date()]
					Delete_date = st.selectbox("post", all_post)

					if st.button("Delete"):
						delete_post_date(Delete_date)
						st.warning("It as been deleted")
					
				elif task == "View Orders":
					st.subheader("Orders")
					view_orders = view_all_order()
					for i in view_orders:
						b_Date = i[0]
						b_Name = i[1]
						b_Phonenum = i[2]
						b_Item = i[3]
						b_quan = i[4]
						st.markdown(order_temp.format(b_Name,b_Date,b_Phonenum,b_Item,b_quan),unsafe_allow_html = True)
				elif task == "Delete Orders":
					st.subheader("Delete orders that are done")
					result1 = view_all_order()
					clean_db2 = pd.DataFrame(result1, columns = ["Date", "Name", "Phonenumber", "Item", "Quantity"])
					st.dataframe(clean_db2)
					all_name = [i[0] for i in get_all_order_Name()]
					Delete_Name = st.selectbox("Name", all_name)

					if st.button("Delete"):
						delete_order_Name(Delete_Name)
						st.warning("It as been deleted")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns = ["username","password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect username/password")



if __name__ == "__main__":
	main()
