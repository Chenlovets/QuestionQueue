var previous_data;

//handle CSRF Token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    //these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//ajax set up
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(getAnswers());

setInterval(function() { getAnswers() }, 1000);

function getAnswers() {
	var lecture_id = $('#lecture_id').attr( "value")
    $.ajax({
        url: '/getAnswers',
        type: 'POST',
        data: { 'lecture_id': lecture_id },
        success: function (data) {
            printAnswers(data)
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
}

function printAnswers(data) {
    console.log(data)
    var answer_dict = JSON.parse(data.answers);

    console.log(JSON.stringify(data) != JSON.stringify(previous_data))

    if (JSON.stringify(data) != JSON.stringify(previous_data)){

        html = ''

        for (i in data.questions) {

            question = data.questions[i]

            var answers_display = ""

            var d = JSON.parse(answer_dict[question.id])
            var count = 1
            var flag = false
            if(d.length==0){
                flag = true
            }
            for (var key in d ) {
                answers_display += '<li class="list-group-item">'
                answers_display += 'Answer '
                answers_display += count
                answers_display += ' : '
                answers_display += d[key].fields.content
                answers_display += '</li>'
                count = count + 1
            }

            question_answer_id = 'questiondiv' + question.id

            html += '<div class="row justify-content-md-center" id =' + question_answer_id +'>'+
            '<div class="col-5">' +
                '<div class="card-container">' +
                    '<div class="card card-front">' +
                        '<div class="card-body">' +
                        '<div class="row">';
                if(flag==false){
                            html += '<h6 class="card-title col-sm-12  col-md-10" align="left">' + question.title + '</h6>' }
                else {
                            html +='<h6 class="card-title col-sm-12  col-md-10" align="left">' + question.title +'(Unresolved)'+ '</h6>'
                }
                            html +='<div class="col-sm-12  col-md-2 pr-0" align="right"><button onclick="deleteQ(' + question.id +')" class="deleteQuestion">' +
                                '<ion-icon name="close" class="delete"></ion-icon></button>' +
                            '</div>' +
                        '</div>' +
                            '<div class="question-body">' +
                            '<p class="card-text mb-1">' + question.description + '</p>' +
                            '</div>' + 
                            '<div class="row pt-0 pb-2">' +
                            '<div class="col-sm-12  col-md-6" align="left"><button onclick="flip(this)" class="viewbutton">'+
                                '<ion-icon name="eye" class="view"></ion-icon></button>' +
                            '</div>' +
                            '<div class="col-sm-12  col-md-6 pr-0" align="right">' +
                                '<ion-item>' +
                                '<ion-icon name="thumbs-up" class="like"></ion-icon>' +
                                '<ion-badge slot="end">' + question.likes + '</ion-badge>' +
                                '</ion-item>' +
                            '</div>' +
                            '</div>' +    
                        '</div>' +
                    '</div>' +
                    '<div class="card card-back" onmouseleave="flipBack(this)">' +
                        '<div class="card-body">' +
                            '<h6 class="card-title">Answer</h6>' +
                            '<div class="question-body pr-0">' +
                            '<ul class="list-group list-group-flush" id="'+question.id +'">' + answers_display +
                            '</ul>'+ 
                            '</div>' + 
                        '</div><br>' +
                    '</div>' +
                '</div>' +      
            '</div>' +

            '<div class="col-5">' +
                '<div class="card card-front">' +
                    '<div class="card-body">' +
                        '<h6 class="card-title">Answer Question</h6>' +
                        '<textarea id="answer_area_'+question.id +'" class=" text form-control mb-3" rows="2" placeholder="Type your answer here..." required></textarea>' +
                        '<div class="input-group">'+
                            '<select class="custom-select" id="bonus_'+question.id +'" aria-label="Example select with button addon">'+
                                '<option selected>Great question, give bonus point!</option>'+
                                '<option value="1">1</option>'+
                                '<option value="2">2</option>'+
                                '<option value="3">3</option>'+
                            '</select>'+
                            '<div class="input-group-append">'+
                            '<button onclick="submitAnswer(this)" value = "'+ question.id + '" type="button" class="submitAnswerButton btn btn-secondary plain-btn">Submit</button>' +
                            '</div>'+
                        '</div>'+          
                    '</div>' +
                '</div>' +  
            '</div>' +
        '</div><br><br>'
        }

        html = html + '<br>'

        $("#answers").html(html)

    $('.collectbutton').on('click', function() {
        var a = $(this).find("ion-icon").attr( "name")
        if (a == 'heart'){
            $(this).find("ion-icon").attr( "name", "heart-empty" );
        } else {
            $(this).find("ion-icon").attr( "name", "heart" );
        }

    });
        previous_data = data

    }
}

function submitAnswer(event)
    {
        var question = $(event).attr('value')
        console.log(question)

        var answer_selector ='#answer_area_' + question
        var text = $(answer_selector).val()
        console.log(text)

        var bonus_selector ='#bonus_' + question
        var bonus = $(bonus_selector).val()
        console.log(bonus)

        var course = $("#course_id").val()
        console.log(course)
        
        $.ajax({
            url: "/submitAnswer",
            type: "POST",
            data: { 'text': text, 'question': question,'bonus':bonus,'course':course},
            success: function(data) {
                addAnswer(data)
            }
        });

        $(event).siblings('.text').val("") 
}


function deleteQ (data) {

    console.log("Delete:" + data)
    
    $.ajax({
        url: "/deleteQuestion",
        type: "POST",
        data: { 'question_id': data},
        success: function(data) {
            console.log(data.success)
        }
    });

    var selector ='#questiondiv' + data
    $(selector).remove() 


}


function addAnswer (data) {

    var question = data.question;
    var answer = '<li class="list-group-item">' +data.answer+ '</li>';
    var selector ='#'+question
    $(selector).append(answer)
}


function flipBack(event){
    //$(event).parent().toggleClass('flipped')
    $(event).parents( '.card-container' ).toggleClass('flipped')
}

function flip(event){
    //$(event).parent().parent().parent().parent().parent().toggleClass('flipped')
    $(event).parents( '.card-container' ).toggleClass('flipped')
}