📦 Intelligent Cargo Load Optimization
An advanced cargo loading optimization system using machine learning and 3D visualization. This project enables intelligent container load calculations and provides users with the best possible 3D visualization of shipment arrangements in a container, utilizing clustering algorithms to optimize load distribution.

![image](https://github.com/user-attachments/assets/7b36d25b-10d7-4b83-b0b0-3c9bb08b7fbd)


🚀 Features
3D Load Visualization: Utilizes Three.js to render cargo containers and shipments in 3D.
Machine Learning Optimization: Applies clustering algorithms to optimize the placement of shipments within the container for better space utilization.
CSV Input: Accepts custom shipment data via CSV files to generate visualizations dynamically.
Fragile Item Highlighting: Color-codes shipments (orange for fragile items, green for others) for easy identification.
User-friendly UI: Built using Flask, with a clean and modern web interface.
📁 Project Structure
bash
Copy code
├── app.py              # The main Flask application
├── static/             # Static assets (CSS, JS, Images)
├── templates/
│   ├── index.html      # Upload page
│   └── visualization.html # 3D visualization page
├── uploads/            # Folder for storing uploaded CSV files
└── README.md           # This readme file
🛠️ Technologies Used
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript
3D Visualization: Three.js
Machine Learning: Clustering algorithms for shipment optimization
Data Handling: Pandas for CSV file processing
📋 Installation and Setup
Follow these steps to set up the project locally.

Prerequisites
Python 3.7+
Flask
Pandas
Three.js (served via CDN in visualization.html)
Steps
Clone the repository

bash
Copy code
git clone https://github.com/7009soham/intelligent-cargo-load-optimization.git
cd intelligent-cargo-load-optimization
Create a virtual environment (optional but recommended)

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the Flask app

bash
Copy code
python app.py
Visit the app in your browser at:

arduino
Copy code
http://localhost:83
📝 CSV File Structure
Your CSV file should contain the following columns:

container_length	container_width	container_height	id	x	y	z	length	width	height	fragile
12	2.4	2.6	1	0.0	0.0	0.0	1.0	1.0	1.0	yes
...	...	...	...	...	...	...	...	...	...	...
Fragile: Should be marked as either "yes" or "no" to indicate if the item is fragile.
📊 Example Visualization
![image](https://github.com/user-attachments/assets/e4edf9ad-e070-4216-b2ab-aac210178065)


The above example shows how the containers and cargo items are visualized with their 3D positions and sizes.

🤖 Machine Learning Approach
This project uses clustering algorithms to optimize how the items are packed into the container:

K-Means Clustering: Helps distribute cargo in groups based on item size and volume to maximize space.
DBSCAN: Used for handling density-based clustering of items in tight spaces.
📂 File Upload and Visualization
Go to the home page.
Upload your shipment data as a CSV file.
Click Visualize to generate the 3D cargo arrangement.
🛡️ License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Collaborators
Soham Tare
Ankush Singh
