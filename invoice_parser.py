# invoice_parser.py
import pdfplumber
import pandas as pd
import re
from datetime import datetime

DATE_PATTERNS = [r"\b(\d{4}-\d{2}-\d{2})\b", r"\b(\d{2}/\d{2}/\d{4})\b", r"\b(\d{1,2}[- ]\w{3,9}[- ]\d{4})\b"]
AMOUNT_PATTERN = r"(Total|Amount|Grand Total)[:\s]*₹?\s*([0-9,]+\.?[0-9]*)"
INVOICE_PATTERN = r"(Invoice|Inv\.? No\.?|Invoice No\.)[:\s]*([A-Za-z0-9\-_/]+)"


def parse_pdf(path):
    text = ''
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += '\n' + page.extract_text() or ''
    except Exception as e:
        return {'error': f'pdf parse error: {e}'}

    return _parse_text_fields(text)


def parse_excel(path):
    try:
        df = pd.read_excel(path, engine='openpyxl')
    except Exception as e:
        return {'error': f'excel parse error: {e}'}
    text = ' '.join(df.astype(str).fillna('').agg(' '.join, axis=1).tolist())
    return _parse_text_fields(text)


def _parse_text_fields(text):
    res = {'vendor': None, 'invoice_no': None, 'date': None, 'amount': None}
    # Basic vendor heuristic: first non-empty line
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines:
        res['vendor'] = lines[0][:60]

    # invoice
    m = re.search(INVOICE_PATTERN, text, flags=re.IGNORECASE)
    if m:
        res['invoice_no'] = m.group(2)

    # date
    for pat in DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            date_str = m.group(1)
            try:
                # try ISO first
                if '-' in date_str:
                    parsed = datetime.strptime(date_str, '%Y-%m-%d')
                elif '/' in date_str:
                    parsed = datetime.strptime(date_str, '%d/%m/%Y')
                else:
                    parsed = datetime.strptime(date_str, '%d %B %Y')
                res['date'] = parsed.strftime('%Y-%m-%d')
                break
            except Exception:
                continue

    # amount
    m = re.search(AMOUNT_PATTERN, text, flags=re.IGNORECASE)
    if m:
        amt = m.group(2).replace(',', '')
        try:
            res['amount'] = float(amt)
        except:
            pass
    else:
        # fallback: find the largest number in text
        nums = re.findall(r"\b[0-9,]+\.?[0-9]*\b", text)
        nums = [n.replace(',', '') for n in nums]
        floats = []
        for n in nums:
            try:
                floats.append(float(n))
            except:
                pass
        if floats:
            res['amount'] = float(max(floats))

    return res