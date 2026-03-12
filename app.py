from flask import Flask, request, render_template, redirect, url_for, flash
import random
from database import *
import time
from common import *
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Initialize database
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        
        if url:
            try:
                # Validate URL format
                try:
                    url.replace(' ', '')
                except:
                    pass
                if not url.startswith('https://'):
                    url = 'https://' + url
                if 'https://www.gasbuddy' not in url:
                    flash('Support only gasbuddy')
                    return redirect(url_for('index'))
                name_data, price_data, updated_data, gmap_link = fetch_data(url)
                
                # Add to database with scraped data
                add_website(url, name_data, price_data, updated_data, gmap_link)
                flash('Website added successfully with scraped data!', 'success')
            except Exception as e:
                print(e)
                flash(f'Error adding website: {str(e)}', 'error')
        else:
            flash('URL and Name are required!', 'error')
        
        return redirect(url_for('index'))
    
    elif request.method == 'GET':
        # Get all websites from database
        websites = get_all_websites()
        return render_template('index.html', websites=websites)

@app.route('/update_all', methods=['POST'])
def update_all():
    websites = get_all_websites()
    try:
        for w in websites:
            update_data(w[0])
            time.sleep(random.uniform(1.1,1.9))
        flash('Data updated successfully!', 'success')
    except:
        None
    return redirect(url_for('index'))

@app.route('/delete/<int:website_id>')
def delete(website_id):
    delete_website(website_id)
    flash('Website deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/update_data/<int:website_id>')
def update_data(website_id):
    try:
        # Get website URL from database
                # Direct database access without connection pooling issues
        conn = sqlite3.connect('websites.db')
        c = conn.cursor()
        c.execute('SELECT url FROM websites WHERE id = ?', (website_id,))
        result = c.fetchone()
        conn.close()
        
        if result:
            url = result[0]
            name_data, price_data, updated_data, gmap_link = fetch_data(url)
            # Update database
            update_website_data(website_id, name_data, price_data, updated_data, gmap_link)
        else:
            print(e)
            flash('Website not found!', url)
    except Exception as e:
        print(e)
        flash(f'Error updating data: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
