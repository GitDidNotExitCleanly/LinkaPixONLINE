/*
 * Game logic and events for solving Linkapix game puzzles
 */

// define some global variables to track states

var picking = false;
var start = [0,0];
var startblock = null;
var number = 0;
var color = null;
var previous = null;
var links = [];
var restartPuzzle = null;

function destroy_puzzle() {
    // (re)start with a clean state, reset all state variables
    // and destroy the game board
    //
    picking = false;
    start = [0,0];
    startblock = null;
    number = 0;
    previous = null;
    links = [];
    $(".linkapix").html("");
}

function string_to_puzzle(json) {
    // convert a JSON string into a puzzle object
    //
    var data = JSON.parse(json);
    return data;
};

function build_puzzle(puzzle) {
    // take a puzzle (puzzle) in the form of a 2D array of blocks that
    // represent all the data/numbers of the puzzle
    //
    var table = $("<table></table>");
    // create a table and append it to linkapix div
    $(".linkapix").append(table);
    $(".linkapix").append();
    // we have an array of arrays, or an arrow of rows, so for each row
    $.each(puzzle, function(rid, row) {
        // create a new table row
        var tr = $("<tr/>")
        var blocks = [];
        $.each(row, function(cid, block) {
            // and for each column in that row, create a new block object
            if(block !== null) {
                if(block.number != 0) {
                    number = block.number;
                } else {
                    number = '';
                }
            } else {
                number = '';
            }
            // if  there is a number for the location, we want to build a table
            // element that has the number and the colour of the block inside
            // it and append it to the row
            if(number != '') {
                var colorstring = 'rgb('+block.color.r+','+block.color.g+','+block.color.b+')';
                    blocks.push('<td class="static" data-color="'+colorstring+'" data-number="'+number+'" data-r="'+block.color.r+'" data-g="'+block.color.g+'" data-b="'+block.color.b+'" data-x="'+cid+'" data-y="'+rid+'" style="color: '+colorstring+';">' + number + "</td>");
            } else {
                // else we append a blank string as colour information not
                // needed
                blocks.push('<td data-number="'+number+'" data-x="'+cid+'" data-y="'+rid+'">' + number + "</td>");
            }
        });
        // append each column to the table row
        // and then append each row to the table
        tr.append(blocks);
        table.append(tr)
    });
    // register the game events when we've built the puzzle
    //register_game_events();

};

function refresh_game() {
    // called after every action to just check on the status of the game board
    // and make sure no state was left weirdly or impossible actions were taken
    $(".linkapix td").each(function(index) {
        if ($(this).data('number') != 0) {
            $(this).html($(this).data('number'));
        } else {
            $(this).html($(this).data('partial'));
        }
    })
    picking = false;
    start = [0,0];
    startblock = null;
    number = 0;
    color = null;
    previous = null;
    links = [];
    
    // check for end of game
    if (!$(".static:not(.linked)")[0]) game_finished();
}

function game_finished() {
    enddate = new Date();
    diff = Math.abs(startdate - enddate);
    elapsed = msToTime(diff);
    alert("Well done! Puzzle completed in "+elapsed+"!");
    //submit_score(diff);
}

function submit_score(ms) {
    var postdata = new Object;
    postdata.time = ms;
    console.log(postdata);
    $.ajax({
        type: "POST",
        url: '/submit_score.php',
        data: postdata,
        success: function(result) {
            console.log(result);
        }
    })
}

function msToTime(duration) {
    var milliseconds = parseInt((duration%1000)/100)
        , seconds = parseInt((duration/1000)%60)
        , minutes = parseInt((duration/(1000*60))%60)
        , hours = parseInt((duration/(1000*60*60))%24);

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;

    return minutes + ":" + seconds;
}

function check_valid_link(start, end) {
    // function to test if a link can be completed, colours must match, numbers
    // must match and the length of the link must equal the numbers
    if (end.data('number') != number) return false;
    if ($("td.picking").length != number) return false;
    if (end.css('color') != start.css('color')) return false;
    return true;
}

