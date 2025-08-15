# features_extraction.py
import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime

FEATURE_COLS = ['amount', 'is_round_amount', 'amount_num_digits', 'vendor_freq', 'amount_zscore']


def extract_invoice_features(parsed_invoice, stats):
    # parsed_invoice is a dict with keys: invoice_no, vendor, date (str YYYY-MM-DD), amount (float)
    amt = float(parsed_invoice.get('amount', 0.0))
    vendor = parsed_invoice.get('vendor', 'UNKNOWN')
    date_str = parsed_invoice.get('date', None)

    is_round = 1 if (amt % 100 == 0) else 0
    num_digits = len(str(int(max(1,amt))))

    vendor_freq = stats['vendor_counts'].get(vendor, 0)
    # amount zscore relative to vendor; fallback to global stats
    vendor_mean = stats['vendor_amount_mean'].get(vendor, stats['global_mean'])
    vendor_std = stats['vendor_amount_std'].get(vendor, stats['global_std'])
    if vendor_std <= 0:
        amt_z = 0.0
    else:
        amt_z = (amt - vendor_mean)/vendor_std

    feat = [amt, is_round, num_digits, vendor_freq, amt_z]
    return feat


def build_features_from_dataframe(df):
    # df: must contain invoice_no, vendor, date, amount, label(optional)
    # compute vendor stats
    vendor_groups = df.groupby('vendor')['amount']
    vendor_counts = df['vendor'].value_counts().to_dict()
    vendor_mean = vendor_groups.mean().to_dict()
    vendor_std = vendor_groups.std(ddof=0).fillna(0).to_dict()
    global_mean = df['amount'].mean()
    global_std = df['amount'].std(ddof=0)

    stats = {
        'vendor_counts': vendor_counts,
        'vendor_amount_mean': {k: float(v) for k,v in vendor_mean.items()},
        'vendor_amount_std': {k: float(v) for k,v in vendor_std.items()},
        'global_mean': float(global_mean),
        'global_std': float(global_std)
    }

    X = []
    y = []
    for _, row in df.iterrows():
        parsed = {'invoice_no': row['invoice_no'], 'vendor': row['vendor'], 'date': row['date'], 'amount': row['amount']}
        feats = extract_invoice_features(parsed, stats)
        X.append(feats)
        if 'label' in row:
            y.append(int(row['label']))
    X = np.array(X)
    y = np.array(y) if len(y)>0 else None
    return X, y, stats