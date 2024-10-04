from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import pandas as pd
import os
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Clustering function
def cluster_shipments(shipments):
    # Use shipment dimensions (length, width, height) and fragile status as features
    X = np.array([[s['length'], s['width'], s['height'], 1 if s['fragile'] == 'yes' else 0] for s in shipments])

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=3)  # Assuming we group into 3 clusters
    kmeans.fit(X)
    
    # Assign cluster labels to shipments
    clusters = kmeans.predict(X)
    for i, shipment in enumerate(shipments):
        shipment['cluster'] = clusters[i]

    return shipments

# Visualization function
def visualize_3d(container_dimensions, shipments):
    fig = go.Figure()

    # Add container (transparent to visualize inside)
    fig.add_trace(go.Mesh3d(
        x=[0, container_dimensions['length'], container_dimensions['length'], 0, 0, container_dimensions['length'], container_dimensions['length'], 0],
        y=[0, 0, container_dimensions['width'], container_dimensions['width'], 0, 0, container_dimensions['width'], container_dimensions['width']],
        z=[0, 0, 0, 0, container_dimensions['height'], container_dimensions['height'], container_dimensions['height'], container_dimensions['height']],
        opacity=0.2,
        color='blue',
        name='Container'
    ))

    # Add shipments with cluster-based coloring
    colors = ['green', 'orange', 'red']  # Different colors for clusters
    for shipment in shipments:
        color = colors[shipment['cluster']]  # Color based on cluster
        fig.add_trace(go.Mesh3d(
            x=[shipment['x'], shipment['x'] + shipment['length'], shipment['x'] + shipment['length'], shipment['x'], shipment['x'], shipment['x'] + shipment['length'], shipment['x'] + shipment['length'], shipment['x']],
            y=[shipment['y'], shipment['y'], shipment['y'] + shipment['width'], shipment['y'] + shipment['width'], shipment['y'], shipment['y'], shipment['y'] + shipment['width'], shipment['y'] + shipment['width']],
            z=[shipment['z'], shipment['z'], shipment['z'], shipment['z'], shipment['z'] + shipment['height'], shipment['z'] + shipment['height'], shipment['z'] + shipment['height'], shipment['z'] + shipment['height']],
            opacity=0.6,
            color=color,
            name=f'Shipment {shipment["id"]} (Cluster {shipment["cluster"]})'
        ))

    # Customize layout
    fig.update_layout(
        scene=dict(
            xaxis_title='Length',
            yaxis_title='Width',
            zaxis_title='Height'
        ),
        title="Container Load Visualization with Clustering",
        autosize=True
    )

    return fig.to_html(full_html=False)

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

        # Extract container dimensions
        container_dimensions = {
            'length': df['container_length'].iloc[0],
            'width': df['container_width'].iloc[0],
            'height': df['container_height'].iloc[0]
        }

        # Extract shipments
        shipments = df[['id', 'x', 'y', 'z', 'length', 'width', 'height', 'fragile']].to_dict('records')

        # Cluster shipments
        clustered_shipments = cluster_shipments(shipments)

        # Generate visualization
        plot_html = visualize_3d(container_dimensions, clustered_shipments)

        return render_template('visualization.html', plot_html=plot_html)

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=83)
