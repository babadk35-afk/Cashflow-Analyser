"""
Invoice Parser & Expense Categorizer
- Extracts text from PDFs in a folder (via pdfminer.six), classifies line-items into categories, and plots spend by category
Usage:
  python 07_invoice_categorizer.py invoices_folder
Dependencies: pdfminer.six, scikit-learn, matplotlib, pandas, numpy
"""
import sys, os, re, pandas as pd, numpy as np, matplotlib.pyplot as plt
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

CATS = ["travel","food","software","office","other"]

def parse_invoice(path):
    text = extract_text(path) or ""
    items = re.findall(r"(?m)^.*?\b(\d+\.\d{2})$", text)  # crude line-item price at EOL
    lines = [l for l in text.splitlines() if l.strip()]
    return lines, [float(x) for x in items] if items else []

def build_dummy_model():
    samples = [
        ("uber ride to airport", "travel"),
        ("hotel accommodation", "travel"),
        ("burger and fries", "food"),
        ("monthly saas subscription", "software"),
        ("laptop stand", "office"),
        ("notebook and pens", "office"),
        ("snacks and coffee", "food"),
        ("cloud compute credits", "software"),
    ]
    X, y = zip(*samples)
    vec = TfidfVectorizer().fit(X)
    clf = MultinomialNB().fit(vec.transform(X), y)
    return vec, clf

def main(folder):
    vec, clf = build_dummy_model()
    rows = []
    for name in os.listdir(folder):
        if not name.lower().endswith(".pdf"): continue
        path = os.path.join(folder, name)
        lines, prices = parse_invoice(path)
        for line in lines:
            cat = clf.predict(vec.transform([line]))[0]
            rows.append({"invoice": name, "desc": line, "category": cat})
    df = pd.DataFrame(rows)
    if df.empty: 
        print("No data parsed."); return
    counts = df['category'].value_counts().reindex(CATS, fill_value=0)
    counts.plot(kind="bar", title="Line Items by Category")
    plt.show()
    print(df.head())

if __name__ == "__main__":
    if len(sys.argv)<2: print(__doc__); sys.exit(0)
    main(sys.argv[1])
