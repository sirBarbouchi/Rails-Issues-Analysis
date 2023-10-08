import requests
import csv

# Define GitHub token (To be defined)
github_token = 'To be defined'

# Define the API URL for the Rails project's issues
api_url = 'https://api.github.com/repos/rails/rails/issues'

# Initialize an empty list to store all issues (without comments)
all_issues = []

# Initialize an empty list to store all comments
all_comments = []

# Set the number of issues to retrieve
issues_to_retrieve = 500

# Initialize the page number
page_number = 1

while len(all_issues) < issues_to_retrieve:
    # Set the parameters for the API request, including the page number and sorting by creation date in descending order
    params = {
        'page': page_number,
        'per_page': min(100, issues_to_retrieve - len(all_issues)),  # Adjust per_page
        'sort': 'created',
        'direction': 'desc'  # Sort in descending order (most recent first)
    }

    # Set the headers with your token
    headers = {
        'Authorization': f'token {github_token}',
    }

    # Make a GET request to retrieve issues data for the current page
    response = requests.get(api_url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        issues_data = response.json()

        # If there are no more issues on this page, break the loop
        if not issues_data:
            break

        # Iterate through issues on this page
        for issue_data in issues_data:
            # Append the issue (without comments) to the list
            all_issues.append(issue_data)

            # Retrieve comments for the current issue
            issue_number = issue_data['number']
            comments_url = f'{api_url}/{issue_number}/comments'
            comments_response = requests.get(comments_url, headers=headers)

            # Check if the comments request was successful (status code 200)
            if comments_response.status_code == 200:
                comments_data = comments_response.json()

                # Append comments to the list with issue_id as a foreign key
                for comment in comments_data:
                    comment['issue_id'] = issue_number
                    all_comments.append(comment)

        # Move to the next page
        page_number += 1
    else:
        print(f'Failed to retrieve issues. Status code: {response.status_code}')
        break



# Export issues to a CSV file with UTF-8 encoding
with open('issues.csv', mode='w', newline='', encoding='utf-8') as issues_file:
    writer = csv.DictWriter(issues_file, fieldnames=all_issues[0].keys())
    
    writer.writeheader()
    for issue in all_issues:
        writer.writerow(issue)

# Export comments to a CSV file with UTF-8 encoding
with open('comments.csv', mode='w', newline='', encoding='utf-8') as comments_file:
    comment_writer = csv.DictWriter(comments_file, fieldnames=all_comments[0].keys())
    
    comment_writer.writeheader()
    for comment in all_comments:
        comment_writer.writerow(comment)

print('Exported data to CSV files: issues.csv and comments.csv')
