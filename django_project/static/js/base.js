$(function(){
     $('#detail_search').autocomplete({
        source: "/json/search_detail",
        select: function(event, ui){
            console.log(ui.item);
            window.location.href = ui.item.href;
        },
        minLength: 2,
     });

    $('#detail_search').keydown(function(event){
        console.log(event.keyCode);
        if (event.keyCode == 13) {
            url = $('#search_url').attr('data-search-url');
            console.log($(this), $(this).val());
            window.location.href = url +'?term=' + $(this).val()
        }
    })
});