function register_game_events() {
    // register all needed mousedown/mouseover/mouseup events
    // if the click is valid, then we emit events to the linkapix object with
    // the expected behavior eg: editlink event or startlink event
    $(".linkapix td").on('mousedown', function() {
        if ($(this).hasClass('link-end')) {
            // if a partial link then undo it
            $(".linkapix").trigger('editlink', [$(this)]);
            return
        }
        if($(this).hasClass('linked')) {
            // if a full link then undo it
            $(".linkapix").trigger('editlink', [$(this)]);
            return
        }
        if($(this).hasClass('unfinished')) {
            $(".linkapix").trigger('editlink', [$(this)]);
            return;
        } else {
            // else we just want to start making a link
            $(".linkapix").trigger('startlink', [$(this), $(this).data('x'), $(this).data('y')]);
        }
    });

    $(".linkapix td").on('mouseover', function() {
        if (picking) {
            // ignore mouseovers unless in picking state
            $(".linkapix").trigger('extendlink', [$(this)]);
        }
    });

    $(".linkapix td").on('mouseup', function() {
        if (picking) {
            // ignore mouseups unless in picking state
            $('.linkapix').trigger('stoplink', [$(this)]);
        }
    });

    $('.linkapix').on('startlink', function(event, block, x, y) {
        // store where we started
        start = [x, y];
        startblock = block;

        if (block.data('number') == '') {
            return;
        }
        // 1s are easy to deal with because clicking them completes them
        else if (block.data('number') == '1') {
            block.addClass('linked');
            block.css("background-color", block.css("color"));
            block.css("color", "white");
            refresh_game();
        }
        else {
            // everything else however we need to enter picking state and store
            // information about the current number and oclour
            number = block.data('number');
            color = block.css("color");
            picking = true;
            block.addClass('picking');
            // we also keep track of every block in the link for undoing
            // purposes
            links.push(block);
        }
    });

    $('.linkapix').on('extendlink', function(event, block) {
        if (previous !== null) previous.html('');
        // we can't go over other links, other numbers, or ourself, so if we
        // do, then exit picking state and go back
        if (block.hasClass('unfinished') || block.hasClass('linked') || block.hasClass('picking') || $('td.picking').length >= number || (block.hasClass('static') && block.data('number') != number)) {
            picking = false;
            if ([block.data('x'), block.data('y')] != start) {
                if(previous == null) {
                    picking = false;
                    $("td.picking").removeClass('picking');
                    links = [];
                    refresh_game();
                    return
                }
                $(this).trigger('stoplink', [previous]);
            }
            $("td.picking").removeClass('picking');
            return;
        } else {
            // however if it's a valid square then add it to the list and move
            // on through it
            block.addClass('picking');
            links.push(block);
            block.html($('td.picking').length);
            //console.log(block != startblock);
            //console.log([block.data('x'), block.data('y')] != start)
            if (block != startblock) {
                previous = block;
            }
        }
    });

    $('.linkapix').on('stoplink', function(event, block) {
        previous = null;
        // if we stop the link on an empty square then we create a partial link
        // to that point
        if (block.data('number') == '') {
            len = $("td.picking").length;
            block.addClass('unfinished link-end');
            block.html(len);
            block.data('partial', $("td.picking").length);
            links.push(block);
            block.data('links', links);
            $.each(links, function(key, val) {
                val.data("links", links);
            });
            links = [];
            // by removing all the picking states from the squares and making
            // them unfinished
            $("td.picking").removeClass('picking').addClass('unfinished');
        } else if (check_valid_link(startblock, block)) {
            // however if we stop on a square that is a number, we want to see
            // if it actually is totally valid and if it is, then we can remove
            // the picking state from the squares and make it a completed link,
            // storing the linked elements in each block for undoing purposes
            $("td.picking").removeClass('picking');
            links.push(block);
            block.data('links', links);
            startblock.data('links', links);
            block.addClass('linked');
            block.css("background-color", block.css("color"));
            block.css("color", "white");
            $.each(links, function(key, val) {
                // each linked block needs the right colour and also inverts
                // the text colour so that you can still see the numbers
                val.addClass('linked');
                val.css("background-color", color);
                val.css("color", "white");
                val.data("links", links);
                val.data("solved", number);
            });
            links = [];
        }
        $("td.picking").removeClass('picking');
        picking = false;
        refresh_game();
    });

    $('.linkapix').on('editlink', function(event, block) {
        // undo completed links incase of error or mistake etc
        link = block.data('links');
        block.html('');
        block.removeClass('link-end');
        $.each(link, function(key, val) {
            val.data('partial', null);
            val.removeAttr('style');
            val.css('color', val.data('color'));
            val.removeClass('unfinished');
            val.removeClass('linked');
            val.removeClass('link-end');
            val.removeData('links');
            val.removeData('solved');
        });
        refresh_game();
    });
};

