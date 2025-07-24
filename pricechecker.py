import os
from dotenv import load_dotenv
from notte_sdk.client import NotteClient

def main():
    # Load environment variables
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

    api_key = os.getenv("NOTTE_API_KEY")
    product_name = os.getenv("PRODUCT_NAME")
    site_1 = os.getenv("SITE_1")
    site_2 = os.getenv("SITE_2")
    site_3 = os.getenv("SITE_3")
    region = os.getenv("REGION", "United States")

    headless_env = os.getenv("HEADLESS", "True")
    headless = headless_env.lower() in ("1", "true", "yes", "on")

    # Basic validation
    missing = []
    if not api_key:
        missing.append("NOTTE_API_KEY")
    if not product_name:
        missing.append("PRODUCT_NAME")
    if not site_1:
        missing.append("SITE_1")
    if not site_2:
        missing.append("SITE_2")
    if not site_3:
        missing.append("SITE_3")
    if missing:
        print(f"❌ Please set the following variables in your .env file: {', '.join(missing)}")
        return

    client = NotteClient(api_key=api_key)

    sites = [
        {"name": "apple.com", "url": site_1},
        {"name": "amazon.com", "url": site_2},
        {"name": "bestbuy.com", "url": site_3},
    ]

    results = []
    summary_rows = []

    for site in sites:
        session = client.Session(headless=headless)
        session.start()
        agent = client.Agent(session=session)
        task = f'''
Go to {site['url']} and search for "{product_name}".
- Immediately click the first non-sponsored product result.
- If a popup, overlay, or region prompt appears, close or accept it and set region to "{region}".
- Do not click on ads, sponsored results, or unrelated links.
- Extract only the following from the product detail page:
  - Title
  - Price
  - Discount or promo (if shown)
- If you cannot find the exact product, extract the closest version and note the difference.
- If you cannot extract information after 2 attempts, skip and note the issue.
Return the result in this format:

---
Site: {site['name']}
Title: ...
Price: ...
Discount: ...
---
'''
        try:
            result = agent.run(task=task)
            answer = result.answer.strip()
            results.append(answer)
            # Try to extract summary info for the table
            title, price, discount = "", "", ""
            for line in answer.splitlines():
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip()
                if line.lower().startswith("price:"):
                    price = line.split(":", 1)[1].strip()
                if line.lower().startswith("discount:"):
                    discount = line.split(":", 1)[1].strip()
            
            # Check if we got any meaningful data
            if not title and not price:
                title = "No data extracted"
                price = "N/A"
                discount = "N/A"
                
            summary_rows.append((site['name'], title, price, discount, len(getattr(result, 'steps', []))))
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if "max steps" in str(e).lower():
                error_msg = "Timeout: Agent reached maximum steps"
            elif "max consecutive failures" in str(e).lower():
                error_msg = "Failed: Too many consecutive failures"
            
            results.append(f"---\nSite: {site['name']}\n{error_msg}\n---")
            summary_rows.append((site['name'], error_msg, "N/A", "N/A", 0))

    print("\nAgent Response (per site):\n")
    for r in results:
        print(r)

    # Print summary table in vertical format
    print("\n" + "="*50)
    print("SUMMARY RESULTS")
    print("="*50)
    
    for i, row in enumerate(summary_rows, 1):
        site, title, price, discount, steps = row
        print(f"\n{i}. {site.upper()}")
        print("-" * 50)
        print(f"   Title:     {title}")
        print(f"   Price:     {price}")
        print(f"   Discount:  {discount}")
        print(f"   Steps:     {steps}")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
