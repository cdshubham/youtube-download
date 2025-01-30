from yt_dlp import YoutubeDL
from datetime import datetime

def save_playlist_urls(playlist_url):
    """
    Extract and save all video URLs from a YouTube playlist to a file
    
    Args:
        playlist_url (str): The URL of the YouTube playlist
    """
    # Configure yt-dlp options
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'ignoreerrors': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Extract playlist info
            print("Fetching playlist information...")
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' not in playlist_info:
                print("Error: No videos found in playlist")
                return
            
            # Create filename with playlist title and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            playlist_title = playlist_info.get('title', 'playlist').replace(" ", "_")
            filename = f"{playlist_title}_{timestamp}.txt"
            
            # Save URLs to file
            with open(filename, 'w', encoding='utf-8') as f:
                # Write playlist information
                f.write(f"Playlist: {playlist_info['title']}\n")
                f.write(f"URL: {playlist_url}\n")
                f.write(f"Total videos: {len(playlist_info['entries'])}\n\n")
                
                # Write each video URL
                for index, video in enumerate(playlist_info['entries'], 1):
                    if video:
                        video_url = f"https://youtube.com/watch?v={video['id']}"
                        f.write(f"{video_url}\n")
                        
                        # Also print to console to show progress
                        print(f"Saved URL {index}: {video_url}")
            
            print(f"\nAll URLs have been saved to {filename}")
            print(f"Total videos: {len(playlist_info['entries'])}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    url = input("Enter YouTube playlist URL: ")
    save_playlist_urls(url)
