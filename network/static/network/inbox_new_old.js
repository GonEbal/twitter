document.addEventListener('DOMContentLoaded', function() {

	document.querySelector('#tweet').addEventListener('click', tweet_post);

	fetch('/tweets')
		.then(response => response.json())
	    .then(data => {
	    	//data.forEach(add_post);
            //data.forEach(define_post);
		})

	});

	function add_post(contents) {

                // Create new post
                var post = document.createElement("div");
                post.setAttribute("class", "post");
                post.setAttribute("id", `Post id for append ${contents.id}`);

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

                if (contents.editable == 'yes') {

                    //Create Edit button
                    var post_edit = document.createElement("div");
                    post_edit.setAttribute("class", "post_edit");
                    var a_href = document.createElement("button");
                    a_href.setAttribute("class", "btn btn-link");
                    a_href.innerHTML="Edit";
                    a_href.setAttribute("onclick", `edit_post(${JSON.stringify(contents)})`);
                    post_edit.appendChild(a_href);
                    post.appendChild(post_edit)
                } else {}


                //Create tweet's body
                var post_body = document.createElement("div");
                post_body.setAttribute("class", "post_body");
                post_body.setAttribute("id", `Tweet id for edit ${contents.id}`);
                post_body.innerHTML=contents.content;
                var post_body_first = document.createElement("div");
                post_body_first.setAttribute("class", "post_body_first");
                post_body_first.setAttribute("id", `Id for each edit ${contents.id}`);
                post_body_first.appendChild(post_body);
                post.appendChild(post_body_first);

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
                if (contents.new_post == "no") {
                    document.querySelector('.lenta_a').append(post);
                } else {
                    console.log(contents.id - 1)
                    var id = contents.id - 1
                    document.getElementById(`Post id for append ${id}`).before(post);
                }
            }

function like_post(contents) {
	console.log("Like was clicked! ", contents);
	fetch(`/like/${contents}`, {
  	method: 'POST',
  	body: JSON.stringify({
      id: contents
  })
})
    .then(response => response.json())
        .then(data => {
            document.getElementById(contents).innerHTML = data.likes;
        })
}

function tweet_post() {

    //const xhr = new XMLHttpRequest()
	fetch('/tweet', {
  	method: 'POST',
  	body: JSON.stringify({
      content: document.querySelector('#content').value
  })
})
    .then(response => response.json())
        .then(data => {
            console.log(data)
            add_post(data)
        })
}

function edit_post(contents) {
    var inner = document.getElementById(`Tweet id for edit ${contents}`).innerHTML;
    var str = `<textarea id="Id for textarea ${contents}" class="edit_field">${inner}</textarea>`; //it can be anything
    var Obj = document.getElementById(`Tweet id for edit ${contents}`); //any element to be fully replaced
    if(Obj.outerHTML) { //if outerHTML is supported
    Obj.outerHTML=str; ///it's simple replacement of whole element with contents of str var
    }
    else { //if outerHTML is not supported, there is a weird but crossbrowsered trick
    var tmpObj=document.createElement("div");
    tmpObj.innerHTML='<textarea class="edit_field"></textarea>';
    ObjParent=Obj.parentNode; //Okey, element should be parented
    ObjParent.replaceChild(tmpObj,Obj); //here we placing our temporary data instead of our target, so we can find it then and replace it into whatever we want to replace to
    ObjParent.innerHTML=ObjParent.innerHTML.replace('<div><textarea class="edit_field"></textarea></div>',str);
    }
    var edit_button_save = document.createElement("button");
    edit_button_save.setAttribute("id", `Save button ID ${contents}`);
    edit_button_save.setAttribute("class", "btn btn-outline-success");
    edit_button_save.setAttribute("onclick", `save_edited_tweet(${JSON.stringify(contents)})`);
    edit_button_save.innerHTML = 'Save'
    document.getElementById(`Id for each edit ${contents}`).append(edit_button_save);
    }

function save_edited_tweet(id) {
    console.log(id)
     var new_text = document.getElementById(`Id for textarea ${id}`).value

     fetch(`/edit_tweet/${id}`, {
        method: 'POST',
        body: JSON.stringify({
          edit_content: new_text
        })
    })
     .then(response => response.json())
        .then(data => {
            document.getElementById(`Id for textarea ${data.id}`).remove()
            document.getElementById(`Save button ID ${data.id}`).remove()
            var post_body = document.createElement("div");
                post_body.setAttribute("class", "post_body");
                post_body.setAttribute("id", `Tweet id for edit ${data.id}`);
                post_body.innerHTML=data.content;
                document.getElementById(`Id for each edit ${data.id}`).append(post_body);

        })
 }