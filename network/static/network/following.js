document.addEventListener('DOMContentLoaded', function() {

	fetch('/following_tweets_load')
		.then(response => response.json())
	    .then(data => {
	    	data.forEach(add_post);
		})

	});

	function add_post(contents) {

                // Create new post
                var post = document.createElement("div");
                post.setAttribute("class", "post");

                //Create username
                var post_user_p = document.createElement("div");
                post_user_p.setAttribute("class", "post_user_p");
                var a_href = document.createElement("a");
                a_href.setAttribute("href", `/profile/${contents.user_p}`);
                var strong = document.createElement("strong");
                strong.innerHTML=contents.user_p;
                a_href.appendChild(strong);
                post_user_p.appendChild(a_href);
                post.appendChild(post_user_p)

                //Create tweet's body
                var post_body = document.createElement("div");
                post_body.setAttribute("class", "post_body");
                post_body.innerHTML=contents.content;
                post.appendChild(post_body);

                //Create timestamp
                var post_date = document.createElement("div");
                post_date.setAttribute("class", "post_date");
                post_date.innerHTML=contents.date_created;
                post.appendChild(post_date);

                //Create likes
                var post_likes = document.createElement("div");
                post_likes.setAttribute("class", "post_likes");
                var img = document.createElement("img");
                //img.setAttribute("data-like", `${contents.id}`);
                //img.setAttribute("id", `${contents.id}`);
                img.setAttribute("class", "like");
                img.setAttribute("src", "https://pngimg.com/uploads/heart/heart_PNG51335.png");
                img.setAttribute("onclick", `like_post(${JSON.stringify(contents)})`);
                var p = document.createElement("p");
                p.setAttribute("class", "like_counter");
                p.setAttribute("id", `${contents.id}`);
                p.innerHTML = contents.likes;
                post_likes.appendChild(img);
                post_likes.appendChild(p);
                post.appendChild(post_likes)

                // Add post to DOM
                document.querySelector('.lenta_a').append(post);

            };

function like_post(contents) {
	console.log("Like was clicked! ", contents.id);
	fetch(`/like/${contents.id}`, {
  	method: 'POST',
  	body: JSON.stringify({
      id: contents.id
  })
})
    .then(response => response.json())
        .then(data => {
            document.getElementById(contents.id).innerHTML = data.likes;
        })
}