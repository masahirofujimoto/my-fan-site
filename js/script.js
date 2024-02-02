document.addEventListener('DOMContentLoaded', function() {
    // 投稿をサーバーに送信する関数
    async function submitPost(content) {
        try {
            const response = await fetch('https://kk03gkw3t7.execute-api.us-east-1.amazonaws.com/store_post_stage/post', {
                method: 'POST',
                body: JSON.stringify({ content: content }),
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // 投稿を表示する関数
    function displayPosts(posts) {
        const postsContainer = document.getElementById('postsContainer');
        postsContainer.innerHTML = '';
        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            postElement.innerHTML = `
            <p>${post.Content}</p>
            <small>${post.CreatedAt}</small>
            <button class="delete-button" data-postid="${post.PostId}">削除</button>`;
            postsContainer.appendChild(postElement);
        });

         // 削除ボタンにイベントリスナーを追加
        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', function() {
                const postId = parseInt(this.getAttribute('data-postid'), 10); // 文字列を数値に変換
                deletePost(postId, this.parentNode);
            });
        });
    }

    // 投稿を取得する関数
    async function fetchPosts() {
        try {
            const response = await fetch('https://858j9m8so6.execute-api.us-east-1.amazonaws.com/get_post_store/get');
            const posts = await response.json();
            displayPosts(posts);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    //投稿を削除する関数
    async function deletePost(postId, element) {
        console.log("Deleting post with ID:", postId);

        try {
            const response = await fetch(`https://plafpoy4re.execute-api.us-east-1.amazonaws.com/delete_post/delete/${postId}`,{
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });
            console.log("response data:", response);

            if (response.ok) {
                const data = await response.json();
                console.log("Response from API:", data);
                element.remove();
            } else {
                console.error('Response error:', response.status);
            }
        } catch (error) {
            console.error('Error during fetch:', error);
        }
    }




    // 投稿フォームのサブミットイベントリスナー
    document.getElementById('newPostForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const postContent = document.getElementById('postContent').value;
        if (!postContent) {
            console.error('投稿内容が空です。');
            return;
        }
        await submitPost(postContent);
        fetchPosts(); // 投稿後、投稿を再取得して表示
        document.getElementById('postContent').value = ''; // フォームをクリア
    });

    // 初期ロード時に投稿を取得して表示
    fetchPosts();
});
