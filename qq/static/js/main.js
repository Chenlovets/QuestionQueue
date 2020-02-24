var previous;
var interval = 3000;

//CSRF Token
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
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//ajax setup
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(getQuestionsRepeat());

function getQuestionsRepeat() {

    lecture_id = $("#lecture_id").val()

    $.ajax({
        url: '/getQuestion',
        type: 'get',
        data: { 'lecture_id':lecture_id },
        success: function (data) {
            printQuestions(data)
            setTimeout(getQuestionsRepeat, interval);
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
}

function getQuestions() {

    lecture_id = $("#lecture_id").val()

    $.ajax({
        url: '/getQuestion',
        type: 'get',
        data: { 'lecture_id':lecture_id },
        success: function (data) {
            printQuestions(data)
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
}

//setInterval(function() { getQuestions() }, 5000);

function printQuestions(data) {
    console.log(JSON.stringify(data) != JSON.stringify(previous))
    if (JSON.stringify(data) != JSON.stringify(previous)){
        html = ''

        for (i in data.questions) {
            question = data.questions[i]
            html += '<div class="card-container">'
            +'<div class="card card-front">'
            +'<div class="card-body">'
            +'<h6 class="card-title">'+question.title+'</h6>'
            +'<div class="question-body">'
            +'<p class="card-text mb-1">'+question.description+'</p>'
            +'</div>'
            +'<div class="row pt-0 pb-2">'
            +'<div class="col-sm-12  col-md-6" align="left" ><button onclick="flip(this)" class="viewbutton">'
            +'<ion-icon name="eye" class="view" ></ion-icon></button>'
            +'</div>'
            +'<div class="col-sm-12  col-md-6 pr-0" align="right">'
            +'<ion-item id="likedIcon">'
            if(question.is_liked == false){
                html += '<button onclick="like(this)" class="likebutton">'
                +'<i class="fa fa-thumbs-o-up thumb-style"></i></button>'
            }else{
                html += '<button onclick="dislike(this)" class="likebutton"><input type="hidden" id="questionID" name="questionID" value='+question.id+'>'
                +'<i class="fa fa-thumbs-up thumb-style"></i></button>'
            }
            html += '<input type="hidden" id="questionID" name="questionID" value='+question.id+'>'
            +'&nbsp;&nbsp;<ion-badge slot="end">'+question.likes+'</ion-badge>'
            +'</ion-item>'
            +'</div>'
            +'</div>'
            +'</div>'
            +'</div>'
            +'<div class="card card-back" onmouseleave="flipBack(this)">'
            +'<div class="card-body">'
            +'<h6 class="card-title">Answer</h6>'
            +'<div class="question-body pr-0">'
            +'<ul class="list-group list-group-flush">'
            for (answer in question.answers) {
                html += question.answers[answer]
            }
       
            html +='</ul></div>'
            +'</div><br>'
            +'</div>'
            +'</div><br>'

        }
        $("#questions").html(html)
        previous = data

    }
}

function flipBack(event) {
    
    $(event).parents( '.card-container' ).toggleClass('flipped')
}

function flip(event) {

    $(event).parents( '.card-container' ).toggleClass('flipped')
}

function like(event) {

    cur_id = $(event).next('input').attr('value')
    $.ajax({
        url: "/likeTheQ",
        type: "POST",
        data: { 'questionID': cur_id },
        success: function()
                    {
                        getQuestions()

                    }
    });


}

function dislike(event) {
    cur_id = $(event).next('input').attr('value')
    $.ajax({
        url: "/dislikeTheQ",
        type: "POST",
        data: { 'questionID': cur_id },
        success: function()
                    {
                        getQuestions()

                    }
    });

}

