import streamlit as st
import pandas as pd
import numpy as np
import re
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time
import os

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Set page configuration
st.set_page_config(
    page_title="CleanSheet Matching Engine™",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main color palette */
    :root {
        --primary-color: #0A1F38;     /* Deep Navy */
        --accent-color: #58B4AE;      /* Teal */
        --background-color: #F5F7FA;  /* Light Grey */
        --text-color: #333333;        /* Dark Grey for text */
        --light-accent: #E8F4F3;      /* Light Teal for backgrounds */
        --highlight: #FF9D5C;         /* Orange highlight */
        --success: #4CAF50;           /* Green for success messages */
        --warning: #FFC107;           /* Yellow for warnings */
        --error: #F44336;             /* Red for errors */
    }

    /* Global styling */
    .stApp {
        background-color: var(--background-color);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', 'Segoe UI', 'Montserrat', sans-serif;
        font-weight: 600;
        color: var(--primary-color);
    }
    p, li, div {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: var(--text-color);
    }

    /* Header styling */
    .main-header {
        color: var(--primary-color);
        font-family: 'Inter', 'Segoe UI', 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0;
        letter-spacing: -0.5px;
    }

    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(10, 31, 56, 0.1);
        padding-bottom: 1rem;
    }

    .logo-text {
        display: flex;
        align-items: center;
    }

    .logo-icon {
        font-size: 2.5rem;
        margin-right: 0.5rem;
        color: var(--accent-color);
    }

    /* Version tag */
    .version-tag {
        font-size: 0.8rem;
        color: var(--accent-color);
        font-weight: 500;
        background-color: rgba(88, 180, 174, 0.1);
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-left: 1rem;
    }

    /* Subtitle */
    .subtitle {
        font-size: 1.1rem;
        color: #555;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }

    /* Card styling */
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border-top: 4px solid var(--accent-color);
    }

    .card-header {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: var(--primary-color);
        display: flex;
        align-items: center;
    }

    .card-icon {
        margin-right: 0.5rem;
        color: var(--accent-color);
    }

    /* Button styling */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px rgba(10, 31, 56, 0.15) !important;
    }
    .stButton>button:hover {
        background-color: #152D4A !important;
        box-shadow: 0 4px 8px rgba(10, 31, 56, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 1px 3px rgba(10, 31, 56, 0.1) !important;
    }

    /* Download button */
    .download-button {
        background-color: var(--accent-color) !important;
        color: white !important;
    }
    .download-button:hover {
        background-color: #4A9E99 !important;
    }

    /* Slider and checkbox accent colors */
    .stSlider>div>div>div {
        background-color: var(--accent-color) !important;
    }
    .stCheckbox>div>div>div {
        background-color: var(--accent-color) !important;
    }

    /* File uploader styling */
    .stFileUploader>div>button {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    .stFileUploader>div {
        border: 1px dashed #CCD4E0 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
        padding: 1.5rem !important;
        background-color: white !important;
    }
    .stFileUploader>div:hover {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 1px var(--accent-color);
    }

    /* Sidebar styling */
    .css-1d391kg, .css-163ttbj, .css-1wrcr25 {
        background-color: white !important;
    }

    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(10, 31, 56, 0.1);
    }

    .sidebar-subheader {
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
    }

    .sidebar-icon {
        margin-right: 0.5rem;
        color: var(--accent-color);
    }

    /* Metrics styling */
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        text-align: center;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.25rem;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }

    /* Table styling */
    .dataframe-container {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    .dataframe {
        border-collapse: collapse;
        width: 100%;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    .dataframe th {
        background-color: var(--primary-color);
        color: white;
        font-weight: 500;
        text-align: left;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
    }

    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #eee;
        font-size: 0.9rem;
    }

    .dataframe tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    .dataframe tr:hover {
        background-color: var(--light-accent);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f8;
        border-radius: 4px 4px 0 0;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-top: 3px solid var(--accent-color) !important;
    }

    /* Loading animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }

    .loading-spinner::after {
        content: "";
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid var(--accent-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* Footer styling */
    .footer {
        font-size: 0.85rem;
        color: #6c757d;
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(10, 31, 56, 0.1);
    }

    .footer-logo {
        font-weight: 600;
        color: var(--primary-color);
    }

    .footer-links {
        margin-top: 0.5rem;
    }

    .footer-link {
        color: var(--accent-color);
        text-decoration: none;
        margin: 0 0.5rem;
    }

    .footer-link:hover {
        text-decoration: underline;
    }

    /* Flag styling */
    .flag-review {
        background-color: rgba(255, 193, 7, 0.1);
        color: #856404;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* Confidence score styling */
    .high-confidence {
        color: #28a745;
        font-weight: 500;
    }

    .medium-confidence {
        color: #fd7e14;
        font-weight: 500;
    }

    .low-confidence {
        color: #dc3545;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('''
<div class="header-container">
    <div class="logo-text">
        <span class="logo-icon">🧹</span>
        <h1 class="main-header">CleanSheet Matching Engine™<span class="version-tag">Matching Drop v1.0</span></h1>
    </div>
</div>
<p class="subtitle">
    <strong>One-click matching. Clean names. Reliable totals.</strong><br>
    This enterprise-grade engine cleans and standardizes product names across your sales and inventory datasets.
    No dictionary. No delay. Just clean, reliable data for your finance team.
</p>
<div class="card">
    <div class="card-header">
        <span class="card-icon">📊</span>
        Welcome to CleanSheet Matching Engine™
    </div>
    <p>
        Our advanced NLP-based matching algorithm helps finance teams reconcile product data across systems.
        Upload your files below to transform messy product names into clean, standardized data.
    </p>
    <ul>
        <li><strong>Token-based matching</strong> - Intelligently groups similar products</li>
        <li><strong>Variant protection</strong> - Prevents incorrect grouping of different product variants</li>
        <li><strong>Size protection</strong> - Ensures products with different sizes remain separate</li>
        <li><strong>Confidence scoring</strong> - Flags uncertain matches for manual review</li>
    </ul>
</div>
''', unsafe_allow_html=True)

# Sidebar for configuration
st.sidebar.markdown('<div class="sidebar-header">Configuration Panel</div>', unsafe_allow_html=True)

# File upload section
st.sidebar.markdown('<div class="sidebar-subheader"><span class="sidebar-icon">📁</span> Drop Zone: Your Raw Inputs</div>', unsafe_allow_html=True)

st.sidebar.markdown('''
<div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
    Upload your files below to begin the matching process.
</div>
''', unsafe_allow_html=True)

sales_file = st.sidebar.file_uploader(
    "Upload File 1 (CSV)",
    type=["csv"],
    help="CSV file containing labels and metric data"
)

inventory_file = st.sidebar.file_uploader(
    "Upload File 2 (CSV)",
    type=["csv"],
    help="CSV file containing labels and metric data"
)

# Advanced settings
st.sidebar.markdown('<div class="sidebar-subheader"><span class="sidebar-icon">⚙️</span> Matching Settings</div>', unsafe_allow_html=True)

st.sidebar.markdown('''
<div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
    Adjust these parameters to fine-tune the matching algorithm.
</div>
''', unsafe_allow_html=True)

min_similarity = st.sidebar.slider(
    "Minimum Similarity Score",
    0.0, 1.0, 0.7, 0.05,
    help="Minimum similarity threshold for considering products as matches. Higher values require more token matches."
)

st.sidebar.markdown('<div class="sidebar-subheader"><span class="sidebar-icon">🛡️</span> Protection Settings</div>', unsafe_allow_html=True)

variant_protection = st.sidebar.checkbox(
    "Enable Variant Protection",
    value=True,
    help="Prevent grouping products with conflicting variants (e.g., Pro vs Mini, Basic vs Premium)"
)

size_protection = st.sidebar.checkbox(
    "Enable Size Protection",
    value=True,
    help="Prevent grouping products with different sizes or volumes (e.g., 32in vs 50in, 330ml vs 500ml)"
)

st.sidebar.markdown('<div class="sidebar-subheader"><span class="sidebar-icon">🔍</span> Review Settings</div>', unsafe_allow_html=True)

manual_review_threshold = st.sidebar.slider(
    "Manual Review Threshold",
    0.0, 1.0, 0.5, 0.05,
    help="Confidence score below which products are flagged for manual review. Lower values flag more items."
)

# Helper functions for text preprocessing
def preprocess_text(text):
    """Clean and normalize text for better matching"""
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Replace special characters with spaces
    text = re.sub(r'[^\w\s]', ' ', text)

    # Replace underscores with spaces
    text = text.replace('_', ' ')

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def extract_tokens(product_name):
    """Extract meaningful tokens from product name"""
    if not isinstance(product_name, str):
        return []

    # Preprocess the text
    text = preprocess_text(product_name)

    # Simple tokenization by splitting on spaces
    tokens = text.split()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    return tokens

def extract_size_info(product_name):
    """Extract size information from product name"""
    if not isinstance(product_name, str):
        return None

    # Preprocess the product name to handle concatenated tokens
    # Insert spaces before digits to help with pattern matching
    processed_name = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', product_name.lower())

    # Look for common size patterns
    size_patterns = [
        r'(\d+)\s*in',  # e.g., 32in, 32 in
        r'(\d+)\s*inch',  # e.g., 32inch, 32 inch
        r'(\d+)\s*ml',  # e.g., 330ml, 330 ml
        r'(\d+)\s*l\b',  # e.g., 1l, 1 l
        r'(\d+)l\b',  # e.g., 1l, 2l
        r'(\d+)\s*oz',  # e.g., 16oz, 16 oz
        r'(\d+)\s*gb',  # e.g., 64gb, 64 gb
        r'(\d+)\s*tb',  # e.g., 1tb, 1 tb
        r'(\d+)\s*kg',  # e.g., 1kg, 1 kg
        r'(\d+)\s*g\b',  # e.g., 200g, 200 g
        r'(\d+)g\b',  # e.g., 200g
    ]

    # Try both the original and processed names
    for name in [product_name.lower(), processed_name]:
        for pattern in size_patterns:
            match = re.search(pattern, name)
            if match:
                return match.group(1)

    # Also check for standalone numbers that might be sizes
    # Only include standalone numbers if they're likely to be sizes (e.g., 13, 32, 40, 50)
    size_numbers = ['13', '32', '40', '50', '55', '65', '75']
    tokens = product_name.lower().split()
    for token in tokens:
        if token in size_numbers:
            return token

    return None

def extract_size_unit(product_name):
    """Extract size unit from product name"""
    if not isinstance(product_name, str):
        return None

    # Preprocess the product name to handle concatenated tokens
    # Insert spaces before digits to help with pattern matching
    processed_name = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', product_name.lower())

    # Look for common unit patterns
    unit_patterns = [
        (r'\d+\s*(in|inch)', 'in'),
        (r'\d+\s*(ml)', 'ml'),
        (r'\d+\s*(l)\b', 'L'),
        (r'\d+l\b', 'L'),
        (r'\d+\s*(oz)', 'oz'),
        (r'\d+\s*(gb)', 'GB'),
        (r'\d+\s*(tb)', 'TB'),
        (r'\d+\s*(kg)', 'kg'),
        (r'\d+\s*(g)\b', 'g'),
        (r'\d+g\b', 'g'),
    ]

    # Try both the original and processed names
    for name in [product_name.lower(), processed_name]:
        for pattern, unit in unit_patterns:
            if re.search(pattern, name):
                return unit

    return None

def extract_variant_tokens(product_name):
    """Extract all variant tokens (size, volume, weight) that should be treated as hard split conditions"""
    if not isinstance(product_name, str):
        return []

    # Preprocess the product name to handle concatenated tokens
    # Insert spaces before digits to help with pattern matching
    processed_name = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', product_name.lower())

    # Look for all variant tokens
    variant_patterns = [
        # Volume patterns
        r'(\d+\s*ml)',  # e.g., 500ml, 500 ml
        r'(\d+\s*l\b)',  # e.g., 2L, 2 L
        r'(\d+l\b)',  # e.g., 2L
        r'(\d+\s*oz)',  # e.g., 16oz, 16 oz

        # Weight patterns
        r'(\d+\s*kg)',  # e.g., 1kg, 1 kg
        r'(\d+\s*g\b)',  # e.g., 200g, 200 g
        r'(\d+g\b)',  # e.g., 200g

        # Size patterns
        r'(\d+\s*in)',  # e.g., 32in, 32 in
        r'(\d+\s*inch)',  # e.g., 32inch, 32 inch
        r'(\d+\s*gb)',  # e.g., 64gb, 64 gb
        r'(\d+\s*tb)',  # e.g., 1tb, 1 tb
    ]

    variant_tokens = []

    # Apply patterns to both original and processed names
    for name in [product_name.lower(), processed_name]:
        for pattern in variant_patterns:
            matches = re.findall(pattern, name)
            variant_tokens.extend([match.strip() for match in matches])

    # Also check for standalone numbers that might be sizes
    # Only include standalone numbers if they're likely to be sizes (e.g., 13, 32, 40, 50)
    size_numbers = ['13', '32', '40', '50', '55', '65', '75']

    # Check in both original tokens and processed tokens
    for name in [product_name.lower(), processed_name]:
        tokens = name.split()
        for token in tokens:
            if token in size_numbers:
                variant_tokens.append(token)

    # Remove duplicates while preserving order
    seen = set()
    unique_tokens = []
    for token in variant_tokens:
        if token not in seen:
            seen.add(token)
            unique_tokens.append(token)

    return unique_tokens

def extract_brand(product_name):
    """Extract potential brand name from product name"""
    if not isinstance(product_name, str):
        return None

    # Common brand names to look for
    common_brands = [
        'samsung', 'apple', 'sony', 'lg', 'coca-cola', 'coke', 'pepsi',
        'microsoft', 'dell', 'hp', 'lenovo', 'asus', 'acer', 'toshiba'
    ]

    tokens = extract_tokens(product_name)

    # Check if any token matches a common brand
    for token in tokens:
        if token.lower() in common_brands:
            return token

    # If no match, assume first token might be brand
    if tokens:
        return tokens[0]

    return None

def extract_variant_info(product_name):
    """Extract variant information from product name"""
    if not isinstance(product_name, str):
        return []

    # Common variant keywords
    variant_keywords = [
        'pro', 'mini', 'max', 'plus', 'basic', 'smart', 'vanilla', 'zero',
        'premium', 'standard', 'lite', 'ultra', 'gold', 'silver', 'black', 'white'
    ]

    tokens = extract_tokens(product_name.lower())
    variants = [token for token in tokens if token in variant_keywords]

    return variants

def calculate_token_similarity(name1, name2):
    """Calculate similarity based on shared tokens"""
    tokens1 = set(extract_tokens(name1))
    tokens2 = set(extract_tokens(name2))

    if not tokens1 or not tokens2:
        return 0.0

    # Calculate Jaccard similarity
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))

    return intersection / union if union > 0 else 0.0

def check_variant_conflict(name1, name2):
    """Check if there's a variant conflict between two product names"""
    if not variant_protection:
        return False

    variants1 = extract_variant_info(name1)
    variants2 = extract_variant_info(name2)

    # If both have variants but they don't match, it's a conflict
    if variants1 and variants2 and not set(variants1).intersection(set(variants2)):
        return True

    return False

def check_size_conflict(name1, name2):
    """Check if there's a size conflict between two product names"""
    if not size_protection:
        return False

    # First check using the traditional size extraction
    size1 = extract_size_info(name1)
    size2 = extract_size_info(name2)

    # If both have sizes but they don't match, it's a conflict
    if size1 and size2 and size1 != size2:
        return True

    # Now check using the variant tokens approach for more comprehensive protection
    variant_tokens1 = extract_variant_tokens(name1)
    variant_tokens2 = extract_variant_tokens(name2)

    # If both have variant tokens but they don't share any, it's a conflict
    if variant_tokens1 and variant_tokens2:
        # Check if there's any overlap in variant tokens
        if not set(variant_tokens1).intersection(set(variant_tokens2)):
            return True

    return False

def standardize_product_name(product_name, product_group):
    """Generate a standardized name for a product based on its group"""
    if not product_group:
        return product_name

    # Extract common tokens across the group
    all_tokens = []
    all_variants = []
    all_sizes = []
    all_size_units = []
    all_brands = []

    # Extract variant tokens for the specific product - will be used for size/unit extraction

    for name in product_group:
        all_tokens.extend(extract_tokens(name))
        all_variants.extend(extract_variant_info(name))

        size = extract_size_info(name)
        if size:
            all_sizes.append(size)

        size_unit = extract_size_unit(name)
        if size_unit:
            all_size_units.append(size_unit)

        brand = extract_brand(name)
        if brand:
            all_brands.append(brand)

    # Count token frequencies
    token_counts = Counter(all_tokens)
    variant_counts = Counter(all_variants)
    size_counts = Counter(all_sizes)
    size_unit_counts = Counter(all_size_units)
    brand_counts = Counter(all_brands)

    # For this specific product, use its own size/variant tokens
    # instead of the most common ones from the group
    product_size = extract_size_info(product_name)
    product_size_unit = extract_size_unit(product_name)

    # Get the most common size only if this product doesn't have one
    common_size = product_size if product_size else (size_counts.most_common(1)[0][0] if size_counts else None)

    # Get the most common size unit only if this product doesn't have one
    common_size_unit = product_size_unit if product_size_unit else (size_unit_counts.most_common(1)[0][0] if size_unit_counts else None)

    # Check if the specific product has a variant
    product_variants = extract_variant_info(product_name)

    # Build standardized name
    std_name_parts = []

    # Format based on product type
    if any('tv' in token.lower() for token in all_tokens):
        # Samsung TV format: "Samsung TV 32in Smart"
        std_name_parts.append('Samsung')
        std_name_parts.append('TV')

        # Add size - use the product's own size if available
        product_size = extract_size_info(product_name)

        if product_size:
            std_name_parts.append(f"{product_size}in")
        elif common_size:
            std_name_parts.append(f"{common_size}in")

        # Add variant
        if 'smart' in product_name.lower() or any(name for name in product_group if 'smart' in name.lower() and calculate_token_similarity(name, product_name) > 0.7):
            std_name_parts.append('Smart')
        elif 'basic' in product_name.lower() or any(name for name in product_group if 'basic' in name.lower() and calculate_token_similarity(name, product_name) > 0.7):
            std_name_parts.append('Basic')
        elif len(variant_counts) > 1 or not any(v for v in ['smart', 'basic'] if v in ' '.join(all_tokens).lower()):
            std_name_parts.append('(Unspecified Variant)')

    elif any('iphone' in token.lower() for token in all_tokens) or any('apple' in token.lower() for token in all_tokens):
        # iPhone format: "Apple iPhone 13 Pro"
        std_name_parts.append('Apple')
        std_name_parts.append('iPhone')

        # Add model number - check in the specific product first
        product_tokens = extract_tokens(product_name)
        model_added = False

        for token in product_tokens:
            if token.isdigit():
                std_name_parts.append(token)
                model_added = True
                break

        # If no model found in the product, look in the group
        if not model_added and any(token.isdigit() for token in all_tokens):
            for token in all_tokens:
                if token.isdigit():
                    std_name_parts.append(token)
                    break

        # Add variant - prioritize the product's own variant
        if 'pro' in product_name.lower():
            std_name_parts.append('Pro')
        elif 'mini' in product_name.lower():
            std_name_parts.append('Mini')
        elif any(name for name in product_group if 'pro' in name.lower() and calculate_token_similarity(name, product_name) > 0.7):
            std_name_parts.append('Pro')
        elif any(name for name in product_group if 'mini' in name.lower() and calculate_token_similarity(name, product_name) > 0.7):
            std_name_parts.append('Mini')
        elif len(variant_counts) > 1 or not any(v for v in ['pro', 'mini'] if v in ' '.join(all_tokens).lower()):
            std_name_parts.append('(Unspecified Variant)')

    elif any('coca' in token.lower() for token in all_tokens) or any('cola' in token.lower() for token in all_tokens):
        # Coca-Cola format: "Coca-Cola 330ml Vanilla"
        std_name_parts.append('Coca-Cola')

        # Add size - use the product's own size if available
        product_size = extract_size_info(product_name)
        product_size_unit = extract_size_unit(product_name)

        if product_size and product_size_unit:
            # Use the product's own size and unit
            if product_size_unit.lower() == 'ml':
                std_name_parts.append(f"{product_size}ml")
            elif product_size_unit.lower() == 'l':
                std_name_parts.append(f"{product_size}L")
        elif common_size:
            # Fallback to common size if product doesn't have one
            if any('ml' in token.lower() for token in all_tokens):
                std_name_parts.append(f"{common_size}ml")
            elif any('l' in token.lower() for token in all_tokens):
                std_name_parts.append(f"{common_size}L")

        # Add variant
        if 'vanilla' in product_name.lower() or any(name for name in product_group if 'vanilla' in name.lower() and calculate_token_similarity(name, product_name) > 0.7):
            std_name_parts.append('Vanilla')
        elif 'zero' in product_name.lower() or any(name for name in product_group if 'zero' in name.lower() and calculate_token_similarity(name, product_name) > 0.7):
            std_name_parts.append('Zero')

    else:
        # Generic format - use the original approach
        # Get the most common brand
        common_brand = brand_counts.most_common(1)[0][0] if brand_counts else None

        # Get the most common tokens (excluding brand, size, and variants)
        exclude_tokens = set()
        if common_brand:
            exclude_tokens.add(common_brand.lower())
        if common_size:
            exclude_tokens.add(common_size.lower())
        for variant in all_variants:
            exclude_tokens.add(variant.lower())

        common_tokens = [token for token, count in token_counts.most_common()
                        if count > len(product_group) / 3 and token.lower() not in exclude_tokens]

        # Add brand if available
        if common_brand:
            std_name_parts.append(common_brand.title())

        # Add common tokens
        std_name_parts.extend([token.title() for token in common_tokens[:2]])

        # Add size if available - use the product's own size if available
        product_size = extract_size_info(product_name)
        product_size_unit = extract_size_unit(product_name)

        if product_size and product_size_unit:
            std_name_parts.append(f"{product_size}{product_size_unit}")
        elif product_size:
            std_name_parts.append(f"{product_size}")
        elif common_size and common_size_unit:
            std_name_parts.append(f"{common_size}{common_size_unit}")
        elif common_size:
            std_name_parts.append(f"{common_size}")

        # Add specific variant if available
        if product_variants:
            std_name_parts.append(product_variants[0].title())
        elif variant_counts:
            # If no specific variant but multiple variants exist in the group
            if len(variant_counts) > 1:
                std_name_parts.append("(Unspecified Variant)")
            else:
                # Add the most common variant
                std_name_parts.append(variant_counts.most_common(1)[0][0].title())

    # Join all parts
    std_name = " ".join(std_name_parts)

    # If we couldn't generate a good name, fallback to original
    if not std_name or len(std_name_parts) < 2:
        return product_name

    return std_name

def group_similar_products(product_names):
    """Group similar product names together"""
    groups = []

    # First, pre-process products to extract variant tokens
    product_variants = {}
    for name in product_names:
        product_variants[name] = extract_variant_tokens(name)

    # Group products by variant tokens first
    variant_groups = {}
    for name, variants in product_variants.items():
        # Create a key from sorted variant tokens
        variant_key = tuple(sorted(variants)) if variants else ('no_variants',)
        if variant_key not in variant_groups:
            variant_groups[variant_key] = []
        variant_groups[variant_key].append(name)

    # Now process each variant group separately
    for variant_key, variant_products in variant_groups.items():
        # Skip processing if there's only one product in this variant group
        if len(variant_products) == 1:
            groups.append(variant_products)
            continue

        # Process products within this variant group
        variant_assigned = set()
        for i, name1 in enumerate(variant_products):
            if i in variant_assigned:
                continue

            current_group = [name1]
            variant_assigned.add(i)

            for j, name2 in enumerate(variant_products):
                if j in variant_assigned or i == j:
                    continue

                # Check for conflicts (still check variant conflicts for other variant types)
                if check_variant_conflict(name1, name2):
                    continue

                # Calculate similarity
                similarity = calculate_token_similarity(name1, name2)

                if similarity >= min_similarity:
                    current_group.append(name2)
                    variant_assigned.add(j)

            groups.append(current_group)

    return groups

def create_standardized_mapping(product_names):
    """Create a mapping from original names to standardized names"""
    groups = group_similar_products(product_names)
    mapping = {}
    confidence_scores = {}

    for group in groups:
        # Create standardized names for each product in the group
        for name in group:
            std_name = standardize_product_name(name, group)
            mapping[name] = std_name

            # Calculate confidence score
            confidence = calculate_token_similarity(name, std_name)

            # Adjust based on whether variants and sizes match
            if check_variant_conflict(name, std_name):
                confidence *= 0.5

            if check_size_conflict(name, std_name):
                confidence *= 0.5

            confidence_scores[name] = confidence

    return mapping, confidence_scores

def process_files(sales_df, inventory_df):
    """Process the sales and inventory files to create matched output"""
    start_time = time.time()

    # Extract all unique product names
    all_products = pd.concat([
        sales_df['Product'].drop_duplicates(),
        inventory_df['Product'].drop_duplicates()
    ]).drop_duplicates().tolist()

    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        # Update status
        status_text.text("Creating standardized mapping...")

        # Create standardized mapping
        std_mapping, confidence_scores = create_standardized_mapping(all_products)

        # Update progress
        progress_bar.progress(50)
        status_text.text("Applying mapping to data...")

        # Create summary dataframe
        summary_df = pd.DataFrame({
            'Product': list(std_mapping.keys()),
            'Standardized Name': [std_mapping[p] for p in std_mapping.keys()],
            'Confidence': [confidence_scores[p] for p in std_mapping.keys()]
        })

        # Add flag for manual review if confidence is low
        summary_df['Flag'] = summary_df['Confidence'].apply(
            lambda x: "Manual Review Needed" if x < manual_review_threshold else ""
        )

        # Apply mapping to sales and inventory dataframes
        sales_df['Standardized Name'] = sales_df['Product'].map(std_mapping)
        inventory_df['Standardized Name'] = inventory_df['Product'].map(std_mapping)

        # Group by standardized name and aggregate
        sales_agg = sales_df.groupby('Standardized Name')['Sales (£)'].sum().reset_index()
        inventory_agg = inventory_df.groupby('Standardized Name')['Inventory Units'].sum().reset_index()

        # Merge the aggregated dataframes
        matched_df = pd.merge(sales_agg, inventory_agg, on='Standardized Name', how='outer')

        # Fill NaN values with 0
        matched_df = matched_df.fillna(0)

        # Update progress
        progress_bar.progress(100)
        status_text.text(f"Processing complete! ({time.time() - start_time:.2f} seconds)")

        return matched_df, summary_df

    finally:
        # Ensure progress bar and status text are cleared even if an error occurs
        time.sleep(0.5)  # Short delay to ensure the progress bar is visible
        progress_bar.empty()
        status_text.empty()

# Main application logic
if sales_file and inventory_file:
    try:
        # Load data
        sales_df = pd.read_csv(sales_file)
        inventory_df = pd.read_csv(inventory_file)

        # Column selection for file 1
        st.markdown('''
        <div class="card">
            <div class="card-header">
                <span class="card-icon">📊</span>
                File 1 — Label & Metric
            </div>
            <p>
                Please select which columns from your first file contain the labels and metric values.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            sales_product_col = st.selectbox(
                "Select Label Column (File 1)",
                options=sales_df.columns.tolist(),
                index=sales_df.columns.tolist().index('Product') if 'Product' in sales_df.columns else 0,
                help="e.g. Product Name, Client, SKU, Region"
            )

        with col2:
            sales_units_col = st.selectbox(
                "Select Metric Column (File 1)",
                options=sales_df.columns.tolist(),
                index=sales_df.columns.tolist().index('Sales (£)') if 'Sales (£)' in sales_df.columns else 0,
                help="e.g. Sales, Units, Inventory, Spend"
            )

        # Column selection for file 2
        st.markdown('''
        <div class="card">
            <div class="card-header">
                <span class="card-icon">📦</span>
                File 2 — Label & Metric
            </div>
            <p>
                Please select which columns from your second file contain the labels and metric values.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            inventory_product_col = st.selectbox(
                "Select Label Column (File 2)",
                options=inventory_df.columns.tolist(),
                index=inventory_df.columns.tolist().index('Product') if 'Product' in inventory_df.columns else 0,
                help="e.g. Product Name, Client, SKU, Region"
            )

        with col2:
            inventory_units_col = st.selectbox(
                "Select Metric Column (File 2)",
                options=inventory_df.columns.tolist(),
                index=inventory_df.columns.tolist().index('Inventory Units') if 'Inventory Units' in inventory_df.columns else 0,
                help="e.g. Sales, Units, Inventory, Spend"
            )

        # Process button
        if st.button("Process Files", help="Click to start processing with selected columns"):
            # Store original column names for display
            file1_label_col = sales_product_col
            file1_metric_col = sales_units_col
            file2_label_col = inventory_product_col
            file2_metric_col = inventory_units_col

            # Rename columns to standardized names for processing
            sales_df = sales_df.rename(columns={
                sales_product_col: 'Product',
                sales_units_col: 'Sales (£)'
            })

            inventory_df = inventory_df.rename(columns={
                inventory_product_col: 'Product',
                inventory_units_col: 'Inventory Units'
            })

            # Process files
            loading_spinner = st.empty()
            loading_text = st.empty()

            with st.spinner(""):
                loading_spinner.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)
                loading_text.markdown('<div style="text-align: center; margin-bottom: 2rem;">Processing your files. This may take a moment...</div>', unsafe_allow_html=True)
                matched_df, summary_df = process_files(sales_df, inventory_df)

                # Rename columns in the matched_df to use original column names
                matched_df = matched_df.rename(columns={
                    'Sales (£)': file1_metric_col,
                    'Inventory Units': file2_metric_col
                })

                # Clear the loading elements after processing is complete
                loading_spinner.empty()
                loading_text.empty()

                # Success message
                st.success("✅ Processing complete! Your data has been matched and standardized.")

                # Display results in tabs
                tab1, tab2 = st.tabs(["📊 Clean View", "🔍 Matching Map"])

                with tab1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-header"><span class="card-icon">📊</span>Clean View</div>', unsafe_allow_html=True)
                    st.markdown(f'<p>This view shows your standardized data with aggregated {file1_metric_col} and {file2_metric_col} values.</p>', unsafe_allow_html=True)

                    # Statistics cards
                    st.markdown('<div style="margin-bottom: 1.5rem;">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'''
                        <div class="metric-container">
                            <div class="metric-value">{len(matched_df)}</div>
                            <div class="metric-label">Total Items</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'''
                        <div class="metric-container">
                            <div class="metric-value">{matched_df[file1_metric_col].sum():,.2f}</div>
                            <div class="metric-label">Total {file1_metric_col}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'''
                        <div class="metric-container">
                            <div class="metric-value">{matched_df[file2_metric_col].sum():,.0f}</div>
                            <div class="metric-label">Total {file2_metric_col}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Display dataframe with custom styling
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.dataframe(
                        matched_df.sort_values(by=file1_metric_col, ascending=False),
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download button with custom styling
                    csv_matched = matched_df.to_csv(index=False)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download Clean View",
                            data=csv_matched,
                            file_name=f"cleansheet_matched_{file1_metric_col}_{file2_metric_col}.csv",
                            mime="text/csv"
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

                with tab2:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="card-header"><span class="card-icon">🔍</span>Matching Map</div>', unsafe_allow_html=True)
                    st.markdown('<p>This view shows how your original product names were mapped to standardized names, with confidence scores for each match.</p>', unsafe_allow_html=True)

                    # Filter options in a cleaner layout
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div style="background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
                        st.markdown('<div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;">Filter Options</div>', unsafe_allow_html=True)
                        show_flags = st.checkbox("Show only items flagged for review", value=False)
                        min_conf = st.slider("Minimum confidence to display", 0.0, 1.0, 0.0, 0.1)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        # Statistics in a card
                        st.markdown('<div style="background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
                        st.markdown('<div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;">Matching Statistics</div>', unsafe_allow_html=True)

                        total_mappings = len(summary_df)
                        flagged_items = len(summary_df[summary_df['Flag'] != ""])
                        avg_conf = summary_df['Confidence'].mean()

                        st.markdown(f'''
                        <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                            <div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: var(--primary-color);">{total_mappings}</div>
                                <div style="font-size: 0.8rem; color: #666;">Total Mappings</div>
                            </div>
                            <div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: var(--warning);">{flagged_items}</div>
                                <div style="font-size: 0.8rem; color: #666;">Flagged Items</div>
                            </div>
                            <div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: var(--accent-color);">{avg_conf:.1%}</div>
                                <div style="font-size: 0.8rem; color: #666;">Avg. Confidence</div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Apply filters
                    filtered_df = summary_df
                    if show_flags:
                        filtered_df = filtered_df[filtered_df['Flag'] != ""]
                    filtered_df = filtered_df[filtered_df['Confidence'] >= min_conf]

                    # Format confidence as percentage and add styling
                    display_df = filtered_df.copy()

                    # Apply custom formatting to the dataframe
                    def format_confidence(val):
                        if val >= 0.8:
                            return f'<span class="high-confidence">{val:.1%}</span>'
                        elif val >= 0.6:
                            return f'<span class="medium-confidence">{val:.1%}</span>'
                        else:
                            return f'<span class="low-confidence">{val:.1%}</span>'

                    def format_flag(val):
                        if val:
                            return f'<span class="flag-review">{val}</span>'
                        return ""

                    # Format for display
                    display_df['Confidence'] = display_df['Confidence'].apply(format_confidence)
                    display_df['Flag'] = display_df['Flag'].apply(format_flag)

                    # Display dataframe with custom styling
                    st.markdown('<div class="dataframe-container" style="margin-top: 1.5rem;">', unsafe_allow_html=True)
                    st.write(display_df.sort_values(by='Confidence', ascending=False).to_html(escape=False), unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download button with custom styling
                    csv_summary = summary_df.to_csv(index=False)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download Matching Map",
                            data=csv_summary,
                            file_name=f"cleansheet_matching_map_{file1_label_col}_{file2_label_col}.csv",
                            mime="text/csv"
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    # Show example if no files are uploaded
    st.markdown('''
    <div class="card">
        <div class="card-header">
            <span class="card-icon">🚀</span>
            Get Started with CleanSheet Matching Engine™
        </div>
        <p>
            Upload your files in the sidebar to begin the matching process. Our engine will clean and standardize your product names,
            allowing you to reconcile sales and inventory data with confidence.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    # Display sample data structure
    st.markdown('''
    <div class="card">
        <div class="card-header">
            <span class="card-icon">📋</span>
            File Format Requirements
        </div>
        <p>
            Your input files should be in CSV format. You'll be able to select which columns contain product names and values after uploading.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); height: 100%;">
            <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.75rem; display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">📊</span> File 1 Format Example
            </div>
            <div style="font-family: monospace; background-color: #f8f9fa; padding: 1rem; border-radius: 4px; font-size: 0.9rem;">
Product Name,Sales Value<br>
Samsung TV 32in S,459<br>
Sam TV 32in,876<br>
Samsung TV,831<br>
Samsung TV Smart,990
            </div>
            <div style="margin-top: 0.75rem; font-size: 0.85rem; color: #666;">
                <strong>Note:</strong> Column names can be different - you'll select them after upload
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); height: 100%;">
            <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.75rem; display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">📦</span> File 2 Format Example
            </div>
            <div style="font-family: monospace; background-color: #f8f9fa; padding: 1rem; border-radius: 4px; font-size: 0.9rem;">
Item,Stock<br>
Samsung TV 32in S,91<br>
Sam TV 32in,21<br>
Samsung TV,42<br>
Samsung TV Smart,42
            </div>
            <div style="margin-top: 0.75rem; font-size: 0.85rem; color: #666;">
                <strong>Note:</strong> Column names can be different - you'll select them after upload
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Show example output
    st.markdown('''
    <div class="card" style="margin-top: 2rem;">
        <div class="card-header">
            <span class="card-icon">✨</span>
            Output Preview
        </div>
        <p>
            After processing, you'll receive two views of your data:
        </p>
    </div>
    ''', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Clean View Example", "🔍 Matching Map Example"])

    with tab1:
        st.markdown('''
        <div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-top: 1rem;">
            <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.75rem;">
                Clean View - Aggregated Results
            </div>
            <p style="font-size: 0.9rem; margin-bottom: 1rem;">
                This view shows your standardized product data with aggregated sales and inventory values.
            </p>
        ''', unsafe_allow_html=True)

        example_matched = pd.DataFrame({
            'Standardized Name': [
                'Samsung TV 32in Smart',
                'Samsung TV 32in Basic',
                'Apple iPhone 13 Pro',
                'Apple iPhone 13 Mini'
            ],
            'Sales (£)': [3087, 2274, 2008, 2741],
            'Inventory Units': [289, 194, 271, 186]
        })

        st.dataframe(example_matched, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('''
        <div style="background-color: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-top: 1rem;">
            <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.75rem;">
                Matching Map - Detailed Mapping
            </div>
            <p style="font-size: 0.9rem; margin-bottom: 1rem;">
                This view shows how your original product names were mapped to standardized names, with confidence scores for each match.
            </p>
        ''', unsafe_allow_html=True)

        example_summary = pd.DataFrame({
            'Product': [
                'Samsung TV 32in S',
                'Sam TV 32in',
                'Samsung TV',
                'Apple Pro 13 iPhone'
            ],
            'Standardized Name': [
                'Samsung TV 32in Smart',
                'Samsung TV 32in (Unspecified Variant)',
                'Samsung TV 32in (Unspecified Variant)',
                'Apple iPhone 13 Pro'
            ],
            'Confidence': ['85.0%', '78.0%', '65.0%', '92.0%'],
            'Flag': ['', '', 'Manual Review Needed', '']
        })

        st.dataframe(example_summary, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # How it works section
    st.markdown('''
    <div class="card" style="margin-top: 2rem;">
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            How It Works
        </div>
        <ol>
            <li><strong>Upload your files</strong> - Provide your data in CSV format</li>
            <li><strong>Select columns</strong> - Choose which columns contain labels and metric values</li>
            <li><strong>Configure settings</strong> - Adjust matching parameters to suit your data</li>
            <li><strong>Process data</strong> - Our engine tokenizes, analyzes, and groups similar items</li>
            <li><strong>Review results</strong> - Examine the clean view and matching map</li>
            <li><strong>Download outputs</strong> - Export the results for use in your systems</li>
        </ol>
        <p style="margin-top: 1rem; font-style: italic; color: #666;">
            The CleanSheet Matching Engine™ uses advanced NLP techniques to identify and group similar items while respecting
            important distinctions like size, volume, and variant information. The flexible column selection feature allows you to
            work with data from any source without reformatting.
        </p>
    </div>
    ''', unsafe_allow_html=True)

# Footer
st.markdown('''
<div class="footer">
    <div class="footer-logo">CleanSheet Matching Engine™</div>
    <div>Matching Drop v1.0 | Enterprise-grade matching engine for finance teams</div>
    <div class="footer-links">
        <a href="#" class="footer-link">Documentation</a>
        <a href="#" class="footer-link">Support</a>
        <a href="#" class="footer-link">Privacy Policy</a>
    </div>
    <div style="margin-top: 0.5rem; font-size: 0.8rem;">© 2023 CleanSheet. All rights reserved.</div>
</div>
''', unsafe_allow_html=True)
