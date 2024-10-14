// // alert('hihii')

// document.addEventListener('DOMContentLoaded', () => {
//     const modal = document.getElementById('previewModal');
//     const closeModalButton = document.getElementById('closeModal');

//     // Function to open the modal
//     window.openModal = function(instanceId) {
//         fetch(`/admin/preview/${instanceId}/`) // Adjust the URL as needed
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.text();
//             })
//             .then(data => {
//                 document.getElementById('modal-body').innerHTML = data;
//                 modal.style.display = 'block'; // Show the modal
//             })
//             .catch(error => console.error('Error fetching preview:', error));
//     };

//     // Close modal when the close button is clicked
//     closeModalButton.addEventListener('click', () => {
//         modal.style.display = 'none';
//     });

//     // Close modal when clicking outside of it
//     window.addEventListener('click', (event) => {
//         if (event.target === modal) {
//             modal.style.display = 'none';
//         }
//     });
// });