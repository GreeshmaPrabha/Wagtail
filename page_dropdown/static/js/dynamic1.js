document.addEventListener("DOMContentLoaded", function () {
    var communityField = document.querySelector('select[name="community"]');
    var projectField = document.querySelector('select[name="project"]');

    function updateProjects() {
        var communityId = communityField.value;

        // Clear current project options
        projectField.innerHTML = '<option value="">---------</option>'; // Clear existing options

        if (communityId) {
            // fetch(`/api/v2/page_dropdown/projects-by-community/${communityId}/`)
            fetch(`http://127.0.0.1:5001/api/v2/page_dropdown/projects-by-community/${communityId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Populate project options
                    Object.entries(data).forEach(([id, name]) => {
                        var option = document.createElement('option');
                        option.value = id;
                        option.textContent = name;
                        projectField.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching projects:', error));
        }
    }

    communityField.addEventListener('change', updateProjects);
});