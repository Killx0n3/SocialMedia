% rebase('base.tpl')
% import interface


<h2>{{title}}</h2>

<div class="posts">

% for post in posts:
       <div class="post">
           <div class="avatar"><img src="{{post[3]}}" alt="avatar"></div>
           <a class="user" href="/users/{{post[2]}}">@{{post[2]}}:</a>
           <span class="timestamp">{{post[1]}}</span> <span class="content">{{!interface.post_to_html(post[4])}}</span>
       </div>
    % end

</div>