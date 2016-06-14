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
        if (event.keyCode == 13) {
            url = $('#price_url').attr('data-search-url');
            window.location.href = url +'?search=' + $(this).val();
        }
    })
});