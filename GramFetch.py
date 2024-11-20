import instaloader
import re
from datetime import datetime
import pyfiglet
from termcolor import colored

# ASCII Banner
def display_banner():
    banner = pyfiglet.figlet_format("GramFetch")
    print(colored(banner, "cyan"))
    print(colored("Scripted by mvh@shamash | Instagram Media Downloader", "yellow"))
    print(colored("=" * 60, "green"))

# Extract username from URL if provided
def extract_username(url_or_username):
    match = re.match(r"https?://(?:www\.)?instagram\.com/([^/?#&]+)", url_or_username)
    return match.group(1) if match else url_or_username

# Download posts by type (images/videos/all)
def download_posts_by_type(loader, username, media_type):
    print(colored(f"🔹 Downloading {media_type} posts for @{username}...", "blue"))
    profile = instaloader.Profile.from_username(loader.context, username)
    posts = profile.get_posts()
    for post in posts:
        if media_type == "all":
            loader.download_post(post, target=username)
        elif media_type == "images" and not post.is_video:
            loader.download_post(post, target=username)
        elif media_type == "videos" and post.is_video:
            loader.download_post(post, target=username)
    print(colored(f"✅ Completed downloading {media_type} posts for @{username}!", "green"))

# Download posts within a date range
def download_posts_by_date(loader, username, start_date, end_date):
    print(colored(f"🔹 Downloading posts for @{username} from {start_date} to {end_date}...", "blue"))
    profile = instaloader.Profile.from_username(loader.context, username)
    posts = profile.get_posts()
    for post in posts:
        post_date = post.date
        if start_date and post_date < start_date:
            continue
        if end_date and post_date > end_date:
            continue
        loader.download_post(post, target=username)
    print(colored(f"✅ Completed downloading posts for @{username} within the date range!", "green"))

# Download posts by keyword
def download_posts_by_keyword(loader, username, keyword):
    print(colored(f"🔹 Downloading posts for @{username} containing the keyword '{keyword}'...", "blue"))
    profile = instaloader.Profile.from_username(loader.context, username)
    posts = profile.get_posts()
    for post in posts:
        if keyword.lower() in (post.caption or "").lower():
            loader.download_post(post, target=username)
    print(colored(f"✅ Completed downloading posts for @{username} with the keyword '{keyword}'!", "green"))

# Download from multiple usernames
def download_from_multiple_users(usernames, loader, media_type=None, start_date=None, end_date=None, keyword=None):
    for username in usernames:
        try:
            if media_type:
                download_posts_by_type(loader, username, media_type)
            elif start_date or end_date:
                download_posts_by_date(loader, username, start_date, end_date)
            elif keyword:
                download_posts_by_keyword(loader, username, keyword)
            else:
                download_posts_by_type(loader, username, "all")
        except Exception as e:
            print(colored(f"❌ An error occurred with @{username}: {e}", "red"))

# Main function
def main():
    display_banner()
    
    loader = instaloader.Instaloader()
    loader.download_videos = True  # Enable video downloads

    try:
        # Prompt for usernames
        print(colored("➤ Enter Instagram usernames or profile URLs (comma-separated):", "cyan"))
        input_data = input(">> ").strip()
        usernames = [extract_username(u.strip()) for u in input_data.split(",")]

        # Prompt for features
        print(colored("\n➤ Do you want to download specific types of posts?", "cyan"))
        print("   [all] - Download all posts")
        print("   [images] - Only images")
        print("   [videos] - Only videos")
        media_type = input(">> (all/images/videos or press Enter to skip): ").strip().lower()

        print(colored("\n➤ Enter date range (optional)", "cyan"))
        start_date = input("   Start date (YYYY-MM-DD) or press Enter to skip: ").strip()
        end_date = input("   End date (YYYY-MM-DD) or press Enter to skip: ").strip()

        print(colored("\n➤ Enter keyword to filter posts (optional):", "cyan"))
        keyword = input(">> (Enter keyword or press Enter to skip): ").strip()

        # Convert dates if provided
        start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        print(colored("\nStarting the download process...\n", "yellow"))

        # Execute based on inputs
        if media_type:
            for username in usernames:
                download_posts_by_type(loader, username, media_type)
        elif start_date or end_date:
            for username in usernames:
                download_posts_by_date(loader, username, start_date, end_date)
        elif keyword:
            for username in usernames:
                download_posts_by_keyword(loader, username, keyword)
        else:
            download_from_multiple_users(usernames, loader)

    except Exception as e:
        print(colored(f"❌ An unexpected error occurred: {e}", "red"))

    print(colored("\n✅ All tasks completed. Thank you for using GramFetch!", "green"))

if __name__ == "__main__":
    main()
