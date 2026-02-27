from src.scraper import session, collect_all_urls, save_to_txt
from src.parser import main as run_parser, save_to_pd_csv


if __name__ == "__main__":
    print("--- Phase 1: Scraping URLs ---")
    urls = collect_all_urls(session)
    save_to_txt(urls)

    print("\n--- Phase 2: Parsing Listings ---")
    all_data = run_parser()

    print("\n--- Phase 3: Saving to CSV ---")
    save_to_pd_csv(all_data)