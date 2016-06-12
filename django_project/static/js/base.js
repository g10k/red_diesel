$(function(){
     $('#detail_seach').autocomplete({
        source: "/json/search_detail",
        select: function(event, ui){
            console.log(ui.item);
            window.location.href = ui.item.href;
        },
        minLength: 2,
     })
});