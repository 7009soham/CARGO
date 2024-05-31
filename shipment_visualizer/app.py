from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import pandas as pd
import plotly.graph_objects as go
import os
import time
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def visualize_3d(container_dimensions, shipments):
    fig = go.Figure()

    # Plot container edges
    fig.add_trace(go.Mesh3d(
        x=[0, container_dimensions['length'], container_dimensions['length'], 0, 0, container_dimensions['length'], container_dimensions['length'], 0],
        y=[0, 0, container_dimensions['width'], container_dimensions['width'], 0, 0, container_dimensions['width'], container_dimensions['width']],
        z=[0, 0, 0, 0, container_dimensions['height'], container_dimensions['height'], container_dimensions['height'], container_dimensions['height']],
        i=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
        j=[1, 2, 3, 2, 3, 0, 3, 0, 1, 0, 1, 2],
        k=[3, 3, 2, 0, 0, 3, 1, 1, 0, 2, 2, 1],
        opacity=0.1,
        color='blue',
        name='Container'
    ))

    # Plot shipments
    for shipment in shipments:
        x, y, z = shipment['x'], shipment['y'], shipment['z']
        length, width, height = shipment['length'], shipment['width'], shipment['height']

        color = 'orange' if shipment.get('fragile') == 'yes' else 'green'
        
        fig.add_trace(go.Mesh3d(
            x=[x, x+length, x+length, x, x, x+length, x+length, x],
            y=[y, y, y+width, y+width, y, y, y+width, y+width],
            z=[z, z, z, z, z+height, z+height, z+height, z+height],
            i=[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
            j=[1, 2, 3, 2, 3, 0, 3, 0, 1, 0, 1, 2],
            k=[3, 3, 2, 0, 0, 3, 1, 1, 0, 2, 2, 1],
            opacity=0.5,
            color=color,
            name=f'Shipment {shipment["id"]}'
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Length'),
            yaxis=dict(title='Width'),
            zaxis=dict(title='Height')
        )
    )

    # Generate a unique filename using timestamp and UUID
    filename = f'visualization_{int(time.time())}_{uuid.uuid4()}.html'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save the plot as an HTML file
    fig.write_html(filepath)

    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)

        # Validate columns
        required_columns = ['container_length', 'container_width', 'container_height', 'id', 'x', 'y', 'z', 'length', 'width', 'height', 'fragile']
        if not all(col in df.columns for col in required_columns):
            return 'Error: CSV file is missing one or more required columns.'

        # Assuming the CSV file contains the necessary columns
        container_dimensions = {
            'length': df['container_length'].iloc[0],
            'width': df['container_width'].iloc[0],
            'height': df['container_height'].iloc[0]
        }

        shipments = df[['id', 'x', 'y', 'z', 'length', 'width', 'height', 'fragile']].to_dict('records')

        # Generate visualization
        visualization_filename = visualize_3d(container_dimensions, shipments)
        
        return render_template('visualization.html', visualization_filename=visualization_filename)

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001)
