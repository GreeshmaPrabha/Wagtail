$(document).ready(function() {
    var $community = $('#id_community');
    var $project = $('#id_project');

    function updateProjects() {
        var communityId = $community.val();
        if (communityId) {
            // /api/v2/dynamic_dropdown/projects
            $.get('api/v2/new_dynamic_page/projects-by-community/' + communityId + '/', function(data) {
                $project.empty();
                $.each(data, function(id, name) {
                    $project.append($('<option></option>').attr('value', id).text(name));
                });
            });
        } else {
            $project.empty();
        }
    }

    $community.change(updateProjects);
    updateProjects();  // Call on page load
});


document.addEventListener("DOMContentLoaded", function () {
    var communityField = document.querySelector('select[name="community"]');
    var projectField = document.querySelector('select[name="project"]');

    function updateProjects() {
        var communityId = communityField.value;

        // Clear current project options
        projectField.innerHTML = '<option value="">---------</option>'; // Clear existing options

        if (communityId) {
            fetch(`api/v2/new_dynamic_page/projects-by-community/${communityId}/`)
                .then(response => response.json())
                .then(data => {
                    // Populate project options
                    data.forEach(project => {
                        var option = document.createElement('option');
                        option.value = project.id;
                        option.textContent = project.name;
                        projectField.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching projects:', error));
        }
    }

    communityField.addEventListener('change', updateProjects);
});