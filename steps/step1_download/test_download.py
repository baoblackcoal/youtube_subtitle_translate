import sys
import os
from download_and_convert import download_subtitles, is_valid_youtube_url

def test_youtube_urls():
    # Test cases with different URL formats
    test_urls = [
        "https://youtu.be/GiEsyOyk1m4?si=xPECLiIHKMwF_lsv",
        "https://www.youtube.com/watch?si=xPECLiIHKMwF_lsv&v=GiEsyOyk1m4&feature=youtu.be",
        "https://www.youtube.com/watch?v=GiEsyOyk1m4&t=17s",
        "https://www.youtube.com/watch?v=GiEsyOyk1m4&list=PLOXw6I10VTv8VOvPNVQ8c4D4NyMRMotXh&index=20"
    ]

    print("Starting YouTube URL format tests...")
    print("-" * 80)

    success_count = 0
    total_count = len(test_urls)
    output_dir = os.path.join(os.path.dirname(__file__), "output")

    for i, url in enumerate(test_urls, 1):
        print(f"\nTest {i}/{total_count}:")
        print(f"Testing URL: {url}")
        
        # First test URL validation
        if not is_valid_youtube_url(url):
            print("❌ URL validation failed")
            continue
        else:
            print("✓ URL validation passed")

        # Try to download subtitles
        try:
            result = download_subtitles(output_dir=output_dir, url=url)
            if result:
                print("✓ Subtitle download successful")
                print(f"Output file: {result}")
                success_count += 1
            else:
                print("❌ Subtitle download failed")
        except Exception as e:
            print(f"❌ Error during download: {str(e)}")

        print("-" * 80)

    # Print summary
    print("\nTest Summary:")
    print(f"Total tests: {total_count}")
    print(f"Successful downloads: {success_count}")
    print(f"Failed downloads: {total_count - success_count}")
    print(f"Success rate: {(success_count/total_count)*100:.2f}%")

if __name__ == '__main__':
    test_youtube_urls() 