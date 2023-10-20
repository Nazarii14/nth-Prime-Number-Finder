const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
const taskNumberElement = document.getElementById('task-number');
const deleteButtons = document.querySelectorAll('.delete-task');
const taskListContainer = document.getElementById('task-list-container');
const errorMessage = document.getElementById("error-message"); 

$(document).on('click', '.delete-task', function() {
    const taskId = $(this).data('task-id');
    console.log('Delete button clicked for task ID:', taskId);
    
    $.ajax({
        type: 'DELETE',
        url: `/task/delete_task/${taskId}`,
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        error: function(error) {
            console.error('Error:', error);
        },
    });
    checkTaskStatus();
});

function checkTaskStatus() {
    fetch('/task/check_task_status/', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const taskStatus = data.task_status;
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';
        tasks_count = data.count
        tasks_left = data.number_of_tasks_left
        
        if (data.message == undefined) {
            data.message = "";
        }
        if (tasks_count == undefined) {
            tasks_count = 0;
        }

        if (tasks_left == 0) {
            taskNumberElement.innerHTML = `Your Tasks: (${tasks_count})\tYou can't add tasks anymore :(`;
        }
        else {
            errorMessage.innerHTML = data.message
            taskNumberElement.innerHTML = `Your Tasks: (${tasks_count})\tYou can add ${tasks_left} more tasks :)`;
        }

        if (taskStatus.length == 0) {
            const noTaskItem = document.createElement('li');
            noTaskItem.textContent = 'No task found';
            taskList.appendChild(noTaskItem);
        }
        else {
            for (const taskId in taskStatus) {
                const taskInfo = taskStatus[taskId];
                const taskItem = document.createElement('li');
                const isRunningText = taskInfo.is_finished ? 'Finished' : 'Running';

                taskItem.className = 'tasks';
                taskItem.id = `task-${taskId}`;
                taskItem.innerHTML = `
                    Number: ${taskInfo.number}
                    (${isRunningText})
                    Result: ${taskInfo.result}
                    <progress class="task-progress" value="${taskInfo.completion_percentage}" max="100"></progress>
                    ${taskInfo.completion_percentage}%
                    <button class="delete-task" data-task-id="${taskId}">Delete</button>
                `;
                taskList.appendChild(taskItem);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

setInterval(checkTaskStatus, 1000);
