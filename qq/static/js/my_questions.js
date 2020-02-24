var my_q_clicked = false;
var liked_q_clicked = false;

var prev_my_questions;
$("#get_default").trigger('click');

function getMyQuestions(event) {
    let course_id = $("#get_my_question").attr('value')
    $.ajax({
        url: '/get_my_question/' + course_id,
        type: 'get',
        success: function (data) {
            printMyQuestions(data)
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
    if (!my_q_clicked ) {
        my_q_clicked = true;
    }
    if (liked_q_clicked) {
        liked_q_clicked = false;
    }
}


function printMyQuestions(data) {
    let cardHtml;
    if (JSON.stringify(data) != prev_my_questions) {
        cardHtml = '';
        for (i in data.questions) {
            question = data.questions[i];
            cardHtml += '<div class="col-5">'
                        +'<div class="card-container">'
                            +'<div class="card card-front">'
                                +'<div class="card-body">'
                                    +'<h6 class="card-title">'+question.title+'</h6>'
                                    +'<div class="question-body">'
                                    +'<p class="card-text mb-1">'+question.description+'</p>'
                                    +'</div>'
                                    +'<div class="row pt-2">'
                                    +'<div class="col-sm-12  col-md-6" align="left" ><button onclick="flip(this)" class="viewbutton">'
                                        +'<ion-icon name="eye" class="view" ></ion-icon></button>'
                                    +'</div>'
                                    +'<div class="col-sm-12  col-md-6 pr-0" align="right">'
                                        +'<ion-item id="likedIcon">'
                                        +'<i class="fa fa-thumbs-o-up thumb-style likedIcon"></i></button><button class="likebutton dislikedIcon">'
                                        +'<i class="fa fa-thumbs-up thumb-style dislikedIcon"></i></button><input type="hidden" id="questionID" name="questionID" value='+question.id+'>'
                                        +'&nbsp;&nbsp;<ion-badge slot="end">'+question.likes+'</ion-badge>'
                                        +'</ion-item>'
                                    +'</div>'
                                    +'</div>'
                                +'</div>'
                            +'</div>'
                            +'<div class="card card-back" onmouseleave="flipBack(this)">'
                                +'<div class="card-body">'
                                    +'<h6 class="card-title">Answer</h6>'
                                    +'<div class="question-body">'
                                    +'<ul class="list-group list-group-flush">'
            for (answer in question.answers) {
                cardHtml += question.answers[answer]
            }
            cardHtml += '</ul></div></div><br></div></div><br></div>'

        }
        $("#my_questions").html(cardHtml)
        $(".dislikedIcon").css("display", "none")

        prev_my_questions = JSON.stringify(data)
    }
}

function flipBack(event){
    $(event).parents( '.card-container' ).toggleClass('flipped')
}

function flip(event){
    $(event).parents( '.card-container' ).toggleClass('flipped')
}

function getLikedQuestions(event) {
    let course_id = $("#get_my_question").attr('value')
    $.ajax({
        url: '/get_liked_question/' + course_id,
        type: 'get',
        success: function (data) {
            printMyQuestions(data)
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
    if (!liked_q_clicked) {
        liked_q_clicked = true;
    }
    if (my_q_clicked) {
        my_q_clicked = false;
    }
}


