function search(e) {
    $("#search_button").html('Searching...');
    if(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    $.get('/search', $('form#search').serialize(true), function(data) {
        if(data.is_success) {
            var th = "<tr><th>Name</th><th>Paying</th><th>Uploaded</th><th>Staff Pick</th></tr>";
            $("#users tbody").html($(th));
            $(data.users).each(function (idx, user) {
                user = user.fields;
                var row = "<tr><td><a href=\"" + user.url + "\">"
                    + user.name + "</a></td><td>" + user.is_paying_user
                    + "</td><td>" + user.has_atleast_one_video + "</td><td>"
                    + user.has_video_in_staff_pick + "</td></tr>";
                $("#users tbody").append($(row));
            });
            $('span#result').html(data.total_count);
            $("#search_button").html('Search');
        }
    }, 'json');
}
