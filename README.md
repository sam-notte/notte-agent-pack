# Notte Price Comparison Script

This script uses the [Notte SDK](https://github.com/nottelabs/notte) to automate price comparisons for a given product across multiple e-commerce websites using LLM agents. It is fully environment-agnostic and designed for repeatable, cross-platform use.

---

## Features

- **Environment-agnostic:** All config via `.env`
- **Headless toggle:** Control visible vs. invisible browser via `HEADLESS` flag
- **Agentic automation:** Uses Notte agents to navigate, search, and extract data
- **Multi-site compatible:** Works across any three target URLs
- **Error-resilient:** Handles popups, region prompts, agent timeouts and failure limits
- **Structured output:** Prints raw agent responses + clean vertical summary

---

## Setup

### 1. Install Dependencies

```bash
pip install notte-sdk python-dotenv
```

### 2. Create a `.env` File

```env
NOTTE_API_KEY=your-api-key
PRODUCT_NAME=iPhone 15
SITE_1=https://www.apple.com/
SITE_2=https://www.amazon.com/
SITE_3=https://www.bestbuy.com/
REGION=United States
HEADLESS=True
```

> `REGION` defaults to `United States` if unset.  
> `HEADLESS` (optional): defaults to `True`. Accepts `True`, `False`, `1`, `0`, `yes`, `no`, etc. (case-insensitive)

---

## Usage

Run the script from the terminal:

```bash
python script_name.py
```

Replace `script_name.py` with your actual filename.

---

## Output

### Per-Site Agent Response

```text
---
Site: apple.com
Title: iPhone 15 Pro
Price: $999
Discount: None
---
```

### Error Example

```text
---
Site: bestbuy.com
Timeout: Agent reached maximum steps
---
```

### Vertical Summary Table

```text
==================================================
SUMMARY RESULTS
==================================================

1. APPLE.COM
--------------------------------------------------
   Title:     iPhone 15 Pro
   Price:     $999
   Discount:  None
   Steps:     13

2. AMAZON.COM
--------------------------------------------------
   Title:     iPhone 15 Pro (Unlocked)
   Price:     $989
   Discount:  Prime Deal -$10
   Steps:     14

3. BESTBUY.COM
--------------------------------------------------
   Title:     Timeout: Agent reached maximum steps
   Price:     N/A
   Discount:  N/A
   Steps:     0
==================================================
```

---

## Requirements

- Python 3.8+
- Notte SDK API key from [console.notte.cc](https://console.notte.cc/)
- Any terminal environment

---

## Notes

- Script exits early if required `.env` vars are missing.
- Browser visibility is controlled by the `HEADLESS` flag.
- Handles popup overlays and region settings automatically.
- Gracefully handles max-step timeouts and consecutive failure crashes.

