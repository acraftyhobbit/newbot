$('button').on('click', function(event){
    
    var url = new URL(window.location)
    $.ajax({
        url: '/bot/post_date',
        type: 'POST',
        data: {
            date : document.getElementsByName('duedate')[0].value,
            sender_id : url.searchParams.get('sender_id')
        }
    });
});