document.addEventListener("DOMContentLoaded", function () {
    var communityField = document.querySelector('select[name="community"]');
    var projectField = document.querySelector('select[name="project"]');
    console.log(communityField,"-------",projectField,"-------")

    function updateProjects() {
        var communityId = communityField.value;
        console.log('communityID',communityId)

        // Clear current project options
        projectField.innerHTML = '<option value="">---------</option>'; // Clear existing options

        if (communityId) {
            fetch(`/api/v2/dynamic_dropdown/projects/${communityId}/`)
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