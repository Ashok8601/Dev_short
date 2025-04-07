import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from isvalid import is_valid_password
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads/profile_photo'
USER_UPLOAD_FOLDER = 'user_upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['USER_UPLOAD_FOLDER'] = USER_UPLOAD_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(USER_UPLOAD_FOLDER, exist_ok=True)

app.secret_key = 'your secret key'

# Route for the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        
        # Validate the password using regex
        valid, message = is_valid_password(password)
        if not valid:
            return message  # Return validation error if the password is invalid
        
        # Proceed with signup if password is valid
        try:
            hashed_password = generate_password_hash(password)  # Hash the password
            conn = sqlite3.connect('matsya.db')
            conn.execute("INSERT INTO user (name, email, password, username) VALUES (?, ?, ?, ?)", 
                         (name, email, hashed_password, username))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "User already exists!"

    return render_template('signup.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('matsya.db')
        cur = conn.cursor()
        cur.execute("SELECT password, id FROM user WHERE username=?", (username,))
        result = cur.fetchone()
        
        # Check if user exists and the password matches the hashed password
        if result and check_password_hash(result[0], password):
            session['username'] = username
            session['id'] = result[1]  # Store user ID in session
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# Route for the home page
@app.route('/home')
def home():
    conn = sqlite3.connect('matsya.db')
    cur = conn.cursor()
    cur.execute('SELECT username, short_title, short_description, upload_time, short_file_path FROM short ORDER BY upload_time DESC')
    
    videos = cur.fetchall() 
    cur.close()
    conn.close()
    return render_template('index.html', videos=videos)

# Route to display the video upload form
@app.route('/upload-video-form')
def upload_video_form():
    return render_template('upload.html')

# Route to handle video upload
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'username' not in session:
        return "User is not logged in"
    
    short_title = request.form.get('title')
    short_description = request.form.get('description')
    video = request.files.get('video')

    if video:
        video_filename = secure_filename(video.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
        video.save(video_path)

        try:
            with sqlite3.connect('matsya.db') as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO short (username, short_title, short_description, short_file_path) VALUES (?, ?, ?, ?)', 
                            (session['username'], short_title, short_description, video_filename))  # Save only filename
                conn.commit()
            return redirect(url_for('home'))
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "No video file provided."

# Route to update user profile
@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        bio = request.form.get('bio')
        profile_picture = request.files.get('profile-picture')

        # Form validation
        if not all([name, email, phone_number, dob, gender, password, confirm_password, bio, address]):
            return "All fields are required!", 400
        
        if password != confirm_password:
            return "Passwords do not match!", 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save profile picture to directory
        profile_picture_path = None
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture_path = os.path.join(USER_UPLOAD_FOLDER, filename)
            profile_picture.save(profile_picture_path)

        # Insert data into the database
        try:
            conn = sqlite3.connect('matsya.db')
            conn.execute('''UPDATE user SET name=?, email=?, phone_number=?, dob=?, gender=?, password=?, bio=?, address=?, profile_photo=? WHERE username=?''', 
                         (name, email, phone_number, dob, gender, hashed_password, bio, address, filename, session['username']))
            conn.commit()
            message = "Profile updated successfully!"
        except Exception as e:
            conn.rollback()
            message = f"An error occurred: {e}"
        finally:
            conn.close()

        return message

    return render_template('complete_profile.html')

# Additional routes to render templates for each section
@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/trending')
def trending():
    return render_template('trending.html')
@app.route('/history')
def history():
    return render_template('history.html')
@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/menu_item_8')
def menu_item_8():
    return render_template('trending.html')
@app.route('/menu_item_9')
def menu_item_9():
    return render_template('trending.html')
@app.route('/menu_item_10')
def menu_item_10():
    return render_template('trending.html')
@app.route('/menu_item_11')
def menu_item_11():
    return render_template('trending.html')
@app.route('/menu_item_12')
def menu_item_12():
    return render_template('trending.html')
# Route to upload short videos
@app.route('/upload_short', methods=['GET', 'POST'])
def upload_short():
    if 'username' not in session:
        return "User is not logged in"

    if request.method == 'POST':
        short_title = request.form.get('title')
        short_description = request.form.get('description')
        video = request.files.get('video')

        if video:
            video_filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['USER_UPLOAD_FOLDER'], video_filename)
            video.save(video_path)

            try:
                with sqlite3.connect('matsya.db') as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO short (username, short_title, short_description, short_file_path) VALUES (?, ?, ?, ?)', 
                                (session['username'], short_title, short_description, video_filename))
                    conn.commit()

                return redirect(url_for('home'))
            except sqlite3.OperationalError as e:
                return f"Database error: {str(e)} - Table 'short' may not exist."
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "No video file provided."

    return render_template('upload_short.html')

