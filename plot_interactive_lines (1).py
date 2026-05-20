import pandas as pd
import plotly.graph_objects as go
import sys

# Configuration
CSV_FILE = 'your_data.csv'  # Change this to your CSV file path
OUTPUT_FILE = 'interactive_plot.html'

# Column mapping - rename MBES_0d_5m to bathydata for display
COLUMNS_TO_PLOT = {
    'MBES_0d_5m': 'Bathydata',
    'DOL': 'DOL',
    'DOT': 'DOT',
    'H30': 'H30',
    'H10': 'H10',
    'H20': 'H20'
}

try:
    # Read the CSV file
    df = pd.read_csv(CSV_FILE)
    print(f"✓ CSV loaded successfully. Shape: {df.shape}")
    
    # Check which columns exist in the CSV
    available_columns = [col for col in COLUMNS_TO_PLOT.keys() if col in df.columns]
    missing_columns = [col for col in COLUMNS_TO_PLOT.keys() if col not in df.columns]
    
    if missing_columns:
        print(f"⚠ Warning: The following columns are missing: {missing_columns}")
    
    if not available_columns:
        print("✗ Error: None of the required columns found in CSV")
        print(f"Available columns: {df.columns.tolist()}")
        sys.exit(1)
    
    # Select only the required columns that exist
    df_filtered = df[available_columns].copy()
    
    # Create index for x-axis (row numbers or you can use df.index)
    x_axis = list(range(len(df_filtered)))
    
    # Create the interactive plot
    fig = go.Figure()
    
    # Add a trace for each column
    for col_original, col_display in COLUMNS_TO_PLOT.items():
        if col_original in df_filtered.columns:
            # This automatically skips NaN values in the plot
            fig.add_trace(go.Scatter(
                x=x_axis,
                y=df_filtered[col_original],
                mode='lines',
                name=col_display,
                hovertemplate='<b>' + col_display + '</b><br>Index: %{x}<br>Value: %{y}<extra></extra>'
            ))
    
    # Update layout for better visualization
    fig.update_layout(
        title='Multiple Line Graph - Water/Bathymetry Data',
        xaxis_title='Sample Index',
        yaxis_title='Value',
        hovermode='x unified',
        template='plotly_white',
        width=1200,
        height=600,
        font=dict(size=12),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="gray",
            borderwidth=1
        ),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    )
    
    # Save the interactive plot
    fig.write_html(OUTPUT_FILE)
    print(f"✓ Interactive plot saved to: {OUTPUT_FILE}")
    print(f"✓ Plotted columns: {', '.join([COLUMNS_TO_PLOT[col] for col in available_columns])}")
    print(f"✓ Total data points per series: {len(df_filtered)}")
    
    # Show the plot (uncomment if you want to open in browser)
    # fig.show()
    
except FileNotFoundError:
    print(f"✗ Error: CSV file '{CSV_FILE}' not found")
    print("Please update the CSV_FILE variable with the correct path")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {str(e)}")
    sys.exit(1)

