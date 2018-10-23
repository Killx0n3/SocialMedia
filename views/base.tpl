<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{title}}</title>

    <!-- Custom styles for this template -->
    <link href="/static/style.css" rel="stylesheet">
  </head>

  <body>
        %if (loginStatus==False):
        <form action="/login" method="POST" id="loginform">
            <fieldset>
                <legend>{{name}}</legend>
            Username: <input type="text" name="nick"><br>
            Password:&nbsp; <input type="password" name="password"><br>
            <input value="Login" type="submit" >
            </fieldset>
          </form>
        %end
        %if (loginStatus==True):
        <p>Logged in as {{lus}}</p>
        <form action="/logout" method="POST" id='logoutform'>
            <input value="logout" type="submit" >
        </form>
        <form action="/post" method="POST" id="postform">
            <fieldset>
                <legend>What's on your mind?</legend>
            <input type="text" name="post"><br>
            <input value="Post" type="submit" >
            </fieldset>
          </form>
        %end

    <ul class="nav navbar-nav">
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>

    <div class="container">

		{{!base}}

    </div>

  </body>
</html>