# Route to serve uploaded profile pictures
@app.route('/uploads/<path:filename>')
def uploads_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to serve user-uploaded videos
@app.route('/user_uploads/<path:filename>')
def user_uploads_file(filename):
    return send_from_directory(app.config['USER_UPLOAD_FOLDER'], filename)

# Route to display video with profile info
@app.route('/play_short')
def play_short():
    conn = sqlite3.connect('matsya.db')
    cur = conn.cursor()
    cur.execute('''SELECT short.*, user.profile_photo FROM short JOIN user ON short.username = user.username''')
    shorts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('play_short.html', shorts=shorts)
@app.route('/comment', methods=['POST'])
def comment():
    # सबसे पहले चेक करें कि यूज़र लॉगिन है या नहीं
    if 'username' in session and 'id' in session:
        username = session['username']
        user_id = session['id']
    else:
        return jsonify(success=False, error="User not logged in")

    # JSON डेटा प्राप्त करें
    data = request.get_json()
    video_id = data.get('video_id')
    content = data.get('content')  # ✅ यूज़र का कमेंट

    # डेटा वेरिफिकेशन
    if not video_id or not content:
        return jsonify(success=False, error="Video ID or comment content is missing")

    try:
        # SQLite3 से कनेक्ट करें
        conn = sqlite3.connect('matsya.db')
        cur = conn.cursor()

        # कमेंट को डेटाबेस में सेव करें
        commented_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # ✅ सही डेट फॉर्मेट

        cur.execute('INSERT INTO comment (user_id, video_id, comment, commented_at) VALUES (?, ?, ?, ?)', 
                    (user_id, video_id, content, commented_at))

        conn.commit()  # ✅ चेंजेस सेव करें
        cur.close()
        conn.close()

        return jsonify(success=True, message="Comment added successfully")
    
    except Exception as e:
        print(f"Error: {e}")  # Debugging के लिए
        return jsonify(success=False, error="Database error occurred")
@app.route('/like', methods=['POST'])
def like_video():
    if 'id' not in session:
        return jsonify(success=False, error="User not logged in")

    user_id = session['id']
    data = request.get_json()
    video_id = data.get('videoId')

    if not video_id:
        return jsonify(success=False, error="Video ID is missing")

    try:
        conn = sqlite3.connect('matsya.db')
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM likees WHERE user_id = ? AND video_id = ?", (user_id, video_id))
        existing_like = cur.fetchone()

        if existing_like:
            cur.execute("DELETE FROM likees WHERE user_id = ? AND video_id = ?", (user_id, video_id))
            cur.execute("UPDATE videos SET like_count = MAX(like_count - 1, 0) WHERE id = ?", (video_id,))
            message = "Like removed"
        else:
            cur.execute("INSERT INTO likees (user_id, video_id, liked_at) VALUES (?, ?, ?)",
                        (user_id, video_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            cur.execute("UPDATE videos SET like_count = like_count + 1 WHERE id = ?", (video_id,))
            message = "Like added"

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(success=True, message=message)

    except Exception as e:
        return jsonify(success=False, error=str(e))
if __name__ == '__main__':
    app.run(debug=True)