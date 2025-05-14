# CleanSheet Matching Engine™

An enterprise-grade matching engine for finance teams that cleans and standardizes data across files using NLP-based matching.

## Features

- **Token-based matching logic** to group similar items (e.g., "Samsung TV 32", "32in Samsung Smart TV")
- **Variant conflict protection** to prevent grouping different variants (e.g., "iPhone 13" vs "iPhone 13 Pro")
- **Size/volume protection** to prevent grouping items with different measurements (e.g., "500ml" vs "2L")
- **Flexible column selection** allowing you to work with any CSV file format
- **Dynamic UI labels** that adapt to your selected column names throughout the application
- **Fully local operation** - no API calls or external services (for confidential data)
- **No glossary/dictionary required** - matching relies on smart rule-based NLP logic
- **Output summary** showing original values, standardized names, confidence scores, and flags

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application using one of the following methods:

**Windows:**
```
run_matcher.bat
```

**macOS/Linux:**
```bash
chmod +x run_matcher.sh
./run_matcher.sh
```

Or run directly with Streamlit:
```bash
streamlit run product_matcher_final.py
```

This will open the application in your default web browser.

### Using the Application

1. **Upload Files**:
   - Upload your first CSV file containing labels and metric data
   - Upload your second CSV file containing labels and metric data

2. **Select Columns**:
   - For each file, select which column contains the labels (e.g., product names, clients, SKUs)
   - For each file, select which column contains the metric values (e.g., sales, units, inventory)

3. **Adjust Settings** (optional):
   - Minimum Similarity Score: Threshold for considering items similar
   - Variant Protection: Enable/disable variant conflict detection
   - Size Protection: Enable/disable size conflict detection
   - Manual Review Threshold: Confidence score below which items are flagged

4. **Process Files**:
   - Click the "Process Files" button to start the matching process

5. **View Results**:
   - Clean View: Shows standardized items with aggregated metric values from both files
   - Matching Map: Shows original items, their standardized versions, confidence scores, and flags

6. **Download Results**:
   - Download the clean view and matching map as CSV files with dynamically named files

## File Format

The application accepts any CSV files. You'll be able to select which columns contain the relevant data after uploading:

### Example File 1
```
Product Name,Sales Value
Samsung TV 32in S,459
Sam TV 32in,876
Samsung TV,831
Samsung TV Smart,990
```

### Example File 2
```
Item,Stock
Samsung TV 32in S,91
Sam TV 32in,21
Samsung TV,42
Samsung TV Smart,42
```

## How It Works

1. **Upload Files**: Provide your data in CSV format
2. **Select Columns**: Choose which columns contain labels and metric values
3. **Configure Settings**: Adjust matching parameters to suit your data
4. **Process Data**: Our engine tokenizes, analyzes, and groups similar items
5. **Review Results**: Examine the clean view and matching map
6. **Download Outputs**: Export the results for use in your systems

The CleanSheet Matching Engine™ uses advanced NLP techniques to identify and group similar items while respecting important distinctions like size, volume, and variant information. The flexible column selection feature allows you to work with data from any source without reformatting.

## License

This project is licensed under the MIT License - see the LICENSE file for details.