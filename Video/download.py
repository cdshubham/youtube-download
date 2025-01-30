from yt_dlp import YoutubeDL
import os
from datetime import datetime

def download_videos(url_file, output_dir=None):
    """
    Download YouTube videos from URLs stored in a text file
    
    Args:
        url_file (str): Path to text file containing video URLs
        output_dir (str): Directory to save downloaded videos (optional)
    """
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        # Create a default directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"youtube_downloads_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'best',  # Best quality
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Output template
        'ignoreerrors': True,  # Skip on errors
        'no_warnings': True,
        'quiet': False,
        'progress': True,
        'progress_hooks': [lambda d: print(f"\nDownloading: {d['filename']}")],
    }
    
    try:
        # Read URLs from file
        with open(url_file, 'r') as f:
            # Filter out empty lines and comments
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            print("No URLs found in the file.")
            return
        
        print(f"Found {len(urls)} URLs to download")
        print(f"Videos will be saved to: {os.path.abspath(output_dir)}")
        
        # Download each video
        with YoutubeDL(ydl_opts) as ydl:
            for index, url in enumerate(urls, 1):
                print(f"\nProcessing video {index} of {len(urls)}")
                print(f"URL: {url}")
                try:
                    ydl.download([url])
                except Exception as e:
                    print(f"Error downloading {url}: {str(e)}")
                    continue
        
        print("\nDownload process completed!")
        print(f"Videos have been saved to: {os.path.abspath(output_dir)}")
        
    except FileNotFoundError:
        print(f"Error: File '{url_file}' not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Get input file path
    url_file = input("Enter the path to your URL file: ")
    
    # Optionally specify output directory
    output_dir = input("Enter output directory (press Enter for default): ").strip()
    if not output_dir:
        output_dir = None
    
    # Start download
    download_videos(url_file, output_dir)
