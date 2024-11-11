// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                // Add title, author, date, content to the post
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p><strong>Author:</strong> ${post.author}</p>
                    <p><strong>Date:</strong> ${post.date}</p>
                    <p>${post.content}</p>
                    <div class="button-wrapper">
                        <!-- Update button -->
                        <button class="update" onclick="editPost(${post.id})">Update</button>
                        <!-- Delete button -->
                        <button class="delete" onclick="deletePost(${post.id})">Delete</button>
                    </div>
                `;

                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}


// Function to send a POST request to the API to add a new post
function addPost() {
    // Retrieve the values from the input fields
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;

    // Get today's date if not provided
    var postDate = new Date().toISOString().split('T')[0];  // Format: YYYY-MM-DD

    // Use the Fetch API to send a POST request to the /posts endpoint
    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            author: postAuthor,  // Include author in the request
            date: postDate       // Include the current date
        })
    })
    .then(response => response.json())  // Parse the JSON data from the response
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one

        // Clear the input fields after adding the post
        document.getElementById('post-title').value = '';
        document.getElementById('post-content').value = '';
        document.getElementById('post-author').value = '';
        document.getElementById('post-date').value = '';
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Use the Fetch API to send a DELETE request to the specific post's endpoint
    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

function editPost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    // Prompt the user for new data (leave blank to keep the current value)
    var postTitle = prompt('Enter new title (leave blank to keep current):');
    var postAuthor = prompt('Enter new author (leave blank to keep current):');
    var postContent = prompt('Enter new content (leave blank to keep current):');

    // Only include fields that the user filled in
    let updatedFields = {};
    if (postTitle && postTitle.trim() !== '') updatedFields.title = postTitle.trim();
    if (postAuthor && postAuthor.trim() !== '') updatedFields.author = postAuthor.trim();
    if (postContent && postContent.trim() !== '') updatedFields.content = postContent.trim();

    // If no fields were filled, exit the function early
    if (Object.keys(updatedFields).length === 0) {
        alert("No changes made to the post.");
        return;
    }

    // Send the PUT request with only the fields that need updating
    fetch(baseUrl + '/posts/' + postId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedFields)
    })
    .then(response => response.json())
    .then(updatedPost => {
        loadPosts();  // Reload posts after update
    })
    .catch(error => console.error('Error:', error));
}
