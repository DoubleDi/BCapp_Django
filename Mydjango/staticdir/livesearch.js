$(document).ready(function(){
    $("#query").autocomplete({
        source: [],
        select: function( event, ui ) {
            event.preventDefault();
            $("#query").val(ui.item.label);
            window.location.href = ui.item.value;
        },
        focus: function( event, ui ) {
            $("#query").val(ui.item.label);
        },
        minLength: 3,
        delay: 500,
    });
 
    $("input#query").keyup(function(){
        var query = $(this).val();
 
        if(query.length>3){
            dataString = 'q=' + query;
            $.ajax({
                type: "POST",
                url: "/search_monster/",
                data: dataString,
                success: function(response){
                    var availableHints = [];
                    for (var i in response.search_monsters){
                        availableHints.push({
                            name: response.search_monsters[i].name
                        });
                    }
                    $("#query").autocomplete({
                        source: availableHints,
                    });
                }
            });
        }
    });
});
