import argparse
import json
import random

def main():
    parser = argparse.ArgumentParser(description='Extract random posts from a JSON file and output to TSV.')
    parser.add_argument('json_file', type=str, help='Input JSON file containing Reddit posts')
    parser.add_argument('num_posts_to_output', type=int, help='Number of random posts to output')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output TSV file')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')
    
    args = parser.parse_args()

    with open(args.json_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    # Access the list of post objects inside data -> children
    posts = raw_data['data']['children']
    num_posts = min(args.num_posts_to_output, len(posts))

    if args.seed is not None:
        random.seed(args.seed)

    selected_posts = random.sample(posts, num_posts)

    with open(args.output, 'w', encoding='utf-8') as out_file:
        out_file.write('Name\ttitle\tcoding\n')
        for item in selected_posts:
            # Step into the inner 'data' dictionary of each child
            post = item['data']
            if args.num_posts_to_output > len(posts):
                print(f"Warning: Requested {args.num_posts_to_output} posts, but only {len(posts)} available. Outputting all available posts.")
            name = post.get('name', '').replace('\t', ' ').replace('\n', ' ')
            title = post.get('title', '').replace('\t', ' ').replace('\n', ' ')
            out_file.write(f'{name}\t{title}\t\n')

if __name__ == '__main__':
    main()