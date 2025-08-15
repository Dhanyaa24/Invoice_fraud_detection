# model_train.py
import os
import json
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from joblib import dump
from features_extraction import build_features_from_dataframe

DATA_PATH = 'data/synthetic_invoices.csv'
ARTIFACT_DIR = 'data/model_artifacts'
os.makedirs(ARTIFACT_DIR, exist_ok=True)


def generate_synthetic(n=3000, out=DATA_PATH):
    vendors = ['Alpha Supplies','Beta Traders','Gamma Co','Delta Services','Omega Inc']
    rows = []
    for i in range(n):
        vendor = random.choice(vendors)
        inv_no = f"INV-{random.randint(1000,9999)}"
        # pick an amount; fraudulent invoices more likely to be round large amounts or tiny amounts
        base = random.choice([100,250,500,1200,5000,10000])
        noise = np.round(np.random.normal(0, base*0.15))
        amount = max(10, base + noise)
        # fraud label probability depends on vendor and patterns
        fraud_prob = 0.02
        if amount > 3000:
            fraud_prob += 0.12
        if amount % 100 == 0:
            fraud_prob += 0.08
        if random.random() < 0.01:
            fraud_prob += 0.4
        label = int(random.random() < fraud_prob)
        date = datetime.now() - timedelta(days=random.randint(0,365))
        rows.append({'invoice_no':inv_no, 'vendor':vendor, 'date':date.strftime('%Y-%m-%d'), 'amount':float(amount), 'label':label})
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Synthetic data saved to {out}")


if __name__ == '__main__':
    if not os.path.exists(DATA_PATH):
        print('Generating synthetic data...')
        generate_synthetic()

    print('Loading data...')
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])

    # Build ML features
    X, y, stats = build_features_from_dataframe(df)

    # Save stats for use at prediction time
    with open(os.path.join(ARTIFACT_DIR, 'stats.json'), 'w') as f:
        json.dump(stats, f, default=str)

    # scale
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    dump(scaler, os.path.join(ARTIFACT_DIR, 'scaler.pkl'))

    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.2, random_state=42, stratify=y)
    print('Training model...')
    clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)
    print('Train acc:', clf.score(X_train, y_train))
    print('Test acc:', clf.score(X_test, y_test))

    dump(clf, os.path.join(ARTIFACT_DIR, 'model.pkl'))
    print('Model and artifacts saved to', ARTIFACT_DIR)