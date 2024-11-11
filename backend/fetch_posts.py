import requests


def fetch_all_posts(api_url, page=1, limit=5, sort="title", direction="asc"):
    """
    Fetch all posts with pagination and sorting.
    Fetches posts in batches until no more posts are available.

    :param api_url: The API URL to fetch posts from.
    :param page: Starting page for pagination.
    :param limit: Number of posts per page.
    :param sort: Field to sort by ('title', 'content', 'author', 'date').
    :param direction: Sort direction ('asc' or 'desc').
    :return: A list of all posts.
    """
    valid_sort_fields = {"title", "content", "author", "date"}
    if sort not in valid_sort_fields:
        raise ValueError(f"Invalid sort field '{sort}'. Choose from {valid_sort_fields}.")

    posts_collected = []

    while True:
        response = requests.get(api_url, params={"page": page, "limit": limit, "sort": sort,
                                                 "direction": direction})

        if response.status_code != 200:
            print("Failed to fetch posts:", response.status_code)
            break

        posts = response.json()

        if not posts:
            print("No more posts to fetch.")
            break

        posts_collected.extend(posts)

        print(f"Page {page}: {posts}")

        page += 1

    print(f"\nTotal posts fetched: {len(posts_collected)}")
    return posts_collected


# Fetch all posts, now allowing sorting by 'author' and 'date' too
all_fetched_posts = fetch_all_posts("http://127.0.0.1:5002/api/posts")
