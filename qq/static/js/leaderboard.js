
$(document).ready(getStudentsInfo());

setInterval(function() { getStudentsInfo() }, 1000)

//leaderboard js
function updateLeaderboard(data) {
    html = ""
    for (i in data.student){
        student = data.student[i]
        count = parseInt(i)+1
        html +='<tr>'
					+'<td scope="row">'+count+'</td>'
					+'<td class="text-center">'+student.name+'</td>'
					+'<td class="text-center">'+student.question_raised+'</td>'
					+'<td class="text-center">'+student.likes_receives+'</td>'
					+'<td class="text-center">'+student.bonus_score+'</td>'
				+'</tr>'
    }
    $("#board").html(html)
}


function getStudentsInfo(){
    course_id = $("#course_id").val()
    $.ajax({
            url: "/get_leaderboard_stu",
            type: "GET",
            data: { 'course_id': course_id },
            success: function(data)
                        {
                            updateLeaderboard(data)

                        }
        });
}