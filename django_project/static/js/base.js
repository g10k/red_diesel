$(function(){
     $('#detail_search').autocomplete({
        source: "/json/search_detail",
        select: function(event, ui){
            console.log(ui.item);
            window.location.href = ui.item.href;
        },
        minLength: 2,
     });

    function go_to_price_page(){
        url = $('#price_url').attr('data-search-url');
        window.location.href = url +'?search=' + $('#detail_search').val();
    }
    $('#detail_search').keydown(function(event){
        if (event.keyCode == 13) {
            go_to_price_page();
        }
    });
    $("#search_button").click(go_to_price_page)

});