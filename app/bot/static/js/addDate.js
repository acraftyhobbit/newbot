$(function () { // this is the jquery shortcut for document.ready()
    function addToProjects(evt) {
        evt.preventDefault();
        var url = new URL(window.location)
        $.post(
            '/bot/post_date',
            {
                date : document.getElementsByName('duedate')[0].value,
                sender_id : url.searchParams.get('sender_id')
            },
            addToProjectsSuccess
        );
    }
    function addToProjectsSuccess(result) {
        console.log(result.status);
        MessengerExtensions.requestCloseBrowser();
    }
    $('button').click(addToProjects);    
});