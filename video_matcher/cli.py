"""Command line interface for video matching."""

import argparse
from pathlib import Path
from . import extract_frame_features, find_best_match


def main(argv=None):
    parser = argparse.ArgumentParser(description="Match a short video to a long video")
    parser.add_argument("long_video", type=Path, help="Path to the long video")
    parser.add_argument("short_video", type=Path, help="Path to the short video")
    parser.add_argument("--stride", type=int, default=1, help="Frame stride for feature extraction")
    parser.add_argument("--window", type=int, default=10, help="Search window size")

    args = parser.parse_args(argv)

    print("Extracting features from long video...")
    long_features = extract_frame_features(str(args.long_video), stride=args.stride)
    print("Extracting features from short video...")
    short_features = extract_frame_features(str(args.short_video), stride=args.stride)

    print("Matching videos...")
    index, cost = find_best_match(long_features, short_features, window=args.window)
    if index >= 0:
        print(f"Best match starts at frame {index} with cost {cost}")
    else:
        print("No match found")


if __name__ == "__main__":
    main()
