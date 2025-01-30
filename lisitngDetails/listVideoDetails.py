from yt_dlp import YoutubeDL
import json
from datetime import datetime

def format_duration(duration_seconds):
    """Convert duration in seconds to HH:MM:SS format"""
    if not duration_seconds:
        return "Unknown"
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return f"{int(minutes):02d}:{int(seconds):02d}"

def list_playlist_videos(playlist_url, save_to_file=True):
    """
    Extract detailed information for all videos in a YouTube playlist
    
    Args:
        playlist_url (str): URL of the YouTube playlist
        save_to_file (bool): Whether to save the results to a file
        
    Returns:
        list: List of dictionaries containing video information
    """
    # Configure yt-dlp options
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Changed to False to get full video info
        'force_generic_extractor': False,
        'ignoreerrors': True,
    }
    
    try:
        # Create YoutubeDL object
        with YoutubeDL(ydl_opts) as ydl:
            # Extract playlist info
            print("Fetching playlist information... This might take a while for large playlists.")
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' not in playlist_info:
                print("No videos found in playlist")
                return []
            
            # Create output string for console
            output = []
            output.append(f"Playlist: {playlist_info.get('title', 'Unknown Title')}")
            output.append(f"Total videos: {len(playlist_info['entries'])}")
            output.append("")
            
            # Process each video
            videos_data = []
            for index, video in enumerate(playlist_info['entries'], 1):
                if video:
                    # Extract all required information
                    video_data = {
                        "position": index,
                        "title": video.get('title', 'Unknown Title'),
                        "description": video.get('description', 'No description available'),
                        "videoUrl": f"https://youtube.com/watch?v={video.get('id', '')}",
                        "thumbnailUrl": video.get('thumbnail', ''),
                        "tags": video.get('tags', []),
                        "category": video.get('categories', ['Unknown'])[0] if video.get('categories') else 'Unknown',
                        "duration": format_duration(video.get('duration')),
                        "duration_seconds": video.get('duration', 0),
                        "createdAt": video.get('upload_date', 'Unknown'),
                        "channel": video.get('uploader', 'Unknown'),
                        "channelId": video.get('uploader_id', 'Unknown'),
                        "viewCount": video.get('view_count', 0),
                        "likeCount": video.get('like_count', 0),
                    }
                    videos_data.append(video_data)
                    
                    # Add to console output
                    output.append(f"{index}. {video_data['title']}")
                    output.append(f"   Duration: {video_data['duration']}")
                    output.append(f"   URL: {video_data['videoUrl']}")
                    output.append(f"   Created: {video_data['createdAt']}")
                    output.append(f"   Channel: {video_data['channel']}")
                    output.append("")
            
            # Print to console
            print("\n".join(output))
            
            # Save to file if requested
            if save_to_file:
                # Create filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                playlist_title = playlist_info.get('title', 'playlist').replace(" ", "_")
                filename = f"{playlist_title}_{timestamp}"
                
                # Save as text file
                with open(f"{filename}.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(output))
                print(f"\nPlaylist information saved to {filename}.txt")
                
                # Save as JSON with full details
                json_data = {
                    "playlist_title": playlist_info.get('title', 'Unknown Title'),
                    "playlist_url": playlist_url,
                    "playlist_id": playlist_info.get('id', ''),
                    "video_count": len(playlist_info['entries']),
                    "fetched_at": datetime.now().isoformat(),
                    "videos": videos_data
                }
                
                with open(f"{filename}.json", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                print(f"Detailed playlist data saved to {filename}.json")
            
            return videos_data
                    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

if __name__ == "__main__":
    playlist_url = input("Enter YouTube playlist URL: ")
    videos = list_playlist_videos(playlist_url)
