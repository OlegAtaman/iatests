$(document).ready(function(){
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var url_ = $("input[name=url]").val();
    $(".ubutton").click(function(){
        var quetions = [];
        var divs = $(this.parentNode).children('#cont').children('.quetion');
        $(divs).each(function(){
            var answers = [];
            var text = $(this).children('.q').text();
            var points = $(this).children('.p').text();
            var ans = $(this).children('.a');
            $(ans).each(function(){
                var text = $(this).text();
                var is_correct = false;
                if (text.slice(3, 12) == "[CORRECT]") {
                    text = text.slice(12, text.length + 1);
                    is_correct = true;
                } else {
                    text = text.slice(3, text.length + 1);
                }
                let answer = {
                    text : text,
                    is_correct : is_correct
                };
                answers.push(answer);
            });
            let quetion = {
                text : text,
                points : points,
                ans : answers
            };
            quetions.push(quetion);
        });

        $.ajax({
            url: "",
            type: "post",
            data: {
                qname : $(this.parentNode).children('.hi').children('input').val(),
                desc : $(this.parentNode).children('textarea').val(),
                time : $(this.parentNode).children('.t_cont').children('input').val(),
                pub_time : $(this.parentNode).children('.dt_cont').children('input').val(),
                m_points: $(this.parentNode).children('.m_points').children('input').val(),
                q : JSON.stringify(quetions),
                csrfmiddlewaretoken : csrf
            },
            success: function(response) {
                window.location = url_;
            },
            error: function(response) {
                console.log(0);
            }
        });
    });

    $(".new_quetion_btn").click(function(){
        $("#cont").append(`
        <div class="unquetion" style="border:1px solid black; margin: 5px; padding: 5px">
        <p class="qname">Текст питання:
        <input  name="q_name" type="text"></p>
        <p class="points">Кількість балів:
        <input  name="points" type="number"></p>
        <hr>
        <div class="ans_cont">
        </div>
        <hr>
        <button class="new_ans" type="button">Додати відповіть</button>
        <button class="post_quet" type="button">Зберегти питання</button>
        </div>
        `);
    });

    $('.ubutton').click(function(){
        if ($(this.parentNode).children('.hi').children('input:checked').length) {
            console.log(1);
        }; 
    });

    $('#cont').on('click', '.new_ans', function(){
        $(this.parentNode).children('.ans_cont').append(`
        <div class="ans">
        <p>Текст відповіді:</p>
        <input type="text" class="ans" name="answer">
        <input type="checkbox" name="correct">Правильна відповідь</div>
        `);
    });

    $('#cont').on('click', '.post_quet', function(){
        var qname = $(this.parentNode).children('.qname').children('input').val();
        var points = $(this.parentNode).children('.points').children('input').val();
        var cnt = $(this.parentNode).children('.ans_cont').children();
        var quetions = '';
        var cnter = 1;
        $(cnt).each(function(){
            quetions += '<p class="a">'
            quetions += cnter;
            quetions += '. '
            cnter += 1;
            if ($(this).children('input:checked').length) {
                quetions += '[CORRECT] ';
            };
            quetions += $(this).children('input.ans').val();
            quetions += '</p>';
        });
        var out = `<div class="quetion" style="border:1px solid black; margin: 5px; padding: 5px"><b>Питання:</b> <p class="q">`
            + qname + '</p><b>Кількість балів:</b> <p class="p">' + points 
            + '</p>' + quetions + '</div>';
        $(this.parentNode).replaceWith(out);

    });

});