function saveGameState() {
    // store current puzzle progress in users LocalStorage
    // we just take the table in raw html form and store it as a string because
    // it is enough to rebuild a puzzle
    localStorage["linkapix.test"] = $('.linkapix').html();
    return true;
}

function loadGameState() {
    // take the table string from the users localstorage from a saved puzzle
    // and render it on the board
    $('.linkapix').html(localStorage["linkapix.test"]);
    return true;
}

$(".save_puzzle").on('click', function() {
    // hook for save_puzzle button
    console.log('saved progress');
    saveGameState();
    return false;
});

$(".load_puzzle").on('click', function() {
    // hook for load_puzzle button
    console.log('loaded progress');
    loadGameState();
    //register_game_events();
    $('.save_puzzle').show(400)
    return false;
});

$(".clear_incorrect").on('click', function (event) {
    $(".linkapix td").each(function(index, val) {
        if ($(this).data('solved') !== undefined) {
            x = $(this).data('x');
            y = $(this).data('y');
            if ($(this).data('solved') != solution[y][x].number) {
                link = $(this).data('links');
                $(this).html('');
                $.each(link, function(key, val) {
                    val.data('partial', null);
                    val.removeAttr('style');
                    val.css('color', val.data('color'));
                    val.removeClass('unfinished');
                    val.removeClass('linked');
                    val.removeClass('link-end');
                    val.removeData('links');
                    val.removeData('solved');
                });
            }
        };
    });
    //refresh_game();
});

$(".show_solution").on('click', function (event) {
    // when we generate a puzzle we generate a solution,
    // which is stored globally as solution
    // we can use this to build a solved puzzle when user clicks show solution
    destroy_puzzle();
    build_puzzle(solution);
    // we want to make it pretty so loop through the table making every square
    // the proper colour but keep the numbers white
    $(".linkapix td").each(function(index) {
        if ($(this).data('number') != 0) {
            $(this).addClass('linked');
            $(this).css("background-color", $(this).css("color"));
            $(this).css("color", "white");
        } else {
            $(this).html($(this).data('partial'));
        }
    })
});

$(".restart_game").on('click', function() {
    destroy_puzzle();
    build_puzzle(puzzle);
    saveGameState();
});


$(".solve_puzzle").on('click', function() {
    // to solve puzzles we call the solveendpoint with the puzzle data
    var postdata = new Object;
    postdata.width = $('#width').val();
    postdata.height = $('#height').val();
    //postdata.difficulty = $('#difficulty').val();
    //postdata.data = JSON.stringify(pixArray);
    console.log(postdata);
    $.ajax({
        type: "POST",
        url: '/solve.php',
        data: postdata,
        success: function(result) {
            // and we can display the solutions by replacing the puzzle with
            // the solved version
            destroy_puzzle();
            puzzle = string_to_puzzle(result.solved);
			restartPuzzle = puzzle;
            build_puzzle(puzzle);
            console.log(result.solved);
        }
    })
});
