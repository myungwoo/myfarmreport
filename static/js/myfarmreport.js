
/* settings */
var url = window.location.href, server_name = 'https://59.5.23.19';
var min_res = 240;
var max_light = 10;

$(function(){
    if (url.search('screen=report') >= 0){
        if ($('#attack_spy_resources tr:first-child .wood').length){
            var scouted_wood = $('#attack_spy_resources tr:first-child .wood').parent().html().split('</span>')[1].trim();
            var scouted_clay = $('#attack_spy_resources tr:first-child .stone').parent().html().split('</span>')[1].trim();
            var scouted_iron = $('#attack_spy_resources tr:first-child .iron').parent().html().split('</span>')[1].trim();

            var name = $('#attack_info_def .village_anchor a:first-child').html().replace('(', '|').replace(')', '|').split('|')[0].trim();
            var target_x = $('#attack_info_def .village_anchor a:first-child').html().replace('(', '|').replace(')', '|').split('|')[1].trim();
            var target_y = $('#attack_info_def .village_anchor a:first-child').html().replace('(', '|').replace(')', '|').split('|')[2].trim();

            var wood_level = 0, clay_level = 0, iron_level = 0, wall_level = 0;
            if ($('#attack_spy_building_data').length){
                var obj = JSON.parse($('#attack_spy_building_data').val());
                for (var i=0;i<obj.length;i++){
                    if (obj[i].id == 'wood') wood_level = obj[i].level;
                    if (obj[i].id == 'clay') clay_level = obj[i].level;
                    if (obj[i].id == 'iron') iron_level = obj[i].level;
                }
            }else{
                wood_level = clay_level = iron_level = wall_level = -1;
            }
            var reported_time = $('.small.grey').parent().html().split('<span')[0].trim();
            // alert('wood: ' + scouted_wood + '\n' + 'clay: ' + scouted_clay + '\n' + 'iron: ' + scouted_iron + '\n' + 'x, y: ' + target_x + ', ' + target_y + '\n\n' + 'Wood Level: ' + wood_level + '\n' + 'Clay Level: ' + clay_level + '\n' + 'Iron Level: ' + iron_level + '\n\nReported at ' + reported_time);
            $.ajax({
                url: server_name + '/ajax/register_village/',
                dataType: 'jsonp',
                jsonp: 'callback',
                data: {
                    coord_x: target_x,
                    coord_y: target_y,
                    name: name,
                    scouted_wood: scouted_wood,
                    scouted_clay: scouted_clay,
                    scouted_iron: scouted_iron,
                    wood_level: wood_level,
                    clay_level: clay_level,
                    iron_level: iron_level,
                    wall_level: wall_level,
                    reported_time: reported_time
                },
                success: function(rsp){
                    // if (rsp.msg == 'skip') alert('Old report. Skipped');
                    // alert(rsp.msg);
                }
            });

        }else{
            // No Resources Info
            //alert('No Resources Info');
        }
        if ($('a#report-next').length)
            window.location.href = $('a#report-next').attr('href');
    }
    else if (url.search('screen=place') >= 0){
        var my_x = game_data.village.x;
        var my_y = game_data.village.y;
        var on_ride = '[';
        $('.quickedit-label').each(function(idx){
            var arr = $(this).html().trim().split(' ');
            if (arr[0] != 'Attack') return;
            var str = arr[arr.length - 2];
            var x = str.replace('(', '').replace(')', '').split('|')[0];
            var y = str.replace('(', '').replace(')', '').split('|')[1];
            on_ride += '(' + x + ', ' + y + '), ';
        });
        on_ride += ']';
        $.ajax({
            url: server_name + '/ajax/get_next_village/',
            dataType: 'jsonp',
            jsonp: 'callback',
            data: {
                my_x: my_x,
                my_y: my_y,
                min_res: min_res,
                on_ride: on_ride
            },
            success: function(rsp){
                if (rsp.msg == 'empty'){
                    alert('No more farms');
                    return true;
                }
                if (rsp.msg != 'success') return false;
                var now_light = parseInt($('#units_entry_all_light').html().replace('(', '').replace(')', ''));
                var next_light = parseInt(rsp.cnt); // TODO: get info (string? number?)
                if (next_light > now_light)
                    next_light = now_light;
                if (next_light > max_light)
                    next_light = max_light;
                // 360|407
                var next_x = rsp.x, next_y = rsp.y;
                $('input[type="text"][name="input"]').val(next_x + '|' + next_y);
                $('input[type="text"][name="spy"]').val('1');
                $('input[type="text"][name="light"]').val(next_light);
            }
        });
    }
});